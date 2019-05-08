import random
import math
import datetime

class Patient:
    # Patient Format
    '''
    {
        id: 1
        x: 100
        y: 100
        zone: "Room5"
        state: "meet nurse"
    }
    '''    

    id = 0
    x = 0
    y = 0
    zone = ""
    state = ""

    def __init__(self, id, x = 0, y = 0, zone = "", state = ""):
        self.id = id
        self.x = x
        self.y = y
        self.zone = zone
        self.state = state

        