from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
)
from PyQt6.QtCore import Qt
import sys

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of 21")

        # set the windows dimensions
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(500, 450)

        self.game = Game21()

        self.initUI()

        # Start first round
        self.new_round_setup()

    def initUI(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("21 Card Game")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50; margin: 10px;")
        main_layout.addWidget(title_label)

        # Dealer Section
        dealer_group = QGroupBox("Dealer")
        dealer_layout = QVBoxLayout()

        self.dealer_total_label = QLabel("Total: --")
        self.dealer_total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #E74C3C;")
        dealer_layout.addWidget(self.dealer_total_label)

        self.dealerCardsLayout = QHBoxLayout()
        dealer_layout.addLayout(self.dealerCardsLayout)

        dealer_group.setLayout(dealer_layout)
        main_layout.addWidget(dealer_group)

        # Spacer
        main_layout.addSpacing(20)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.result_label)

        # Player Section
        player_group = QGroupBox("Player")
        player_layout = QVBoxLayout()

        self.player_total_label = QLabel("Total: --")
        self.player_total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27AE60;")
        player_layout.addWidget(self.player_total_label)

        self.playerCardsLayout = QHBoxLayout()
        player_layout.addLayout(self.playerCardsLayout)

        player_group.setLayout(player_layout)
        main_layout.addWidget(player_group)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()

        self.hit_button = QPushButton("Hit")
        self.hit_button.setFixedSize(100, 40)
        self.hit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        self.hit_button.clicked.connect(self.on_hit)
        controls_layout.addWidget(self.hit_button)

        self.stand_button = QPushButton("Stand")
        self.stand_button.setFixedSize(100, 40)
        self.stand_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        self.stand_button.clicked.connect(self.on_stand)
        controls_layout.addWidget(self.stand_button)

        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setFixedSize(100, 40)
        self.new_round_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.new_round_button.clicked.connect(self.on_new_round)
        controls_layout.addWidget(self.new_round_button)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        # Status bar
        self.status_bar = QLabel("Ready to play! Click 'New Round' to start a new game.")
        self.status_bar.setStyleSheet("padding: 5px; background-color: #ECF0F1; color: #2C3E50;")
        main_layout.addWidget(self.status_bar)

        # Set accessible names for screen readers
        self.hit_button.setAccessibleName("Hit button. Draw another card.")
        self.stand_button.setAccessibleName("Stand button. End your turn.")
        self.new_round_button.setAccessibleName("New Round button. Start a new game.")

    # BUTTON ACTIONS

    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)
        self.player_total_label.setText(f"Total: {self.game.player_total()}")

        if self.game.player_total() > 21:
            # TODO: what should happen if a player goes over 21? Remove pass when complete
            self.result_label.setText("Bust! You went over 21.")
            self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E74C3C; padding: 10px;")
            self.end_round()
            self.update_dealer_cards(full=True)
            self.dealer_total_label.setText(f"Total: {self.game.dealer_total()}")
            self.status_bar.setText("Player busted. Click 'New Round' to play again.")

    def on_stand(self):
        # TODO: Player ends turn; dealer reveals their hidden card and plays. Remove pass when complete
        self.game.reveal_dealer_card()
        self.update_dealer_cards(full=True)
        self.dealer_total_label.setText(f"Total: {self.game.dealer_total()}")
        self.game.play_dealer_turn()

        # Update dealer total after dealer plays
        self.dealer_total_label.setText(f"Total: {self.game.dealer_total()}")

        # Show result
        result_text = self.game.decide_winner()
        self.result_label.setText(result_text)

        # Set color based on result
        if "Player wins" in result_text:
            self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27AE60; padding: 10px;")
        elif "Dealer wins" in result_text:
            self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E74C3C; padding: 10px;")
        else:
            self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #7F8C8D; padding: 10px;")

        self.end_round()
        self.status_bar.setText(f"Round ended: {result_text} Click 'New Round' to play again.")

    def on_new_round(self):
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS

    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, layout, card_text):
        # Create a QLabel showing the card value and add it to the chosen layout.
        label = QLabel(card_text)
        label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                padding: 15px 10px;
                font-size: 20px;
                font-weight: bold;
                margin: 5px;
                min-width: 60px;
                text-align: center;
            }
        """)

        # Color the card based on suit
        if "♥" in card_text or "♦" in card_text:
            label.setStyleSheet(label.styleSheet() + "color: #E74C3C;")
        else:
            label.setStyleSheet(label.styleSheet() + "color: #2C3E50;")

        layout.addWidget(label)
        label.setProperty("card", True)

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                # Create a face-down card
                hidden_label = QLabel("??")
                hidden_label.setStyleSheet("""
                    QLabel {
                        background-color: #3498DB;
                        color: white;
                        border: 2px solid #2980B9;
                        border-radius: 5px;
                        padding: 15px 10px;
                        font-size: 20px;
                        font-weight: bold;
                        margin: 5px;
                        min-width: 60px;
                        text-align: center;
                    }
                """)
                self.dealerCardsLayout.addWidget(hidden_label)
            else:
                self.add_card(self.dealerCardsLayout, card)

        # TODO: update relevant labels in response to dealer actions. Remove pass when complete
        if full:
            # When dealer cards are fully revealed, update the total
            self.dealer_total_label.setText(f"Total: {self.game.dealer_total()}")
        else:
            # Don't show the total until cards are revealed
            self.dealer_total_label.setText("Total: --")

    def new_round_setup(self):
        # TODO: Prepare a fresh visual layout
        self.game.deal_initial_cards()

        # Clear card layouts
        self.clear_layout(self.playerCardsLayout)
        self.clear_layout(self.dealerCardsLayout)

        # TODO: update relevant labels (reset dealer and player totals)
        self.player_total_label.setText(f"Total: {self.game.player_total()}")
        self.dealer_total_label.setText("Total: --")
        self.result_label.setText("")
        self.result_label.setStyleSheet("")

        # TODO: display new cards for dealers and players
        # Add player cards
        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)

        # Add dealer cards (with one hidden)
        self.update_dealer_cards(full=False)

        # TODO: enable buttons for Stand and Hit - Remove pass when complete
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.new_round_button.setEnabled(True)

        self.status_bar.setText("Your turn. Click 'Hit' to draw a card or 'Stand' to end your turn.")

    def end_round(self):
        # TODO: Disable button actions after the round ends. Remove pass when complete
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.new_round_button.setEnabled(True)


# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application style and palette for accessibility
    app.setStyle("Fusion")

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())