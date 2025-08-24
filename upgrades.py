# upgrades.py
# Version: 1.0.0
# Description: This file contains the Upgrades class, which is responsible for managing game upgrades.

class Upgrades:
    """
    The Upgrades class manages the purchasing of upgrades.
    """
    def __init__(self, game):
        """
        Initializes the Upgrades manager.

        Args:
            game: The main game object.
        """
        self.game = game
        self.dropper_upgrade_cost = 50
        self.conveyor_upgrade_cost = 50
        self.price_upgrade_cost = 100

    def upgrade_dropper(self):
        """
        Upgrades the dropper if the player has enough money.
        """
        if self.game.money >= self.dropper_upgrade_cost:
            self.game.money -= self.dropper_upgrade_cost
            self.game.dropper.upgrade_dropper(0.1)
            self.dropper_upgrade_cost *= 1.5 # Increase cost for next upgrade
            return True
        return False

    def upgrade_conveyor(self):
        """
        Upgrades the conveyor if the player has enough money.
        """
        if self.game.money >= self.conveyor_upgrade_cost:
            self.game.money -= self.conveyor_upgrade_cost
            self.game.conveyor_belt.upgrade_conveyor(0.5)
            self.conveyor_upgrade_cost *= 1.5 # Increase cost for next upgrade
            return True
        return False

    def upgrade_price(self):
        """
        Upgrades the object price if the player has enough money.
        """
        if self.game.money >= self.price_upgrade_cost:
            self.game.money -= self.price_upgrade_cost
            self.game.object_price += 5
            self.price_upgrade_cost *= 1.5 # Increase cost for next upgrade
            return True
        return False
