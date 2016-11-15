import curses;
screen = curses.initscr()
curses.noecho()
#curses.cbreak()
screen.keypad(1)

		#y    x
NONE  = ( 0,  0)
UP    = (-1,  0)
RIGHT = ( 0,  1)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)

GAME_OVER = "Game over. Press 'q' to quit"

(S_H, S_W) = screen.getmaxyx()

mapp = [""] * 20 
mapp.insert(0,  "                              ................................                \n")
mapp.insert(1,  "                              .                              .                \n")
mapp.insert(2,  " ========================     .     ======================   .                \n")
mapp.insert(3,  " |......................|     .     |.........................                \n")
mapp.insert(4,  " |......................|     .     |....................|                    \n")
mapp.insert(5,  " |......................|     .     |....................|                    \n")
mapp.insert(6,  " |......................|     .     |....................|                    \n")
mapp.insert(7,  " |.......................................................|                    \n")
mapp.insert(8,  " ========================           |....................|                    \n")
mapp.insert(9,  "                                    ===========.==========                    \n")
mapp.insert(10, "                                              ..                             \n")
mapp.insert(11, "                                              .       ==================     \n")
mapp.insert(12, "    ==================                        .       |................|     \n")
mapp.insert(13, "    |................|                        .       |................|     \n")
mapp.insert(14, "    |..........................................       |................|     \n")
mapp.insert(15, "    |................|                                |................|     \n")
mapp.insert(16, "    |................|                                ==.===============    \n")
mapp.insert(17, "    |................|                                  .                    \n")
mapp.insert(18, "    |....................................................                    \n")
mapp.insert(19, "    =================|                                                       \n")

class 	Object(object):
	def __init__(self, y, x):
		self.pos = [y, x]
		self.char = '$'

	def update_pos(self, direction):
		screen.addstr(self.pos[0], self.pos[1], '.')
		y = self.pos[0] + direction[0] 
		x = self.pos[1] + direction[1] 
		if x >= 0 and y >= 0 and mapp[y][x] == '.':
			self.pos[0] += direction[0]
			self.pos[1] += direction[1]
		self._draw()

	def _draw(self):
		y = self.pos[0]
		x = self.pos[1]
		screen.addstr(y, x, self.char)
		screen.move(0, 0)
		

class 	Monstr(object):
	def __init__(self):
		self.pos = [4, 40]
		self.char = '&'

	def update_pos(self, direction):
		screen.addstr(self.pos[0], self.pos[1], '.')
		y = self.pos[0] + direction[0] 
		x = self.pos[1] + direction[1] 
		if x >= 0 and y >= 0 and mapp[y][x] == '.':
			self.pos[0] += direction[0]
			self.pos[1] += direction[1]
		self._draw()

	def _draw(self):
		y = self.pos[0]
		x = self.pos[1]
		screen.addstr(y, x, self.char)
		screen.move(0, 0)
		

class 	Rogue(object):
	def __init__(self):
		self.char = '#'
		self.prev = ' '
		self.lives = 9
		self.wallet = 0
		self.pos = [3, 5]
		self.monstr = Monstr()
		self.obj = Object(14, 60)
		self.obj1 = Object(4, 10)
		self.obj2 = Object(15, 20)

	def update_map(self):
		y = -1
		screen.move(0, 0)
		for i in mapp:
			screen.addstr(i)
		screen.move(0, 0)

	def check_wallet(self):
		if self.pos[1] == self.obj.pos[1] and self.pos[0] == self.obj.pos[0]:
			self.wallet += 10
		if self.pos[1] == self.obj1.pos[1] and self.pos[0] == self.obj1.pos[0]:
			self.wallet += 10
		if self.pos[1] == self.obj2.pos[1] and self.pos[0] == self.obj2.pos[0]:
			self.wallet += 10

	def check_monstr(self):
		if self.pos[1] == self.monstr.pos[1] and self.pos[0] == self.monstr.pos[0]:
			self.lives -= 1
		if self.lives == 0:
			game = 0

	def update_pos(self, direction):
		screen.addstr(self.pos[0], self.pos[1], '.')
		y = self.pos[0] + direction[0] 
		x = self.pos[1] + direction[1] 
		if x >= 0 and y >= 0 and mapp[y][x] == '.':
			self.pos[0] += direction[0]
			self.pos[1] += direction[1]
		self.check_wallet()
		self.check_monstr()
		self._draw()

	def _draw(self):
		x = self.pos[1]
		y = self.pos[0]
		screen.addstr(y, x, self.char)
		screen.addstr(0, 1, 'Lives ' + str(self.lives))
		screen.addstr(1, 1, 'Wallet ' + str(self.wallet))
		screen.move(0, 0)

def game_over():
	win = screen.getmaxyx()
	screen.addstr(win[0]/2, win[1]/2, GAME_OVER)

def main():
	rogue = Rogue()
	rogue.update_map()
	rogue.update_pos(NONE)
	rogue.monstr.update_pos(NONE)
	rogue.obj.update_pos(NONE)
	rogue.obj1.update_pos(NONE)
	rogue.obj2.update_pos(NONE)
	while True:
		c = screen.getch()
		if c == ord('q'):
			break  # Exit the while()
		elif rogue.lives:
			if c == curses.KEY_UP:
				rogue.update_pos(UP)
			elif c == curses.KEY_DOWN:
				rogue.update_pos(DOWN)
			elif c == curses.KEY_LEFT:
				rogue.update_pos(LEFT)
			elif c == curses.KEY_RIGHT:
				rogue.update_pos(RIGHT)
			rogue.monstr.update_pos(NONE)
		elif rogue.lives == 0:
			game_over()

main()

curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
