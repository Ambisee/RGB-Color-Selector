# --- Modules --- #
from win32api import GetSystemMetrics
from Modules_Configs.config import *
from Modules_Configs.mouse import *
from Modules_Configs.draw import *
from Modules_Configs.colors import *
from Modules_Configs.text_input import *
from pygame import gfxdraw
import pyperclip
import pygame
import sys
import os

# --- Pygame Window --- #
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{GetSystemMetrics(0) // 2 - WIDTH // 2}, {GetSystemMetrics(1) // 2 - HEIGHT // 2}"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RGB Color Selector")

font1 = pygame.font.Font(os.path.abspath("Fonts/SourceCodePro-Medium.ttf"), 35)
font2 = pygame.font.Font(os.path.abspath("Fonts/Poppins-Medium.ttf"), 35)
font3 = pygame.font.Font(os.path.abspath("Fonts/Poppins-Medium.ttf"), 20)
        
# --- Functions --- #
def init_scroll(surface):
    scroll_list = []
    scroll_list.append(ColorScroll(0, 0, surface, "R", font1))
    scroll_list.append(ColorScroll(1, 1, surface, "G", font1))
    scroll_list.append(ColorScroll(2, 2, surface, "B", font1))
    return scroll_list

def isIncircle(x, y, x_circ, y_circ, radius):
    x_confirm = (x in range(x_circ - radius, x_circ + radius + 1))
    y_confirm = (y in range(y_circ - radius, y_circ + radius + 1))
    return x_confirm and y_confirm

def isInbar(x, y, x_bar, y_bar, length, height):
    x_confirm = (x in range(x_bar, x_bar + length + 1))
    y_confirm = (y in range(y_bar, y_bar + height + 1))
    return x_confirm and y_confirm

def createValue(text):
    return font1.render(text, True, (0, 0, 0))

def main():
    clock = pygame.time.Clock()
    FPS = 60
    drag = False
    selected = None
    dropdown = False

    cd = ColorDisplay()
    cp = ColorPicker()
    cs = init_scroll(cp.surface)
    ingroup = InputGroup(WIDTH//2, 450, font3)
    copy_button = CopyButton(font3, 395)
    
    dif = None
    radius = cs[0].radius
    timer = 0
    
    title = font2.render("RGB Color Picker", True, (0, 0, 0))
    result = font2.render('Result : ', True, (abs(cd.red - 255), abs(cd.green - 255), abs(cd.blue - 255)))
    notif = pygame.font.Font(os.path.abspath("Fonts/KronaOne-Regular.ttf"), 22).render("Value Copied", True, (0,0,0))
    value = font1.render("Value", True, (208, 0, 212))
    text = f"({cd.red}, {cd.green}, {cd.blue})"
    _value = createValue(text)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mb = pygame.mouse.get_pos()
                if ingroup.selector.checkClicked(mb[0], mb[1]):
                    ingroup.selector.drop = True
                elif ingroup.selector.isSelected(mb[0], mb[1]):
                    ingroup.selector.switch(mb[1])
                elif ingroup.button.collidepoint(mb[0], mb[1]):
                    ingroup.change(cs)
                else:
                    ingroup.selector.drop = False
                
                ingroup.ibar.isSelected(mb[0], mb[1])
                
                if copy_button.isSelected(mb[0], mb[1], text):
                    timer = 1 * FPS

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ingroup.change(cs)
                elif event.key == pygame.K_c:
                    copy_button.pycopy(text)
                    timer = 1 * FPS
                elif event.key == pygame.K_r:
                    ingroup.selector.selected_col = 0
                elif event.key == pygame.K_g:
                    ingroup.selector.selected_col = 1
                elif event.key == pygame.K_b:
                    ingroup.selector.selected_col = 2
                else:
                    ingroup.ibar.keyFunc(event)

        clicked = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        if any(clicked) and cp.rect.collidepoint(x, y):          
            drag, selected, dif = m_handle(x, y - cp.y , cs, radius, drag, selected, dif, isIncircle, isInbar)
            m_result(x, y, drag, selected, dif)
        else:
            selected = None
            drag = False
            dif = None

        cd.update_color(cs[0].color[cs[0].color_in], cs[1].color[cs[1].color_in], cs[2].color[cs[2].color_in])
        result = font2.render('Result : ', True, (abs(cd.red - 255), abs(cd.green - 255), abs(cd.blue - 255)))
        text = f"({cd.red}, {cd.green}, {cd.blue})"
        _value = createValue(text)

        redraw_window(screen, cd, cp, cs, title, result, value, _value)
        ingroup.draw(screen)
        copy_button.draw(screen)

        if timer > 0:
            screen.blit(notif, (WIDTH//4 - notif.get_width() // 2, HEIGHT - notif.get_height() - 5))
            timer -= 1
        else:
            timer = 0

        pygame.display.update()

# --- Main Function --- #
if __name__ == "__main__":
    main()