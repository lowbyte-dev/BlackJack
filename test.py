import random
import os
from art import logo
from playsound3 import playsound

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw_cards(stack,count):
    card = decks_of_cards.pop()
    card_draw()
    if card in face_cards:
        count += 10
        stack.append(card)
    else:
        stack.append(card)
        count += card
    if count > 21:
        if 11 in stack:
            stack[stack.index(11)] = 1
            count -= 10
    return stack,count

def winning_sound():
    print("Music Loading, vibe on it wait a second to play again.")
    playsound("sounds/winning.wav")

def card_draw():
    playsound("sounds/card_draw.mp3")

def losing_sound():
    print("Music Loading, vibe on it wait a second to play again.")
    playsound("sounds/lose.wav")

def shuffling():
    playsound("sounds/shuffling.mp3")
    print("Wait for a second the cards are being shuffled by the player")

def tie_music():
    print("Music Loading, vibe on it wait a second to play again.")
    playsound("sounds/game_draw.wav")

balance = int(input("How much you want in your account balance? $"))

deck_choice = int(input("How many decks would you like '6' or '8'? "))
while deck_choice not in [6,8]:
    print("You chose an invalid option. Please choose between 6 and 8.")
    deck_choice = int(input("How many decks would you like '6' or '8'? "))
decks_of_cards = [11,2,3,4,5,6,7,8,9,10,"King","Queen","Jack"]*4*deck_choice

if deck_choice == 6:
    margin = 78
else:
    margin = 104

len_of_decks = len(decks_of_cards)
face_cards =["King","Queen","Jack"]

game_on = True

while game_on:
    random.shuffle(decks_of_cards)
    shuffling()

    player_cards = []
    dealer_cards = []
    player_count = 0
    dealer_count = 0

    choice = input("Do you want to play a game of blackjack? Type 'y' or 'n': ").strip().lower()
    if choice == "y":
        if balance <= 0:
            option = input("Your balance is insufficient to continue playing you must add money into the account,if you want to press 'y' or 'n' to apply.").lower()
            if option == "y":
                money = int(input("How much money would you like? $"))
                balance += money
            else:
                print("Thanks for playing this game")
                game_on = False
                break

        bet = int(input("How much do you want to bet? $"))
        if 0 < bet <= balance:
            balance -= bet
            print(f"Your current balance now is ${balance}")

            for i in range(2):
                player_cards,player_count = draw_cards(player_cards,player_count)
                dealer_cards,dealer_count = draw_cards(dealer_cards,dealer_count)

            clear()
            print(logo)
            print(f"    Your cards: {player_cards}, current score: {player_count}")
            print(f"    Dealer's first card: {[dealer_cards[0]]}")

            draw_on = True
            is_winning_player = True
            while player_count < 21 and draw_on == True:
                player_draw = input("Do you want to draw another card? Type 'y' or 'n': ").strip().lower()
                if player_draw == "y":
                    player_cards,player_count = draw_cards(player_cards,player_count)

                    if player_count > 21:
                        is_winning_player=False
                    if player_count == 21:
                        break

                    clear()
                    print(logo)
                    print(f"    Your cards: {player_cards}, current score: {player_count}")
                    print(f"    Dealer's first card: {[dealer_cards[0]]}")
                else:
                    draw_on = False
            if player_count < 21:
                while dealer_count <= 16:
                    dealer_cards,dealer_count = draw_cards(dealer_cards,dealer_count)


            print(f"Your final card: {player_cards}, final score: {player_count}")
            print(f"Dealer's final card: {dealer_cards} final score: {dealer_count}")

            if is_winning_player == False:
                print("You lose.")
                losing_sound()
            elif dealer_count > 21 and is_winning_player == True:
                print("You win.")
                balance += 2*bet
                winning_sound()
            elif player_count > dealer_count:
                print("You win")
                balance += 2 * bet
                winning_sound()
            elif dealer_count > player_count:
                print("You lose")
                losing_sound()
            else:
                print("Draw")
                tie_music()
                balance +=  bet
            print(f"Your current balance now is ${balance} after this game.")

            if len(decks_of_cards) < (len_of_decks - margin):
                print("The cards reached the limit of threshold to shuffle, reshuffling in progress here, choose the deck size again.")
                deck_choice = int(input("How many decks would you like '6' or '8'? "))
                decks_of_cards = [11,2,3,4,5,6,7,8,9,10,"King","Queen","Jack"]*4*deck_choice
                random.shuffle(decks_of_cards)
                shuffling()

        elif bet > balance:
            print("Bet is higher than balance try again with lower bid")
        else:
            print("Invalid bet this is not possible")
    else:
        game_on = False