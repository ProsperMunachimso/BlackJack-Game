from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import os

from welcome_page import WelcomePage
from game_page import GamePage


def load_stylesheet(filename):
    """This method loads and returns the QSS stylesheet from a file"""
    try:
        if not os.path.exists(filename): # This checks if the stylesheet file exists in the file system.
            print(f" ERROR: Stylesheet file '{filename}' not found!")
            return ""

        # This opens the file for reading.
        with open(filename, 'r', encoding='utf-8') as f:
            # This reads the entire content of the stylesheet file
            content = f.read()
            print(f" Successfully loaded '{filename}' ({len(content)} chars)")
            return content
    except Exception as e:
        print(f" ERROR loading stylesheet: {e}")
        return ""


class MainWindow(QMainWindow):
    """This is the main application window that manages the page navigation"""

    def __init__(self):
        # This calls the parent class constructor
        super().__init__()
        print(" MainWindow initializing...")
        # This sets the initial theme to light mode
        self.current_theme = "light"
        # This calls the method to set up the user interface
        self.init_ui()

    def init_ui(self):
        """This method initializes the user interface"""
        self.setWindowTitle("ZA Great's and Victor's 21 Card Game")
        # This sets the minimum window size
        self.setMinimumSize(700, 800)

        # This creates a status bar widget
        self.status_bar = QStatusBar()
        # This adds the status bar to the main window
        self.setStatusBar(self.status_bar)

        # This creates a stacked widget for page navigation
        self.stacked_widget = QStackedWidget()
        # This sets the stacked widget as the central widget of the window
        self.setCentralWidget(self.stacked_widget)

        # This creates the welcome page instance
        self.welcome_page = WelcomePage(self)
        # This adds the welcome page to the stacked widget
        self.stacked_widget.addWidget(self.welcome_page)

        # This creates the game page instance
        self.game_page = GamePage(self)
        # This adds the game page to the stacked widget
        self.stacked_widget.addWidget(self.game_page)

        # This applies the initial theme to all pages
        self.apply_theme_to_all(self.current_theme)

        self.stacked_widget.setCurrentWidget(self.welcome_page)

        self.status_bar.showMessage("Welcome to ZA Great and Victor's 21 Card Game! Click 'Start Game' to begin.")
        # This prints a completion message
        print(" MainWindow initialization complete")

    def apply_theme_to_all(self, theme):
        """This method applies a theme to all pages and the main window. We did this, so the changing themes can be smooter. """
        print(f" Applying {theme} theme to all pages...")

        # This applies the theme to the main window
        self.current_theme = theme
        # This sets a CSS property for styling
        self.setProperty("theme", theme)
        # This refreshes the window's styling
        self.style().unpolish(self)
        self.style().polish(self)

        # This applies the theme to the welcome page
        self.welcome_page.current_theme = theme
        self.welcome_page.setProperty("theme", theme)
        # This calls the welcome page's theme application method
        self.welcome_page.apply_theme(theme)
        # This refreshes the welcome page's styling
        self.welcome_page.style().unpolish(self.welcome_page)
        self.welcome_page.style().polish(self.welcome_page)

        # This applies the theme to the game page
        self.game_page.current_theme = theme
        self.game_page.setProperty("theme", theme)
        # This calls the game page's theme application method
        self.game_page.set_theme(theme)
        # This refreshes the game page's styling
        self.game_page.style().unpolish(self.game_page)
        self.game_page.style().polish(self.game_page)

        # This applies the theme to the status bar
        self.status_bar.setProperty("theme", theme)
        self.status_bar.style().unpolish(self.status_bar)
        self.status_bar.style().polish(self.status_bar)

        # This prints a completion message
        print(f" Theme {theme} applied globally")

    def toggle_theme(self):
        """This method toggles the theme between light and dark"""
        # This determines the new theme based on the current one
        new_theme = "dark" if self.current_theme == "light" else "light"
        print(f" Toggling theme from {self.current_theme} to {new_theme}")

        # This applies the new theme to all components
        self.apply_theme_to_all(new_theme)

        # This creates a status bar message based on the new theme
        message = "Dark theme activated" if new_theme == "dark" else "Light theme activated"
        self.status_bar.showMessage(message)

    def show_game_page(self):
        """This method switches to the game page and resets the game"""
        # This resets the game logic
        self.game_page.game.reset_game()
        # This switches to the game page
        self.stacked_widget.setCurrentWidget(self.game_page)
        self.status_bar.showMessage("New game started! Click 'New Round' to begin playing.")
        # This calls the game page's new round setup method
        self.game_page.new_round_setup()

    def show_welcome_page(self):
        """This method switches to the welcome page"""
        # This switches to the welcome page
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        # This displays a welcome message in the status bar
        self.status_bar.showMessage("Welcome to 21 Card Game! Click 'Start Game' to begin.")


def main():
    """This is the main application entry point"""
    app = QApplication(sys.argv)
    print(" STARTING 21 CARD GAME APPLICATION")

    # This sets the application style to Fusion for consistent look
    app.setStyle("Fusion")
    stylesheet = load_stylesheet("style.qss")
    if stylesheet: # This checks if the stylesheet was loaded successfully
        app.setStyleSheet(stylesheet)
        print(" Global stylesheet applied successfully")
    else:
        print(" No stylesheet applied - using default styling")

    font = QFont("Arial", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    print("  Application is now running")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()