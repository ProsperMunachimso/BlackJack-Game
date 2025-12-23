from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

# Import modules
from game_logic import Game21
from welcome_page import WelcomePage
from game_page import GamePage


def load_stylesheet(filename):
    """Load and return the QSS stylesheet from file"""
    try:
        if not os.path.exists(filename):
            print(f"❌ ERROR: Stylesheet file '{filename}' not found!")
            return ""

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"✅ Successfully loaded '{filename}' ({len(content)} chars)")
            return content
    except Exception as e:
        print(f"❌ ERROR loading stylesheet: {e}")
        return ""


class MainWindow(QMainWindow):
    """Main application window with stacked pages"""

    def __init__(self):
        super().__init__()
        print("🚀 MainWindow initializing...")
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

        # Show welcome page initially
        self.stacked_widget.setCurrentWidget(self.welcome_page)

        print("✅ MainWindow initialization complete")

    def show_game_page(self):
        """Switch to game page and reset game"""
        self.game_page.game.reset_game()
        self.stacked_widget.setCurrentWidget(self.game_page)
        self.status_bar.showMessage("New game started! Click 'New Round' to begin playing.")
        self.game_page.new_round_setup()

    def show_welcome_page(self):
        """Switch to welcome page"""
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.status_bar.showMessage("Welcome to 21 Card Game! Click 'Start Game' to begin.")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    print("=" * 50)
    print("🚀 STARTING 21 CARD GAME")
    print("=" * 50)

    # Set application style
    app.setStyle("Fusion")

    # Load and apply global stylesheet
    stylesheet = load_stylesheet("style.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("✅ Global stylesheet applied")
    else:
        print("⚠️ No stylesheet applied - using default styling")

    # Set application font
    font = QFont("Arial", 10)
    app.setFont(font)

    # Create and show main window
    window = MainWindow()
    window.show()

    print("✅ Application running")
    print("=" * 50)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()