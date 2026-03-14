# SPDX-FileCopyrightText: 2018-2024 Kartoza <info@kartoza.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Async GBIF data fetcher using QgsTask.

This module provides non-blocking, cancellable data fetching from GBIF
using QGIS task infrastructure.
"""

import json
from typing import Any, Callable, Dict, List, Optional

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsMessageLog,
    QgsNetworkAccessManager,
    QgsPointXY,
    QgsProject,
    QgsTask,
    QgsVectorLayer,
)

# PyQt5/PyQt6 compatibility for Qgis.MessageLevel
if hasattr(Qgis, 'MessageLevel'):
    MSG_INFO = Qgis.MessageLevel.Info
    MSG_WARNING = Qgis.MessageLevel.Warning
    MSG_CRITICAL = Qgis.MessageLevel.Critical
else:
    MSG_INFO = Qgis.Info
    MSG_WARNING = Qgis.Warning
    MSG_CRITICAL = Qgis.Critical
from qgis.PyQt.QtCore import QEventLoop, QUrl, QVariant
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

# GBIF API limits
GBIF_PAGE_SIZE = 300  # Max records per page
GBIF_MAX_OFFSET = 100000  # Hard limit for search API


class GBIFFetchTask(QgsTask):
    """Background task for fetching GBIF occurrence data.

    This task runs in a background thread and emits progress updates
    that can be used to update the UI without blocking.

    Attributes:
        species_name: Scientific name to search for.
        layer: The resulting vector layer (set after completion).
        error_message: Error message if task failed.
        record_count: Number of records fetched.
    """

    def __init__(
        self,
        species_name: str,
        description: str = "Fetching GBIF occurrences",
        on_finished: Optional[Callable] = None,
    ):
        """Initialize the fetch task.

        Args:
            species_name: Scientific name to search for.
            description: Task description for progress dialog.
            on_finished: Optional callback when task completes.
        """
        super().__init__(description, QgsTask.CanCancel)
        self.species_name = species_name
        self.layer: Optional[QgsVectorLayer] = None
        self.error_message: str = ""
        self.record_count: int = 0
        self._on_finished = on_finished
        self._records_data: List[Dict[str, Any]] = []  # Store raw record data
        self._field_names: List[str] = []
        self._total_count: int = 0

    def run(self) -> bool:
        """Execute the task in background thread.

        Returns:
            True if successful, False otherwise.
        """
        try:
            return self._fetch_occurrences()
        except Exception as e:
            self.error_message = str(e)
            QgsMessageLog.logMessage(
                f"GBIF fetch error: {e}", "SpeciesExplorer", level=MSG_CRITICAL
            )
            return False

    def _fetch_occurrences(self) -> bool:
        """Fetch occurrence records from GBIF.

        Returns:
            True if successful, False otherwise.
        """
        offset = 0
        end_of_records = False

        # First request to get total count
        first_result = self._make_request(offset)
        if first_result is None:
            return False

        self._total_count = first_result.get("count", 0)

        if self._total_count == 0:
            self.error_message = f"No records found for {self.species_name}"
            return False

        if self._total_count > GBIF_MAX_OFFSET:
            QgsMessageLog.logMessage(
                f"Warning: {self._total_count} records found, but GBIF API limits to {GBIF_MAX_OFFSET}. "
                "Consider using GBIF's download service for complete data.",
                "SpeciesExplorer",
                level=MSG_WARNING,
            )

        # Process first batch
        self._process_records(first_result.get("results", []))
        offset += GBIF_PAGE_SIZE
        end_of_records = first_result.get("endOfRecords", False)

        # Fetch remaining pages
        while not end_of_records and offset < GBIF_MAX_OFFSET:
            if self.isCanceled():
                return False

            # Update progress
            progress = min(100, (offset / min(self._total_count, GBIF_MAX_OFFSET)) * 100)
            self.setProgress(progress)

            result = self._make_request(offset)
            if result is None:
                return False

            self._process_records(result.get("results", []))
            end_of_records = result.get("endOfRecords", False)
            offset += GBIF_PAGE_SIZE

        self.setProgress(100)
        return True

    def _make_request(self, offset: int) -> Optional[Dict[str, Any]]:
        """Make a synchronous request to GBIF API.

        Args:
            offset: Record offset for pagination.

        Returns:
            Parsed JSON response or None on error.
        """
        url = (
            f"https://api.gbif.org/v1/occurrence/search?"
            f"scientificName={self.species_name}&limit={GBIF_PAGE_SIZE}&offset={offset}"
        )

        QgsMessageLog.logMessage(f"Fetching: {url}", "SpeciesExplorer", level=MSG_INFO)

        # Use QgsNetworkAccessManager for thread-safe requests
        nam = QgsNetworkAccessManager.instance()
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # Synchronous request in background thread
        loop = QEventLoop()
        reply = nam.get(request)
        reply.finished.connect(loop.quit)
        loop.exec_()

        if reply.error() != QNetworkReply.NoError:
            self.error_message = f"Network error: {reply.errorString()}"
            reply.deleteLater()
            return None

        data = reply.readAll().data().decode("utf-8")
        reply.deleteLater()

        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            self.error_message = f"Invalid JSON response: {e}"
            return None

    def _process_records(self, records: List[Dict[str, Any]]) -> None:
        """Process occurrence records into raw data for later feature creation.

        Args:
            records: List of GBIF occurrence records.
        """
        for record in records:
            if self.isCanceled():
                return

            # Skip records without coordinates
            if "decimalLongitude" not in record or "decimalLatitude" not in record:
                continue

            try:
                lon = float(record["decimalLongitude"])
                lat = float(record["decimalLatitude"])
            except (ValueError, TypeError):
                continue

            # Initialize field names from first valid record
            if not self._field_names:
                self._field_names = list(record.keys())

            # Store raw data - we'll create features later with proper field mapping
            self._records_data.append({
                "lon": lon,
                "lat": lat,
                "attributes": record,
            })
            self.record_count += 1

    def finished(self, result: bool) -> None:
        """Called when task completes (in main thread).

        Args:
            result: True if task succeeded.
        """
        QgsMessageLog.logMessage(
            f"finished() called: result={result}, records_data_len={len(self._records_data)}, "
            f"record_count={self.record_count}, field_names_len={len(self._field_names)}",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        if result and self._records_data:
            self._create_layer()
        elif not result:
            QgsMessageLog.logMessage(
                f"Task did not succeed: {self.error_message}",
                "SpeciesExplorer",
                level=MSG_CRITICAL,
            )
        elif not self._records_data:
            QgsMessageLog.logMessage(
                "No records data available despite record_count > 0",
                "SpeciesExplorer",
                level=MSG_CRITICAL,
            )

        if self._on_finished:
            self._on_finished(self)

    def _create_layer(self) -> None:
        """Create vector layer from fetched data."""
        QgsMessageLog.logMessage(
            f"_create_layer called with {len(self._records_data)} records, {len(self._field_names)} fields",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        # Sanitize field names (remove special chars, limit length)
        safe_field_names = []
        for name in self._field_names:
            safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
            safe_name = safe_name[:60]  # Limit field name length
            if not safe_name:
                safe_name = "field"
            safe_field_names.append(safe_name)

        # Build field definitions for URI
        field_defs = "&".join([f"field={name}:string(255)" for name in safe_field_names])
        uri = f"Point?crs=EPSG:4326&{field_defs}"

        QgsMessageLog.logMessage(
            f"Creating layer with URI (first 200 chars): {uri[:200]}...",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        # Create layer with fields in URI
        self.layer = QgsVectorLayer(uri, self.species_name, "memory")

        if not self.layer.isValid():
            QgsMessageLog.logMessage(
                "Failed to create valid memory layer!",
                "SpeciesExplorer",
                level=MSG_CRITICAL,
            )
            return

        provider = self.layer.dataProvider()
        if provider is None:
            QgsMessageLog.logMessage(
                "Failed to get data provider!",
                "SpeciesExplorer",
                level=MSG_CRITICAL,
            )
            return

        QgsMessageLog.logMessage(
            f"Layer has {self.layer.fields().count()} fields, provider caps: {provider.capabilities()}",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        # Create features with proper field mapping
        layer_fields = self.layer.fields()
        features = []
        for i, record_data in enumerate(self._records_data):
            feature = QgsFeature(layer_fields)
            geom = QgsGeometry.fromPointXY(
                QgsPointXY(record_data["lon"], record_data["lat"])
            )
            feature.setGeometry(geom)

            # Build attributes list in field order
            attributes = []
            for orig_name in self._field_names:
                value = record_data["attributes"].get(orig_name, "")
                attributes.append(str(value) if value is not None else "")

            feature.setAttributes(attributes)
            features.append(feature)

            # Log first feature for debugging
            if i == 0:
                QgsMessageLog.logMessage(
                    f"First feature: geom_valid={geom.isGeosValid()}, attrs_count={len(attributes)}, "
                    f"field_count={layer_fields.count()}",
                    "SpeciesExplorer",
                    level=MSG_INFO,
                )

        # Add features using data provider
        QgsMessageLog.logMessage(
            f"Adding {len(features)} features to provider...",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        # Start editing, add features, commit
        self.layer.startEditing()
        for feature in features:
            self.layer.addFeature(feature)
        commit_success = self.layer.commitChanges()

        QgsMessageLog.logMessage(
            f"commitChanges result: {commit_success}, layer feature count: {self.layer.featureCount()}",
            "SpeciesExplorer",
            level=MSG_INFO,
        )

        self.layer.updateExtents()

    def cancel(self) -> None:
        """Request task cancellation."""
        QgsMessageLog.logMessage(
            f"Cancelling GBIF fetch for {self.species_name}",
            "SpeciesExplorer",
            level=MSG_INFO,
        )
        super().cancel()


def fetch_species_async(
    species_name: str,
    on_finished: Optional[Callable[[GBIFFetchTask], None]] = None,
) -> GBIFFetchTask:
    """Fetch species occurrences asynchronously.

    This is the main entry point for async fetching. The task runs
    in the background and calls on_finished when complete.

    Args:
        species_name: Scientific name to search for.
        on_finished: Callback function receiving the completed task.

    Returns:
        The running task (can be used to check status or cancel).

    Example:
        >>> def handle_result(task):
        ...     if task.layer:
        ...         QgsProject.instance().addMapLayer(task.layer)
        ...     else:
        ...         print(f"Error: {task.error_message}")
        >>> task = fetch_species_async("Panthera leo", handle_result)
    """
    task = GBIFFetchTask(
        species_name=species_name,
        description=f"Fetching occurrences for {species_name}",
        on_finished=on_finished,
    )

    QgsApplication.taskManager().addTask(task)
    return task
