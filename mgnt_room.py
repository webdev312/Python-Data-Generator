import random
import datetime
import math

import location
import simulator_util
import database

class Rooms:
    # Room state JSON Format
    '''
    {
        patient: patient object
        room: "Room1"
        day: 1
        from_time: 130 (minutes)
        to_time: 145 (minutes)
    }
    '''
    arr_room_state = []
    arr_rooms = []

    def __init__(self):
        self.arr_rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6",]
        self.arr_room_state = []

    def is_available_room(self):
        if (len(self.arr_rooms) > 0):
            return True
        else:
            return False
    
    def get_room(self):
        rest_room = self.arr_rooms[0]
        self.arr_rooms = self.arr_rooms[1:]
        return rest_room

    def assign_room(self, patient, room, day, mins, tagdata):
        n_delay = random.randint(60,180)
        n_from = mins
        n_to = mins + n_delay

        room_state = {
            "patient": patient,
            "day": day,
            "room": room,
            "from_time": n_from,
            "to_time": n_to,
        }

        self.save_to_tagdata(tagdata, room_state)
        self.arr_room_state.append(room_state)
    
    def save_to_tagdata(self, tagdata, room_state):
        now = datetime.datetime.now()
        n_day = room_state["day"]
        n_hour = math.floor(room_state["from_time"] / 60)
        n_min = room_state["from_time"] % 60
        n_seq = room_state["to_time"] - room_state["from_time"]
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))

        p1,q1,p2,q2 = database.get_room_position(room_state["room"])
        x1,y1 = room_state["patient"].x,room_state["patient"].y
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(location.get_patient_location(room_state["patient"].id,
                                         "ROOM",
                                         from_time,
                                         to_time,
                                         x1,y1, x2,y2,
                                         room_state["room"]))
        room_state["patient"].x = x2
        room_state["patient"].y = y2

    def get_completed_assigned_patients(self, mins):
        empty_room = []
        for i in range(0, len(self.arr_room_state)):
            if (mins == self.arr_room_state[i]["to_time"]):
                empty_room.append(self.arr_room_state[i])

        # charge self.arr_rooms        
        for i in range(0, len(empty_room)):            
            self.arr_rooms.append(empty_room[i]["room"])
        
        # remove assigned room from self.arr_room_state
        arr_temp = []
        for i in range(0, len(self.arr_room_state)):
            b_is_exist = False
            for j in range(0, len(empty_room)):
                if (self.arr_room_state[i]["patient"].id == empty_room[j]["patient"].id):
                    b_is_exist = True
                    break
            if (b_is_exist == False):
                arr_temp.append(self.arr_room_state[i])
        self.arr_room_state = arr_temp

        # get completed patients
        return empty_room

    def get_all_rooms(self):
        return self.arr_rooms
    
    def get_all_room_states(self):
        return self.arr_room_state