import random as rd
import sys
import re
import time
from blackjack_cards import create_deck

player_pot = 0     # Global variable to keep track of the player's available pot
different_bet = 0  # Global variable used to save a different bet for a game after depositing funds

def main():
    global player_pot
    deck = create_deck()                        # Create_deck() creates a list containing the standard 52 cards
    rd.shuffle(deck)                            # Shuffles the deck 
    
    start_game()
    print(f"You have deposited {player_pot} dollars to your pot.")                                # Starts a game
    player_hand, dealer_hand, post_deal_deck = deal_hand(deck)
    print(type(player_hand))
    print(type(dealer_hand))
    winner = standard_game(player_hand, dealer_hand, post_deal_deck)
    print(f"The {winner} has won this game")


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
    post_deal_deck = deck[4:]

    return player_hand, dealer_hand, post_deal_deck

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
    
def standard_game(ph, dh, pd_deck):
    global player_pot
    while True:
        try:
            bet = input("Please place a bet from your remaining pot funds for this game: ")
            if USD_check(bet) and int(bet) != 0:
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

    while True: # Needed to break away if an instant win occurs before anything else happens
        # Scenario where player has a blackjack
        ph_blackjack = False
        blackjack_ranks = ["10", "J", "Q", "K"]
        if ph[0].rank in blackjack_ranks or ph[1].rank in blackjack_ranks:
            if ph[0].rank == "A" or ph[1].rank == "A":
                print("You have blackjack")
                ph_blackjack = True

        # Scenario where dealer's faceup card is an Ace
        if dh[0].rank == "A":
            # Scenario where player already has blackjack
            if ph_blackjack == True:
                if offer_even_money():
                    winnings = bet * 2              # Instant Payout 1:1
                    print(f"You won {winnings} dollars this game.")
                    player_pot += winnings          # Updates the player_pot with the winnings
                    break
                else:
                    continue
            else:
                if offer_insurance():
                    if validate_insurance(bet):
                        insurance_bet = bet / 2
                        player_pot -= insurance_bet
                        side_bet_exists = True
                        print(f"Insurance has been purchased. Side bet is {insurance_bet} dollars")
                        print("Checking Facedown Card...")
                        time.sleep(2)
                        if dh[1].rank in blackjack_ranks:
                            print(f"Dealer's facedown is {dh[1]}, therefore the dealer has blackjack.") 
                            print(f"You lose your main bet, but earn {insurance_bet * 2} dollars from insurance.")
                            player_pot += (insurance_bet * 2)
                            break

        # Check to see if the player can split their cards?
        if ph[0].value == ph[1].value:
            split_option = True
        else:
            split_option = False
            
        # Check with player how they want to proceed in the game.
        if split_option == True:
            game_choice = input("What would you like to do? Split, Hit, Stand, or Double Down? ").lower()    
        else:
            game_choice = input("What would you llke to do? Hit, Stand, or Double Down? ").lower()
            
        while True:
            try:
                return game_time(game_choice, dh, ph, pd_deck)
            except:
                sys.exit("An Error Has Occurred")

def bet_validation(bet):
    global player_pot
    return True if 0 < bet <= player_pot else False

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
    response = input("Would you like even money (Y/N)? Instant payout of 1:1. ")
    return True if response == "Y" else False

def offer_insurance():
    response = input("Purchase insurance (Y/N)? Wager half of your game bet; payout is 2:1 ")
    return True if response == "Y" else False

def validate_insurance(bet):
    global player_pot
    global different_bet
    if different_bet != 0:
        if (different_bet/2) > player_pot:
            print("Sorry, you do not have enough funds to buy insurance. We will continue without it.")
            return False
        else:
            return True
    else:
        if (bet/2) > player_pot:
            print("Sorry, you do not have enough funds to buy insurance. We will continue without it.")
            return False
        else:
            return True

def offer_to_split():
    ...

def game_time(decision, dh, ph, deck):
    match decision:
        case "stand":
            print("Player has chosen to Stand.")
            time.sleep(1.5)
            print(f"Dealer's facedown: {dh[1]}")
            dh_sum = dh[0].value + dh[1].value
            print(f"Dealer has a sum of {dh_sum}")
            while True:
                if dh_sum > 17 and dh_sum <= 21:
                    print("No more cards will be drawn")
                    determine_winner()
                    break
                else:
                    i = 2   # index to use to sum new card.value
                    while dh_sum <= 17:
                        print("Dealer will draw another card")
                        dh.append(deck[0])
                        deck.pop(0)
                        print("Dealer's hand: ", end="")
                        for card in dh:
                            print(card, ", ", end="")
                        print()
                        dh_sum += dh[i].value
                        print(f"Dealer has a sum of {dh_sum}")
                        i += 1
                        if dh_sum > 21:
                            print("Dealer has bust")
                            determine_winner()
                            break
                        elif dh_sum == 21:
                            print("Dealer has blackjack")
                            determine_winner()
                            break
                        time.sleep(2)                
        
        case "hit":
            print("Player has chosen to Hit.")
            ph_sum = ph[0].value + ph[1].value
            dh_sum = dh[0].value + dh[1].value
            time.sleep(1.5)
            i_ph, i_dh = 2, 2   # indeces to help update ph_sum & dh_sum
            # First we ask the player how many times they want to hit
            while ph_sum < 21:
                print("Testing...")
                ph.append(deck[0])
                print("What the heck???")
                deck.pop(0)
                print("Your hand: ", end="")
                for card in ph:
                    print(card, ", ", end="")
                print()
                ph_sum += ph[i_ph].value
                print(f"sum of {ph_sum}")
                i_ph += 1
                if ph_sum > 21:
                    print("You have bust")
                    return "Dealer"         # The dealer wins this situation automatically
                elif ph_sum == 21:
                    print("You have blackjack")
                    player_blackjack = True
                else:
                    player_blackjack = False
                
                if player_blackjack:
                    break

                response = input("Would you like to Stand or Hit? ").lower().strip()
                if response == "stand":
                    break
                elif response == "hit":
                    time.sleep(2)
                    continue
            time.sleep(2)
            
            print()
            
            # Next we have the dealer draw cards
            while dh_sum <= 17:
                print("Dealer will now draw")
                time.sleep(1.5)
                dh.append(deck[0])
                deck.pop(0)
                print("Dealer's hand: ", end="")
                for card in dh:
                    print(card, ", ", end="")
                print()
                dh_sum += dh[i_dh].value
                print(f"Dealer has a sum of {dh_sum}")
                i_dh += 1
                if dh_sum > 21:
                    print("Dealer has bust")
                    return "Player"
                elif dh_sum == 21:
                    print("Dealer has blackjack")
                    dealer_blackjack = True
                else:
                    dealer_blackjack = False
                
                if dealer_blackjack:
                    break

                time.sleep(2)    
            
            return determine_winner(ph_sum, dh_sum)
        case "double down":
            print("Player has chosen to Double Down.")


        case "split":
            print("Player has chosen to Split")

def determine_winner(player_sum, dealer_sum):
    if player_sum > dealer_sum:
        return "Player"
    elif dealer_sum > player_sum:
        return "Dealer"
    else:
        return "Tie"
if __name__ == "__main__":
    main()