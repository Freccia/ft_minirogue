#!/usr/bin/env python
import curses
from random import randint
from time import sleep
from os import environ

# Variables that may never change:
UP    = (-1,  0)
RIGHT = ( 0,  1)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)

# Variables that may be changed in the future, or downstream:
GAME_OVER_MESSAGE = "Game over. Press 'q' to quit."

# Settings:
FOOD_AMOUNT = 5
COLOR = True
SPEED = 0.1

# Variables that change at runtime
game = True

def center(screen, raw_text):
    (screen_height, screen_width) = screen.getmaxyx()
    texts = raw_text.split('\n')
    y_padding = ( (screen_height-len(texts)) / 2 )
    for i in range(0, len(texts)):
        x_padding = ( (screen_width-len(texts[i])) / 2 )
        try: screen.addstr(y_padding+i, x_padding, str(texts[i]))
        except curses.error: pass
    screen.move(0, 0)  # Keep the cursor out of the way

def game_over(screen, score):
    global game
    game = False
    center(screen, GAME_OVER_MESSAGE+'\n'+'Score: '+str(score))

def out(screen, y, x, char_out):
    for chars, color in chars_colors:
        if char_out in chars:
            try: screen.addstr(y, x, char_out, color)
            except curses.error: pass
            screen.move(0, 0)  # Keep the cursor out of the way
            return True
    try: screen.addstr(y, x, char_out)
    except curses.error: pass
    screen.move(0, 0)  # Keep the cursor out of the way
    return False

class Cell(object):
    def __init__(self, screen, position, char='#'):
        self.screen = screen
        self.char = char
        self.pos = position
        self.old_pos = [None, None]
        self._draw()

    def update(self, position):
        self.old_pos = tuple(self.pos)
        self.pos = position
        if not game: return
        self._draw()

    def _draw(self):
        if self.pos is not self.old_pos:
            out(self.screen, self.pos[0], self.pos[1], self.char)

class Head(Cell):
    def __init__(self, screen, position, direction):
        self.direction = direction
        Cell.__init__(self, screen, position, '@')

    def update(self, collides, direction=None):
        if direction is not None:
            if type(direction[0]) is int and type(direction[1]) is int:
                self.direction = direction
        new_pos = \
            (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        if self._collisions(new_pos, collides) == False: return False
        Cell.update(self, new_pos)

    def _collisions(self, pos, collides):
        (screen_height, screen_width) = self.screen.getmaxyx()

        if pos[1] > screen_width-1 or pos[1] < 0 \
            or pos[0] > screen_height-1 or pos[0] < 0:
                return False

        for i in range(0, len(collides)):
            if pos == collides[i]:
                return False

class Snake(object):
    def __init__(self, screen, position, direction):
        self.screen = screen
        self.body = []
        self.body.append(Head(self.screen, position, direction))

    def update(self, direction=None):
        if self.body[0].update([cell.pos for cell in self.body[1:-1]], direction) \
            == False: game_over(self.screen, len(self.body)-1) ; return
        for i in range(1, len(self.body)):
            self.body[i].update(self.body[i-1].old_pos)
        self._draw()

    def grow(self):
        self.body.append(Cell(self.screen, self.body[-1].old_pos))

    def _draw(self):
        if self.body[0].pos != self.body[-1].old_pos and None not in self.body[-1].old_pos:
            try: self.screen.addstr(self.body[-1].old_pos[0], self.body[-1].old_pos[1], ' ')
            except curses.error: pass
        self.screen.move(0, 0)  # Keep the cursor out of the way

    def _get_pos(self):
        return self.body[0].pos
    pos = property(_get_pos)

class Food(object):
    def __init__(self, screen, blacklist):
        self.screen = screen
        self.char = '*'
        (screen_height, screen_width) = screen.getmaxyx()
        while True:
            self.pos = tuple([randint(1,screen_height-1), \
                randint(1,screen_width-1)])
            if self.pos not in blacklist: break
        self._draw()

    def _draw(self): out(self.screen, self.pos[0], self.pos[1], self.char)

def main(screen):
    global chars_colors
    chars_colors = []
    if COLOR == True and curses.has_colors() is True:
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        chars_colors.append(('@#' ,curses.color_pair(1)))
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        chars_colors.append(('*' ,curses.color_pair(2)))
    screen.nodelay(1)
    oldchar = -1
    (screen_height, screen_width) = screen.getmaxyx()
    position = screen_height/2, screen_width/2
    snake = Snake(screen, position, LEFT)
    foods = []
    for i in range(FOOD_AMOUNT):
        foods.append(Food(screen, [cell.pos for cell in snake.body] \
            +[food.pos for food in foods]))
    screen.move(0, 0)  # Keep the cursor out of the way

    while True:
        char = screen.getch()
        if char == 113: break  # q
        elif game == True:
            if char != oldchar:
                if char == curses.KEY_RIGHT: snake.update(RIGHT)
                elif char == curses.KEY_LEFT: snake.update(LEFT)
                elif char == curses.KEY_UP: snake.update(UP)
                elif char == curses.KEY_DOWN: snake.update(DOWN) 
                else: snake.update()
            else:
                snake.update()
                curses.flushinp()
            oldchar = char
        for food in foods:
            if food.pos == snake.pos:
                snake.grow()
                foods.pop(foods.index(food))
                foods.append(Food(screen,[cell.pos for cell in snake.body] \
                    +[food.pos for food in foods]))
        sleep(SPEED)
    quit()

try: _orig_ESCDELAY = environ['ESCDELAY']
except KeyError: pass
environ['ESCDELAY'] = str(0)  # Stop escape key from pausing game

curses.wrapper(main)

environ['ESCDELAY'] = _orig_ESCDELAY  # Revert to original ESCDELAY
