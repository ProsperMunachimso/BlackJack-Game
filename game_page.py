from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_logic import Game21, Card


class CardWidget(QWidget):
    """Widget to display a single card"""

    def __init__(self, card=None, is_hidden=False, parent=None):
        super().__init__(parent)
        self.card = card
        self.is_hidden = is_hidden
        self.setFixedSize(80, 120)

        # Define consistent fonts for all card elements
        self.rank_font = QFont("Arial", 24, QFont.Weight.Bold)
        self.suit_font = QFont("Arial", 32, QFont.Weight.Bold)
        self.hidden_font = QFont("Arial", 24, QFont.Weight.Bold)
        self.setObjectName("cardWidget")

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
            painter.setFont(self.hidden_font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "?")
        elif self.card:
            # Determine card color
            suit = self.card.suit
            if suit in ['H', 'D']:
                color = QColor(220, 53, 69)  # Red
            else:
                color = QColor(33, 37, 41)  # Black

            painter.setPen(QPen(color, 2))

            # Get card text and suit symbol
            text = self.card.get_display_text()
            suit_symbols = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}
            suit_symbol = suit_symbols[suit]

            # Draw rank and suit in top-left
            painter.setFont(self.rank_font)
            painter.drawText(10, 25, text)

            # Draw large suit symbol in center
            painter.setFont(self.suit_font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, suit_symbol)

            # Draw rank and suit in bottom-right (rotated) - USING EXACT SAME FONT
            painter.save()
            painter.translate(self.width(), self.height())
            painter.rotate(180)
            painter.setFont(self.rank_font)  # EXACT SAME FONT as top-left
            painter.drawText(10, 25, text)  # EXACT SAME POSITION as top-left
            painter.restore()


