import random as rd
import sys
import re
import time
from blackjack_cards import create_deck

player_pot = 0     # Global variable to keep track of the player's available pot
different_bet = 0

def main():
    global player_pot
    deck = create_deck()                        # Create_deck() creates a list containing the standard 52 cards
    rd.shuffle(deck)                            # Shuffles the deck 
    
    start_game()
    print(f"Player pot = {player_pot}")                                # Starts a game
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
                return int(response)
            else:
                print("Please deposit an appropriate amount of money (USD number only)")
                raise ValueError
        except ValueError:
            pass

def USD_check(response):
    return True if re.search(r"^\d+$", response) else False
    
def standard_game(ph, dh):
    global player_pot
    while True:
        try:
            bet = input("Please place a bet from your remaining pot funds for this game: ")
            if USD_check(bet):
                if bet_validation(int(bet)):
                    bet = int(bet)
                    player_pot -= bet
                    break
                else:
                    condition = deposit_more_funds(int(bet))
                    if condition == 1:   # Return 1: Player agreed to deposit the difference.  
                        bet = player_pot               # Return 2: Player made a different deposit.
                        break                          # Return 0: Player refused to make a new deposit.
                    elif condition == 2:
                        ...
                    else:
                        sys.exit("Unable to continue the game. Please start a new one.")
            else:
                raise ValueError
        except ValueError:
            print("Please input an appropriate value in USD.")
            pass


    for card in ph:
        if card.rank == "A":
            print(f"{card.rank} of {card.suit} with a value of 1 or 11")
            player_is_ace = True
    
    # Show the player their hand
    print(f"Your hand: {ph[0]}, {ph[1]}, with a sum of {ph[0].value + ph[1].value}")

    # Show the dealer their hand
    print(f"Dealer's hand: {dh[0]}, *Facedown*")

def bet_validation(bet):
    global player_pot
    return True if bet <= player_pot else False

def deposit_more_funds(bet):
    global player_pot
    global different_bet

    try:
        difference = bet - player_pot
        print(f"Your current account has {player_pot} dollars. You have insufficient funds to place this bet.")
        response1 = input(f"To place this bet. Would you like to add {difference} dollars to your account? Y/N ")
        if response1 == "Y":
            player_pot += difference
            return 1
        else:
            while True:
                try:
                    print("Let's deposit a different amount to your account to complete this bet.")
                    response2 = input("What amount would you like to deposit to your account? ")
                    if USD_check(response2):
                        player_pot += int(response2)
                        response3 = input("Please place your bet for this game now. ")
                        if USD_check(response3):
                            if bet_validation(int(response3)):
                                different_bet = int(response3)
                                return 2
                            else:
                                return 0
                        else:
                            player_pot -= int(response2)
                            raise ValueError
                    else:
                        raise ValueError
                except ValueError:
                    print("Please input an appropriate amount of dollars in USD.")
                    pass
    except ValueError:
        sys.exit()

if __name__ == "__main__":
    main()