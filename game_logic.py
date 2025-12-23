import random


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


class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.new_round()

        # Game statistics
        self.player_wins = 0
        self.dealer_wins = 0
        self.rounds_played = 0

    # ROUND MANAGEMENT

    def new_round(self):
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.dealer_hand.is_dealer = True

        # Game state tracking
        self.game_state = "idle"  # idle, player_turn, dealer_turn, finished
        self.result = None  # win, lose, push
        self.dealer_hidden_revealed = False

    def reset_game(self):
        """
        Reset the entire game - all scores and rounds to zero
        """
        self.player_wins = 0
        self.dealer_wins = 0
        self.rounds_played = 0
        self.new_round()

    def deal_initial_cards(self):
        """
        Deal two cards each to player and dealer.
        """
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

    # DECK AND CARD DRAWING

    def create_deck(self):
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        """
        Return the next card in the shuffled deck.
        Note: Using our Card class instead of string representation
        """
        return self.deck.draw()

    # HAND VALUES + ACE HANDLING

    def card_value(self, card):
        """
        Convert a card string into its numeric value.

        Rules:
        - Number cards = their number (2–10)
        - J, Q, K = 10
        - A is normally 11, may later count as 1 if needed
        """
        return card.get_value()

    def hand_total(self, hand):
        """
        Calculates the best possible total for a hand.
        Aces are counted as 11 unless this would bust the hand,
        in which case they are reduced to 1.
        """
        return hand.calculate_value()

    # PLAYER ACTIONS

    def player_hit(self):
        """
        Add one card to the player's hand and return it
        """
        if self.game_state != "player_turn":
            return None

        card = self.draw_card()
        self.player_hand.add_card(card)

        if self.player_hand.is_bust():
            self.game_state = "finished"
            self.result = "lose"
            self.dealer_wins += 1
            self.rounds_played += 1
            self.dealer_hand.reveal_hidden_card()

        return card

    def player_total(self):
        """
        Return the player's total
        """
        return self.player_hand.calculate_value()

    # DEALER ACTIONS

    def reveal_dealer_card(self):
        """
        Called when the player presses Stand.
        After this, the UI should show both dealer cards.
        """
        self.dealer_hidden_revealed = True
        self.dealer_hand.reveal_hidden_card()

    def dealer_total(self):
        """
        Return the dealer's total
        """
        return self.dealer_hand.calculate_value()

    def play_dealer_turn(self):
        """
        Dealer must hit until their total is 17 or more, then stand.
        Returns list of cards drawn during dealer's turn.
        """
        self.game_state = "dealer_turn"
        drawn_cards = []

        while self.dealer_hand.calculate_value() < 17:
            card = self.draw_card()
            self.dealer_hand.add_card(card)
            drawn_cards.append(card)

        self.game_state = "finished"
        self.determine_winner()
        self.rounds_played += 1

        return drawn_cards

    # WINNER DETERMINATION

    def decide_winner(self):
        """
        Decide the outcome of the round.
        """
        self.determine_winner()

        if self.result == "win":
            self.player_wins += 1
            return "Player wins!"
        elif self.result == "lose":
            self.dealer_wins += 1
            return "Dealer wins!"
        elif self.result == "push":
            return "Push (tie)."
        else:
            return "Game in progress"

    def determine_winner(self):
        """Determine the winner of the round"""
        if self.game_state != "finished":
            return

        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        if self.player_hand.is_bust():
            self.result = "lose"
        elif self.dealer_hand.is_bust():
            self.result = "win"
        elif player_value > dealer_value:
            self.result = "win"
        elif dealer_value > player_value:
            self.result = "lose"
        else:
            self.result = "push"

    def player_stand(self):
        """Player ends their turn"""
        if self.game_state != "player_turn":
            return

        self.reveal_dealer_card()
        # Note: play_dealer_turn will be called separately from UI

    def get_statistics(self):
        """
        Returns the current game statistics
        """
        return {
            'player_wins': self.player_wins,
            'dealer_wins': self.dealer_wins,
            'rounds_played': self.rounds_played,
            'ties': self.rounds_played - self.player_wins - self.dealer_wins
        }