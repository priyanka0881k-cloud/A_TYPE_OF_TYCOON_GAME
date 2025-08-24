# game_core.py
# Version: 1.0.0
# Description: This file contains the Game class, which is the core of the game logic.

import time
from dropper import Dropper
from conveyor import ConveyorBelt
from upgrades import Upgrades

class Game:
    """
    The main Game class.
    """
    def __init__(self):
        """
        Initializes the game.
        """
        self.money = 100.0
        self.object_price = 10.0
        self.dropper = Dropper()
        self.conveyor_belt = ConveyorBelt()
        self.upgrades = Upgrades(self)
        self.running = True
        self.last_update_time = time.time()

    def update(self):
        """
        Updates the game state.
        """
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update dropper
        new_object = self.dropper.update()
        if new_object:
            self.conveyor_belt.add_object(new_object)

        # Update conveyor belt
        self.conveyor_belt.update(dt)

        # Check for sold objects
        sold_objects = self.conveyor_belt.get_sold_objects()
        if sold_objects:
            self.money += len(sold_objects) * self.object_price

    def stop(self):
        """
        Stops the game.
        """
        self.running = False

    def render(self):
        """
        Renders the game state to the console.
        This will be called from main.py, but is here for completeness.
        """
        # A simple way to clear the screen
        print("\n" * 30)
        print("=" * 30)
        print("      TYCOON GAME")
        print("=" * 30)
        print(f"Money: ${self.money:.2f}")
        print("-" * 30)
        print("Stats:")
        print(f"  Drop Speed: {1/self.dropper.drop_interval:.2f}/s (Interval: {self.dropper.drop_interval:.2f}s)")
        print(f"  Conveyor Speed: {self.conveyor_belt.speed:.2f}")
        print(f"  Object Price: ${self.object_price:.2f}")
        print("-" * 30)
        print("Upgrades:")
        print(f"  1. Upgrade Dropper (Cost: ${self.upgrades.dropper_upgrade_cost:.2f})")
        print(f"  2. Upgrade Conveyor (Cost: ${self.upgrades.conveyor_upgrade_cost:.2f})")
        print(f"  3. Upgrade Price (Cost: ${self.upgrades.price_upgrade_cost:.2f})")
        print("-" * 30)
        print("Objects on belt:", len(self.conveyor_belt.objects))

        belt_viz = ['.'] * self.conveyor_belt.length
        for obj in self.conveyor_belt.objects:
            pos = int(obj['position'])
            if 0 <= pos < self.conveyor_belt.length:
                belt_viz[pos] = 'O'
        print("Belt: [", ''.join(belt_viz), "]--> $")
        print("=" * 30)
