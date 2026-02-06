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
                    print(f"{bet} dollars have been bet on this game. Good luck!")
                    break
                else:
                    condition = deposit_more_funds(int(bet))
                    if condition == 1:   # Return 1: Player agreed to deposit the difference.  
                        bet = player_pot               # Return 2: Player made a different deposit.
                        print(f"{bet} dollars have been bet for this game. Good luck!")
                        break                          # Return 0: Player refused to make a new deposit.
                    elif condition == 2:
                        break
                    else:
                        sys.exit("Unable to continue the game. Please start a new one.")
            else:
                raise ValueError
        except ValueError:
            print("Please input an appropriate value in USD.")
            pass
            
    # Show the player their hand
    time.sleep(1.5)
    print(f"Your hand: {ph[0]}, {ph[1]}, with a sum of {ph[0].value + ph[1].value}")

    # Show the dealer their hand
    time.sleep(1.5)
    print(f"Dealer's hand: {dh[0]}, *Facedown*")

    # Scenario where player has a blackjack
    ph_blackjack = False
    if ph[0].value or ph[1].value == 10:
        if ph[0].rank or ph[1].rank == "A":
            print("You have blackjack")
            ph_blackjack = True

    # Scenario where dealer's faceup card is an Ace
    if dh[0].rank == "A":
        # Scenario where player already has blackjack
        if ph_blackjack == True:
            offer_even_money()
        else:
            offer_insurance()

    # Check to see if the player can split their cards?
    if ph[0].value == ph[1].value:
        split_option = True
    else:
        split_option = False
    
    # Check with player how they want to proceed in the game.
    if split_option == True:
        game_choice = input("What would you like to do? Split, Hit, Stand, or Double Down?" ).lower()
    else:
        game_choice = input("What would you llke to do? Hit, Stand, or Double Down? ").lower()

    while True:
        try:
            game_time(game_choice)
        except:
            ...

            


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
                    print(f"Let's deposit a different amount to your account to complete this bet. " \
                    f"Your current account holds {player_pot} dollars.")
                    response2 = input("What amount would you like to deposit to your account? ")
                    if USD_check(response2):
                        player_pot += int(response2)
                        print(f"Your account now has {player_pot} dollars in it.")
                        response3 = input("Please place your bet for this game now. ")
                        if USD_check(response3):
                            if bet_validation(int(response3)):
                                different_bet = int(response3)
                                player_pot -= different_bet
                                print(f"{different_bet} dollars have been bet for this game. Good luck!")
                                return 2
                            else:
                                return 0
                        else:
                            player_pot -= int(response2)
                            print("Sorry, your bet still exceeds your account funds. " \
                            "Your account deposit has been returned.")
                            raise ValueError
                    else:
                        raise ValueError
                except ValueError:
                    print("Please input an appropriate amount of dollars in USD.")
                    pass
    except ValueError:
        sys.exit()

def offer_even_money():
    ...

def offer_insurance():
    ...

def offer_to_split():
    ...

def game_time(decision):
    match decision:
        case "Stand":
            ...
        case "Hit":
            ...
        case "Double Down":
            ...
        case "Split":
            ...
if __name__ == "__main__":
    main()