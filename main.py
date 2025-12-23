from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Import modules
from game_logic import Game21
from welcome_page import WelcomePage
from game_page import GamePage


class MainWindow(QMainWindow):
    """Main application window with stacked pages"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("21 Card Game")
        self.setMinimumSize(900, 800)

        # Create stacked widget for page navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create welcome page
        self.welcome_page = WelcomePage(self)
        self.stacked_widget.addWidget(self.welcome_page)

        # Create game page
        self.game_page = GamePage(self)
        self.stacked_widget.addWidget(self.game_page)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to 21 Card Game! Click 'Start Game' to begin.")

        # Apply light theme by default
        self.apply_initial_theme()

        # Show welcome page initially
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def apply_initial_theme(self):
        """Apply initial theme to both pages"""
        # Welcome page has its own styling, so we only need to apply to game page
        self.game_page.set_light_theme()

    def show_game_page(self):
        """Switch to game page"""
        self.stacked_widget.setCurrentWidget(self.game_page)
        self.status_bar.showMessage("Game started! Click 'New Round' to begin playing.")
        self.game_page.new_round_setup()

    def show_welcome_page(self):
        """Switch to welcome page"""
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.status_bar.showMessage("Welcome to 21 Card Game! Click 'Start Game' to begin.")

    def resizeEvent(self, event):
        """Handle window resize for responsiveness"""
        super().resizeEvent(event)
        self.status_bar.showMessage(f"Window size: {self.width()}x{self.height()}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application style and palette for better contrast
    app.setStyle("Fusion")

    # Create and customize palette for accessibility
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 37, 41))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(248, 249, 250))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(33, 37, 41))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(248, 249, 250))
    palette.setColor(QPalette.ColorRole.Text, QColor(33, 37, 41))
    palette.setColor(QPalette.ColorRole.Button, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(41, 128, 185))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Set application font for better readability
    font = QFont("Arial", 10)
    app.setFont(font)

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()