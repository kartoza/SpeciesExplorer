# SPDX-FileCopyrightText: 2018-2024 Kartoza <info@kartoza.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kartoza branding utilities for Species Explorer.

Provides consistent styling and branding components following
the Kartoza corporate identity guidelines.
"""

from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

# Kartoza brand colors
KARTOZA_GREEN_DARK = "#589632"
KARTOZA_GREEN_LIGHT = "#93b023"
KARTOZA_GOLD = "#E8B849"


def get_resources_path() -> Path:
    """Get the path to the resources directory."""
    return Path(__file__).parent.parent / "resources"


def load_stylesheet() -> str:
    """Load the Kartoza QSS stylesheet.

    Returns:
        The stylesheet content as a string, or empty string if not found.
    """
    stylesheet_path = get_resources_path() / "styles" / "kartoza.qss"
    if stylesheet_path.exists():
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def apply_kartoza_styling(widget: QWidget) -> None:
    """Apply Kartoza branding stylesheet to a widget.

    Args:
        widget: The widget to style.
    """
    stylesheet = load_stylesheet()
    if stylesheet:
        widget.setStyleSheet(stylesheet)


class KartozaFooter(QWidget):
    """A branded footer widget with Kartoza links."""

    def __init__(self, parent: QWidget = None):
        """Initialize the Kartoza footer.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the footer UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Create the footer label with HTML content
        footer_label = QLabel()
        footer_label.setObjectName("kartoza_footer")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setOpenExternalLinks(True)
        footer_label.setTextFormat(Qt.RichText)

        footer_html = """
        <div style="text-align: center; font-size: 11px; color: #589632;">
            Made with &#10084; by
            <a href="https://kartoza.com" style="color: #93b023; text-decoration: none;">Kartoza</a>
            &nbsp;|&nbsp;
            <a href="https://github.com/sponsors/timlinux" style="color: #93b023; text-decoration: none;">Donate</a>
            &nbsp;|&nbsp;
            <a href="https://github.com/kartoza/SpeciesExplorer" style="color: #93b023; text-decoration: none;">GitHub</a>
        </div>
        """
        footer_label.setText(footer_html)

        layout.addStretch()
        layout.addWidget(footer_label)
        layout.addStretch()


class KartozaHeader(QWidget):
    """A branded header widget with logo and title."""

    def __init__(
        self,
        title: str = "Species Explorer",
        subtitle: str = "",
        parent: QWidget = None,
    ):
        """Initialize the Kartoza header.

        Args:
            title: Main title text.
            subtitle: Optional subtitle text.
            parent: Parent widget.
        """
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the header UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        # Logo
        logo_label = QLabel()
        icon_path = get_resources_path().parent / "icon.png"
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            scaled_pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(48, 48)

        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)

        # Main title
        title_label = QLabel(self._title)
        title_label.setObjectName("header_label")
        title_label.setStyleSheet(
            f"""
            font-size: 18px;
            font-weight: bold;
            color: {KARTOZA_GREEN_DARK};
            """
        )
        title_layout.addWidget(title_label)

        # Subtitle if provided
        if self._subtitle:
            subtitle_label = QLabel(self._subtitle)
            subtitle_label.setStyleSheet(
                f"""
                font-size: 12px;
                color: {KARTOZA_GREEN_LIGHT};
                """
            )
            title_layout.addWidget(subtitle_label)

        title_layout.addStretch()

        layout.addWidget(logo_label)
        layout.addWidget(title_widget)
        layout.addStretch()

        # Style the header background
        self.setStyleSheet(
            f"""
            KartozaHeader {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(88, 150, 50, 0.1),
                    stop:1 rgba(147, 176, 35, 0.05)
                );
                border-bottom: 2px solid {KARTOZA_GREEN_DARK};
                border-radius: 4px;
            }}
            """
        )


class StatusLabel(QLabel):
    """A styled status label for showing operation progress."""

    def __init__(self, parent: QWidget = None):
        """Initialize the status label.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setObjectName("status_label")
        self.setAlignment(Qt.AlignCenter)
        self.clear_status()

    def set_status(self, message: str, is_error: bool = False) -> None:
        """Set the status message.

        Args:
            message: Status message to display.
            is_error: Whether this is an error message.
        """
        color = "#e74c3c" if is_error else KARTOZA_GREEN_DARK
        self.setStyleSheet(f"color: {color}; font-style: italic; padding: 4px;")
        self.setText(message)

    def clear_status(self) -> None:
        """Clear the status message."""
        self.setText("")
