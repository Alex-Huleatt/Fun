#!/usr/bin/env python

'''
@author AlexHuleatt
Terminal-based Tron or Light-cycles remake. 
Made just for fun.

Uses a breadth-first search for the enemy.
Can be pretty easily tricked into going down 1-cell wide sections, as long as end is open.
Game was sped up to make this slightly more challenging. 

Only tested in Terminal on OSX. 
Should? be pretty crossplatform.
'''

import curses, time, random

dir_map = {'left':(0,-1), 'right':(0,1), 'up':(-1,0), 'down':(1,0)}
grid = set([]) #active cells
win = None #our window

player_pos = None #player position
player_dir = None #player direction

comp_pos = None
comp_dir = None

h,w = 0,0 #height and width of the screen
scared = 0 #distance computer-player wants to keep from player

inf = 10**100 #"infinity"

def button():
    '''This function uses curses's getch function
    This grabs *all* keys pressed since last call.'''
    s = set([])
    while True:
        k = win.getch()
        if k == -1:
            break
        s.add(k)

    if curses.KEY_LEFT in s:
        return 'left'
    elif curses.KEY_RIGHT in s:
        return 'right'
    elif curses.KEY_UP in s:
        return 'up'
    elif curses.KEY_DOWN in s:
        return 'down'
    else:
        return ''

def init():
    '''initializes the game.'''
    global win
    global player_pos, player_dir
    global comp_pos, comp_dir
    global h,w
    global scared
    win = curses.initscr()

    win.nodelay(1) #make getch non-blocking
    win.keypad(1) #required for arrowkeys to work

    curses.noecho()
    curses.curs_set(0)

    h,w = win.getmaxyx() #get size of window
    scared = (w*h)**.5
    for i in range(h):
        win.addch(i, 0, '|')
        win.addch(i, w-2, '|')
        
        grid.add((i,0))
        grid.add((i,w-2))

    for i in range(1,w-1):
        win.addch(0, i, '-')
        win.addch(h-1,i, '-')
        
        grid.add((0,i))
        grid.add((h-1,i))

    player_pos = (h//2, w//4)
    player_dir = 'right'
    grid.add(player_pos)

    comp_pos = (h//2, 3*w//4)
    comp_dir = 'left'
    grid.add(comp_pos)

def move(p, d):
    y,x = p
    dy, dx = dir_map[d]
    return (y+dy, x+dx)

#for AI to play
def think():
    global comp_dir, comp_pos
    global player_pos, player_dir
    global grid, h, w
    global scared

    def flood():
        '''flood-fill, or breadth first search, starting at the player.'''
        q = [player_pos]
        costs = {player_pos:0}
        q_s = set([player_pos])
        while len(q) > 0:
            top = q[0]
            q = q[1:]
            q_s.remove(top)
            for d in dir_map:
                nei = move(top, d)

                if nei in grid or nei[0] <= 0 or nei[0] >= h-1 or nei[1] <= 0 or nei[1] >= w-2:
                    costs[nei] = inf
                    continue

                if nei in costs or nei in q_s:
                    continue

                costs[nei] = costs[top]+1
                q.append(nei)
                q_s.add(nei)

        return costs
   
    costs = flood()
    best = comp_dir
    best_cost = inf

    dirs = list(dir_map.keys()) #copy the keys list
    random.shuffle(dirs) #randomness for replayability.

    for d in dirs:
        n = move(comp_pos, d)
        if n in grid:
            v = inf
        elif n in costs:
            v = costs[n]
        else:
            v = inf
        v = abs(scared - v)

        if v <= best_cost: #use scared - distance to keep computer player away.
            best = d
            best_cost = v

    scared = max(0,scared-.25) #have the enemy slowly start attacking.
    comp_dir = best


def main():
    global player_pos, player_dir
    global win, grid
    global comp_pos, como_dir
    c_lost = False
    p_lost = False
    try: #curses throws all kinds of errors.
        init() #initialize game
        t = time.time()
        lastTime = t 
        FPS = 23 #arbitrary, felt right

        #keep going until both players lose
        while not c_lost or not p_lost:

            if not p_lost:
                #--player update--
                k = button()
                if k != "":
                    player_dir=k
                y,x = player_pos
                player_pos = move(player_pos, player_dir)
                win.addch(y,x,'#')

                if player_pos in grid:
                    p_lost = True
                grid.add(player_pos)
                #--------------

            if not c_lost:
                #--computer update--
                think()
                y,x = comp_pos
                comp_pos = move(comp_pos, comp_dir)
                win.addch(y,x,"X")
                if comp_pos in grid:
                    c_lost = True
                grid.add(comp_pos)
                #--------------

            win.refresh() #display

            #game loop logic
            sleepTime = 1./FPS - (time.time() - lastTime)
            if sleepTime > 0:
                time.sleep(sleepTime)
            lastTime = time.time()

        time.sleep(2)
    finally:
        curses.endwin() #clean up


if __name__ == "__main__":
    print('Use the arrow-keys!')
    print("You're on the left!")
    time.sleep(2)
    main()

