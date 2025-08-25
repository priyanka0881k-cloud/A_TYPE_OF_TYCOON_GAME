# main.py
# Version: 2.0.0
# Description: This is the main entry point for the tycoon game with a GUI.

import tkinter as tk
from tkinter import messagebox
from game_core import Game


class TycoonGUI:
    """
    The main class for the Tycoon Game GUI.
    """
    def __init__(self, root):
        """
        Initializes the GUI.

        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("Tycoon Game")
        self.game = Game()

        self._init_ui_variables()
        self._create_widgets()

        # Start the game loop
        self.update_game()

    def _init_ui_variables(self):
        """Initializes tkinter StringVars."""
        self.money_var = tk.StringVar()
        self.dropper_stats_var = tk.StringVar()
        self.conveyor_stats_var = tk.StringVar()
        self.price_stats_var = tk.StringVar()

    def _create_widgets(self):
        """Creates and lays out the GUI widgets."""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()

        # Stats Frame
        stats_frame = tk.LabelFrame(main_frame, text="Factory Stats")
        stats_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self._create_stats_widgets(stats_frame)

        # Conveyor Canvas
        self.canvas_width = 400
        self.canvas_height = 100
        self.canvas = tk.Canvas(
            main_frame, width=self.canvas_width, height=self.canvas_height, bg="#cccccc"
        )
        self.canvas.grid(row=1, column=0, pady=10)
        self.canvas.create_line(
            0, self.canvas_height / 2, self.canvas_width, self.canvas_height / 2,
            width=20, fill="#666666"
        )
        self.canvas.create_rectangle(
            self.canvas_width - 20, self.canvas_height / 2 - 20,
            self.canvas_width, self.canvas_height / 2 + 20,
            fill="gold", outline="black"
        )

        # Upgrades Frame
        upgrades_frame = tk.LabelFrame(main_frame, text="Upgrades")
        upgrades_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self._create_upgrade_widgets(upgrades_frame)

    def _create_stats_widgets(self, parent_frame):
        """Creates the widgets for the stats frame."""
        tk.Label(parent_frame, text="Money:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        tk.Label(parent_frame, textvariable=self.money_var).grid(row=0, column=1, padx=5, pady=2, sticky="w")

        tk.Label(parent_frame, text="Dropper:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        tk.Label(parent_frame, textvariable=self.dropper_stats_var).grid(row=1, column=1, padx=5, pady=2, sticky="w")

        tk.Label(parent_frame, text="Conveyor:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        tk.Label(parent_frame, textvariable=self.conveyor_stats_var).grid(row=2, column=1, padx=5, pady=2, sticky="w")

        tk.Label(parent_frame, text="Object Price:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        tk.Label(parent_frame, textvariable=self.price_stats_var).grid(row=3, column=1, padx=5, pady=2, sticky="w")

    def _create_upgrade_widgets(self, parent_frame):
        """Creates the widgets for the upgrades frame."""
        self.dropper_button = tk.Button(parent_frame, command=self.purchase_dropper_upgrade)
        self.dropper_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.conveyor_button = tk.Button(parent_frame, command=self.purchase_conveyor_upgrade)
        self.conveyor_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.price_button = tk.Button(parent_frame, command=self.purchase_price_upgrade)
        self.price_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_columnconfigure(2, weight=1)

    def update_game(self):
        """The main game loop, driven by tkinter's after method."""
        self.game.update()
        self.update_gui_elements()
        self.root.after(50, self.update_game)

    def update_gui_elements(self):
        """Updates all GUI elements with the latest game state."""
        self.money_var.set(f"${self.game.money:.2f}")
        self.dropper_stats_var.set(f"Interval: {self.game.dropper.drop_interval:.2f}s")
        self.conveyor_stats_var.set(f"Speed: {self.game.conveyor_belt.speed:.2f}")
        self.price_stats_var.set(f"Price: ${self.game.object_price:.2f}")

        dropper_cost = self.game.upgrades.dropper_upgrade_cost
        conveyor_cost = self.game.upgrades.conveyor_upgrade_cost
        price_cost = self.game.upgrades.price_upgrade_cost

        self.dropper_button.config(text=f"Upgrade Dropper (${dropper_cost:.2f})")
        self.conveyor_button.config(text=f"Upgrade Conveyor (${conveyor_cost:.2f})")
        self.price_button.config(text=f"Upgrade Price (${price_cost:.2f})")

        self.draw_conveyor_objects()

    def draw_conveyor_objects(self):
        """Clears and redraws the objects on the conveyor belt canvas."""
        self.canvas.delete("item")
        belt_y = self.canvas_height / 2
        object_radius = 5

        for obj in self.game.conveyor_belt.objects:
            x_pos = (obj['position'] / self.game.conveyor_belt.length) * self.canvas_width
            if x_pos < self.canvas_width:
                self.canvas.create_oval(
                    x_pos - object_radius, belt_y - object_radius,
                    x_pos + object_radius, belt_y + object_radius,
                    fill="blue", tags="item"
                )

    def purchase_dropper_upgrade(self):
        if not self.game.upgrades.upgrade_dropper():
            messagebox.showwarning("Upgrade Failed", "Not enough money to upgrade the dropper!")

    def purchase_conveyor_upgrade(self):
        if not self.game.upgrades.upgrade_conveyor():
            messagebox.showwarning("Upgrade Failed", "Not enough money to upgrade the conveyor!")

    def purchase_price_upgrade(self):
        if not self.game.upgrades.upgrade_price():
            messagebox.showwarning("Upgrade Failed", "Not enough money to upgrade the price!")


def main():
    """
    The main function to run the game.
    """
    root = tk.Tk()
    app = TycoonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
