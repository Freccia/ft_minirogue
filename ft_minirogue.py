import curses;
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(1)

game = 1

		#y    x
NONE  = ( 0,  0)
UP    = (-1,  0)
RIGHT = ( 0,  1)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)

GAME_OVER = "Game over. Press 'q' to quit"

(S_H, S_W) = screen.getmaxyx()


class 	Rogue(object):
	def __init__(self):
		self.char = '#'
		self.prev = ' '
		self.pos = [0, 0]
		self.mapp = [""] * 12
		self.mapp.insert(0, "                                                                 \n")
		self.mapp.insert(1, "                                                                 \n")
		self.mapp.insert(2, " ========================           ======================       \n")
		self.mapp.insert(3, " |                      |           |                    |       \n")
		self.mapp.insert(4, " |                      |           |         &          |       \n")
		self.mapp.insert(5, " |                      |           |                    |       \n")
		self.mapp.insert(6, " |                      |           |                    |       \n")
		self.mapp.insert(7, " |                      +++++++++++++                    |       \n")
		self.mapp.insert(8, " ========================           |                    |       \n")
		self.mapp.insert(9, "                                    ======================       \n")
		self.mapp.insert(10, "                                                                 \n")
		self.mapp.insert(11, "                                                                 \n")

	def update_pos(self, direction):
		self.pos[0] += direction[0]
		self.pos[1] += direction[1]
		y = -1
		screen.move(0, 0)
		self.mapp.insert(self.pos[0], '#')
		for i in self.mapp:
			screen.addstr(i)
		screen.move(0, 0)

	def _draw(self):
		x = self.pos[1]
		y = self.pos[0]
		screen.addstr(y, x, self.char)
		screen.move(0, 0)


def main():
	rogue = Rogue()
	rogue.update_pos(NONE)
	while True:
		c = screen.getch()
		if c == ord('q'):
			break  # Exit the while()
		elif game == True:
			if c == curses.KEY_UP:
				rogue.update_pos(UP)
			elif c == curses.KEY_DOWN:
				rogue.update_pos(DOWN)
			elif c == curses.KEY_LEFT:
				rogue.update_pos(LEFT)
			elif c == curses.KEY_RIGHT:
				rogue.update_pos(RIGHT)

main()

curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
