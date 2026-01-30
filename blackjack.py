import random as rd
import sys
import re
from blackjack_cards import create_deck

player_pot = 0     # Global variable to keep track of the player's available pot

def main():
    deck = create_deck()                        # Create_deck() creates a list containing the standard 52 cards
    rd.shuffle(deck)                            # Shuffles the deck 
    
    start_game()                                # Starts a game
    player_hand, dealer_hand = deal_hand(deck)
    winner = standard_game(player_hand, dealer_hand)


def start_game():
    print("Welcome to a game of blackjack")
    while True:
        try:
            name = input("What is your name? ").strip()
            if not 0 < len(name) < 13:
                raise ValueError
            break           
        except ValueError:
            print("Please choose a new name")
            pass

    global player_pot
    player_pot = add_account_funds()


def deal_hand(deck):
    player_hand = [deck[0], deck[2]]
    dealer_hand = [deck[1], deck[3]]

    return player_hand, dealer_hand

def add_account_funds():
    while True:
        try:
            response = input("How many dollars would you like to deposit to your pot? ").strip()
            if USD_check(response):
                global player_pot
                player_pot = int(response)
                break
            else:
                print("Please deposit an appropriate amount of money (USD number only)")
                raise ValueError
        except ValueError:
            pass

def USD_check(response):
    if re.search("^\d$", response):
        return True
    else:
        return False
    
def standard_game(ph, dh):
    ask_for_bet()
    for card in ph:
        if card.rank == "A":
            print(f"{card.rank} of {card.suit} with a value of 1 or 11")
            player_is_ace = True
    
    # Show the player their hand
    print(f"Your hand: {ph[0]}, {ph[1]}, with a sum of {ph[0].value + ph[1].value}")

    # Show the dealer their hand
    print(f"Dealer's hand: {dh[0]}, *Facedown*")

def ask_for_bet():
    ...
if __name__ == "__main__":
    main()