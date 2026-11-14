import random
import os
from art import logo
from playsound3 import playsound


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def deal_card(hand, total):
    drawn_card = shoe.pop()
    play_card_sound()
    if drawn_card in FACE_CARDS:
        total += 10
        hand.append(drawn_card)
    else:
        hand.append(drawn_card)
        total += drawn_card
    if total > 21:
        if 11 in hand:
            hand[hand.index(11)] = 1
            total -= 10
    return hand, total


def play_win_sound():
    print("🎵 Loading victory music... hang on a second before the next round! 🎵")
    playsound("sounds/winning.wav")


def play_card_sound():
    playsound("sounds/card_draw.wav")


def play_lose_sound():
    print("🎵 Loading sad trombone... hang on a second before the next round! 🎵")
    playsound("sounds/lose.wav")


def play_shuffle_sound():
    print("🔀 One moment, the dealer is shuffling the cards...")
    playsound("sounds/shuffling.mp3")



def play_tie_sound():
    print("🎵 Loading tie music... hang on a second before the next round! 🎵")
    playsound("sounds/game_draw.wav")


balance = int(input("💰 How much money would you like to start with? $"))

number_of_decks = int(input("🃏 How many decks would you like to play with, '6' or '8'? "))
while number_of_decks not in [6, 8]:
    print("❌ Invalid choice! Please choose either 6 or 8 decks.")
    number_of_decks = int(input("🃏 How many decks would you like to play with, '6' or '8'? "))
shoe = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, "King", "Queen", "Jack"] * 4 * number_of_decks

if number_of_decks == 6:
    reshuffle_threshold = 78
else:
    reshuffle_threshold = 104

total_cards_in_shoe = len(shoe)
FACE_CARDS = ["King", "Queen", "Jack"]

game_running = True

while game_running:
    random.shuffle(shoe)
    play_shuffle_sound()

    player_hand = []
    dealer_hand = []
    player_total = 0
    dealer_total = 0

    play_choice = input("🎰 Ready for a round of Blackjack? Type 'y' or 'n': ").strip().lower()
    if play_choice == "y":
        if balance <= 0:
            top_up_choice = input("😬 You're out of money! Add funds to keep playing? Type 'y' or 'n': ").lower()
            if top_up_choice == "y":
                top_up_amount = int(input("💵 How much would you like to add? $"))
                balance += top_up_amount
            else:
                print("👋 Thanks for playing! See you next time.")
                game_running = False
                break

        bet_amount = int(input("🪙 How much would you like to bet? $"))
        if 0 < bet_amount <= balance:
            balance -= bet_amount
            print(f"💼 Bet placed! Your balance is now ${balance:.2f}")

            for _ in range(2):
                player_hand, player_total = deal_card(player_hand, player_total)
                dealer_hand, dealer_total = deal_card(dealer_hand, dealer_total)

            clear_screen()
            print(logo)
            print(f"    🧑 Your hand: {player_hand}  |  Total: {player_total}")
            print(f"    🎩 Dealer's face-up card: {[dealer_hand[0]]}")

            player_has_blackjack = player_total == 21  # two cards totalling 21 right after the deal
            player_can_draw = True
            player_not_bust = True
            while player_total < 21 and player_can_draw == True:
                hit_choice = input("👉 Do you want to hit (draw another card)? Type 'y' or 'n': ").strip().lower()
                if hit_choice == "y":
                    player_hand, player_total = deal_card(player_hand, player_total)

                    if player_total > 21:
                        player_not_bust = False
                    if player_total == 21:
                        break

                    clear_screen()
                    print(logo)
                    print(f"    🧑 Your hand: {player_hand}  |  Total: {player_total}")
                    print(f"    🎩 Dealer's face-up card: {[dealer_hand[0]]}")
                else:
                    player_can_draw = False
            if player_total < 21:
                while dealer_total <= 16:
                    dealer_hand, dealer_total = deal_card(dealer_hand, dealer_total)

            print("\n=========== 🏁 FINAL RESULT 🏁 ===========")
            print(f"🧑 Your final hand: {player_hand}  |  Final total: {player_total}")
            print(f"🎩 Dealer's final hand: {dealer_hand}  |  Final total: {dealer_total}")

            if player_not_bust == False:
                print("💥 BUST! You went over 21. You lose. 😢")
                play_lose_sound()
            elif player_has_blackjack and dealer_total == 21:
                print("🤝 Both you and the dealer have Blackjack! It's a draw, your bet is returned.")
                play_tie_sound()
                balance += bet_amount
            elif player_has_blackjack:
                print("🃏🔥 BLACKJACK! Paid 3:2! 🏆")
                balance += bet_amount * 2.5  # bet back + 1.5x winnings
                play_win_sound()
            elif dealer_total > 21 and player_not_bust == True:
                print("🎉 The dealer busted! You win! 🏆")
                balance += 2 * bet_amount
                play_win_sound()
            elif player_total > dealer_total:
                print("🎉 You beat the dealer! You win! 🏆")
                balance += 2 * bet_amount
                play_win_sound()
            elif dealer_total > player_total:
                print("😢 The dealer wins this round. You lose.")
                play_lose_sound()
            else:
                print("🤝 It's a draw! Your bet is returned.")
                play_tie_sound()
                balance += bet_amount
            print(f"💰 Your balance after this round: ${balance:.2f}")

            if len(shoe) < (total_cards_in_shoe - reshuffle_threshold):
                print("🔄 The shoe is running low, time to reshuffle! Please choose the deck size again.")
                number_of_decks = int(input("🃏 How many decks would you like to play with, '6' or '8'? "))
                shoe = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, "King", "Queen", "Jack"] * 4 * number_of_decks
                random.shuffle(shoe)
                play_shuffle_sound()

        elif bet_amount > balance:
            print("🚫 That bet is more than your balance. Try a smaller amount.")
        else:
            print("❌ Invalid bet! Please enter an amount greater than $0.")
    else:
        print("👋 Thanks for playing! See you next time.")
        game_running = False