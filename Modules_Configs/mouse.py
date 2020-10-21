# -- Modules -- #
import pygame

try:
    from config import *
except:
    from Modules_Configs.config import *

# -- Functions -- #
def m_handle(x, y, cs, radius, drag, selected, dif, inCircle, inBar):
    if drag and selected:
        pass
    elif inCircle(x, y, cs[0].x_circ, cs[0].y_circ, radius):
        drag = True
        selected = cs[0]
        dif = selected.x_circ - x
    elif inCircle(x, y, cs[1].x_circ, cs[1].y_circ, radius):
        drag = True
        selected = cs[1]
        dif = selected.x_circ - x
    elif inCircle(x, y, cs[2].x_circ, cs[2].y_circ, radius):
        drag = True
        selected = cs[2]
        dif = selected.x_circ - x
    
    elif inBar(x, y, cs[0].x_bar, cs[0].y_bar, cs[0].length, cs[0].height):
        drag = True
        selected = cs[0]
        dif = 0
    elif inBar(x, y, cs[1].x_bar, cs[1].y_bar, cs[1].length, cs[1].height):
        drag = True
        selected = cs[1]
        dif = 0
    elif inBar(x, y, cs[2].x_bar, cs[2].y_bar, cs[2].length, cs[2].height):
        drag = True
        selected = cs[2]
        dif = 0
    
    return [drag, selected, dif]

def m_result(x, y, drag, selected, dif):
    if drag and selected:
        if x in range(selected.x_bar - dif, selected.x_bar + selected.length - dif + 1):
            selected.update_x(x + dif)
            selected.color[selected.color_in] = (x + dif) - selected.x_bar
        elif x < selected.x_bar:
            selected.update_x(selected.x_bar)
            selected.color[selected.color_in] = 0
        elif x > selected.x_bar + selected.length:
            selected.update_x(selected.x_bar + selected.length)
            selected.color[selected.color_in] = 255