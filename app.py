import app
import asyncio
import random

from app_components import YesNoDialog, clear_background
from events.input import Buttons, BUTTON_TYPES

# Get the eight cells around a cell
def neighbours(x, y):
    return [[x-1, y-1],
            [x, y-1],
            [x+1, y-1],
            [x-1, y],
            [x+1, y],
            [x-1, y+1],
            [x, y+1],
            [x+1, y+1]]

class LifeApp(app.App):
    def __init__(self):
        # Need to call to access overlays
        super().__init__()
        # non-app stuff
        self.dialog = None

        self.step = 0

        # Set up app state ...
        # board is 240px^2, 5px cell size, so 48x48 grid
        self.setup_glider_gun();

    def setup_glider_gun(self):
        self.cells = [
            # left square
            [1, 5],
            [1, 6],
            [2, 5],
            [2, 6],
            # right square
            [35, 3],
            [35, 4],
            [36, 3],
            [36, 4],

            # left C
            [14, 3],
            [13, 3],
            [12, 4],
            [11, 5],
            [11, 6],
            [11, 7],
            [12, 8],
            [13, 9],
            [14, 9],

            # left dot+ arrow
            [15, 6], # dot
            [16, 4],
            [17, 5],
            [17, 6],
            [17, 7],
            [18, 6], # tip
            [16, 8],

            # right shapes
            [21, 3],
            [21, 4],
            [21, 5],
            [22, 3],
            [22, 4],
            [22, 5],
            [23, 2],
            [23, 6],
            # right top dash
            [25, 1],
            [25, 2],
            # right bottom dash
            [25, 6],
            [25, 7]]

        # offset to better view
        for i in range(len(self.cells)):
            self.cells[i][0] += 4
            self.cells[i][1] += 13


    def _reset(self):
        # set everything back to start ...
        self.cells = []

    def _exit(self):
        self._reset()
        # self.button_states.clear()
        self.minimise()

    def update(self, delta):
        self.step = self.step + delta
        # @NOTE: running as fast as possible, can use delta to target a max framerate
        if self.step > 0:
            self.step = 0
            new_cells = []
            # print(self.cells)
            for x, y in ([x, y] for x in range(48) for y in range(48)):
                # if [x, y] in self.cells: print("CHECKING", [x, y])
                total = 0
                for n in neighbours(x, y):
                    if n in self.cells:
                        # if [x, y] in self.cells: print(n)
                        total += 1
                if total in [2, 3] and [x, y] in self.cells:
                    # print(x, y, neighbours(x, y))
                    new_cells.append([x, y])
                elif total == 3 and [x, y] not in self.cells:
                    new_cells.append([x, y])
            self.cells = new_cells


    # @NOTE assuming ctx is some graphics context for now?
    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()

        # draw game board
        ctx.translate(-120,-120)
        ctx.rgb(0, 0, 0).rectangle(0, 0, 240, 240).fill()

        # draw living cells
        for x, y in self.cells:
            ctx.rgb(1, 1, 1).rectangle(x*5, y*5, 5, 5).fill()

        ctx.restore()

        if self.dialog:
            self.dialog.draw(ctx)

__app_export__ = LifeApp
