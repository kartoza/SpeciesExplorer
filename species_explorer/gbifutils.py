# SPDX-FileCopyrightText: 2018-2024 Kartoza <info@kartoza.com>
# SPDX-FileCopyrightText: Scott Chamberlain (original pygbif code)
# SPDX-License-Identifier: MIT

"""
GBIF API utilities for Species Explorer.

This module provides functions for interacting with the GBIF REST API
using QGIS native networking classes (QgsNetworkAccessManager/QgsFileDownloader).

Original logic by Scott Chamberlain, extracted from his pygbif repo.
"""

import json
import os
from tempfile import mkstemp
from typing import Any, Dict, List, Optional, Union

from qgis.core import QgsFileDownloader, QgsMessageLog, QgsNetworkAccessManager
from qgis.PyQt.QtCore import QEventLoop, QUrl

__version__ = "0.3.0"
__title__ = "gbifutils"
__author__ = "Scott Chamberlain, Tim Sutton, Etienne Trimaille"
__license__ = "MIT"

# GBIF API base URL (using HTTPS)
GBIF_BASE_URL = "https://api.gbif.org/v1/"


class NoResultException(Exception):
    """Raised when no results are returned from GBIF."""

    pass


class GBIFNetworkError(Exception):
    """Raised when a network error occurs."""

    pass


def gbif_GET(url: str, args: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
    """Make a GET request to the GBIF API using QGIS native networking.

    Uses QgsFileDownloader which respects QGIS proxy settings and
    provides proper SSL handling.

    Args:
        url: The URL to request.
        args: Optional query arguments (currently unused, for API compatibility).
        **kwargs: Additional keyword arguments (for API compatibility).

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        GBIFNetworkError: If the request fails.
    """
    handle, output_path = mkstemp(suffix=".json")
    os.close(handle)  # Close the file handle immediately

    QgsMessageLog.logMessage(f"gbif_GET URL: {url}", "SpeciesExplorer", 0)

    # Use QEventLoop to make the async download synchronous
    loop = QEventLoop()
    error_occurred = [False]  # Use list to allow modification in closure
    error_message = [""]

    def on_error(errors: List[str]) -> None:
        error_occurred[0] = True
        error_message[0] = ", ".join(errors) if errors else "Unknown error"

    downloader = QgsFileDownloader(QUrl(url), output_path, delayStart=True)
    downloader.downloadExited.connect(loop.quit)
    downloader.downloadError.connect(on_error)
    downloader.startDownload()
    loop.exec_()

    if error_occurred[0]:
        raise GBIFNetworkError(f"Failed to fetch {url}: {error_message[0]}")

    try:
        with open(output_path, "rt", encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise GBIFNetworkError(f"Invalid JSON response from {url}: {e}")
    finally:
        # Clean up temp file
        try:
            os.unlink(output_path)
        except OSError:
            pass


def name_parser(name: str, **kwargs) -> List[Dict[str, Any]]:
    """Parse taxon names using the GBIF name parser.

    Args:
        name: A scientific name string to parse.

    Returns:
        List of parsed name dictionaries.

    Reference:
        https://www.gbif.org/developer/species#parser

    Example:
        >>> name_parser('Vanessa atalanta (Linnaeus, 1758)')
        [{'scientificName': 'Vanessa atalanta', ...}]
    """
    # URL encode the name
    encoded_name = name.replace(" ", "%20")
    url = f"{GBIF_BASE_URL}parser/name?name={encoded_name}"
    return gbif_GET(url, None, **kwargs)


def name_usage(
    key: Optional[int] = None,
    name: Optional[str] = None,
    data: str = "all",
    language: Optional[str] = None,
    datasetKey: Optional[str] = None,
    uuid: Optional[str] = None,
    sourceId: Optional[int] = None,
    rank: Optional[str] = None,
    shortname: Optional[str] = None,
    limit: int = 100,
    offset: Optional[int] = None,
    **kwargs,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Lookup details for specific names in all taxonomies in GBIF.

    Args:
        key: A GBIF key for a taxon.
        name: Filters by a case insensitive, canonical namestring.
        data: The type of data to get. Options: 'all', 'verbatim', 'name',
            'parents', 'children', 'related', 'synonyms', 'descriptions',
            'distributions', 'media', 'references', 'speciesProfiles',
            'vernacularNames', 'typeSpecimens', 'root'.
        language: Language filter (e.g., 'FRENCH').
        datasetKey: Filter by dataset UUID.
        uuid: A uuid for a dataset (same as datasetKey).
        sourceId: Filter by source identifier.
        rank: Taxonomic rank filter (e.g., 'SPECIES', 'GENUS').
        shortname: A short name.
        limit: Number of records to return (default: 100, max: 1000).
        offset: Record number to start at.

    Returns:
        Species information dictionary or list of dictionaries.

    Reference:
        https://www.gbif.org/developer/species#nameUsages

    Example:
        >>> name_usage(key=5219404)
        {'key': 5219404, 'scientificName': 'Panthera leo', ...}
    """
    data_choices = [
        "all",
        "verbatim",
        "name",
        "parents",
        "children",
        "related",
        "synonyms",
        "descriptions",
        "distributions",
        "media",
        "references",
        "speciesProfiles",
        "vernacularNames",
        "typeSpecimens",
        "root",
    ]

    if data not in data_choices:
        raise ValueError(f"data must be one of: {', '.join(data_choices)}")

    return _name_usage_fetch(data, key, shortname, uuid, **kwargs)


def _name_usage_fetch(
    data: str,
    key: Optional[int],
    shortname: Optional[str],
    uuid: Optional[str],
    **kwargs,
) -> Dict[str, Any]:
    """Internal function to fetch name usage data.

    Args:
        data: Type of data to fetch.
        key: GBIF taxon key.
        shortname: Short name.
        uuid: Dataset UUID.

    Returns:
        Species information dictionary.
    """
    if data != "all" and key is None:
        raise TypeError("You must specify 'key' if 'data' does not equal 'all'")

    if data == "all" and key is None:
        url = f"{GBIF_BASE_URL}species"
    elif data == "all" and key is not None:
        url = f"{GBIF_BASE_URL}species/{key}"
    elif data in [
        "verbatim",
        "name",
        "parents",
        "children",
        "related",
        "synonyms",
        "descriptions",
        "distributions",
        "media",
        "references",
        "speciesProfiles",
        "vernacularNames",
        "typeSpecimens",
    ]:
        url = f"{GBIF_BASE_URL}species/{key}/{data}"
    elif data == "root":
        url = f"{GBIF_BASE_URL}species/{uuid}/{shortname}"
    else:
        raise ValueError(f"Unknown data type: {data}")

    return gbif_GET(url, None, **kwargs)
