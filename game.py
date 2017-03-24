#!/usr/bin/env python

import sys
import os
import random

SIZE            = 50
BLOCKS          = (SIZE * SIZE) / 10
PLAYERS         = 2

class directions:
    DOWN            = 0
    UP              = 1
    LEFT            = 2
    RIGHT           = 3

players         = []
goal            = [random.randint(0,SIZE-1), random.randint(0,SIZE-1)]
blocks          = []

class colors:
    BACKGROUND  = '\033[0;47m'
    PLAYER      = '\033[34m'
    GOAL        = '\033[91m'
    ENDC        = '\033[0m'
    
def has_player_won():
    for player in players:
        if player['x'] == goal[0] and player['y'] == goal[1]:
            return player['id']
    return None

def get_player_by_location(location):#print players
    player_found = None;
    
    for player in players:
        if player['x'] == location[0] and player['y'] == location[1]:
            return player
    return None
            
def get_player_by_id(player_id):
    for player in players:
        if player['id'] == player_id:
            return player
    return None

###############################################################################
# pulled from http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/

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
###############################################################################

def moveLeft(player_id):
    movePlayerAlongX(player_id, directions.LEFT)

def moveRight(player_id):
    movePlayerAlongX(player_id, directions.RIGHT)

def moveUp(player_id):
    movePlayerAlongY(player_id, directions.UP)

def moveDown(player_id):
    movePlayerAlongY(player_id, directions.DOWN)

def movePlayerAlongX(player_id, direction):
    player = get_player_by_id(player_id)
    new_coords = getNewXCoords(player['x'], player['y'], direction)
    player['x'] = new_coords[0]
    player['y'] = new_coords[1]
    
def movePlayerAlongY(player_id, direction):
    player = get_player_by_id(player_id)
    new_coords = getNewYCoords(player['x'], player['y'], direction)
    player['x'] = new_coords[0]
    player['y'] = new_coords[1]

def getNewXCoords(curr_x, curr_y, direction):

    # get proposed coords
    new_x = curr_x
    new_y = curr_y

    if direction == directions.LEFT:
        new_x = (curr_x - 1 if curr_x > 0 else curr_x)

    elif direction == directions.RIGHT:
        new_x = (curr_x + 1 if curr_x < SIZE-1 else curr_x)

    # check for goal or block
    if [new_x, new_y] != goal and [new_x,new_y] in blocks:
        return [curr_x, curr_y]

    return [new_x, new_y]
    
def getNewYCoords(curr_x, curr_y, direction):
    
    # get proposed coords
    new_x = curr_x
    new_y = curr_y
    
    if direction == directions.DOWN:
        new_y = (curr_y + 1 if curr_y < SIZE-1 else curr_y)
        
    elif direction == directions.UP:
        new_y = (curr_y - 1 if curr_y > 0 else curr_y)
        
    # check for goal or block
    if [new_x, new_y] != goal and [new_x,new_y] in blocks:
        return [curr_x, curr_y]
    
    return [new_x, new_y]

def display():
    player_id = has_player_won()
    if player_id != None:
        os.system('clear')
        print "Congratulations Player %s! You win!" % player_id
        sys.exit()

    gameboard = ""
    for y in range(SIZE):
        gameboard += "|"
        for x in range(SIZE):
            player = get_player_by_location([x, y])
            if player != None:
                gameboard += colors.PLAYER + "%s" % player['id'] + colors.ENDC
            elif [x, y] == goal:
                gameboard += colors.GOAL + "$" + colors.ENDC
            elif [x, y] in blocks:
                gameboard += "#"
            else:
                gameboard += " "
            gameboard += "|"
        gameboard += "\n"
    os.system('clear') # moved this down here to further minimize redraw time
    print(gameboard)

if __name__=="__main__":

    player1_id = 1
    player2_id = 2

    for i in range(1, PLAYERS+1):
        player = {"id": i, "name": "", "x": random.randint(0,SIZE-1), "y": random.randint(0,SIZE-1)}
        players.append(player)

    for i in range(BLOCKS):
        x = random.randint(0,SIZE-1)
        y = random.randint(0,SIZE-1)
        if get_player_by_location([x,y]) == None:
            blocks.append([x,y])
    
    #print players
            
    while True:

        display()
        
        # blocking action
        k = ord(getch())

        if k == 3:                  # ctrl-c to quit
            break
            
        # player 1
        elif k == 119:              # w
            moveUp(player1_id)
        elif k == 122:              # z
            moveDown(player1_id)
        elif k == 115:              # s
            moveRight(player1_id)
        elif k == 97:               # a
            moveLeft(player1_id)
        
        # player 2
        elif k == 105:              # i
            moveUp(player2_id)
        elif k == 109:              # m
            moveDown(player2_id)
        elif k == 107:              # k
            moveRight(player2_id)
        elif k == 106:               # j
            moveLeft(player2_id)
