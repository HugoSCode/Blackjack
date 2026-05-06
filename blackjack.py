import random
import time

quit = False


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # Returns blackjack value of a card
    def get_value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        rank_names = {"A": "Ace", "K": "King", "Q": "Queen", "J": "Jack"}
        display_rank = rank_names.get(self.rank, self.rank)
        return f"{display_rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.reset()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)

    # Builds a fresh deck
    def reset(self):
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in [
                "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
            ]:
                self.cards.append(Card(rank, suit))


class Hand:
    def __init__(self):
        self.cards = []

    # Splits a hand into two new hands (assumes exactly 2 cards)
    def split_hand(self):
        card1, card2 = self.cards
        hand1 = Hand()
        hand2 = Hand()

        hand1.add_card(card1)
        hand2.add_card(card2)

        return [hand1, hand2]

    def add_card(self, card):
        self.cards.append(card)

    # Calculates best blackjack value (handles aces as 1 or 11)
    def get_value(self):
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == "A":
                value += 11
                aces += 1
            else:
                value += card.get_value()

        # Convert Aces from 11 → 1 if busting
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    # Returns True if hand is "soft" (contains usable Ace)
    def is_soft(self):
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == "A":
                value += 11
                aces += 1
            else:
                value += card.get_value()

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return aces > 0

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21

    # Can only split if both cards have same rank
    def can_split(self):
        return self.cards[0].rank == self.cards[1].rank

    def is_bust(self):
        return self.get_value() > 21

    def reset_hand(self):
        self.cards = []

    def get_partial_value(self):
        if self.cards:
            return self.cards[0].get_value()

    def __str__(self):
        return (
            f"{', '.join(str(card) for card in self.cards)} | Value: {self.get_value()}"
        )


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hands = []  # list of Hand objects (important for splitting)
        self.surrendered = False
        self.split = False  # tracks if player already split

    # Updates score based on outcome
    def receive_result(self, outcome):
        if outcome == "win":
            self.score += 1
        elif outcome == "blackjack":
            self.score += 2
        elif outcome == "loss":
            self.score -= 1

    def get_score(self):
        return self.score

    def __str__(self):
        return f"{self.name} | Score: {self.score}"


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.name = "Dealer"

    # Shows only first card (used at start of round)
    def show_partial_hand(self):
        return f"Dealer's Hand: {self.hand.cards[0]} | Value: {self.hand.cards[0].get_value()} "

    def show_full_hand(self):
        return f"Dealer's Hand: {', '.join(str(card) for card in self.hand.cards)} | Value: {self.hand.get_value()}"

    # Dealer hits on 16 or less (standard rule)
    def should_hit(self):
        return self.hand.get_value() <= 16

    def __str__(self):
        return self.show_full_hand()


