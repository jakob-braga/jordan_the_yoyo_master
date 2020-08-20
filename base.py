import pygame
import random
import math

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

window_size = (1280, 720)
window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
pygame.display.set_icon(pygame.image.load('./images/icon.png').convert_alpha())
pygame.display.set_caption('Jordan The Yo-Yo Master')
clock = pygame.time.Clock()

mid_x = window_size[0] // 2

tile_len = 16 * 5


def load_img(path):
    img = pygame.image.load(path).convert_alpha()
    new_img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5)).convert_alpha()
    return new_img


# scaling for the images in the game


def scale(num):
    new = num * tile_len
    return new


def p_scale(num):
    new = num * 5
    return new


def r_scale(x, y, wid, hei):
    new = (scale(x), scale(y), scale(wid), scale(hei))
    return new


# vector stuff


def unit_vector(pos1, pos2):
    vec = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    mag = math.sqrt((vec[0] ** 2) + (vec[1] ** 2))
    if mag == 0:
        uv = (vec[0] / 1, vec[1] / 1)
    else:
        uv = (vec[0] / mag, vec[1] / mag)
    return uv


def scale_vec(uv, factor):
    new_vec = (uv[0] * factor, uv[1] * factor)
    return new_vec


def d_vec(tup, x, y):
    new_vec = (tup[0] + x, tup[1] + y)
    return new_vec


def rotate_vec(vec, angle):
    a = math.radians(angle)
    new_vec_x = math.cos(a)*vec[0] - math.sin(a)*vec[1]
    new_vec_y = math.sin(a)*vec[0] + math.cos(a)*vec[1]
    new_vec = (new_vec_x, new_vec_y)
    return new_vec


# misc


def get_random(lst):
    if len(lst) > 1:
        i = random.randint(0, len(lst) - 1)
        new = lst[i]
    else:
        new = lst[0]
    return new


# text


def split_text(text):
    i = 0
    last_space = 0
    low = []
    for char in text:
        if last_space == 0 and char == " ":
            low.append(text[last_space:i + 1])
            last_space = i
        elif char == " ":
            low.append(text[last_space + 1:i + 1])
            last_space = i
        elif i == len(text) - 1:
            low.append(text[last_space + 1:])
        i += 1
    return low


def back_to_text(low):
    text = ""
    for word in low:
        text = text + word
    return text


def print_text_to_screen(text, rect):
    font = pygame.font.Font('font/pfont.ttf', 40)
    text_colour = (200, 200, 200)
    lot = []
    low = split_text(text)
    i = 0
    while i <= len(low):
        text = back_to_text(low[:i])
        text_surf = font.render(text, True, text_colour).convert_alpha()
        if back_to_text(low[i - 1]) == '$%^ ':
            text = back_to_text(low[:i - 1])
            lot.append(text)
            low = low[i:]
            i = 0
        if text_surf.get_width() < rect[2]:
            i += 1
        else:
            text = back_to_text(low[:i - 1])
            lot.append(text)
            low = low[i - 1:]
            i = 0
    lot.append(text)

    read_loop = True
    while read_loop:
        j = 0
        k = 0
        cool_down = 0
        for j in range(0, len(lot)):
            while k <= len(lot[j]):
                if cool_down == 0:
                    text_surf = font.render(lot[j][:k], True, text_colour).convert_alpha()
                    window.blit(text_surf, (rect[0], rect[1] + j*text_surf.get_height()*2))
                cool_down += 1
                if cool_down == 25:
                    cool_down = 0
                    k += 1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

                pygame.display.update()
            k = 0

        read_loop = False
