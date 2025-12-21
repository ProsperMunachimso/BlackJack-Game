import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Card:
    """Represents a playing card with suit and rank"""

    def __init__(self, suit, rank):
        self.suit = suit  # 'H', 'D', 'C', 'S'
        self.rank = rank  # 'A', '2', '3', ..., '10', 'J', 'Q', 'K'

        # Define suit symbols and colors
        self.suit_symbols = {
            'H': '♥',  # Hearts (red)
            'D': '♦',  # Diamonds (red)
            'C': '♣',  # Clubs (black)
            'S': '♠'  # Spades (black)
        }

        self.suit_colors = {
            'H': QColor(220, 53, 69),  # Red
            'D': QColor(220, 53, 69),  # Red
            'C': QColor(33, 37, 41),  # Black
            'S': QColor(33, 37, 41)  # Black
        }

    def get_value(self):
        """Get the numerical value of the card"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Default to 11, will be adjusted in hand calculation
        else:
            return int(self.rank)

    def get_display_text(self):
        """Get the text representation of the card"""
        return f"{self.rank}{self.suit_symbols[self.suit]}"

    def get_color(self):
        """Get the color of the card"""
        return self.suit_colors[self.suit]

    def get_suit_name(self):
        """Get the full suit name"""
        names = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
        return names[self.suit]


class Deck:
    """Represents a standard 52-card deck"""

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        """Reset and shuffle the deck"""
        suits = ['H', 'D', 'C', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def draw(self):
        """Draw a card from the deck"""
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop()


class Hand:
    """Represents a player's hand"""

    def __init__(self):
        self.cards = []
        self.is_dealer = False
        self.face_down_card = None  # For dealer's hidden card

    def add_card(self, card, face_up=True):
        """Add a card to the hand"""
        if not face_up and self.is_dealer:
            self.face_down_card = card
        else:
            self.cards.append(card)

    def reveal_hidden_card(self):
        """Reveal the hidden card (for dealer)"""
        if self.face_down_card:
            self.cards.append(self.face_down_card)
            self.face_down_card = None

    def calculate_value(self):
        """Calculate the hand value with optimal ace handling"""
        total = 0
        aces = 0

        # Count all cards (excluding hidden dealer card)
        for card in self.cards:
            value = card.get_value()
            if card.rank == 'A':
                aces += 1
            total += value

        # Adjust for aces if needed
        while total > 21 and aces > 0:
            total -= 10  # Change Ace from 11 to 1
            aces -= 1

        return total

    def is_bust(self):
        """Check if hand is bust"""
        return self.calculate_value() > 21

    def has_blackjack(self):
        """Check if hand is a natural blackjack (21 with 2 cards)"""
        return (len(self.cards) == 2 and
                self.calculate_value() == 21 and
                ('A' in [card.rank for card in self.cards]))

    def clear(self):
        """Clear the hand"""
        self.cards = []
        self.face_down_card = None

    def get_card_count(self):
        """Get total number of cards (including hidden)"""
        return len(self.cards) + (1 if self.face_down_card else 0)


