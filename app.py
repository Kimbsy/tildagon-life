import app
import random

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

# Get the eight cells around a cell
def neighbours(x, y):
    return (
        (x-1, y-1),
        (x, y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1)
    )

def in_bounds(n):
    return n <= 48 and 0 <= n

class LifeApp(app.App):
    def __init__(self):
        super().__init__()
        self.button_states = Buttons(self)
        self.dialog = None
        self.step = 0
        print(self.setup_random())
        self.setup_glider_gun()

    def setup_random(self):
        # try and reduce the number of times we call into random, the badge struggles
        cell_count = 200
        cells = set()
        while len(cells) < cell_count:
            x_coords = random.choices(range(48), k=cell_count)
            y_coords = random.choices(range(48), k=cell_count)
            cells.update(zip(x_coords, y_coords))
        self.cells = cells

    def setup_glider_gun(self):
        # basic glider gun
        self.cells = {
            (1, 5), (1, 6), (2, 5), (2, 6), (35, 3), (35, 4), (36, 3), (36, 4),
            (14, 3), (13, 3), (12, 4), (11, 5), (11, 6), (11, 7), (12, 8), (13, 9), (14, 9),
            (15, 6), (16, 4), (17, 5), (17, 6), (17, 7), (18, 6), (16, 8),
            (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6),
            (25, 1), (25, 2), (25, 6), (25, 7)
        }

        # offset to see it better
        self.cells = {(x + 4, y + 13) for x, y in self.cells}

    def _reset(self):
        self.cells = set()

    def _exit(self):
        self._reset()
        self.button_states.clear()
        self.minimise()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.setup_random()
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.setup_glider_gun()
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            print("CANCEL")
            self.button_states.clear()
            self.game = ""
            self.minimise()

        self.step += delta
        if self.step > 0:
            self.step = 0
            new_cells = set()
            check_cells = set(self.cells)  # Cells to be checked
            for cell in self.cells:
                check_cells.update(neighbours(*cell))  # Add neighbors to the set
            for x, y in check_cells:
                total = sum((nx, ny) in self.cells for nx, ny in neighbours(x, y))
                if in_bounds(x) and in_bounds(y) and (total == 3 or (total == 2 and (x, y) in self.cells)):
                    new_cells.add((x, y))
            self.cells = new_cells

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()

        ctx.translate(-120, -120)
        ctx.rgb(0, 0, 0).rectangle(0, 0, 240, 240).fill()

        for x, y in self.cells:
            ctx.rgb(1, 1, 1).rectangle(x * 5, y * 5, 5, 5).fill()

        ctx.restore()

        if self.dialog:
            self.dialog.draw(ctx)

__app_export__ = LifeApp
