import random
class Card:
    """Represents a playing card with suit and rank"""

    def __init__(self, suit, rank):
        self.suit = suit  # 'H', 'D', 'C', 'S'
        self.rank = rank  # 'A', '2', '3', ..., '10', 'J', 'Q', 'K'

        # This defines suit symbols using Unicode characters
        # We used Unicode because it provides proper suit symbols that work across all platforms
        self.suit_symbols = {
            'H': '♥',  # Hearts (red)
            'D': '♦',  # Diamonds (red)
            'C': '♣',  # Clubs (black)
            'S': '♠'  # Spades (black)
        }

    def get_value(self):
        """Get the numerical value of the card. We wrote this method to calculate card values for the game."""
        # This checks if the card is a face card (Jack, Queen, King)
        if self.rank in ['J', 'Q', 'K']:
            # This returns 10 for face cards
            return 10
        # This checks if the card is an Ace
        elif self.rank == 'A':
            # This returns 11 for Aces by default, we adjusted this later in the code.
            return 11
        else:
            # This converts number cards to integers
            return int(self.rank)

    def get_display_text(self):
        """Get the text representation of the card. We wrote this method for displaying cards in the UI."""
        # This returns the card rank followed by the suit symbol
        return f"{self.rank}{self.suit_symbols[self.suit]}"



class Deck:
    """Represents a standard 52-card deck. We created this class to manage the deck of cards."""

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        """Reset and shuffle the deck. We wrote this method to recreate a full deck when needed."""
        # This defines the four suits
        suits = ['H', 'D', 'C', 'S']
        # This defines all possible ranks
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        # This creates all 52 cards using list comprehension
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        # This shuffles the deck
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck. We wrote this method to randomize card order."""
        # This shuffles the cards using Python's random module
        random.shuffle(self.cards)

    def draw(self):
        """Draw a card from the deck. We wrote this method to remove and return the top card."""
        # This checks if the deck is empty
        if len(self.cards) == 0:
            # This resets the deck if empty
            self.reset()
        # This removes and returns the last card from the deck
        return self.cards.pop()

class Hand:
    """Represents a player's hand. We created this class to manage a collection of cards."""
    def __init__(self):
        self.cards = []
        self.is_dealer = False
        self.face_down_card = None  # For dealer's hidden card

    def add_card(self, card, face_up=True):
        """Add a card to the hand. We wrote this method to handle both face-up and face-down cards."""
        # This checks if the card should be hidden and if this is the dealer's hand
        if not face_up and self.is_dealer:
            # This stores the card as hidden for dealer
            self.face_down_card = card
        else:
            # This adds the card normally to the hand
            self.cards.append(card)

    def reveal_hidden_card(self):
        """Reveal the hidden card. We wrote this method for the dealer to show their hidden card."""
        # This checks if there's a hidden card
        if self.face_down_card:
            # This adds the hidden card to the visible cards
            self.cards.append(self.face_down_card)
            # This clears the hidden card reference
            self.face_down_card = None

    def calculate_value(self):
        """Calculate the hand value. We wrote this method to handle Ace values intelligently."""
        # This initializes the total value
        total = 0
        # This counts the number of Aces
        aces = 0

        # This loops through all visible cards
        for card in self.cards:
            # This gets the card's value
            value = card.get_value()
            # This checks if the card is an Ace
            if card.rank == 'A':
                # This increments the Ace count
                aces += 1
            # This adds the card value to the total
            total += value

        # This adjusts Aces from 11 to 1 if the total is over 21
        while total > 21 and aces > 0:
            # This subtracts 10 (changes Ace from 11 to 1)
            total -= 10
            # This decreases the Ace count
            aces -= 1

        # This returns the final total
        return total

    def is_bust(self):
        """Check if hand is bust. We wrote this method to determine if a hand exceeds 21."""
        # This checks if the hand value is greater than 21
        return self.calculate_value() > 21


    def has_blackjack(self):
        """Check if hand is a natural blackjack. We wrote this method to detect instant wins."""
        # This checks if there are exactly 2 cards with total value 21 and one is an Ace
        return (len(self.cards) == 2 and
                self.calculate_value() == 21 and
                ('A' in [card.rank for card in self.cards]))


    def clear(self):
        """Clear the hand. We wrote this method to reset the hand for a new round."""
        # This empties the cards list
        self.cards = []
        # This clears any hidden card
        self.face_down_card = None


    def get_card_count(self):
        """Get total number of cards. We wrote this method to count all cards including hidden ones."""
        # This returns the count of visible cards plus hidden card if present
        return len(self.cards) + (1 if self.face_down_card else 0)


