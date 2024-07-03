# The Engine of the game
# it manages the main loop and calls all subclasses

import os
import time
import numpy as np
import platform

class Engine:
    def __init__(self):
        self.display = np.zeros((20, 60), dtype=np.int8)
        self.fps = 20
        self.platform = platform.system()

        self.symbols = {
            -1: '▒', 
            0 : ' ', 
            1 : '█'}

        # border
        self.display[0, :] = -1
        self.display[-1, :] = -1
        self.display[:, 0] = -1
        self.display[:, -1] = -1

    def clear(self):
        if self.platform == "Windows":
            os.system('cls')
        else:
            os.system('clear')

        self.display[1:-1, 1:-1] = 0

    def draw(self):
        if not all([i in self.symbols.keys() for i in np.unique(self.display)]):
            print("Warning: display have values other than 0, 1, -1")

        str_array = np.full(self.display.shape, ' ')
        for k, v in self.symbols.items():
            str_array = np.where(self.display == k, v, str_array)

        lines = [''.join(row) for row in str_array]
        print('\n'.join(lines))

    def update(self) -> bool:
        print("update function not implemented")
        return True
    
    def loop(self):
        while True:
            self.clear()                # reset display
            if self.update(): break     # update game state
            self.draw()                 # draw game state
            time.sleep(1 / self.fps)    # delay

