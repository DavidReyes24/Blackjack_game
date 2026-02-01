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
    if re.search(r"^\d$", response):
        return True
    else:
        return False
    
def standard_game(ph, dh):
    bet = ask_for_bet()
    for card in ph:
        if card.rank == "A":
            print(f"{card.rank} of {card.suit} with a value of 1 or 11")
            player_is_ace = True
    
    # Show the player their hand
    print(f"Your hand: {ph[0]}, {ph[1]}, with a sum of {ph[0].value + ph[1].value}")

    # Show the dealer their hand
    print(f"Dealer's hand: {dh[0]}, *Facedown*")

def ask_for_bet():
    global player_pot
    while True:
        try:
            wager = input("Please place a bet from your remaining pot funds for this game: ")
            if USD_check(wager):
                if int(wager) < player_pot:
                    response = input("You have insufficient funds to place this bet. Would you like to deposit" \
                    "the difference? Y/N: ")
                    if response == "Y":
                        player_pot += (int(wager) - player_pot)
                        break
                    else:
                        try:
                            response2 = input("Please deposit more funds to your pot to continue this game: ")
                            if USD_check(response2):
                                player_pot += int(response2)
                                ask_for_bet()
                            else:
                                raise Exception("Not enough funds")
                        except Exception as e:
                            if e == "Not enough funds":
                                print(f"Sorry, the game cannot continue. {e}.")
                                sys.exit()
            else:
                raise ValueError
        except ValueError:
            print("Please input an appropriate amount in USD dollars")
            pass

if __name__ == "__main__":
    main()