from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class WelcomePage(QWidget):
    """Welcome page with game introduction and start button. We created this class to display the welcome screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.current_theme = "light"
        self.init_ui()

    def init_ui(self):
        """Initialize welcome page UI. We wrote this method to set up all the visual elements on the welcome screen."""
        # This sets the object name for styling
        self.setObjectName("welcomePage")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # The block of code below handles the title with theme-aware styling
        self.title_label = QLabel("Welcome to ZA Great's and Victor's Card Game") # This creates the title label
        self.title_label.setObjectName("titleLabel")
        title_font = QFont("Arial", 36, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        #  The block of code below handles the Card symbols with theme-aware styling
        # This creates a widget to hold card symbols
        card_symbols_widget = QWidget()
        # This creates a horizontal layout for the card symbols
        card_layout = QHBoxLayout(card_symbols_widget)
        # This sets spacing between card symbols
        card_layout.setSpacing(20)

        # This creates a list to store card symbol labels
        self.card_symbols = []
        # This defines the four card suits using Unicode symbols
        suits = ['♠', '♥', '♦', '♣']

        for i, suit in enumerate(suits): # This loops through each suit to create a symbol label
            symbol_label = QLabel(suit)
            symbol_label.setObjectName(f"cardSymbol{i}")
            symbol_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            symbol_font = QFont("Arial", 48, QFont.Weight.Bold)
            symbol_label.setFont(symbol_font)
            symbol_label.setFixedSize(80, 80)
            card_layout.addWidget(symbol_label)
            self.card_symbols.append(symbol_label)

        card_layout.addStretch()
        main_layout.addWidget(card_symbols_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Game rules/instructions
        self.rules_group = QGroupBox("Game Rules & Instructions")
        self.rules_group.setObjectName("rulesGroup")

        # This creates a scroll area for the rules with visible scrollbar
        self.rules_scroll = QScrollArea()
        self.rules_scroll.setWidgetResizable(True)
        self.rules_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.rules_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # This creates the rules content widget
        self.rules_content = QWidget()
        self.rules_layout = QVBoxLayout(self.rules_content)
        self.rules_layout.setSpacing(15)
        self.rules_layout.setContentsMargins(20, 20, 25, 20)

        # This creates labels for each section of the rules
        # Objective section
        self.objective_title = QLabel("Objective:")
        self.objective_title.setObjectName("objectiveTitle")
        self.objective_content = QLabel("Get as close to 21 as possible without going over.")
        self.objective_content.setObjectName("objectiveContent")
        self.objective_content.setWordWrap(True)

        # Card Values section
        self.card_values_title = QLabel("Card Values:")
        self.card_values_title.setObjectName("cardValuesTitle")
        self.card_values_content = QLabel()
        self.card_values_content.setObjectName("cardValuesContent")
        self.card_values_content.setTextFormat(Qt.TextFormat.PlainText)
        self.card_values_content.setText(
            "• Number cards = face value (2-10)\n"
            "• Face cards (J, Q, K) = 10 points\n"
            "• Aces = 1 or 11 points (whichever is better)"
        )

        # Game Flow section
        self.game_flow_title = QLabel("Game Flow:")
        self.game_flow_title.setObjectName("gameFlowTitle")
        self.game_flow_content = QLabel()
        self.game_flow_content.setObjectName("gameFlowContent")
        self.game_flow_content.setTextFormat(Qt.TextFormat.PlainText)
        self.game_flow_content.setText(
            "1. Each round starts with 2 cards dealt to both player and dealer\n"
            "2. Dealer's first card is hidden\n"
            "3. Player can:\n"
            "   • Hit: Take another card\n"
            "   • Stand: End your turn\n"
            "4. Dealer must hit until reaching 17 or higher\n"
            "5. Closest to 21 wins!"
        )

        # Additional Features section
        self.features_title = QLabel("Additional Features:")
        self.features_title.setObjectName("featuresTitle")
        self.features_content = QLabel()
        self.features_content.setObjectName("featuresContent")
        self.features_content.setTextFormat(Qt.TextFormat.PlainText)
        self.features_content.setText(
            "• Light/Dark theme toggle\n"
            "• Single self-contained rounds\n"
            "• Clear visual feedback"
        )

        # Add all sections to the layout
        self.rules_layout.addWidget(self.objective_title)
        self.rules_layout.addWidget(self.objective_content)
        self.rules_layout.addSpacing(10)
        self.rules_layout.addWidget(self.card_values_title)
        self.rules_layout.addWidget(self.card_values_content)
        self.rules_layout.addSpacing(10)
        self.rules_layout.addWidget(self.game_flow_title)
        self.rules_layout.addWidget(self.game_flow_content)
        self.rules_layout.addSpacing(10)
        self.rules_layout.addWidget(self.features_title)
        self.rules_layout.addWidget(self.features_content)

        # Add stretch at the end to push content to top
        self.rules_layout.addStretch()

        # Set the content widget to the scroll area
        self.rules_scroll.setWidget(self.rules_content)

        # Create a container for the rules
        rules_container = QVBoxLayout()
        rules_container.addWidget(self.rules_scroll)
        self.rules_group.setLayout(rules_container)

        main_layout.addWidget(self.rules_group)

        # Start game button
        self.start_button = QPushButton("START GAME")
        self.start_button.setObjectName("startButton")
        self.start_button.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.start_button.setFixedSize(300, 70)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_button.clicked.connect(self.start_game)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add some spacing at the bottom
        main_layout.addStretch()

        # Apply initial theme
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        """Apply theme to welcome page"""
        self.current_theme = theme
        self.setProperty("theme", theme)

        # Apply theme to all child widgets
        for child in self.findChildren(QWidget):
            if child != self:  # Don't set on self again
                child.setProperty("theme", theme)

        # Update scrollbar styling
        scrollbar_style = ""
        if theme == "light":
            scrollbar_style = """
                QScrollBar:vertical {
                    background: #f0f0f0;
                    width: 14px;
                    margin: 0px;
                    border-radius: 7px;
                }
                QScrollBar::handle:vertical {
                    background: #3498db;
                    min-height: 30px;
                    border-radius: 7px;
                    border: 2px solid #f0f0f0;
                }
                QScrollBar::handle:vertical:hover {
                    background: #2980b9;
                }
                QScrollBar::handle:vertical:pressed {
                    background: #1f618d;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """
        else:
            scrollbar_style = """
                QScrollBar:vertical {
                    background: #34495e;
                    width: 14px;
                    margin: 0px;
                    border-radius: 7px;
                }
                QScrollBar::handle:vertical {
                    background: #2980b9;
                    min-height: 30px;
                    border-radius: 7px;
                    border: 2px solid #34495e;
                }
                QScrollBar::handle:vertical:hover {
                    background: #1f618d;
                }
                QScrollBar::handle:vertical:pressed {
                    background: #154360;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """

        self.rules_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            {scrollbar_style}
        """)

        # This forces stylesheet reapplication on the welcome page
        self.style().unpolish(self)
        self.style().polish(self)

        # This forces stylesheet reapplication on all child widgets
        for child in self.findChildren(QWidget):
            if child != self:
                child.style().unpolish(child)
                child.style().polish(child)

    def start_game(self):
        """Switch to game page"""
        if self.parent_window:
            print(" Starting game...")
            self.parent_window.show_game_page()