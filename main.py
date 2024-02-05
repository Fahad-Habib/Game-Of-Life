"""
A Python program to simulate John Conway's Game of Life.
"""

from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from threading import Thread
from time import sleep

x, y = 16, 16
X, Y = 1280 // x, 720 // y
GEN_DELAY = 0.01
PATTERN = 'gosper_glider_gun.txt'  # Pattern to load, set to None to generate a random pattern


class GridEntry(Label):
	def __init__(self, bg_color=[0, 0, 0, 255], **kwargs):
		super().__init__(**kwargs)
		
		self.size = (x, y)
		self.size_hint = (None, None)

		with self.canvas.before:
			self.background_color = Color(rgba=[i/255 for i in bg_color])
			self.background = Rectangle(size=self.size)
	
	@property
	def dimensions(self):
		return self.size

	@property
	def position(self):
		return self.pos
	
	@dimensions.setter
	def dimensions(self, value):
		self.size = value
		self.background.size = value
	
	@position.setter
	def position(self, value):
		self.pos = value
		self.background.pos = value


class MainWindow(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.colors = [[0, 0, 0, 1], [1, 1, 1, 1]]
		self.grid = [[GridEntry() for _ in range(X)] for _ in range(Y)]
		
		for i, row in enumerate(self.grid):
			for j, entry in enumerate(row):
				entry.position = (x*j, y*i)
				self.add_widget(entry)
		
		if PATTERN:
			with open(PATTERN) as file:
				grid = file.read().strip().split('\n')[::-1]
			grid = [list(map(int, row)) for row in grid]
			self.grid_ = grid
		else:
			self.grid_ = [[0 for _ in range(X+2)] for _ in range(Y+2)]
			temp = []
			for i in range(20, 60):
				for j in range(10, 30):
					temp.append([j, i])
			temps = [choice(temp) for _ in range(200)]
			for i, j in temps:
				self.grid_[i][j] = 1

		Thread(target=self.start_game).start()
	
	def start_game(self):
		while True:
			for i in range(1, Y+1):
				for j in range(1, X+1):
					self.grid[i-1][j-1].background_color.rgba = self.colors[self.grid_[i][j]]
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
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        self.manager = ScreenManagement()
        return self.manager


if __name__ == '__main__':
    Game_Of_Life().run()
