# -*- coding: utf-8 -*-

import sys, random, math, pygame
from pygame.locals import *
from datetime import datetime, date, time


#数字位置不是很好排，有点歪


Pi = 3.141593

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

def draw_sec_taple(radain):
    len = 180
    width = 4
    target = (len * math.cos(radain) + pos_x, len * math.sin(radain) + pos_y)
    pygame.draw.line(screen, white, (300, 250), target, width)

def draw_min_taple(radain):
    len = 140
    width = 8
    target = (len * math.cos(radain) + pos_x, len * math.sin(radain) + pos_y)
    pygame.draw.line(screen, yellow, (300, 250), target, width)

def draw_hour_taple(radain):
    len = 120
    width = 13
    target = (len * math.cos(radain) + pos_x, len * math.sin(radain) + pos_y)
    pygame.draw.line(screen, orange, (300, 250), target, width)

def draw_num():
    for i in range(12):
        num = i+1
        radain = (num * 360/12)/360 * (2 * Pi)
        radain -= Pi/2
        set_x = 190 * math.cos(radain) + pos_x - 18
        set_y = 190 * math.sin(radain) + pos_y - 18
        print_text(font, set_x, set_y, str(num), (200, 200, 200))


pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Analog Clock Demo")
font = pygame.font.SysFont('SimHei', 36)

orange = 220, 180, 0
white = 255, 255, 255
yellow = 255, 255, 0
pink = 255, 100, 100
gray = 77, 77, 77
pos_x = 300
pos_y = 250
radius = 220

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    screen.fill((77, 77, 77))
    pygame.draw.circle(screen, pink, (pos_x, pos_y), radius, 5)
    draw_num()

    today = datetime.today()
    hour = today.hour % 12
    minu = today.minute
    sec = today.second
    print_text(font, 5, 5, str(hour) + ":" + str(minu)+ ":" + str(sec), (200, 200, 200))

    #real clock
    hour += minu/60 + sec/3600
    minu += sec/60

    hour_r = -Pi/2 + hour / 12 * 2 * Pi
    min_r = -Pi/2 + minu / 60 * 2 * Pi
    sec_r = -Pi/2 + sec / 60 * 2 * Pi

    draw_sec_taple(sec_r)
    draw_min_taple(min_r)
    draw_hour_taple(hour_r)
    pygame.draw.circle(screen, pink, (pos_x, pos_y), 15, 0)
    pygame.display.update()