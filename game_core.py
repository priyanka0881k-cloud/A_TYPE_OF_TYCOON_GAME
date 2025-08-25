# game_core.py
# Version: 2.0.0
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

        Returns:
            bool: True if a new object was dropped, False otherwise.
        """
        drop_happened = False
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update dropper
        new_object = self.dropper.update()
        if new_object:
            self.conveyor_belt.add_object(new_object)
            drop_happened = True

        # Update conveyor belt
        self.conveyor_belt.update(dt)

        # Check for sold objects
        sold_objects = self.conveyor_belt.get_sold_objects()
        if sold_objects:
            self.money += len(sold_objects) * self.object_price

        return drop_happened

    def stop(self):
        """
        Stops the game.
        """
        self.running = False