class GamePage(QWidget):
    """Main game page"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.game = Game21()
        self.current_theme = "light"
        self.current_state = "idle"
        self.init_ui()

    def init_ui(self):
        """Initialize the game interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        # Set object name for QSS styling
        self.setObjectName("gamePage")

        # Set properties for QSS
        self.setProperty("theme", "light")
        self.setProperty("state", "idle")
        self.setProperty("result", "none")

        # Title
        title_label = QLabel("21 Card Game")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Scoreboard - commented out because assignment requires only single self-contained rounds
        # No running score history or persistent multi-round state needed
        # scoreboard = self.create_scoreboard()
        # main_layout.addWidget(scoreboard)

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

        # Back to welcome button
        self.back_button = QPushButton(" Back to Home")
        self.back_button.setObjectName("backButton")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setFixedSize(150, 40)
        self.back_button.setToolTip("Return to welcome page (current progress will be lost)")
        self.back_button.clicked.connect(self.go_to_welcome)
        theme_layout.addWidget(self.back_button)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # Apply initial theme
        self.set_theme("light")

    def create_theme_switcher(self):
        """Create theme toggle button"""
        theme_button = QPushButton(" Dark Mode")
        theme_button.setObjectName("themeButton")
        theme_button.setCheckable(True)
        theme_button.setToolTip("Toggle between light and dark theme")
        theme_button.setAccessibleName("Theme toggle button. Switch between light and dark mode.")
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setFixedSize(140, 40)
        return theme_button

    def toggle_theme(self, checked):
        """Toggle between light and dark themes"""
        if checked:
            self.set_theme("dark")
            self.theme_button.setText(" Light Mode")
            if hasattr(self.parent, 'status_bar'):
                self.parent.status_bar.showMessage("Dark theme activated")
        else:
            self.set_theme("light")
            self.theme_button.setText(" Dark Mode")
            if hasattr(self.parent, 'status_bar'):
                self.parent.status_bar.showMessage("Light theme activated")

    def set_theme(self, theme):
        """Set the theme for the game page"""
        self.current_theme = theme
        self.setProperty("theme", theme)
        self.style().unpolish(self)
        self.style().polish(self)

        # Update child widgets
        for child in self.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)

    def set_game_state(self, state, result="none"):
        """Set the game state for QSS styling"""
        self.current_state = state
        self.setProperty("state", state)
        self.setProperty("result", result)
        self.style().unpolish(self)
        self.style().polish(self)

        # Update result label specifically
        self.result_label.style().unpolish(self.result_label)
        self.result_label.style().polish(self.result_label)

    def create_scoreboard(self):
        """Create the scoreboard widget - commented out for assignment compliance"""
        scoreboard = QGroupBox("Scoreboard")
        scoreboard.setObjectName("scoreboardGroup")

        layout = QHBoxLayout()

        # Player score
        self.player_score_label = QLabel("Player: 0")
        self.player_score_label.setObjectName("playerScoreLabel")
        self.player_score_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.player_score_label)

        # Separator
        layout.addStretch()
        separator = QLabel("|")
        separator.setFont(QFont("Arial", 16))
        layout.addWidget(separator)
        layout.addStretch()

        # Rounds played
        self.rounds_label = QLabel("Rounds: 0")
        self.rounds_label.setObjectName("roundsLabel")
        self.rounds_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.rounds_label)

        layout.addStretch()
        separator2 = QLabel("|")
        separator2.setFont(QFont("Arial", 16))
        layout.addWidget(separator2)
        layout.addStretch()

        # Dealer score
        self.dealer_score_label = QLabel("Dealer: 0")
        self.dealer_score_label.setObjectName("dealerScoreLabel")
        self.dealer_score_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.dealer_score_label)

        scoreboard.setLayout(layout)
        return scoreboard

    def create_game_area(self):
        """Create the main game area"""
        game_area = QWidget()
        layout = QVBoxLayout(game_area)

        # Dealer area
        dealer_group = QGroupBox("Dealer")
        dealer_group.setObjectName("dealerGroup")
        dealer_layout = QVBoxLayout()

        self.dealer_total_label = QLabel("Total: --")
        self.dealer_total_label.setFont(QFont("Arial", 16))
        dealer_layout.addWidget(self.dealer_total_label)

        self.dealer_cards_layout = QHBoxLayout()
        dealer_layout.addLayout(self.dealer_cards_layout)
        dealer_group.setLayout(dealer_layout)

        layout.addWidget(dealer_group)

        # Result display
        self.result_label = QLabel("Click 'New Round' to start!")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(self.result_label)

        # Player area
        player_group = QGroupBox("Player")
        player_group.setObjectName("playerGroup")
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
        self.hit_button.setObjectName("hitButton")
        self.hit_button.setFont(QFont("Arial", 14))
        self.hit_button.setFixedSize(120, 50)
        self.hit_button.clicked.connect(self.on_hit)
        layout.addWidget(self.hit_button)

        # Stand button
        self.stand_button = QPushButton("Stand")
        self.stand_button.setObjectName("standButton")
        self.stand_button.setFont(QFont("Arial", 14))
        self.stand_button.setFixedSize(120, 50)
        self.stand_button.clicked.connect(self.on_stand)
        layout.addWidget(self.stand_button)

        # New Round button
        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setObjectName("newRoundButton")
        self.new_round_button.setFont(QFont("Arial", 14))
        self.new_round_button.setFixedSize(120, 50)
        self.new_round_button.clicked.connect(self.on_new_round)
        layout.addWidget(self.new_round_button)

        # New Game button - COMMENTED OUT as per assignment requirements
        # The assignment requires only single self-contained rounds, so New Round is sufficient
        # self.new_game_button = QPushButton("🔄 New Game")
        # self.new_game_button.setObjectName("newGameButton")
        # self.new_game_button.setFont(QFont("Arial", 14))
        # self.new_game_button.setFixedSize(120, 50)
        # self.new_game_button.setToolTip("Start a fresh self-contained round")
        # self.new_game_button.clicked.connect(self.on_new_game)
        # layout.addWidget(self.new_game_button)

        layout.addStretch()
        return controls

    def go_to_welcome(self):
        """Return to welcome page with confirmation"""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Return to Home",
            "Are you sure you want to return to home?\nYour current game progress will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.parent:
                self.parent.show_welcome_page()

    # BUTTON ACTIONS

    def on_hit(self):
        """Player takes a card"""
        self.set_game_state("player_turn")
        card = self.game.player_hit()
        if card:
            # Add card widget to player's hand
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

            # Update player total
            player_total = self.game.player_total()
            self.player_total_label.setText(f"Total: {player_total}")

            if self.game.player_hand.is_bust():
                self.game_state_finished()

    def on_stand(self):
        """Player ends turn; dealer reveals their hidden card and plays"""
        self.set_game_state("dealer_turn")
        self.game.player_stand()
        self.update_dealer_cards(full=True)

        # Disable hit and stand buttons during dealer's turn
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

        # Show dealer's total
        dealer_total = self.game.dealer_total()
        self.dealer_total_label.setText(f"Total: {dealer_total}")

        # Dealer plays their turn
        self.result_label.setText("Dealer's turn...")

        # Use a timer to animate dealer's card drawing
        QTimer.singleShot(1000, self.process_dealer_turn)

    def on_new_round(self):
        """Start a new round"""
        self.game.new_round()
        self.new_round_setup()

    # New Game button functionality - COMMENTED OUT as per assignment requirements
    # def on_new_game(self):
    #     """Reset entire game - starts a fresh self-contained round"""
    #     # Show confirmation dialog
    #     reply = QMessageBox.question(
    #         self,
    #         "New Game Confirmation",
    #         "Are you sure you want to start a new game?\nThis will start a fresh self-contained round.",
    #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    #         QMessageBox.StandardButton.No
    #     )
    #
    #     if reply == QMessageBox.StandardButton.Yes:
    #         # Reset the game (starts a fresh round)
    #         self.game.reset_game()
    #
    #         # Update UI
    #         self.new_round_setup()
    #
    #         # Update status bar
    #         if self.parent and hasattr(self.parent, 'status_bar'):
    #             self.parent.status_bar.showMessage("New game started! Starting a fresh round.")
    #
    #         # Update result label
    #         self.result_label.setText("New game started! Click 'New Round' to begin.")

    def process_dealer_turn(self):
        """Process dealer's turn with animation"""
        drawn_cards = self.game.play_dealer_turn()

        # Add each drawn card with a delay for animation
        for i, card in enumerate(drawn_cards):
            QTimer.singleShot(i * 500, lambda c=card: self.add_dealer_card(c))

        # After dealer is done, update and show result
        QTimer.singleShot((len(drawn_cards) + 1) * 500, self.finish_dealer_turn)

    def add_dealer_card(self, card):
        """Add a card to dealer's hand display"""
        card_widget = CardWidget(card)
        self.dealer_cards_layout.addWidget(card_widget)
        dealer_total = self.game.dealer_total()
        self.dealer_total_label.setText(f"Total: {dealer_total}")

    def finish_dealer_turn(self):
        """Finish dealer's turn and show result"""
        dealer_total = self.game.dealer_total()
        self.dealer_total_label.setText(f"Total: {dealer_total}")

        # Determine winner
        result_text = self.game.decide_winner()
        self.result_label.setText(result_text)

        # Set game state for styling
        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        # Enable new round button
        self.new_round_button.setEnabled(True)

        # Update status bar
        if self.parent and hasattr(self.parent, 'status_bar'):
            if self.game.result == "win":
                self.parent.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent.status_bar.showMessage("Dealer won this round. Better luck next time!")
            else:
                self.parent.status_bar.showMessage("It's a tie! The round ends in a push.")

    def game_state_finished(self):
        """Handle game finished state"""
        result_text = self.game.decide_winner()
        self.result_label.setText(result_text)

        # Set game state for styling
        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        # Disable hit and stand buttons
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.new_round_button.setEnabled(True)

        # Update status bar
        if self.parent and hasattr(self.parent, 'status_bar'):
            if self.game.result == "win":
                self.parent.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent.status_bar.showMessage("You busted! Dealer wins.")
            else:
                self.parent.status_bar.showMessage("It's a tie! The round ends in a push.")

    # HELPER METHODS

    def clear_layout(self, layout):
        """Remove all widgets from a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_dealer_cards(self, full=False):
        """Show dealer cards; hide the first card until revealed"""
        self.clear_layout(self.dealer_cards_layout)

        # Show dealer's cards
        if full or self.game.game_state in ["dealer_turn", "finished"]:
            # Show all cards
            for card in self.game.dealer_hand.cards:
                card_widget = CardWidget(card)
                self.dealer_cards_layout.addWidget(card_widget)
        else:
            # Show first card face up, second card hidden
            if self.game.dealer_hand.cards:
                card_widget = CardWidget(self.game.dealer_hand.cards[0])
                self.dealer_cards_layout.addWidget(card_widget)

            # Add hidden card if exists
            if self.game.dealer_hand.face_down_card:
                hidden_widget = CardWidget(is_hidden=True)
                self.dealer_cards_layout.addWidget(hidden_widget)

    def new_round_setup(self):
        """Prepare a fresh visual layout"""
        # Clear existing cards
        self.clear_layout(self.player_cards_layout)
        self.clear_layout(self.dealer_cards_layout)

        # Deal initial cards
        self.game.deal_initial_cards()

        # Update dealer cards (first one hidden)
        self.update_dealer_cards(full=False)

        # Show player cards
        for card in self.game.player_hand.cards:
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

        # Update totals
        player_total = self.game.player_total()
        self.player_total_label.setText(f"Total: {player_total}")
        self.dealer_total_label.setText("Total: ?")

        # Update status
        if self.game.game_state == "finished":
            # Blackjack occurred
            result_text = self.game.decide_winner()
            self.result_label.setText(result_text)
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.new_round_button.setEnabled(True)

            # Set game state for styling
            if self.game.result == "win":
                self.set_game_state("finished", "win")
            elif self.game.result == "push":
                self.set_game_state("finished", "push")

            if self.parent and hasattr(self.parent, 'status_bar'):
                if self.game.result == "win":
                    self.parent.status_bar.showMessage("Blackjack! You win!")
                elif self.game.result == "push":
                    self.parent.status_bar.showMessage("Both have blackjack! It's a tie.")
        else:
            self.result_label.setText("Your turn! Hit or Stand?")
            self.set_game_state("player_turn")
            if self.parent and hasattr(self.parent, 'status_bar'):
                self.parent.status_bar.showMessage("Your turn. Click Hit to draw a card or Stand to end your turn.")
            self.hit_button.setEnabled(True)
            self.stand_button.setEnabled(True)
            self.new_round_button.setEnabled(False)

    def update_ui(self):
        """Update the UI based on game state"""
        pass