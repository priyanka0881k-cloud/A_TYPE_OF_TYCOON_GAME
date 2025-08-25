# dropper.py
# Version: 1.0.0
# Description: This file contains the Dropper class, which is responsible for creating objects in the game.

import time

class Dropper:
    """
    The Dropper class is responsible for creating objects at a set interval.
    """
    def __init__(self, drop_interval=2.0):
        """
        Initializes the Dropper.

        Args:
            drop_interval (float): The time in seconds between drops.
        """
        self.drop_interval = drop_interval
        self.last_drop_time = time.time()

    def update(self):
        """
        Checks if it's time to drop a new object.

        Returns:
            A new object if it's time to drop, otherwise None.
        """
        current_time = time.time()
        if current_time - self.last_drop_time >= self.drop_interval:
            self.last_drop_time = current_time
            return self.drop_object()
        return None

    def drop_object(self):
        """
        Creates a new game object.
        For now, an object is represented as a simple dictionary.
        """
        return {'position': 0, 'creation_time': time.time()}

    def upgrade_dropper(self, amount):
        """
        Upgrades the dropper to decrease the drop interval.

        Args:
            amount (float): The amount to decrease the drop interval by.
        """
        self.drop_interval -= amount
        if self.drop_interval < 0.1: # Prevent interval from being too low
            self.drop_interval = 0.1
