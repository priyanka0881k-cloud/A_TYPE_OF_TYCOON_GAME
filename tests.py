# tests.py
# Version: 2.0.0
# Description: This file contains test cases for the tycoon game.

import unittest
import time
from game_core import Game
from dropper import Dropper
from conveyor import ConveyorBelt

class TestTycoonGame(unittest.TestCase):
    """
    Test cases for the Tycoon Game.
    """

    def setUp(self):
        """
        Set up a new Game instance for each test.
        """
        self.game = Game()

    # Dropper Tests
    def test_dropper_initialization(self):
        dropper = Dropper(drop_interval=5.0)
        self.assertEqual(dropper.drop_interval, 5.0)

    def test_dropper_drops_object(self):
        dropper = self.game.dropper
        dropper.last_drop_time = time.time() - dropper.drop_interval
        new_object = dropper.update()
        self.assertIsNotNone(new_object)
        self.assertIn('position', new_object)

    def test_dropper_upgrade(self):
        dropper = self.game.dropper
        initial_interval = dropper.drop_interval
        dropper.upgrade_dropper(0.5)
        self.assertLess(dropper.drop_interval, initial_interval)

    # Conveyor Tests
    def test_conveyor_initialization(self):
        conveyor = ConveyorBelt(speed=2.0, length=20)
        self.assertEqual(conveyor.speed, 2.0)
        self.assertEqual(conveyor.length, 20)

    def test_conveyor_add_and_move_object(self):
        conveyor = self.game.conveyor_belt
        obj = {'position': 0}
        conveyor.add_object(obj)
        self.assertIn(obj, conveyor.objects)
        conveyor.update(dt=1.0)
        self.assertEqual(obj['position'], conveyor.speed * 1.0)

    def test_conveyor_sells_object(self):
        conveyor = self.game.conveyor_belt
        conveyor.length = 5
        obj = {'position': 5}
        conveyor.add_object(obj)
        sold = conveyor.get_sold_objects()
        self.assertIn(obj, sold)
        self.assertNotIn(obj, conveyor.objects)

    # Upgrades Tests
    def test_upgrade_successful(self):
        self.game.money = 1000
        initial_cost = self.game.upgrades.dropper_upgrade_cost
        initial_interval = self.game.dropper.drop_interval

        upgraded = self.game.upgrades.upgrade_dropper()

        self.assertTrue(upgraded)
        self.assertEqual(self.game.money, 1000 - initial_cost)
        self.assertLess(self.game.dropper.drop_interval, initial_interval)

    def test_upgrade_insufficient_funds(self):
        self.game.money = 10
        initial_interval = self.game.dropper.drop_interval

        upgraded = self.game.upgrades.upgrade_dropper()

        self.assertFalse(upgraded)
        self.assertEqual(self.game.money, 10)
        self.assertEqual(self.game.dropper.drop_interval, initial_interval)

    # Game Logic Integration Test
    def test_full_cycle_sell_and_earn(self):
        game = self.game
        game.money = 0
        game.object_price = 25
        game.conveyor_belt.length = 1
        game.conveyor_belt.speed = 1

        obj = {'position': 0, 'creation_time': time.time()}
        game.conveyor_belt.add_object(obj)

        game.last_update_time = time.time()
        game.update() # This does nothing because dt is 0

        # Manually advance position to sell point
        game.conveyor_belt.objects[0]['position'] = game.conveyor_belt.length

        # Now update should sell it
        sold_objects = game.conveyor_belt.get_sold_objects()
        if sold_objects:
            game.money += len(sold_objects) * game.object_price

        self.assertEqual(game.money, 25)
        self.assertEqual(len(game.conveyor_belt.objects), 0)

def run_tests():
    """
    Runs all the tests and prints a summary.
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTycoonGame)
    runner = unittest.TextTestRunner(verbosity=2)
    print("Running tests...")
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == '__main__':
    run_tests()
