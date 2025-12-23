from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_logic import Game21


class CardWidget(QWidget):
    """Widget to display a single card"""

    def __init__(self, card=None, is_hidden=False, parent=None):
        super().__init__(parent)
        self.card = card
        self.is_hidden = is_hidden
        # This sets a fixed size for all card widgets
        self.setFixedSize(80, 120)
        # This sets an object name for CSS styling
        self.setObjectName("cardWidget")

        self.rank_font = QFont("Arial", 24, QFont.Weight.Bold)
        self.suit_font = QFont("Arial", 32, QFont.Weight.Bold)
        self.hidden_font = QFont("Arial", 24, QFont.Weight.Bold)

    def paintEvent(self, event):
        # This creates a QPainter object for drawing
        painter = QPainter(self)
        # This enables antialiasing for smoother graphics
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # This draws the card background with theme-aware colors
        if self.parent() and hasattr(self.parent(), 'current_theme'):
            if self.parent().current_theme == "dark":
                # This uses dark blue for dark theme because we decided to go with a blue color palette
                painter.setBrush(QBrush(QColor(44, 62, 80)))
            else:
                # This uses white for light theme
                painter.setBrush(QBrush(QColor(255, 255, 255)))
        else:
            # This sets white as default color
            painter.setBrush(QBrush(QColor(255, 255, 255)))

        # This sets a light gray border for the card
        painter.setPen(QPen(QColor(189, 195, 199), 2))
        # This draws a rounded rectangle for the card
        painter.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 10, 10)

        if self.is_hidden:
            # This draws a hidden card with blue background
            painter.setBrush(QBrush(QColor(52, 152, 219)))
            # This draws the inner blue rectangle
            painter.drawRoundedRect(5, 5, self.width() - 10, self.height() - 10, 8, 8)
            # This sets white color for the question mark
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            # This uses the hidden font
            painter.setFont(self.hidden_font)
            # This draws a question mark in the center
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "?")
        elif self.card:
            # This determines card color based on suit
            suit = self.card.suit
            if suit in ['H', 'D']:
                # This uses red for hearts and diamonds
                color = QColor(231, 76, 60)
            else:
                # This uses dark blue for clubs and spades
                color = QColor(52, 73, 94)

            # This sets the pen color for card details
            painter.setPen(QPen(color, 2))

            # This gets the display text for the card
            text = self.card.get_display_text()
            # This creates suit symbols using Unicode characters
            # We used Unicode because it provides proper suit symbols that work across platforms and it is easier than using 52 images of cards.
            suit_symbols = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}
            # This looks up the Unicode symbol for the suit
            suit_symbol = suit_symbols[suit]

            # This draws the rank in the top-left corner
            painter.setFont(self.rank_font)
            painter.drawText(10, 25, text)

            # This draws a large suit symbol in the center
            painter.setFont(self.suit_font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, suit_symbol)

            # This draws the rank in the bottom-right corner (upside down)
            painter.save()
            # This moves to the bottom-right corner
            painter.translate(self.width(), self.height())
            # This rotates 180 degrees for upside-down text
            painter.rotate(180)
            painter.setFont(self.rank_font)
            # This draws the upside-down rank
            painter.drawText(10, 25, text)
            painter.restore()


