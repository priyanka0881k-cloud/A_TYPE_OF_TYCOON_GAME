# main.py
# Version: 1.0.0
# Description: This is the main entry point for the tycoon game.

from game_core import Game
import time

def main():
    """
    The main function to run the game.
    """
    game = Game()

    print("Starting Tycoon Game...")
    time.sleep(1)

    while game.running:
        game.update()
        game.render()

        choice = input("Enter command (1-3 to upgrade, 'q' to quit): ").strip().lower()

        if choice == '1':
            if not game.upgrades.upgrade_dropper():
                print("Not enough money to upgrade the dropper!")
                time.sleep(1)
        elif choice == '2':
            if not game.upgrades.upgrade_conveyor():
                print("Not enough money to upgrade the conveyor!")
                time.sleep(1)
        elif choice == '3':
            if not game.upgrades.upgrade_price():
                print("Not enough money to upgrade the price!")
                time.sleep(1)
        elif choice == 'q':
            game.stop()
            print("Thanks for playing!")
        else:
            print("Invalid command. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
