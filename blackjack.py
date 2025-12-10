import random as rd
import sys
import re
from blackjack_cards import create_deck

def main():
    deck = create_deck()
    rd.shuffle(deck)
    
    start_game()


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

main()