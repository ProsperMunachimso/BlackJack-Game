from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class WelcomePage(QWidget):
    """Welcome page with game introduction and start button"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize welcome page UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)

        # Title with animation effect
        title_label = QLabel(" Welcome to ZA Great's and Victor's Card Game ")
        title_label.setObjectName("titleLabel")  # Set object name for QSS
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Game icon/logo
        game_icon = QLabel("♠♥♣♦")
        game_icon.setObjectName("gameIcon")  # Set object name for QSS
        game_icon.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        game_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(game_icon)

        # Game rules/instructions
        rules_group = QGroupBox("Game Rules")
        rules_group.setObjectName("rulesGroup")  # Set object name for QSS

        rules_layout = QVBoxLayout()
        rules_text = QLabel("""
        <div style='font-size: 14pt; line-height: 1.6; text-align: left;'>
        <b>How to Play:</b><br>
        • Get as close to 21 as possible without going over<br>
        • Dealer must hit on 16 and stand on 17<br>
        • Aces count as 1 or 11<br>
        • Face cards (J, Q, K) are worth 10<br>
        • Number cards are worth their face value<br><br>
        <b>Controls:</b><br>
        • <b>Hit:</b> Take another card<br>
        • <b>Stand:</b> End your turn<br>
        • <b>New Round:</b> Start a new game<br>
        • <b>Theme:</b> Switch between light/dark mode
        </div>
        """)
        rules_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        rules_layout.addWidget(rules_text)
        rules_group.setLayout(rules_layout)

        main_layout.addWidget(rules_group)

        # Start game button
        self.start_button = QPushButton(" START GAME ")
        self.start_button.setObjectName("startButton")  # Set object name for QSS
        self.start_button.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.start_button.setFixedSize(300, 70)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_button.clicked.connect(self.start_game)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_game(self):
        """Switch to game page"""
        if self.parent:
            self.parent.show_game_page()