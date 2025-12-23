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
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:0.5 #9B59B6, stop:1 #E74C3C);
                border-radius: 15px;
                border: 3px solid #2C3E50;
            }
        """)
        main_layout.addWidget(title_label)

        # Game icon/logo
        game_icon = QLabel("♠♥♣♦")
        game_icon.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        game_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_icon.setStyleSheet("""
            QLabel {
                color: #E74C3C;
                padding: 10px;
            }
        """)
        main_layout.addWidget(game_icon)

        # Game rules/instructions
        rules_group = QGroupBox("Game Rules")
        rules_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #3498DB;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2C3E50;
            }
        """)

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
        self.start_button.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.start_button.setFixedSize(300, 70)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27AE60, stop:1 #2ECC71);
                color: white;
                border-radius: 15px;
                border: 3px solid #1E8449;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #229954, stop:1 #27AE60);
                border: 3px solid #145A32;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1E8449, stop:1 #229954);
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
            }
        """)

    def start_game(self):
        """Switch to game page"""
        if self.parent:
            self.parent.show_game_page()