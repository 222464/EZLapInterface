import numpy as np

class Tracker:
    def __init__(self):
        self.last_ts = {}

    def track(self, uid, t):
        if uid in self.last_ts:
            dt = t - self.last_ts[uid]

            return dt

        self.last_ts[uid] = t

        return None
        

