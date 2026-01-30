import random as rd
import sys
import re
from blackjack_cards import create_deck

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

    while True:
        try:
            player_pot = input("How much money would you like to deposit? ").strip()
            if re.search(r'\d+', player_pot):
                break
            else:
                raise ValueError
        except ValueError:
            print("Please deposit an appropriate amount of money")
            pass


def deal_hand(deck):
    player_hand = [deck[0], deck[2]]
    dealer_hand = [deck[1], deck[3]]

    return player_hand, dealer_hand


def standard_game(ph, dh):
    player_is_ace = False
    dealer_is_ace = False
    
    for card in ph:
        if card.rank == "A":
            print(f"{card.rank} of {card.suit} with a value of 1 or 11")
            player_is_ace = True
            
    print(f"Your hand: {ph[0]}, {ph[1]}, with a sum of {ph[0].value + ph[1].value}")

    print(f"Dealer's hand: {dh[0]}, *Facedown*")
main()