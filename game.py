#!/usr/bin/env python
import sys
import os
import random

SIZE = 50
BLOCKS = (SIZE * SIZE) / 10
PLAYERS = 7

players = []
goal = [random.randint(0,SIZE-1), random.randint(0,SIZE-1)]
blocks = []

class colors:
    BACKGROUND = '\033[0;47m'
    PLAYER = '\033[34m'
    GOAL = '\033[91m'
    ENDC = '\033[0m'

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def has_player_won():
    for player in players:
        if player['x'] == goal[0] and player['y'] == goal[1]:
            return player['id']
        return None

def get_player_by_location(location):
    for player in players:
        if player['x'] == location[0] and player['y'] == location[1]:
            return player
        return None
            
def get_player_by_id(player_id):
    for player in players:
        if player['id'] == player_id:
            return player
        return None

def display():
    print colors.ENDC
    os.system('clear')

    player_id = has_player_won()
    if player_id != None:
        print "Congratulations Player %s! You win!" % player_id
        sys.exit()

    for y in range(SIZE):
        sys.stdout.write("|")
        for x in range(SIZE):
            player = get_player_by_location([x, y])
 
            if player != None:
                sys.stdout.write(colors.PLAYER + "%s" % player['id'] + colors.ENDC + "|" )
            elif [x, y] == goal:
                sys.stdout.write(colors.GOAL + "$" + colors.ENDC + "|")
            elif [x, y] in blocks:
                sys.stdout.write("#|")
            else:
                sys.stdout.write(" |")

        sys.stdout.write("\n")

def moveUp(player_id):
    player = get_player_by_id(player_id)
    y = player['y']
    player['y'] = (y - 1 if y > 0 else y)
    if [player['x'],player['y']] in blocks:
        player['y'] = y
    display()

def moveDown(player_id):
    player = get_player_by_id(player_id)
    y = player['y']
    player['y'] = (y + 1 if y < SIZE-1 else y)
    if [player['x'],player['y']] in blocks:
        player['y'] = y
    display()

def moveLeft(player_id):
    player = get_player_by_id(player_id)
    x = player['x']
    player['x'] = (x - 1 if x > 0 else x)
    if [player['x'],player['y']] in blocks:
        player['x'] = x
    display()

def moveRight(player_id):
    player = get_player_by_id(player_id)
    x = player['x']
    player['x'] = (x + 1 if x < SIZE-1 else x)
    if [player['x'],player['y']] in blocks:
        player['x'] = x
    display()

if __name__=="__main__":

    player_id = 1

    player_start = [random.randint(0,SIZE-1), random.randint(0,SIZE-1)]
    for i in range(1, PLAYERS+1):
        player = {"id": i, "name": "", "x": player_start[0], "y": player_start[1]}
        players.append(player)

    for i in range(BLOCKS):
        x = random.randint(0,SIZE-1)
        y = random.randint(0,SIZE-1)
        if get_player_by_location([x,y]) == None:
            blocks.append([x,y])

    display()

    while True:
        k = ord(getch())

        if k == 3:
            break
        elif k == 65:
            moveUp(player_id)
        elif k == 66:
            moveDown(player_id)
        elif k == 67:
            moveRight(player_id)
        elif k == 68:
            moveLeft(player_id)
