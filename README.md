🃏 Blackjack in Python

A terminal-style Blackjack game with sounds, emojis, a 6 or 8 deck shoe and a real 3:2 payout on natural blackjacks. It runs in your terminal, and it also runs right in your browser.

🎮 Play it now
👉 Click here to play: lowbyte-dev.github.io/BlackJack 👈

No install, no sign-up. Open the link, wait a few seconds for Python to load, then press the Run button.

Want your own copy? Hit the Fork button at the top right of this repo, or see Run it on your own device below. 🍴

🙋 Who made what
✍️ I wrote the game. main.py is my own Python script: all the game logic, rules, text and emojis.
🤖 I used AI for the web part. The index.html page and the linker script webrunner.py (which lets my Python script run inside the browser) were made with AI. I did not write those two files.

The game script is exactly the one you can run in a normal terminal. The web files only act as a bridge around it.

📜 How the game works
🏁 Getting started
💰 Enter how much money you want to start with.
🃏 Choose 6 or 8 decks.
🎰 Type y to play a round, or n to quit.
🪙 Place your bet. It can't be more than your balance.
🎴 Card values
Card	Value
2 to 10	Face value
Jack, Queen, King	10
Ace	11, or automatically 1 if 11 would push you over 21
🧑 Your turn
You and the dealer each get 2 cards. You see both of yours and only the dealer's first card.
Type y to hit (draw another card) or n to stand (keep your total).
Go over 21 and you bust 💥. You lose your bet straight away.
If you reach exactly 21, your turn ends automatically.
🎩 Dealer's turn
The dealer draws until they have 17 or more.
If you reach 21, the dealer does not draw extra cards.
If the dealer goes over 21, you win. 🎉
💵 Payouts
Result	What happens
🏆 You beat the dealer, or the dealer busts	Win 1:1. You get your bet back plus the same amount.
🃏🔥 Blackjack (Ace + a 10-value card as your first two cards)	Win 3:2. A $10 bet returns $25.
🤝 Same total as the dealer	Draw. Your bet is returned.
🤝 You and the dealer both have Blackjack	Draw. Your bet is returned.
😢 Dealer has the higher total	You lose your bet.
💥 You bust	You lose your bet.
🔄 The shoe

Cards are dealt from a shoe of 6 or 8 decks. Once about 78 cards (6 decks) or 104 cards (8 decks) have been used, the game tells you the shoe is low and asks you to choose the deck size again. The new shoe is shuffled.

😬 Running out of money

If your balance hits $0, the game offers to add more funds so you can keep playing.

🚫 Not in this version

Splitting, doubling down, insurance and surrender are not included. It's a simple, classic hit-or-stand game.

🎵 Sounds

The game plays sound effects for shuffling, dealing a card, winning, losing and drawing. The game waits for each sound to finish before moving on, just like in the terminal. If a sound file is missing, the game still works.

Put these files in the sounds/ folder:

File	Used for
shuffling.mp3	Shuffling the shoe
card_draw.wav	Every card dealt
winning.wav	Winning a round
lose.wav	Losing a round
game_draw.wav	A draw
💻 Run it on your own device
Option 1: Play in the terminal 🖥️

You need Python 3 installed.

bash
git clone https://github.com/lowbyte-dev/BlackJack.git
cd BlackJack
pip install playsound3
python main.py

main.py needs art.py (the logo) and the sounds/ folder next to it. Both are already in this repo.

Option 2: Fork it and host your own website 🍴
Click Fork at the top right of this page.
In your fork, go to Settings > Pages.
Set Source to Deploy from a branch, choose main and / (root), then click Save.
After a minute or two, your copy is live at https://YOUR-USERNAME.github.io/BlackJack/.
Option 3: Run the web version locally 🌐
bash
git clone https://github.com/lowbyte-dev/BlackJack.git
cd BlackJack
python -m http.server

Then open http://localhost:8000 in your browser. Opening index.html by double-clicking won't work, because the browser blocks loading main.py that way.

📁 What's in this repo
File or folder	What it is
main.py	🎲 The game itself (my code)
art.py	🖼️ The ASCII logo
sounds/	🔊 Sound effects
index.html	🌐 The web page with the console and Run button (made with AI)
webrunner.py	🔗 Linker that lets main.py run in the browser (made with AI)
🔧 How the web version works

The page uses Pyodide, which is Python compiled to run inside a browser. When you press Run, the page loads main.py and hands it to webrunner.py. That helper makes three things behave like they do in a terminal: input() waits for you to type in the page, playsound() plays through the browser and waits until the sound ends, and clearing the screen clears the page's console. The game file itself is never changed.

🧰 Built with

Python 3 · playsound3 · Pyodide · GitHub Pages

Enjoy the game, and good luck at the table! 🍀🃏