class BlackJackGame:
    def __init__(self, player_names):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer()
        self.players = [Player(name) for name in player_names]
        self.current_round = 0

        print("Welcome to this game of BlackJack bruzzas and beezes")
        print(",  ".join(str(player) for player in self.players), "\n")

    # Starts a new round (resets hands, deals cards)
    def start_round(self):
        self.current_round += 1
        self.dealer.hand.reset_hand()

        for player in self.players:
            player.hands = [Hand()]  # reset to one hand

        self.deal_initial_cards()

    # Deals 2 cards to each player and dealer
    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.deal_card()
                player.hands[0].add_card(card)

            dealer_card = self.deck.deal_card()
            self.dealer.hand.add_card(dealer_card)

    # Handles one player's entire turn (including splits)
    def player_turn(self, player):

        i = 0
        # IMPORTANT: use index loop because hands can change (splitting)
        while i < len(player.hands):
            hand = player.hands[i]

            while not hand.is_bust():
                print(f"\n{player.name}'s turn")
                print(f"\n{hand}")

                if hand.is_blackjack():
                    print("\nBlackjack!")
                    break

                # Dynamic menu (options appear only when valid)
                choice = input(
                    f"\n1. Hit\n2. Stand"
                    f"{'\n3. Surrender'  if len(hand.cards) == 2 else ''}"
                    f"{'\n4. Split' if hand.can_split() and not player.split else ''}"
                    "\nChoose an option:\n"
                )

                if choice == "1":
                    card = self.deck.deal_card()
                    hand.add_card(card)
                    print(f"\nYou drew: {card}")
                    print(f"Current hand: {hand}\n")
                    time.sleep(1)

                elif choice == "2":
                    print(f"\n{player.name} stands")
                    time.sleep(1)
                    break

                elif choice == "3" and len(player.hands[0].cards) == 2:
                    print(f"\n{player.name} surrenders")
                    time.sleep(1)
                    player.surrendered = True
                    break

                elif choice == "4" and hand.can_split() and not player.split:
                    print(f"\n{player.name} splits")

                    player.split = True

                    # Split current hand into two
                    new_hands = hand.split_hand()

                    # Replace current hand with new split hands
                    player.hands.remove(hand)
                    player.hands.extend(new_hands)

                    # Give each new hand one extra card
                    for i in range(2):
                        card = self.deck.deal_card()
                        player.hands[i].add_card(card)

                    break  # exit loop to process new hands

                else:
                    print("Invalid choice.")

            i += 1  # move to next hand

    # Dealer plays after all players
    def dealer_turn(self):
        self.dealer.show_full_hand()

        while self.dealer.should_hit():
            card = self.deck.deal_card()
            self.dealer.hand.add_card(card)
            print(f"Dealer hits and draws: {card} | Current hand: {self.dealer.hand}")

            if self.dealer.hand.is_bust():
                print("Dealer busts!")
                break

            time.sleep(2)

    # Determines results for each player
    def determine_winners(self):
        dealer = self.dealer.hand
        dealer_value = dealer.get_value()
        dealer_bj = dealer.is_blackjack()

        print("\n===== ROUND RESULTS =====")
        print(f"Dealer: {dealer} \n")

        for player in self.players:
            hand = player.hands[0]  # NOTE: only checks first hand (bug if split!)
            player_value = hand.get_value()
            player_bj = hand.is_blackjack()

            print(f"--- {player.name} ---")
            print(f"Hand: {hand}")

            if player.surrendered:
                print("Result: Surrendered")
                player.receive_result("loss")
                print()
                continue

            if hand.is_bust():
                print("Result: Bust")
                player.receive_result("loss")

            elif player_bj:
                if dealer_bj:
                    print("Result: Push (both Blackjack)")
                    player.receive_result("push")
                else:
                    print("Result: Blackjack!")
                    player.receive_result("blackjack")

            elif dealer.is_bust():
                print("Result: Win (dealer bust)")
                player.receive_result("win")

            elif player_value > dealer_value:
                print(f"Result: Win ({player_value} vs {dealer_value})")
                player.receive_result("win")

            elif player_value == dealer_value:
                print(f"Result: Push ({player_value} vs {dealer_value})")
                player.receive_result("push")

            else:
                print(f"Result: Loss ({player_value} vs {dealer_value})")
                player.receive_result("loss")

            print()

        print("===== SCOREBOARD =====")
        for player in self.players:
            print(f"{player.name}: {player.score}")
        print("======================\n")

    # Shows current game state
    def display_game_state(self, hide_dealer_card):
        print()
        if hide_dealer_card:
            print(self.dealer.show_partial_hand())
        else:
            print(self.dealer.show_full_hand())

        print()

        for player in self.players:
            print(player)
            print(player.hands[0])  # NOTE: only shows first hand
            print()

    # Main game loop
    def play_game(self):
        while True:
            self.start_round()
            self.display_game_state(hide_dealer_card=True)

            for player in self.players:
                self.player_turn(player)

            self.display_game_state(hide_dealer_card=False)

            self.dealer_turn()
            self.determine_winners()

            print("\nEnd of Round\n")

            cont = input("Play another round? (y/n): ")
            if cont.lower() != "y":
                break


game = BlackJackGame(["Alice", "Bob"])
game.play_game()