class Game21:
    """Main game class implementing the 21 Card Game"""

    def __init__(self):
        # Start immediately with a fresh round
        self.new_round()

        # Game statistics - commented out for assignment compliance
        # The assignment requires only single self-contained rounds
        # These lines are kept for future use if needed
        # self.player_wins = 0
        # self.dealer_wins = 0
        # self.rounds_played = 0

    # ROUND MANAGEMENT

    def new_round(self):
        """
        Prepares for a new self-contained round
        - Create and shuffle a new deck
        - Reset both hands
        - Reset game state
        """
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.dealer_hand.is_dealer = True

        # Game state tracking - reset for each round
        self.game_state = "idle"  # idle, player_turn, dealer_turn, finished
        self.result = None  # win, lose, push
        self.dealer_hidden_revealed = False

    def reset_game(self):
        """
        Reset the entire game - starts a fresh round
        (For assignment compliance, this just starts a new round since no persistent scores)
        """
        # For future use if statistics tracking is implemented
        # self.player_wins = 0
        # self.dealer_wins = 0
        # self.rounds_played = 0

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
                # Commented out for assignment compliance - no persistent statistics
                # self.player_wins += 1
            # Commented out for assignment compliance - no persistent statistics
            # self.rounds_played += 1
        else:
            self.game_state = "player_turn"
            self.result = None

    # DECK AND CARD DRAWING

    def draw_card(self):
        """Return the next card in the shuffled deck"""
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
            # Commented out for assignment compliance - no persistent statistics
            # self.dealer_wins += 1
            # self.rounds_played += 1
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
        # Commented out for assignment compliance - no persistent statistics
        # self.rounds_played += 1

        return drawn_cards

    # WINNER DETERMINATION

    def decide_winner(self):
        """
        Decide the outcome of the round.
        """
        self.determine_winner()

        if self.result == "win":
            # Commented out for assignment compliance - no persistent statistics
            # self.player_wins += 1
            return "Player wins!"
        elif self.result == "lose":
            # Commented out for assignment compliance - no persistent statistics
            # self.dealer_wins += 1
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
            # Commented out for assignment compliance - no persistent statistics
            # self.dealer_wins += 1
        elif self.dealer_hand.is_bust():
            self.result = "win"
            # Commented out for assignment compliance - no persistent statistics
            # self.player_wins += 1
        elif player_value > dealer_value:
            self.result = "win"
            # Commented out for assignment compliance - no persistent statistics
            # self.player_wins += 1
        elif dealer_value > player_value:
            self.result = "lose"
            # Commented out for assignment compliance - no persistent statistics
            # self.dealer_wins += 1
        else:
            self.result = "push"

    def player_stand(self):
        """Player ends their turn"""
        if self.game_state != "player_turn":
            return

        self.reveal_dealer_card()
        # Note: play_dealer_turn will be called separately from UI

    # Commented out for assignment compliance - no persistent statistics needed
    # def get_statistics(self):
    #     """
    #     Returns the current game statistics
    #     """
    #     return {
    #         'player_wins': self.player_wins,
    #         'dealer_wins': self.dealer_wins,
    #         'rounds_played': self.rounds_played,
    #         'ties': self.rounds_played - self.player_wins - self.dealer_wins
    #     }