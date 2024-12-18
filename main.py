import os
import numpy as np
import pygame
import pygame.freetype
import threading
from ezlap_reader import EZLapReader
from tracker import Tracker
from db_interface import DBInterface
import pyttsx3
import time

fps = 60

engine = pyttsx3.init()
engine.setProperty('rate', 125)

reader = EZLapReader()
tracker = Tracker()
db = DBInterface()

last_n = 10
latest = db.read_last_n(last_n)
speech = []

def reader_func():
    global reader

    while reader.is_open():
        data = reader.read()

        if data is not None:
            print(data)
            # log data
            log_data(data)

def log_data(data):
    global tracker
    global db

    result = tracker.track(data[0], data[1])

    if result is not None: # if completed a lap
        speech.append(f'{result/1000.0:.2f}')

        db.insert(data[0], result, time.time())

        # update latest
        latest = db.read_last_n(last_n)

reader_thread = threading.Thread(target=reader_func, daemon=True)
reader_thread.start()

pygame.init()
screen = pygame.display.set_mode((800, 480))

font = pygame.freetype.Font('terminal.ttf', 30)

running = True

start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ks = pygame.key.get_pressed()

    if ks[pygame.K_q]:
        running = False
        
    if len(speech) > 0:
        engine.say(speech[0])
        engine.runAndWait()

        speech = []

    #screen.blit(surf, (0, 0))
    screen.fill((0, 0, 0))

    # heading
    text_surface, rect = font.render('UID, LAPTIME', (32, 255, 32))

    screen.blit(text_surface, (10, 10))

    for i, r in enumerate(latest):
        text_surface, rect = font.render(f'{r[0]}, {r[1]/1000.0:.2f}', (32, 255, 32))

        screen.blit(text_surface, (10, 10 + 32 * (1 + i)))

    pygame.display.flip()

    end_time = pygame.time.get_ticks()

    dt = end_time - start_time

    start_time = end_time

    pygame.time.delay(max(0, 1000 // fps - dt))

reader.close()
reader_thread.join()
