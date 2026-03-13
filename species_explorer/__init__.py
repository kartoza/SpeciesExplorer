# SPDX-FileCopyrightText: 2018-2024 Kartoza <info@kartoza.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Species Explorer QGIS Plugin.

A QGIS plugin for quickly fetching and visualizing species occurrence
data from GBIF (Global Biodiversity Information Facility).
"""


def classFactory(iface):  # noqa: N802
    """Load SpeciesExplorer class from file species_explorer.

    Args:
        iface: A QGIS interface instance.

    Returns:
        SpeciesExplorer plugin instance.
    """
    from .species_explorer import SpeciesExplorer

    return SpeciesExplorer(iface)
