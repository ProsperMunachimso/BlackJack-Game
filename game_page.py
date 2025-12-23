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
        self.setObjectName("cardWidget")

        # Define consistent fonts for all card elements
        self.rank_font = QFont("Arial", 24, QFont.Weight.Bold)
        self.suit_font = QFont("Arial", 32, QFont.Weight.Bold)
        self.hidden_font = QFont("Arial", 24, QFont.Weight.Bold)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw card background - theme aware
        if self.parent() and hasattr(self.parent(), 'current_theme'):
            if self.parent().current_theme == "dark":
                painter.setBrush(QBrush(QColor(55, 71, 79)))  # Dark theme card background
            else:
                painter.setBrush(QBrush(QColor(255, 255, 255)))  # Light theme card background
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255)))  # Default light

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

            # Draw rank and suit in bottom-right (rotated)
            painter.save()
            painter.translate(self.width(), self.height())
            painter.rotate(180)
            painter.setFont(self.rank_font)
            painter.drawText(10, 25, text)
            painter.restore()


class GamePage(QWidget):
    """Main game page"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.game = Game21()
        self.current_theme = "light"
        self.current_state = "idle"
        self.current_result = "none"
        self.init_ui()
        print(f"🎮 GamePage created with theme: {self.current_theme}")

    def init_ui(self):
        """Initialize the game interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        # CRITICAL: Set object name and initial theme property
        self.setObjectName("gamePage")
        self.setProperty("theme", "light")

        # Title
        title_label = QLabel("21 Card Game")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

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
        self.back_button = QPushButton("← Back to Home")
        self.back_button.setObjectName("backButton")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setFixedSize(150, 40)
        self.back_button.setToolTip("Return to welcome page")
        self.back_button.clicked.connect(self.go_to_welcome)
        theme_layout.addWidget(self.back_button)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

    def create_theme_switcher(self):
        """Create theme toggle button"""
        theme_button = QPushButton("🌙 Switch to Dark Mode")
        theme_button.setObjectName("themeButton")
        theme_button.setCheckable(False)  # NOT checkable - we handle state manually
        theme_button.setToolTip("Toggle between light and dark theme")
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setFixedSize(200, 40)
        theme_button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        return theme_button

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        print(f"🎨 Theme button clicked. Current theme: {self.current_theme}")

        if self.current_theme == "light":
            new_theme = "dark"
            self.theme_button.setText("☀️ Switch to Light Mode")
            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                self.parent_window.status_bar.showMessage("Dark theme activated")
        else:
            new_theme = "light"
            self.theme_button.setText("🌙 Switch to Dark Mode")
            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                self.parent_window.status_bar.showMessage("Light theme activated")

        print(f"🎨 Switching to {new_theme} theme")
        self.set_theme(new_theme)

    def set_theme(self, theme):
        """Set the theme for the game page"""
        print(f"🎨 Setting theme to: {theme}")

        # Update current theme
        self.current_theme = theme

        # Set theme property on self
        self.setProperty("theme", theme)
        print(f"🎨 Property 'theme' set to: {self.property('theme')}")

        # Set theme property on ALL child widgets
        for child in self.findChildren(QWidget):
            if child != self:  # Don't set on self again
                child.setProperty("theme", theme)

        # FORCE stylesheet reapplication on self and all children
        self.style().unpolish(self)
        self.style().polish(self)

        for child in self.findChildren(QWidget):
            if child != self:
                child.style().unpolish(child)
                child.style().polish(child)

        # Force UI update
        self.update()
        print(f"🎨 Theme set complete. Current theme: {self.current_theme}")

    def set_game_state(self, state, result="none"):
        """Set the game state for styling"""
        print(f"🎮 Setting game state: {state}, result: {result}")
        self.current_state = state
        self.current_result = result

        # Set properties
        self.setProperty("state", state)
        self.setProperty("result", result)

        # Also set on result label
        if hasattr(self, 'result_label'):
            self.result_label.setProperty("state", state)
            self.result_label.setProperty("result", result)

        # Force stylesheet reapplication
        self.style().unpolish(self)
        self.style().polish(self)

        if hasattr(self, 'result_label'):
            self.result_label.style().unpolish(self.result_label)
            self.result_label.style().polish(self.result_label)

        print(f"🎮 Game state updated")

    def create_game_area(self):
        """Create the main game area"""
        game_area = QWidget()
        game_area.setObjectName("gameArea")
        layout = QVBoxLayout(game_area)

        # Dealer area
        dealer_group = QGroupBox("Dealer")
        dealer_group.setObjectName("dealerGroup")
        dealer_layout = QVBoxLayout()

        self.dealer_total_label = QLabel("Total: --")
        self.dealer_total_label.setObjectName("dealerTotalLabel")
        self.dealer_total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
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
        self.player_total_label.setObjectName("playerTotalLabel")
        self.player_total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        player_layout.addWidget(self.player_total_label)

        self.player_cards_layout = QHBoxLayout()
        player_layout.addLayout(self.player_cards_layout)
        player_group.setLayout(player_layout)

        layout.addWidget(player_group)

        return game_area

    def create_controls(self):
        """Create the control buttons"""
        controls = QWidget()
        controls.setObjectName("controls")
        layout = QHBoxLayout(controls)
        layout.addStretch()

        # Hit button
        self.hit_button = QPushButton("Hit")
        self.hit_button.setObjectName("hitButton")
        self.hit_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.hit_button.setFixedSize(120, 50)
        self.hit_button.clicked.connect(self.on_hit)
        layout.addWidget(self.hit_button)

        # Stand button
        self.stand_button = QPushButton("Stand")
        self.stand_button.setObjectName("standButton")
        self.stand_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.stand_button.setFixedSize(120, 50)
        self.stand_button.clicked.connect(self.on_stand)
        layout.addWidget(self.stand_button)

        # New Round button
        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setObjectName("newRoundButton")
        self.new_round_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.new_round_button.setFixedSize(120, 50)
        self.new_round_button.clicked.connect(self.on_new_round)
        layout.addWidget(self.new_round_button)

        layout.addStretch()
        return controls

    def go_to_welcome(self):
        """Return to welcome page with confirmation"""
        reply = QMessageBox.question(
            self,
            "Return to Home",
            "Are you sure you want to return to home?\nYour current game progress will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.parent_window:
                self.parent_window.show_welcome_page()

    # BUTTON ACTIONS

    def on_hit(self):
        """Player takes a card"""
        self.set_game_state("player_turn")
        card = self.game.player_hit()
        if card:
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

            player_total = self.game.player_total()
            self.player_total_label.setText(f"Total: {player_total}")

            if self.game.player_hand.is_bust():
                self.game_state_finished()

    def on_stand(self):
        """Player ends turn; dealer reveals their hidden card and plays"""
        self.set_game_state("dealer_turn")
        self.game.player_stand()
        self.update_dealer_cards(full=True)

        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

        dealer_total = self.game.dealer_total()
        self.dealer_total_label.setText(f"Total: {dealer_total}")

        self.result_label.setText("Dealer's turn...")

        QTimer.singleShot(1000, self.process_dealer_turn)

    def on_new_round(self):
        """Start a new round"""
        self.game.new_round()
        self.new_round_setup()

    def process_dealer_turn(self):
        """Process dealer's turn with animation"""
        drawn_cards = self.game.play_dealer_turn()

        for i, card in enumerate(drawn_cards):
            QTimer.singleShot(i * 500, lambda c=card: self.add_dealer_card(c))

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

        result_text = self.game.decide_winner()
        self.result_label.setText(result_text)

        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        self.new_round_button.setEnabled(True)

        if self.parent_window and hasattr(self.parent_window, 'status_bar'):
            if self.game.result == "win":
                self.parent_window.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent_window.status_bar.showMessage("Dealer won this round. Better luck next time!")
            else:
                self.parent_window.status_bar.showMessage("It's a tie! The round ends in a push.")

    def game_state_finished(self):
        """Handle game finished state"""
        result_text = self.game.decide_winner()
        self.result_label.setText(result_text)

        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.new_round_button.setEnabled(True)

        if self.parent_window and hasattr(self.parent_window, 'status_bar'):
            if self.game.result == "win":
                self.parent_window.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent_window.status_bar.showMessage("You busted! Dealer wins.")
            else:
                self.parent_window.status_bar.showMessage("It's a tie! The round ends in a push.")

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

        if full or self.game.game_state in ["dealer_turn", "finished"]:
            for card in self.game.dealer_hand.cards:
                card_widget = CardWidget(card)
                self.dealer_cards_layout.addWidget(card_widget)
        else:
            if self.game.dealer_hand.cards:
                card_widget = CardWidget(self.game.dealer_hand.cards[0])
                self.dealer_cards_layout.addWidget(card_widget)

            if self.game.dealer_hand.face_down_card:
                hidden_widget = CardWidget(is_hidden=True)
                self.dealer_cards_layout.addWidget(hidden_widget)

    def new_round_setup(self):
        """Prepare a fresh visual layout"""
        self.clear_layout(self.player_cards_layout)
        self.clear_layout(self.dealer_cards_layout)

        self.game.deal_initial_cards()
        self.update_dealer_cards(full=False)

        for card in self.game.player_hand.cards:
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

        player_total = self.game.player_total()
        self.player_total_label.setText(f"Total: {player_total}")
        self.dealer_total_label.setText("Total: ?")

        if self.game.game_state == "finished":
            result_text = self.game.decide_winner()
            self.result_label.setText(result_text)
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.new_round_button.setEnabled(True)

            if self.game.result == "win":
                self.set_game_state("finished", "win")
            elif self.game.result == "push":
                self.set_game_state("finished", "push")

            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                if self.game.result == "win":
                    self.parent_window.status_bar.showMessage("Blackjack! You win!")
                elif self.game.result == "push":
                    self.parent_window.status_bar.showMessage("Both have blackjack! It's a tie.")
        else:
            self.result_label.setText("Your turn! Hit or Stand?")
            self.set_game_state("player_turn")
            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                self.parent_window.status_bar.showMessage(
                    "Your turn. Click Hit to draw a card or Stand to end your turn.")
            self.hit_button.setEnabled(True)
            self.stand_button.setEnabled(True)
            self.new_round_button.setEnabled(False)

    def update_ui(self):
        """Update the UI based on game state"""
        pass