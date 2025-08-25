# conveyor.py
# Version: 1.0.0
# Description: This file contains the ConveyorBelt class, which is responsible for moving objects in the game.

class ConveyorBelt:
    """
    The ConveyorBelt class is responsible for moving objects along a belt.
    """
    def __init__(self, speed=1.0, length=10):
        """
        Initializes the ConveyorBelt.

        Args:
            speed (float): The speed at which the belt moves objects.
            length (int): The length of the conveyor belt.
        """
        self.speed = speed
        self.length = length
        self.objects = []

    def add_object(self, obj):
        """
        Adds a new object to the conveyor belt.

        Args:
            obj: The object to add.
        """
        self.objects.append(obj)

    def update(self, dt):
        """
        Updates the position of all objects on the belt.

        Args:
            dt (float): The time delta since the last update.
        """
        for obj in self.objects:
            obj['position'] += self.speed * dt

    def get_sold_objects(self):
        """
        Checks for objects that have reached the end of the belt and returns them.
        Removes the sold objects from the belt.

        Returns:
            A list of objects that have been sold.
        """
        sold_objects = [obj for obj in self.objects if obj['position'] >= self.length]
        self.objects = [obj for obj in self.objects if obj['position'] < self.length]
        return sold_objects

    def upgrade_conveyor(self, amount):
        """
        Upgrades the conveyor to increase its speed.

        Args:
            amount (float): The amount to increase the speed by.
        """
        self.speed += amount
