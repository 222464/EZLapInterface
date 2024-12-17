import os
import numpy as np
import pygame
import threading
from ezlap_reader import EZLapReader

fps = 60

reader = EZLapReader()

def reader_func():
    global reader

    while reader.is_open():
        data = reader.read()

        if data is not None:
            # log data
            log_data(data)

def log_data(data):
    print("DATA")
    print(data)

reader_thread = threading.Thread(target=reader_func, daemon=True)
reader_thread.start()

screen = pygame.display.set_mode((800, 480))

running = True

start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ks = pygame.key.get_pressed()

    if ks[pygame.K_q]:
        running = False

    #screen.blit(surf, (0, 0))

    pygame.display.flip()

    end_time = pygame.time.get_ticks()

    dt = end_time - start_time

    start_time = end_time

    pygame.time.delay(max(0, 1000 // fps - dt))

reader.close()
reader_thread.join()
