import random as rd
import sys
import re
from blackjack_cards import create_deck

def main():
    deck = create_deck()
    rd.shuffle(deck)
    
    start_game()
    player_hand, dealer_hand = deal_hand(deck)
    


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

main()