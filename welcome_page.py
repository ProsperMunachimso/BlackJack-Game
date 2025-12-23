from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("🎮 21 Card Game")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("A classic card game similar to Blackjack")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 18))
        layout.addWidget(subtitle)

        layout.addStretch()

        # Rules
        rules = QGroupBox("📜 How to Play")
        rules_layout = QVBoxLayout()
        rules_text = QLabel(
            "<b>Objective:</b> Get as close to 21 as possible without going over.<br><br>"
            "<b>Card Values:</b><br>"
            "• Number cards = face value (2-10)<br>"
            "• Face cards (J, Q, K) = 10<br>"
            "• Ace = 1 or 11 (whichever is better)<br><br>"
            "<b>Game Flow:</b><br>"
            "1. Click 'Start Game' to begin<br>"
            "2. Click 'New Round' to deal cards<br>"
            "3. Choose 'Hit' to draw a card<br>"
            "4. Choose 'Stand' to end your turn<br>"
            "5. Dealer reveals cards and plays automatically<br>"
            "6. Winner is determined"
        )
        rules_text.setWordWrap(True)
        rules_layout.addWidget(rules_text)
        rules.setLayout(rules_layout)
        layout.addWidget(rules)

        layout.addStretch()

        # Start button
        start_btn = QPushButton("🚀 Start Game")
        start_btn.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        start_btn.setFixedSize(300, 70)
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Footer
        footer = QLabel("© 2024 21 Card Game - HGP Assignment")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFont(QFont("Arial", 10))
        layout.addWidget(footer)

        self.setLayout(layout)

    def start_game(self):
        if self.parent:
            self.parent.show_game_page()