class Game:
    """Manages game state and logic"""

    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.dealer_hand.is_dealer = True
        self.game_state = "idle"  # idle, player_turn, dealer_turn, finished
        self.result = None  # win, lose, push
        self.player_wins = 0
        self.dealer_wins = 0
        self.rounds_played = 0

    def start_new_round(self):
        """Start a new round of the game"""
        # Reset hands
        self.player_hand.clear()
        self.dealer_hand.clear()

        # Reset deck if less than 20 cards
        if len(self.deck.cards) < 20:
            self.deck.reset()

        # Deal initial cards
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw(), face_up=False)

        # Check for player blackjack
        if self.player_hand.has_blackjack():
            self.game_state = "finished"
            self.dealer_hand.reveal_hidden_card()
            # Check if dealer also has blackjack
            if self.dealer_hand.has_blackjack():
                self.result = "push"
            else:
                self.result = "win"
                self.player_wins += 1
            self.rounds_played += 1
        else:
            self.game_state = "player_turn"
            self.result = None

        return self.game_state

    def player_hit(self):
        """Player draws a card"""
        if self.game_state != "player_turn":
            return False

        self.player_hand.add_card(self.deck.draw())

        if self.player_hand.is_bust():
            self.game_state = "finished"
            self.result = "lose"
            self.dealer_wins += 1
            self.rounds_played += 1
            self.dealer_hand.reveal_hidden_card()
            return False

        return True

    def player_stand(self):
        """Player ends their turn"""
        if self.game_state != "player_turn":
            return

        self.game_state = "dealer_turn"
        self.dealer_hand.reveal_hidden_card()
        self.dealer_play()

    def dealer_play(self):
        """Dealer plays according to rules (hit on 16 or less, stand on 17 or more)"""
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())

        self.game_state = "finished"
        self.determine_winner()
        self.rounds_played += 1

    def determine_winner(self):
        """Determine the winner of the round"""
        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        if self.player_hand.is_bust():
            self.result = "lose"
            self.dealer_wins += 1
        elif self.dealer_hand.is_bust():
            self.result = "win"
            self.player_wins += 1
        elif player_value > dealer_value:
            self.result = "win"
            self.player_wins += 1
        elif dealer_value > player_value:
            self.result = "lose"
            self.dealer_wins += 1
        else:
            self.result = "push"


class CardWidget(QWidget):
    """Widget to display a single card"""

    def __init__(self, card=None, is_hidden=False, parent=None):
        super().__init__(parent)
        self.card = card
        self.is_hidden = is_hidden
        self.setFixedSize(80, 120)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw card background
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 10, 10)

        if self.is_hidden:
            # Draw hidden card pattern
            painter.setBrush(QBrush(QColor(41, 128, 185)))
            painter.drawRoundedRect(5, 5, self.width() - 10, self.height() - 10, 8, 8)
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "?")
        elif self.card:
            # Draw card content
            color = self.card.get_color()
            painter.setPen(QPen(color, 2))

            # Draw rank and suit in top-left
            painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            text = self.card.get_display_text()
            painter.drawText(10, 25, text)

            # Draw large suit symbol in center
            painter.setFont(QFont("Arial", 32, QFont.Weight.Bold))
            suit_symbol = self.card.suit_symbols[self.card.suit]
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, suit_symbol)

            # Draw rank and suit in bottom-right (rotated)
            painter.save()
            painter.translate(self.width(), self.height())
            painter.rotate(180)
            painter.drawText(10, 25, text)
            painter.restore()


class GameWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.init_ui()
        self.update_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("21 Card Game")
        self.setMinimumSize(800, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("21 Card Game")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2C3E50; margin: 10px;")
        main_layout.addWidget(title_label)

        # Scoreboard
        scoreboard = self.create_scoreboard()
        main_layout.addWidget(scoreboard)

        # Game area
        game_area = self.create_game_area()
        main_layout.addWidget(game_area, 1)

        # Controls
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # Theme switcher section
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_button = self.create_theme_switcher()
        theme_layout.addWidget(self.theme_button)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to play! Click 'New Round' to start.")

        # Accessibility: Set tab order
        QWidget.setTabOrder(self.hit_button, self.stand_button)
        QWidget.setTabOrder(self.stand_button, self.new_round_button)
        QWidget.setTabOrder(self.new_round_button, self.theme_button)

    def create_theme_switcher(self):
        """Create theme toggle button"""
        theme_button = QPushButton("🌙 Dark Mode")
        theme_button.setCheckable(True)
        theme_button.setToolTip("Toggle between light and dark theme")
        theme_button.setAccessibleName("Theme toggle button. Switch between light and dark mode.")
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setFixedSize(140, 40)
        theme_button.setStyleSheet("""
            QPushButton {
                background-color: #34495E;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
            QPushButton:checked {
                background-color: #F39C12;
            }
        """)
        return theme_button

    def toggle_theme(self, checked):
        """Toggle between light and dark themes"""
        if checked:
            self.set_dark_theme()
            self.theme_button.setText("☀️ Light Mode")
            self.status_bar.showMessage("Dark theme activated")
        else:
            self.set_light_theme()
            self.theme_button.setText("🌙 Dark Mode")
            self.status_bar.showMessage("Light theme activated")

    def set_light_theme(self):
        """Apply light theme colors"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
            }
            QLabel {
                color: #212529;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #DEE2E6;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #495057;
            }
            QStatusBar {
                background-color: #E9ECEF;
                color: #495057;
            }
        """)

        # Update scoreboard colors for light theme
        self.player_score_label.setStyleSheet("color: #27AE60; font-size: 16px;")
        self.dealer_score_label.setStyleSheet("color: #E74C3C; font-size: 16px;")
        self.rounds_label.setStyleSheet("color: #7F8C8D; font-size: 14px;")

        # Update result label colors for light theme
        if self.game.result == "win":
            self.result_label.setStyleSheet("color: #27AE60; padding: 10px;")
        elif self.game.result == "lose":
            self.result_label.setStyleSheet("color: #E74C3C; padding: 10px;")
        elif self.game.result == "push":
            self.result_label.setStyleSheet("color: #7F8C8D; padding: 10px;")
        elif self.game.game_state == "player_turn":
            self.result_label.setStyleSheet("color: #3498DB; padding: 10px;")
        elif self.game.game_state == "dealer_turn":
            self.result_label.setStyleSheet("color: #E67E22; padding: 10px;")
        else:
            self.result_label.setStyleSheet("color: #2C3E50; padding: 10px;")

    def set_dark_theme(self):
        """Apply dark theme colors"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #E0E0E0;
            }
            QGroupBox {
                background-color: #1E1E1E;
                border: 2px solid #424242;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #E0E0E0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #BB86FC;
            }
            QStatusBar {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border-top: 1px solid #424242;
            }
        """)

        # Update scoreboard colors for dark theme
        self.player_score_label.setStyleSheet("color: #4CAF50; font-size: 16px;")
        self.dealer_score_label.setStyleSheet("color: #F44336; font-size: 16px;")
        self.rounds_label.setStyleSheet("color: #9E9E9E; font-size: 14px;")

        # Update result label colors for dark theme
        if self.game.result == "win":
            self.result_label.setStyleSheet("color: #4CAF50; padding: 10px;")
        elif self.game.result == "lose":
            self.result_label.setStyleSheet("color: #F44336; padding: 10px;")
        elif self.game.result == "push":
            self.result_label.setStyleSheet("color: #9E9E9E; padding: 10px;")
        elif self.game.game_state == "player_turn":
            self.result_label.setStyleSheet("color: #64B5F6; padding: 10px;")
        elif self.game.game_state == "dealer_turn":
            self.result_label.setStyleSheet("color: #FFB74D; padding: 10px;")
        else:
            self.result_label.setStyleSheet("color: #E0E0E0; padding: 10px;")

    def create_scoreboard(self):
        """Create the scoreboard widget"""
        scoreboard = QGroupBox("Scoreboard")
        scoreboard.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #3498DB;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        layout = QHBoxLayout()

        # Player score
        self.player_score_label = QLabel("Player: 0")
        self.player_score_label.setFont(QFont("Arial", 16))
        self.player_score_label.setStyleSheet("color: #27AE60;")
        layout.addWidget(self.player_score_label)

        # Separator
        layout.addStretch()
        separator = QLabel("|")
        separator.setFont(QFont("Arial", 16))
        separator.setStyleSheet("color: #7F8C8D;")
        layout.addWidget(separator)
        layout.addStretch()

        # Rounds played
        self.rounds_label = QLabel("Rounds: 0")
        self.rounds_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.rounds_label)

        layout.addStretch()
        separator2 = QLabel("|")
        separator2.setFont(QFont("Arial", 16))
        separator2.setStyleSheet("color: #7F8C8D;")
        layout.addWidget(separator2)
        layout.addStretch()

        # Dealer score
        self.dealer_score_label = QLabel("Dealer: 0")
        self.dealer_score_label.setFont(QFont("Arial", 16))
        self.dealer_score_label.setStyleSheet("color: #E74C3C;")
        layout.addWidget(self.dealer_score_label)

        scoreboard.setLayout(layout)
        return scoreboard

    def create_game_area(self):
        """Create the main game area"""
        game_area = QWidget()
        layout = QVBoxLayout(game_area)

        # Dealer area
        dealer_group = QGroupBox("Dealer")
        dealer_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #E74C3C;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)
        dealer_layout = QVBoxLayout()

        self.dealer_total_label = QLabel("Total: --")
        self.dealer_total_label.setFont(QFont("Arial", 16))
        dealer_layout.addWidget(self.dealer_total_label)

        self.dealer_cards_layout = QHBoxLayout()
        dealer_layout.addLayout(self.dealer_cards_layout)
        dealer_group.setLayout(dealer_layout)

        layout.addWidget(dealer_group)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.result_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.result_label)

        # Player area
        player_group = QGroupBox("Player")
        player_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #27AE60;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)
        player_layout = QVBoxLayout()

        self.player_total_label = QLabel("Total: --")
        self.player_total_label.setFont(QFont("Arial", 16))
        player_layout.addWidget(self.player_total_label)

        self.player_cards_layout = QHBoxLayout()
        player_layout.addLayout(self.player_cards_layout)
        player_group.setLayout(player_layout)

        layout.addWidget(player_group)

        return game_area

    def create_controls(self):
        """Create the control buttons"""
        controls = QWidget()
        layout = QHBoxLayout(controls)
        layout.addStretch()

        # Hit button
        self.hit_button = QPushButton("Hit")
        self.hit_button.setFont(QFont("Arial", 14))
        self.hit_button.setFixedSize(120, 50)
        self.hit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        self.hit_button.clicked.connect(self.hit)
        layout.addWidget(self.hit_button)

        # Stand button
        self.stand_button = QPushButton("Stand")
        self.stand_button.setFont(QFont("Arial", 14))
        self.stand_button.setFixedSize(120, 50)
        self.stand_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        self.stand_button.clicked.connect(self.stand)
        layout.addWidget(self.stand_button)

        # New Round button
        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setFont(QFont("Arial", 14))
        self.new_round_button.setFixedSize(120, 50)
        self.new_round_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.new_round_button.clicked.connect(self.new_round)
        layout.addWidget(self.new_round_button)

        layout.addStretch()
        return controls

    def update_ui(self):
        """Update the UI based on game state"""
        # Update scores
        self.player_score_label.setText(f"Player: {self.game.player_wins}")
        self.dealer_score_label.setText(f"Dealer: {self.game.dealer_wins}")
        self.rounds_label.setText(f"Rounds: {self.game.rounds_played}")

        # Clear card layouts
        self.clear_layout(self.player_cards_layout)
        self.clear_layout(self.dealer_cards_layout)

        # Display player cards
        player_value = self.game.player_hand.calculate_value()
        self.player_total_label.setText(f"Total: {player_value}")

        for card in self.game.player_hand.cards:
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

        # Display dealer cards
        if self.game.game_state == "finished" or self.game.game_state == "dealer_turn":
            dealer_value = self.game.dealer_hand.calculate_value()
            self.dealer_total_label.setText(f"Total: {dealer_value}")

            # Show all dealer cards
            for card in self.game.dealer_hand.cards:
                card_widget = CardWidget(card)
                self.dealer_cards_layout.addWidget(card_widget)
        else:
            self.dealer_total_label.setText("Total: --")

            # Show dealer cards with one hidden
            if self.game.dealer_hand.cards:
                card_widget = CardWidget(self.game.dealer_hand.cards[0])
                self.dealer_cards_layout.addWidget(card_widget)

            if self.game.dealer_hand.face_down_card:
                hidden_widget = CardWidget(is_hidden=True)
                self.dealer_cards_layout.addWidget(hidden_widget)

        # Update button states
        if self.game.game_state == "player_turn":
            self.hit_button.setEnabled(True)
            self.stand_button.setEnabled(True)
            self.new_round_button.setEnabled(False)
            self.result_label.setText("Your turn - Hit or Stand?")
            self.status_bar.showMessage("Your turn. Click Hit to draw a card or Stand to end your turn.")
        elif self.game.game_state == "dealer_turn":
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.new_round_button.setEnabled(False)
            self.result_label.setText("Dealer's turn...")
            self.status_bar.showMessage("Dealer's turn. The dealer will draw cards until reaching 17 or more.")
        elif self.game.game_state == "finished":
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.new_round_button.setEnabled(True)

            # Display result
            if self.game.result == "win":
                self.result_label.setText("You Win! 🎉")
                self.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.result_label.setText("Dealer Wins 💔")
                self.status_bar.showMessage("Dealer won this round. Better luck next time!")
            else:  # push
                self.result_label.setText("Push (Tie) 🤝")
                self.status_bar.showMessage("It's a tie! The round ends in a push.")
        else:  # idle
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.new_round_button.setEnabled(True)
            self.result_label.setText("Click 'New Round' to start!")

        # Apply current theme colors to result label
        if hasattr(self, 'theme_button') and self.theme_button.isChecked():
            # Dark theme is active
            if self.game.result == "win":
                self.result_label.setStyleSheet("color: #4CAF50; padding: 10px;")
            elif self.game.result == "lose":
                self.result_label.setStyleSheet("color: #F44336; padding: 10px;")
            elif self.game.result == "push":
                self.result_label.setStyleSheet("color: #9E9E9E; padding: 10px;")
            elif self.game.game_state == "player_turn":
                self.result_label.setStyleSheet("color: #64B5F6; padding: 10px;")
            elif self.game.game_state == "dealer_turn":
                self.result_label.setStyleSheet("color: #FFB74D; padding: 10px;")
            else:
                self.result_label.setStyleSheet("color: #E0E0E0; padding: 10px;")
        else:
            # Light theme is active
            if self.game.result == "win":
                self.result_label.setStyleSheet("color: #27AE60; padding: 10px;")
            elif self.game.result == "lose":
                self.result_label.setStyleSheet("color: #E74C3C; padding: 10px;")
            elif self.game.result == "push":
                self.result_label.setStyleSheet("color: #7F8C8D; padding: 10px;")
            elif self.game.game_state == "player_turn":
                self.result_label.setStyleSheet("color: #3498DB; padding: 10px;")
            elif self.game.game_state == "dealer_turn":
                self.result_label.setStyleSheet("color: #E67E22; padding: 10px;")
            else:
                self.result_label.setStyleSheet("color: #2C3E50; padding: 10px;")

        # Force UI update
        self.update()

    def clear_layout(self, layout):
        """Clear all widgets from a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def hit(self):
        """Handle hit button click"""
        self.game.player_hit()
        self.update_ui()

    def stand(self):
        """Handle stand button click"""
        self.game.player_stand()
        self.update_ui()

    def new_round(self):
        """Handle new round button click"""
        self.game.start_new_round()
        self.update_ui()

    def resizeEvent(self, event):
        """Handle window resize for responsiveness"""
        super().resizeEvent(event)
        # The layout managers automatically handle responsiveness
        self.status_bar.showMessage(f"Window resized to {self.width()}x{self.height()}")


# Additional Feature: Game Statistics Dialog
class StatisticsDialog(QDialog):
    """Dialog showing detailed game statistics"""

    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.setWindowTitle("Game Statistics")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Game Statistics")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Statistics
        total_games = self.game.rounds_played
        if total_games > 0:
            win_rate = (self.game.player_wins / total_games) * 100
            loss_rate = (self.game.dealer_wins / total_games) * 100
            push_rate = ((total_games - self.game.player_wins - self.game.dealer_wins) / total_games) * 100
        else:
            win_rate = loss_rate = push_rate = 0

        stats_text = f"""
        <div style='font-size: 14pt; line-height: 1.5;'>
        <b>Total Rounds:</b> {total_games}<br><br>
        <b>Player Wins:</b> {self.game.player_wins}<br>
        <b>Dealer Wins:</b> {self.game.dealer_wins}<br>
        <b>Ties:</b> {total_games - self.game.player_wins - self.game.dealer_wins}<br><br>
        <b>Win Rate:</b> {win_rate:.1f}%<br>
        <b>Loss Rate:</b> {loss_rate:.1f}%<br>
        <b>Tie Rate:</b> {push_rate:.1f}%<br>
        </div>
        """

        stats_label = QLabel(stats_text)
        stats_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(stats_label)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setFixedSize(300, 300)


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
    window = GameWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()