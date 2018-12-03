
import curses
import time
import numpy as np
from collections import namedtuple


def DCloop(stdscr):
    #https://docs.python.org/3/howto/curses.html
    #https://docs.python.org/3/library/curses.html#curses.window.clrtobot
    delay_time = 0.0
    print(curses.LINES) #Lines go from left to right, so this is the max y coord.
    print(curses.COLS) #Max X coord.
    #For each angle, the list is forward and back.

    box_side_y = 5
    box_side_x = 3

    grid_state = np.full((box_side_x, box_side_y), False, dtype=bool)

    box_coord_y = 2
    box_coord_x = 5

    pos_y = 0
    pos_x = 0
    pos = np.array([pos_x, pos_y])
    angle = 0

    box_info = (box_coord_y, box_coord_x, box_side_y, box_side_x)
    drawAllStandard(stdscr, pos, box_info, grid_state)
    drawCartesianPosition(stdscr, pos, box_info)
    stdscr.move(0,0)

    state = 'draw'
    fname = ''

    while True:
        c = stdscr.getch()

        if state == 'draw':

            if c == curses.KEY_LEFT:
                if pos[0] > 0:
                    pos += [-1, 0]
                    drawAllStandard(stdscr, pos, box_info, grid_state)
                    drawCartesianPosition(stdscr, pos, box_info)

            if c == curses.KEY_RIGHT:
                if pos[0] < (box_side_x - 1):
                    pos += [1, 0]
                    drawAllStandard(stdscr, pos, box_info, grid_state)
                    drawCartesianPosition(stdscr, pos, box_info)

            if c == curses.KEY_UP:
                if pos[1] > 0:
                    pos += [0, -1]
                    drawAllStandard(stdscr, pos, box_info, grid_state)
                    drawCartesianPosition(stdscr, pos, box_info)

            if c == curses.KEY_DOWN:
                if pos[1] < (box_side_y - 1):
                    pos += [0, 1]
                    drawAllStandard(stdscr, pos, box_info, grid_state)
                    drawCartesianPosition(stdscr, pos, box_info)

            if c == ord(' '):

                grid_state[pos[0], pos[1]] = not grid_state[pos[0], pos[1]]
                drawAllStandard(stdscr, pos, box_info, grid_state)
                drawCartesianPosition(stdscr, pos, box_info)


            if c == 10:
                state = 'fname_dialog'
                c = ''
                dialogScreen(stdscr)
                drawFname(stdscr, fname)
                continue


            if c == ord('q') or c == 27:
                print('you pressed q! exiting')
                break  # Exit the while loop

        if state == 'fname_dialog':



            if c == 27:
                #print('you pressed escape! exiting to main screen')
                state = 'draw'
                drawAllStandard(stdscr, pos, box_info, grid_state)
                drawCartesianPosition(stdscr, pos, box_info)
                continue

            if c == 10:
                saveTextFile(fname, grid_state)
                break

            dialogScreen(stdscr)
            fname += chr(c)
            drawFname(stdscr, fname)



def saveTextFile(fname, grid_state):

    np.savetxt(fname + '.txt', grid_state.transpose(), fmt='%d')




def dialogScreen(stdscr):
    stdscr.erase()
    x0 = int(curses.LINES/2)
    y0 = int(curses.COLS/2)
    x0 = 3
    y0 = 3
    #stdscr.addstr(y0, x0, '_')
    stdscr.refresh()


def drawFname(stdscr, fname):

    x0 = 3
    y0 = 3
    stdscr.addstr(y0, x0, fname + '_')
    stdscr.refresh()


def redrawBox(stdscr, box_info):
    side_symbol = '-'
    (box_coord_y, box_coord_x, box_side_y, box_side_x) = box_info
    stdscr.addstr(box_coord_y - 1, box_coord_x, side_symbol*box_side_x)
    stdscr.addstr(box_coord_y + box_side_y, box_coord_x, side_symbol*box_side_x)
    for i in range(box_side_y+1):
        stdscr.addstr(box_coord_y + i, box_coord_x - 1, '|')
        stdscr.addstr(box_coord_y + i, box_coord_x + box_side_x, '|')



def drawFill(stdscr, pos, box_info, grid_state):
    (box_coord_y, box_coord_x, box_side_y, box_side_x) = box_info
    box_coord_x_shifted = box_coord_x + 20
    box_info_shifted = (box_coord_y, box_coord_x_shifted, box_side_y, box_side_x)

    redrawBox(stdscr, box_info_shifted)

    for i in range(box_side_x):
        for j in range(box_side_y):
            if grid_state[i, j]:
                stdscr.addstr(box_coord_y + j, box_coord_x_shifted + i, '▒')






def drawAllStandard(stdscr, pos, box_info, grid_state):
    #return(0)
    stdscr.erase() #Use this one supposedly https://stackoverflow.com/questions/9653688/how-to-refresh-curses-window-correctly
    redrawBox(stdscr, box_info)
    drawFill(stdscr, pos, box_info, grid_state)
    stdscr.addstr(curses.LINES - 1, 0,  'Press q or Esc to quit, press spacebar to save')
    drawPosInfo(stdscr, pos, box_info)
    stdscr.move(0,0)
    stdscr.refresh()


def drawCartesianPosition(stdscr, pos, box_info):
    (pos_x, pos_y) = (pos[0], pos[1])
    (box_coord_y, box_coord_x, box_side_y, box_side_x) = box_info
    stdscr.addstr(box_coord_y + pos_y, box_coord_x + pos_x, 'o')
    stdscr.move(0,0)
    stdscr.refresh()

def drawPosInfo(stdscr, pos, box_info):
    (pos_x, pos_y) = (pos[0], pos[1])
    (box_coord_y, box_coord_x, box_side_y, box_side_x) = box_info

    info_str = 'pos[0] = {}, pos[1] = {}'.format(pos[0], pos[1])
    stdscr.addstr(0, 30,  info_str)


def drawGrid():
    print('entering curses loop')
    curses.wrapper(DCloop)
    print('exited curses loop.')



drawGrid()
















#
