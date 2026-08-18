import os
import numpy as np
import threading
from ezlap_reader import EZLapReader
from tracker import Tracker
import pyttsx3
import time
import csv

fps = 60
min_time = 3.0
max_time = 12.0

engine = pyttsx3.init()
engine.setProperty('rate', 125)

reader = EZLapReader()
tracker = Tracker()

last_n = 10
latest = []
speech = []

# logging laps
csvfile = open('lap_log.csv', 'w', newline='')

csvwriter = csv.writer(csvfile)

# header
csvwriter.writerow(["timestamp", "uid", "laptime"])

def reader_func():
    global reader

    while reader.is_open():
        data = reader.read()

        if data is not None:
            # log data
            log_data(data)

def log_data(data):
    global tracker
    global latest
    global csvwriter

    result = tracker.track(data[0], data[1])

    if result > 0: # if completed a lap
        seconds = result / 1000.0

        # range check to ignore outliers
        if seconds >= min_time and seconds <= max_time:
            t = round(time.time() * 1000)

            speech.append(f'{seconds:.2f}')

            latest.insert(0, (data[0], result, time.time()))

            text = f'Lap from {latest[0][0]}, {latest[0][1]/1000.0:.2f}s'

            csvwriter.writerow([t, latest[0][0], latest[0][1]/1000.0])

            print(text)

            # discard older
            if len(latest) > last_n:
                latest = latest[:last_n]

reader_thread = threading.Thread(target=reader_func, daemon=True)
reader_thread.start()

running = True

start_time = time.time()

while running:
    if len(speech) > 0:
        engine.say(speech[0])
        engine.runAndWait()

        speech = []

    end_time = time.time()

    dt = end_time - start_time

    start_time = end_time

    time.sleep(max(0.0, 1.0 / fps - dt))

reader.close()
reader_thread.join()
csvwriter.close()
