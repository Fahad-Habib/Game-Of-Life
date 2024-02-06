"""
A Python program to simulate John Conway's Game of Life.
"""

from kivy.config import Config

WIDTH, HEIGHT = 1600, 950

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
X, Y = WIDTH // x, (HEIGHT-50) // y
GEN_DELAY = 0.01
PATTERN = 'gosper_glider_gun.txt'  # Initial pattern to load, set to None to generate a random pattern


class MainWindow(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.colors = [[0, 0, 0, 1], [1, 1, 1, 1]]
		self.grid = []
		self.grid_mask = [[0 for _ in range(X+2)] for _ in range(Y+2)]
		self.current_gen = 0
		self.label = Label(text="Current Generation: 0", font_size=30, size=(20, 20), pos=(790, 915), size_hint=(None, None))		
		self.add_widget(self.label)

		self.create_grid()
		self.apply_initial_mask()
		
		Thread(target=self.start_game).start()
	
	def create_grid(self):
		for i in range(Y):
			self.grid.append([])
			for j in range(X):
				with self.canvas.before:
					self.grid[-1].append(Color(rgba=[0, 0, 0, 1]))
					Rectangle(size=(x, y), pos=(x*j, y*i))
	
	def apply_initial_mask(self):
		if PATTERN:
			with open(PATTERN) as file:
				grid = file.read().strip().split('\n')[::-1]
			grid = [list(map(int, row)) for row in grid]
			self.grid_mask = grid
		else:
			temp = []
			for i in range(20, 50):
				for j in range(10, 40):
					temp.append([j, i])
			temps = [choice(temp) for _ in range(400)]
			for i, j in temps:
				self.grid_mask[i][j] = 1
	
	def start_game(self):
		while True:
			for i in range(1, Y+1):
				for j in range(1, X+1):
					self.grid[i-1][j-1].rgba = self.colors[self.grid_mask[i][j]]
			new_mask = [[0 for _ in range(X+2)] for _ in range(Y+2)]
			for i in range(1, Y+1):
				for j in range(1, X+1):
					temp = self.grid_mask[i-1][j-1:j+2] + self.grid_mask[i+1][j-1:j+2] + [self.grid_mask[i][j-1], self.grid_mask[i][j+1]]
					ones = temp.count(1)
					if self.grid_mask[i][j]:  # If alive
						if ones in [2, 3]:
							new_mask[i][j] = 1
					else:  # If dead
						if ones == 3:
							new_mask[i][j] = 1
			self.grid_mask = new_mask
			self.current_gen += 1
			self.label.text = f"Current Generation: {self.current_gen}"
			sleep(GEN_DELAY)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

        self.add_widget(MainWindow(name='main'))


class Game_Of_Life(App):
	def build(self):
		Window.clearcolor = (0.5, 0.5, 0.5, 1)
		self.manager = ScreenManagement()
		return self.manager


if __name__ == '__main__':
    Game_Of_Life().run()
