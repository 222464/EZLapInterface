import numpy as np

class Tracker:
    def __init__(self):
        self.last_ts = {}

    def track(self, uid, t):
        dt = -1

        if uid in self.last_ts:
            dt = t - self.last_ts[uid]

        self.last_ts[uid] = t

        return dt
        

