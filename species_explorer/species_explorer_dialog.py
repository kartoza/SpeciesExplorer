# SPDX-FileCopyrightText: 2018-2024 Kartoza <info@kartoza.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Species Explorer Dialog.

This module contains the main dialog for the Species Explorer plugin,
handling user interaction for searching species and fetching occurrence data.
"""

import os
from typing import Optional

from qgis.core import Qgis, QgsMessageLog, QgsProject

# PyQt5/PyQt6 compatibility for Qgis.MessageLevel
if hasattr(Qgis, 'MessageLevel'):
    MSG_INFO = Qgis.MessageLevel.Info
    MSG_WARNING = Qgis.MessageLevel.Warning
    MSG_CRITICAL = Qgis.MessageLevel.Critical
else:
    MSG_INFO = Qgis.Info
    MSG_WARNING = Qgis.Warning
    MSG_CRITICAL = Qgis.Critical
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import Qt

# PyQt5/PyQt6 compatibility for Qt.UserRole
if hasattr(Qt, 'ItemDataRole'):
    UserRole = Qt.ItemDataRole.UserRole
else:
    UserRole = Qt.UserRole

from .gbif_fetcher import GBIFFetchTask, fetch_species_async
from .gbifutils import gbif_GET, name_parser, name_usage
from .gui.kartoza_branding import (
    KartozaFooter,
    KartozaHeader,
    StatusLabel,
    apply_kartoza_styling,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "species_explorer_dialog_base.ui")
)


class SpeciesExplorerDialog(QtWidgets.QDialog, FORM_CLASS):
    """Main dialog for Species Explorer plugin.

    Provides UI for searching species and fetching occurrence data
    from GBIF in a non-blocking, cancellable manner.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        """Initialize the dialog.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setupUi(self)
        self._current_task: Optional[GBIFFetchTask] = None
        self._setup_branding()
        self._connect_signals()

    def _setup_branding(self) -> None:
        """Set up Kartoza branding and styling."""
        apply_kartoza_styling(self)

        main_layout = self.layout()

        # Add header at the top
        self.header = KartozaHeader(
            title="Species Explorer",
            subtitle="Explore biodiversity data from GBIF",
        )
        main_layout.insertWidget(0, self.header)

        # Add status label
        self.status_label = StatusLabel()
        main_layout.insertWidget(main_layout.count() - 1, self.status_label)

        # Add footer at the bottom
        self.footer = KartozaFooter()
        main_layout.addWidget(self.footer)

        # Enable alternating row colors for lists
        self.results_list.setAlternatingRowColors(True)
        self.taxonomy_list.setAlternatingRowColors(True)

        # Set tooltips
        self.search_text.setToolTip("Enter a scientific or common species name")
        self.search_button.setToolTip("Search GBIF for matching species")
        self.fetch_button.setToolTip(
            "Download occurrence records for selected species (runs in background)"
        )
        self.results_list.setToolTip("Click a species to view its taxonomy")
        self.taxonomy_list.setToolTip("Taxonomic classification of selected species")

    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        self.search_button.clicked.connect(self.find)
        self.fetch_button.clicked.connect(self.fetch)
        self.results_list.itemClicked.connect(self.select)
        self.search_text.returnPressed.connect(self.find)

    def _set_status(self, message: str, is_error: bool = False) -> None:
        """Set the status message.

        Args:
            message: Status message to display.
            is_error: Whether this is an error message.
        """
        self.status_label.set_status(message, is_error)
        QtWidgets.QApplication.processEvents()

    def _clear_status(self) -> None:
        """Clear the status message."""
        self.status_label.clear_status()

    def _set_fetching_state(self, fetching: bool) -> None:
        """Update UI state during fetch operation.

        Args:
            fetching: Whether a fetch is in progress.
        """
        self.fetch_button.setEnabled(not fetching)
        self.search_button.setEnabled(not fetching)
        self.results_list.setEnabled(not fetching)

        if fetching:
            self.fetch_button.setText("Fetching...")
        else:
            self.fetch_button.setText("Fetch Occurrences")

    def find(self) -> None:
        """Search GBIF for the species provided."""
        text = self.search_text.text().strip()
        if not text:
            self._set_status("Please enter a species name", is_error=True)
            return

        self._set_status(f"Searching for '{text}'...")
        self.taxonomy_list.clear()

        try:
            parsed_species = name_parser(text)[0]
            genus = parsed_species.get("genusOrAbove", text)
            species = parsed_species.get("specificEpithet", "")
        except (KeyError, IndexError):
            genus = text
            species = ""

        QgsMessageLog.logMessage(f"Searching for {text}", "SpeciesExplorer", MSG_INFO)

        url = (
            "https://api.gbif.org/v1/species/search?"
            f"q={genus}%20{species}&rank=SPECIES&qField=SCIENTIFIC&status=ACCEPTED"
        )

        try:
            matches = gbif_GET(url, None)
        except Exception as e:
            self._set_status(f"Search failed: {e}", is_error=True)
            return

        self.results_list.clear()
        names = {}

        for match in matches.get("results", []):
            name = match.get("canonicalName")
            if not name or name in names:
                continue

            if "nubKey" in match:
                taxon_key = match["nubKey"]
            elif "speciesKey" in match:
                taxon_key = match["speciesKey"]
            else:
                continue

            species_item = QtWidgets.QListWidgetItem(name)
            species_item.setData(UserRole, taxon_key)
            self.results_list.addItem(species_item)
            names[name] = taxon_key

        count = len(names)
        if count > 0:
            self._set_status(f"Found {count} species matching '{text}'")
        else:
            self._set_status(f"No species found matching '{text}'", is_error=True)

    def select(self, item: QtWidgets.QListWidgetItem) -> None:
        """Handle species selection from results list.

        Args:
            item: QListWidgetItem that was clicked.
        """
        species_name = item.text()
        self._set_status(f"Loading taxonomy for {species_name}...")

        QgsMessageLog.logMessage(f"{species_name} selected", "SpeciesExplorer", MSG_INFO)

        try:
            species = name_usage(item.data(UserRole))
        except Exception as e:
            self._set_status(f"Failed to load taxonomy: {e}", is_error=True)
            return

        self.taxonomy_list.clear()

        taxonomy_fields = [
            ("Kingdom", "kingdom"),
            ("Phylum", "phylum"),
            ("Class", "class"),
            ("Order", "order"),
            ("Family", "family"),
            ("Genus", "genus"),
            ("Species", "species"),
            ("Taxon ID", "taxonID"),
            ("Canonical Name", "canonicalName"),
        ]

        for label, key in taxonomy_fields:
            if key in species:
                self.taxonomy_list.addItem(f"{label}: {species[key]}")

        if "accepted" in species:
            self.taxonomy_list.addItem(f"Accepted Name: {species['accepted']}")

        self.taxonomy_list.addItem(f"Accepted Key: {item.data(UserRole)}")
        self._set_status(f"Selected: {species_name}")

    def fetch(self) -> None:
        """Fetch occurrence records for selected taxon asynchronously.

        This method starts a background task that fetches data without
        blocking the UI. The task can be cancelled by the user.
        """
        if not self.results_list.selectedItems():
            self._set_status("Please select a species first", is_error=True)
            return

        # Cancel any existing task
        if self._current_task and self._current_task.status() == 1:  # Running
            self._current_task.cancel()

        name = self.results_list.selectedItems()[0].text()
        self._set_status(f"Fetching occurrences for {name} (background task)...")
        self._set_fetching_state(True)

        QgsMessageLog.logMessage(
            f"Starting async fetch for {name}", "SpeciesExplorer", MSG_INFO
        )

        # Start async fetch
        self._current_task = fetch_species_async(
            species_name=name,
            on_finished=self._on_fetch_finished,
        )

    def _on_fetch_finished(self, task: GBIFFetchTask) -> None:
        """Handle fetch task completion.

        Args:
            task: The completed fetch task.
        """
        self._set_fetching_state(False)
        self._current_task = None

        if task.status() == 4:  # Cancelled
            self._set_status("Fetch cancelled", is_error=False)
            return

        if task.layer:
            QgsProject.instance().addMapLayer(task.layer)
            self._set_status(
                f"Added {task.record_count} occurrences for {task.species_name}"
            )
            QgsMessageLog.logMessage(
                f"Successfully fetched {task.record_count} records",
                "SpeciesExplorer",
                MSG_INFO,
            )
        else:
            self._set_status(
                f"Fetch failed: {task.error_message or 'Unknown error'}",
                is_error=True,
            )
            QgsMessageLog.logMessage(
                f"Fetch failed: {task.error_message}",
                "SpeciesExplorer",
                MSG_CRITICAL,
            )

    def cancel_fetch(self) -> None:
        """Cancel the current fetch operation if running."""
        if self._current_task and self._current_task.status() == 1:
            self._current_task.cancel()
            self._set_status("Cancelling fetch...")

    def closeEvent(self, event) -> None:
        """Handle dialog close event.

        Args:
            event: Close event.
        """
        # Cancel any running task
        if self._current_task and self._current_task.status() == 1:
            self._current_task.cancel()
        super().closeEvent(event)
