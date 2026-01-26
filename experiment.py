import os
import numpy as np
import threading
import pyttsx3
import time

def delay(t, max_sleep=0.01):
    start = time.time()

    target = start + t

    while start < target:
        time.sleep(min(max_sleep, target - start))
        start = time.time()

def delay_to(end, max_sleep=0.01):
    t = time.time()

    while t < end:
        time.sleep(min(max_sleep, end - t))
        t = time.time()

experiment_delay = 10.0
experiment_time0 = 120.0
experiment_time1 = 180.0
test_time = 240.0

checkpoints = [ experiment_delay, experiment_time0, experiment_time1, test_time ]

engine = pyttsx3.init()
engine.setProperty('rate', 125)

time.sleep(1.0)

# prefix sum
cumm = time.time()

for i in range(len(checkpoints)):
    cumm += checkpoints[i]
    checkpoints[i] = cumm

engine.say("get ready")
engine.runAndWait()

delay_to(checkpoints[0])

engine.say("go go go!")
engine.runAndWait()

delay_to(checkpoints[1])

engine.say("intervene! intervene! intervene!")
engine.runAndWait()

delay_to(checkpoints[2])

engine.say("test! test! test!")
engine.runAndWait()
