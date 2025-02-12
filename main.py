import os
import numpy as np
import pygame
import pygame.freetype
import threading
from ezlap_reader import EZLapReader
from tracker import Tracker
from db_interface import DBInterface
import time

fps = 60

reader = EZLapReader()
tracker = Tracker()
db = DBInterface()

last_n = 10
latest = db.read_last_n(last_n)

IMG_SIZE = (720, 1280) # height, width

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[0])
cap.set(cv2.CAP_PROP_FPS, fps)

if not cap.isOpened():
    raise Exception("Can't open camera.")

VIDEO_NAME_BASE = "data/video"
VIDEO_NAME_EXT = ".mp4"

fourcc = cv2.VideoWriter_fourcc(*"MJPG")

video_index = 0

while os.path.exists(VIDEO_NAME_BASE + str(video_index) + VIDEO_NAME_EXT):
    video_index += 1

video_filename = VIDEO_NAME_BASE + str(video_index) + VIDEO_NAME_EXT

new_video = False
out = None

def reader_func():
    global reader

    while reader.is_open():
        data = reader.read()

        if data is not None:
            # log data
            log_data(data)

def log_data(data):
    global tracker
    global db
    global latest
    global new_video

    result = tracker.track(data[0], data[1])

    if result > 0: # if completed a lap
        new_video = True

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

    ret, frame = self.cap.read()

    # if frame is read correctly ret is True
    if not ret:
        raise Exception("Can't receive frame.")

    if new_video:
        new_video = False

        if out is not None:
            out.release()

            video_index += 1

            video_filename = VIDEO_NAME_BASE + str(video_index) + VIDEO_NAME_EXT

        print("New video.")

        out = cv2.VideoWriter(video_filename, fourcc, fps, (IMG_SIZE[1], IMG_SIZE[0]), 0) # 0 at end for grayscale

    if out is not None:
        out.write(frame)

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