class GamePage(QWidget):
    """Main game page"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.game = Game21()
        # This sets the initial theme to light mode
        self.current_theme = "light"
        # This tracks the current game state
        self.current_state = "idle"
        # This tracks the current game result
        self.current_result = "none"
        self.init_ui()
        print(f" GamePage created with theme: {self.current_theme}")

    def init_ui(self):
        """Initialize the game interface"""
        # This creates a vertical box layout for the main window
        main_layout = QVBoxLayout(self)
        # This sets spacing between widgets
        main_layout.setSpacing(20)

        # This sets an object name for CSS styling
        self.setObjectName("gamePage")
        # This sets a CSS property for theme styling
        self.setProperty("theme", "light")

        # This creates a title label for the game
        title_label = QLabel("ZA Great's and Victor's Card Game")
        title_label.setObjectName("gameTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # This creates the main game area
        game_area = self.create_game_area()
        main_layout.addWidget(game_area, 1)

        # This creates the control buttons
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # This creates a horizontal layout for theme switcher
        theme_layout = QHBoxLayout()
        # This adds stretchable space on the left
        theme_layout.addStretch()
        # This creates the theme toggle button
        self.theme_button = self.create_theme_switcher()
        theme_layout.addWidget(self.theme_button)

        # This creates a button to go back to the welcome page, we created this for easy navigation.
        self.back_button = QPushButton("Back to Home")
        self.back_button.setObjectName("backButton")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setFixedSize(150, 40)
        self.back_button.setToolTip("Return to welcome page")
        # This connects the button click to the go_to_welcome method
        self.back_button.clicked.connect(self.go_to_welcome)
        theme_layout.addWidget(self.back_button)
        # This adds stretchable space on the right
        theme_layout.addStretch()
        # This adds the theme layout to the main layout
        main_layout.addLayout(theme_layout)

    def create_theme_switcher(self):
        """Create theme toggle button"""
        theme_button = QPushButton("Switch to Dark Mode")
        theme_button.setObjectName("themeButton")
        theme_button.setToolTip("Toggle between light and dark theme")
        # This connects the button click to toggle_theme method
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setFixedSize(180, 40)
        return theme_button

    def toggle_theme(self):
        """Toggle theme globally through main window"""
        print(f" Theme button clicked. Current theme: {self.current_theme}")

        # This checks if parent window has toggle_theme method
        if self.parent_window and hasattr(self.parent_window, 'toggle_theme'):
            # This calls the parent window's toggle_theme method
            self.parent_window.toggle_theme()
        else:
            # This provides fallback if parent window doesn't exist
            new_theme = "dark" if self.current_theme == "light" else "light"
            print(f" Switching to {new_theme} theme (fallback)")
            # This calls the local set_theme method
            self.set_theme(new_theme)

    def set_theme(self, theme):
        """Set the theme for the game page. We wrote this method to ensure all child widgets get the theme property."""
        # This prints which theme is being set
        print(f" Setting theme to: {theme}")

        # This updates the current theme variable
        self.current_theme = theme

        # This updates the button text based on current theme
        if hasattr(self, 'theme_button'):
            self.theme_button.setText("Switch to Light Mode" if theme == "dark" else "Switch to Dark Mode")

        # This sets the theme property on the game page
        self.setProperty("theme", theme)

        # This sets the theme property on all child widgets
        for child in self.findChildren(QWidget):
            if child != self:  # This avoids setting property on self again
                child.setProperty("theme", theme)

        # This forces stylesheet reapplication on the game page
        self.style().unpolish(self)
        self.style().polish(self)

        # This forces stylesheet reapplication on all child widgets
        for child in self.findChildren(QWidget):
            if child != self:
                child.style().unpolish(child)
                child.style().polish(child)

        # This forces a UI update to reflect theme changes
        self.update()
        print(f" Theme set complete. Current theme: {self.current_theme}")

    def set_game_state(self, state, result="none"):
        """Set the game state for styling. We wrote this method to allow CSS to style different game states."""
        # This prints the state and result being set
        print(f" Setting game state: {state}, result: {result}")
        # This updates the current state and result
        self.current_state = state
        self.current_result = result

        # This sets CSS properties for state-based styling
        self.setProperty("state", state)
        self.setProperty("result", result)

        # This also sets properties on the result label
        if hasattr(self, 'result_label'):
            self.result_label.setProperty("state", state)
            self.result_label.setProperty("result", result)

        # This forces stylesheet reapplication on the game page
        self.style().unpolish(self)
        self.style().polish(self)

        # This forces stylesheet reapplication on the result label
        if hasattr(self, 'result_label'):
            self.result_label.style().unpolish(self.result_label)
            self.result_label.style().polish(self.result_label)
        print(f" Game state updated")

    def create_game_area(self):
        """Create the main game area. We wrote this method to organize the game layout into separate sections."""
        game_area = QWidget()
        game_area.setObjectName("gameArea")
        layout = QVBoxLayout(game_area)

        # This creates the dealer area group box
        dealer_group = QGroupBox("Dealer")
        dealer_group.setObjectName("dealerGroup")
        dealer_layout = QVBoxLayout()

        # This creates a label to show the dealer's total
        self.dealer_total_label = QLabel("Total: --")
        self.dealer_total_label.setObjectName("dealerTotalLabel")
        self.dealer_total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        dealer_layout.addWidget(self.dealer_total_label)

        # This creates a layout to hold dealer's cards
        self.dealer_cards_layout = QHBoxLayout()
        dealer_layout.addLayout(self.dealer_cards_layout)
        dealer_group.setLayout(dealer_layout)

        layout.addWidget(dealer_group)

        # This creates a label to display game results
        self.result_label = QLabel("Click 'New Round' to start!")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(self.result_label)

        # This creates the player area group box
        player_group = QGroupBox("Player")
        player_group.setObjectName("playerGroup")
        player_layout = QVBoxLayout()

        # This creates a label to show the player's total
        self.player_total_label = QLabel("Total: --")
        self.player_total_label.setObjectName("playerTotalLabel")
        self.player_total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        player_layout.addWidget(self.player_total_label)

        # This creates a layout to hold player's cards
        self.player_cards_layout = QHBoxLayout()
        player_layout.addLayout(self.player_cards_layout)
        player_group.setLayout(player_layout)

        layout.addWidget(player_group)

        return game_area

    def create_controls(self):
        """Create the control buttons. We wrote this method to group all game controls in one place. using the Principle of Proximity."""
        controls = QWidget()
        controls.setObjectName("controls")
        layout = QHBoxLayout(controls)
        # This adds stretchable space on the left
        layout.addStretch()

        # This creates the Hit button
        self.hit_button = QPushButton("Hit")
        self.hit_button.setObjectName("hitButton")
        self.hit_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.hit_button.setFixedSize(120, 50)
        # This connects the Hit button to the on_hit method
        self.hit_button.clicked.connect(self.on_hit)
        layout.addWidget(self.hit_button)

        # This creates the Stand button
        self.stand_button = QPushButton("Stand")
        self.stand_button.setObjectName("standButton")
        self.stand_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.stand_button.setFixedSize(120, 50)
        # This connects the Stand button to the on_stand method
        self.stand_button.clicked.connect(self.on_stand)
        layout.addWidget(self.stand_button)

        # This creates the New Round button
        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setObjectName("newRoundButton")
        self.new_round_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.new_round_button.setFixedSize(120, 50)
        # This connects the New Round button to the on_new_round method
        self.new_round_button.clicked.connect(self.on_new_round)
        layout.addWidget(self.new_round_button)

        # This adds stretchable space on the right
        layout.addStretch()
        return controls

    def go_to_welcome(self):
        """Return to welcome page with confirmation. We wrote this method to prevent accidental loss of game progress because a good design should have proper Error handling."""
        # This shows a confirmation dialog
        reply = QMessageBox.question(
            self,
            "Return to Home",
            "Are you sure you want to return to home?\nYour current game progress will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        # This checks if the user clicked Yes
        if reply == QMessageBox.StandardButton.Yes:
            if self.parent_window:
                # This calls the parent window's method to show welcome page
                self.parent_window.show_welcome_page()

    # The blocks of codes below deals with the button actions.
    def on_hit(self):
        """Player takes a card. We wrote this method to handle player drawing a card."""
        # This sets the game state to player's turn
        self.set_game_state("player_turn")
        # This gets a card from the game logic
        card = self.game.player_hit()
        if card:
            # This creates a card widget for the drawn card
            card_widget = CardWidget(card)
            # This adds the card widget to player's cards layout
            self.player_cards_layout.addWidget(card_widget)

            # This calculates player's total
            player_total = self.game.player_total()
            # This updates the player total label
            self.player_total_label.setText(f"Total: {player_total}")

            # This checks if player is bust
            if self.game.player_hand.is_bust():
                # This calls method to handle game finished state
                self.game_state_finished()

    def on_stand(self):
        """Player ends turn. We wrote this method to handle player ending their turn and starting dealer's turn."""
        # This sets the game state to dealer's turn
        self.set_game_state("dealer_turn")
        # This calls game logic for player standing
        self.game.player_stand()
        # This updates dealer cards to show the hidden card
        self.update_dealer_cards(full=True)

        # This disables Hit and Stand buttons during dealer's turn
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

        # This gets dealer's total
        dealer_total = self.game.dealer_total()
        # This updates the dealer total label
        self.dealer_total_label.setText(f"Total: {dealer_total}")

        # This updates the result label
        self.result_label.setText("Dealer's turn...")

        # This sets a timer to process dealer's turn
        QTimer.singleShot(1000, self.process_dealer_turn)

    def on_new_round(self):
        """Start a new round. We wrote this method to reset the game for a new round."""
        # This calls game logic to start a new round
        self.game.new_round()
        # This sets up the UI for the new round
        self.new_round_setup()

    def process_dealer_turn(self):
        """Process dealer's turn with animation. We wrote this method to animate dealer drawing cards."""
        # This gets cards drawn by dealer
        drawn_cards = self.game.play_dealer_turn()

        # This sets up timers to animate dealer drawing cards
        for i, card in enumerate(drawn_cards):
            QTimer.singleShot(i * 500, lambda c=card: self.add_dealer_card(c))

        # This schedules the finish of dealer's turn
        QTimer.singleShot((len(drawn_cards) + 1) * 500, self.finish_dealer_turn)

    def add_dealer_card(self, card):
        """Add a card to dealer's hand display. We wrote this method to add cards with visual feedback."""
        # This creates a card widget for the dealer's card
        card_widget = CardWidget(card)
        # This adds the card widget to dealer's cards layout
        self.dealer_cards_layout.addWidget(card_widget)
        # This updates the dealer total label
        dealer_total = self.game.dealer_total()
        self.dealer_total_label.setText(f"Total: {dealer_total}")

    def finish_dealer_turn(self):
        """Finish dealer's turn and show result. We wrote this method to handle end of dealer's turn."""
        # This gets dealer's final total
        dealer_total = self.game.dealer_total()
        # This updates dealer total label
        self.dealer_total_label.setText(f"Total: {dealer_total}")

        # This gets the result text from game logic
        result_text = self.game.decide_winner()
        # This updates the result label
        self.result_label.setText(result_text)

        # This sets the game state based on the result
        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        # This enables the New Round button
        self.new_round_button.setEnabled(True)

        # This updates the parent window's status bar
        if self.parent_window and hasattr(self.parent_window, 'status_bar'):
            if self.game.result == "win":
                self.parent_window.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent_window.status_bar.showMessage("Dealer won this round. Better luck next time!")
            else:
                self.parent_window.status_bar.showMessage("It's a tie! The round ends in a push.")

    def game_state_finished(self):
        """Handle game finished state. We wrote this method to handle when player busts or game ends."""
        # This gets the result text
        result_text = self.game.decide_winner()
        # This updates the result label
        self.result_label.setText(result_text)

        # This sets the game state based on result
        if self.game.result == "win":
            self.set_game_state("finished", "win")
        elif self.game.result == "lose":
            self.set_game_state("finished", "lose")
        else:
            self.set_game_state("finished", "push")

        # This disables Hit and Stand buttons
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        # This enables the New Round button
        self.new_round_button.setEnabled(True)

        # This updates the parent window's status bar
        if self.parent_window and hasattr(self.parent_window, 'status_bar'):
            if self.game.result == "win":
                self.parent_window.status_bar.showMessage("Congratulations! You won this round.")
            elif self.game.result == "lose":
                self.parent_window.status_bar.showMessage("You busted! Dealer wins.")
            else:
                self.parent_window.status_bar.showMessage("It's a tie! The round ends in a push.")


    def clear_layout(self, layout):
        """Remove all widgets from a layout. We wrote this method to clean up layouts before adding new cards."""
        # This loops through all items in the layout
        while layout.count():
            # This takes the first item from the layout
            child = layout.takeAt(0)
            if child.widget():
                # This deletes the widget
                child.widget().deleteLater()

    def update_dealer_cards(self, full=False):
        """Show dealer cards. We wrote this method to hide the first card until revealed."""
        # This clears the current dealer cards layout
        self.clear_layout(self.dealer_cards_layout)

        # This checks if we should show all dealer cards
        if full or self.game.game_state in ["dealer_turn", "finished"]:
            # This shows all dealer cards
            for card in self.game.dealer_hand.cards:
                card_widget = CardWidget(card)
                self.dealer_cards_layout.addWidget(card_widget)
        else:
            # This shows only the first dealer card
            if self.game.dealer_hand.cards:
                card_widget = CardWidget(self.game.dealer_hand.cards[0])
                self.dealer_cards_layout.addWidget(card_widget)

            # This shows a hidden card for the second card
            if self.game.dealer_hand.face_down_card:
                hidden_widget = CardWidget(is_hidden=True)
                self.dealer_cards_layout.addWidget(hidden_widget)

    def new_round_setup(self):
        """Prepare a fresh visual layout. We wrote this method to reset the UI for a new round."""
        # This clears player's and dealer's card layouts
        self.clear_layout(self.player_cards_layout)
        self.clear_layout(self.dealer_cards_layout)

        # This deals initial cards
        self.game.deal_initial_cards()
        # This updates dealer cards
        self.update_dealer_cards(full=False)

        # This adds player's initial cards
        for card in self.game.player_hand.cards:
            card_widget = CardWidget(card)
            self.player_cards_layout.addWidget(card_widget)

        # This updates player's total label
        player_total = self.game.player_total()
        self.player_total_label.setText(f"Total: {player_total}")
        # This sets dealer's total to unknown
        self.dealer_total_label.setText("Total: ?")

        # This checks for immediate win/loss conditions
        if self.game.game_state == "finished":
            # This gets the result text
            result_text = self.game.decide_winner()
            self.result_label.setText(result_text)
            # This disables Hit and Stand buttons
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            # This enables New Round button
            self.new_round_button.setEnabled(True)

            # This sets the game state based on result
            if self.game.result == "win":
                self.set_game_state("finished", "win")
            elif self.game.result == "push":
                self.set_game_state("finished", "push")

            # This updates parent window's status bar
            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                if self.game.result == "win":
                    self.parent_window.status_bar.showMessage("Blackjack! You win!")
                elif self.game.result == "push":
                    self.parent_window.status_bar.showMessage("Both have blackjack! It's a tie.")
        else:
            # This sets up UI for normal round start
            self.result_label.setText("Your turn! Hit or Stand?")
            self.set_game_state("player_turn")
            if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                self.parent_window.status_bar.showMessage(
                    "Your turn. Click Hit to draw a card or Stand to end your turn.")
            # This enables Hit and Stand buttons
            self.hit_button.setEnabled(True)
            self.stand_button.setEnabled(True)
            # This disables New Round button during active round
            self.new_round_button.setEnabled(False)

    def update_ui(self):
        """Update the UI based on game state. We wrote this method as a placeholder for future UI updates."""
        pass