import random
import time

quit=False


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        rank_names = {
            'A': 'Ace',
            'K': 'King',
            'Q': 'Queen',
            'J': 'Jack'
        }
        display_rank = rank_names.get(self.rank, self.rank)
        return f"{display_rank} of {self.suit}"
    


class Deck():
    def __init__(self):
        self.reset()
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_card(self):
        return self.cards.pop()
    def cards_remaining(self):
        return len(self.cards)
    def reset(self):
        self.cards = []
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                self.cards.append(Card(rank, suit))




class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == 'A':
                value += 11
                aces += 1
            else:
                value += card.get_value()

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def is_soft(self):
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == 'A':
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

    def is_bust(self):
        return self.get_value() > 21

    def reset_hand(self):
        self.cards = []

    def get_partial_value(self):
        if self.cards:
            return self.cards[0].get_value()

    def __str__(self):
        return f"{', '.join(str(card) for card in self.cards)} | Value: {self.get_value()}"
    


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hands = []

    def receive_result(self, outcome):
        if outcome == 'win':
            self.score += 1
        elif outcome == 'blackjack':
            self.score += 2
        elif outcome == 'loss':
            self.score -= 1

    def get_score(self):
        return self.score

    def __str__(self):
        return f"{self.name} | Score: {self.score}"
    

    
class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.name = "Dealer"

    def show_partial_hand(self):
        return f"Dealer's Hand: {self.hand.cards[0]} | Value: {self.hand.get_partial_value()} "

    def show_full_hand(self):
        return f"Dealer's Hand: {', '.join(str(card) for card in self.hand.cards)} | Value: {self.hand.get_value()}"

    def should_hit(self):
        return self.hand.get_value() <= 16

    def __str__(self):
        return self.show_full_hand()
    


class BlackJackGame:
    def __init__(self, player_names):
        self.deck=Deck()
        self.deck.shuffle()
        self.dealer=Dealer()
        self.players=[Player(name) for name in player_names] #Creates player object with each name passed to player_names
        self.current_round=0

        print("Welcome to this game of BlackJack bruzzas and beezes")
        print(",  ".join(str(player) for player in self.players),"\n")

    def start_round(self):
        self.current_round += 1
        self.dealer.hand.reset_hand()

        for player in self.players:
            player.hands = [Hand()] 

        self.deal_initial_cards()

    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                card=self.deck.deal_card()
                player.hands[0].add_card(card)
            dealer_card=self.deck.deal_card()
            self.dealer.hand.add_card(dealer_card)

    def player_turn(self, player):
        hand = player.hands[0]

        while not hand.is_bust():
            print(player.name)

            if hand.is_blackjack():
                print("Blackjack!")
                break

            choice = input("1. Hit\n2. Stand\n3. Surrender\nChoose an option:\n")

            if choice == '1':
                card = self.deck.deal_card()
                hand.add_card(card)
                print(f"You drew: {card}")
                print(f"Current hand: {hand}\n")
                time.sleep(1)

            elif choice == '2':
                break
            


            else:
                print("Invalid choice.")

    def dealer_turn(self):
        self.dealer.show_full_hand()

        while self.dealer.should_hit():
            card=self.deck.deal_card()
            self.dealer.hand.add_card(card)
            print(f"Dealer hits and draws: {card} | Current hand: {self.dealer.hand}")
            if self.dealer.hand.is_bust():
                print("Dealer busts!")
                break
            time.sleep(2)

    def determine_winners(self):
        dealer = self.dealer.hand
        dealer_value = dealer.get_value()
        dealer_bj = dealer.is_blackjack()

        for player in self.players:
            hand = player.hands[0]
            player_value = hand.get_value()
            player_bj = hand.is_blackjack()

            if hand.is_bust():
                print(f"{player.name} busts.")
                player.receive_result('loss')

            elif player_bj:
                if dealer_bj:
                    print(f"{player.name} pushes with Blackjack.")
                    player.receive_result('push')
                else:
                    print(f"{player.name} gets BLACKJACK!")
                    player.receive_result('blackjack')

            elif dealer.is_bust() or player_value > dealer_value:
                print(f"{player.name} wins with {player_value}!")
                player.receive_result('win')

            elif player_value == dealer_value:
                print(f"{player.name} pushes.")
                player.receive_result('push')

            else:
                print(f"{player.name} loses.")
                player.receive_result('loss')


    def display_game_state(self, hide_dealer_card):
        print()
        if hide_dealer_card:
            print(self.dealer.show_partial_hand())
        else:
            print(self.dealer.show_full_hand())
        
        print()

        for player in self.players:
            print(player)
            print(player.hands[0])
            print()
    
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
            if cont.lower() != 'y':
                break

    def check_for_bankruptcies(self):
        for player in self.players:
            if not player.can_continue():
                print(f"{player.name} is bankrupt and out of the game.")
                self.players.remove(player)
    def game_over(self):
        if not self.players:
            print("All players are bankrupt. Game over.")
            return True
        return False

game =BlackJackGame(["Alice", "Bob"])
game.play_game()

    




    
        