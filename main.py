"""
A Python program to simulate John Conway's Game of Life.
"""

from kivy.config import Config

WIDTH, HEIGHT = 1600, 900

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from threading import Thread
from time import sleep
from random import choice	

x, y = 10, 10
X, Y = WIDTH // x, HEIGHT // y
GEN_DELAY = 0.01
PATTERN = None  # 'gosper_glider_gun.txt'  # Pattern to load, set to None to generate a random pattern


class MainWindow(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.colors = [[0, 0, 0, 1], [1, 1, 1, 1]]
		self.grid = []
		
		for i in range(Y):
			self.grid.append([])
			for j in range(X):
				with self.canvas.before:
					self.grid[-1].append(Color(rgba=[0, 0, 0, 1]))
					Rectangle(size=(x, y), pos=(x*j, y*i))

		if PATTERN:
			with open(PATTERN) as file:
				grid = file.read().strip().split('\n')[::-1]
			grid = [list(map(int, row)) for row in grid]
			self.grid_ = grid
		else:
			self.grid_ = [[0 for _ in range(X+2)] for _ in range(Y+2)]
			temp = []
			for i in range(20, 50):
				for j in range(10, 40):
					temp.append([j, i])
			temps = [choice(temp) for _ in range(400)]
			for i, j in temps:
				self.grid_[i][j] = 1

		Thread(target=self.start_game).start()
	
	def start_game(self):
		while True:
			for i in range(1, Y+1):
				for j in range(1, X+1):
					self.grid[i-1][j-1].rgba = self.colors[self.grid_[i][j]]
			new_grid = [[0 for _ in range(X+2)] for _ in range(Y+2)]
			for i in range(1, Y+1):
				for j in range(1, X+1):
					temp = self.grid_[i-1][j-1:j+2] + self.grid_[i+1][j-1:j+2] + [self.grid_[i][j-1], self.grid_[i][j+1]]
					ones = temp.count(1)
					if self.grid_[i][j]:  # If alive
						if ones in [2, 3]:
							new_grid[i][j] = 1
					else:  # If dead
						if ones == 3:
							new_grid[i][j] = 1
			self.grid_ = new_grid
			sleep(GEN_DELAY)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

        self.add_widget(MainWindow(name='main'))


class Game_Of_Life(App):
    def build(self):
        self.manager = ScreenManagement()
        return self.manager


if __name__ == '__main__':
    Game_Of_Life().run()
