import sys
import pdb
import matplotlib.pyplot as plt


def volt3(i, r):
    return i * r


def trueplot(truesketch, justonce=False, doverify=False, justclose=False,
             *args, **kwargs):

    plt.clf()
    truesketch(*args, **kwargs)

    if justonce:
        plt.show()
    else:
        plt.draw_all()

    plt.pause(1e-3)  # allows time to draw

    fig2 = plt.get_fignums()
    if justclose and not fig2:
        sys.exit()

    if doverify:
        string2 = input(
            'Hit <Enter> to continue, "d" for debugger and "x" to exit: ')
        if string2 == 'x' or string2 == 'exit':
            sys.exit()
        if string2 == 'd' or string2 == 'debug':
            print('\nType "exit" to continue program execution\n')
            pdb.runeval('u')


def pow3(i, v):
    return i * v


def figs(*args, **kwargs):
    plt.ion()
    plt.figure(*args, **kwargs)
