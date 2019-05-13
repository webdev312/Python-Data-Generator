import random
import datetime
import math

import location
import simulator_util
import database
import alert

class Rooms:
    # Room state JSON Format
    '''
    {
        patient: patient object
        room: "Room1"
        day: 1
        from_time: 130 (minutes)
        to_time: 245 (minutes)
        state: "waiting nurse"
        nurse: "Nurse1"
        doctor: ""
        equipment: ""
        meet_to_time: 150
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
        n_delay = random.randint(100,180)
        n_from = mins
        n_to = mins + n_delay

        room_state = {
            "patient": patient,
            "day": day,
            "room": room,
            "from_time": n_from,
            "to_time": n_to,
            "state": "waiting nurse",
            "nurse": "",
            "doctor": "",
            "equipment": "",
            "meet_to_time": 0
        }

        self.save_to_tagdata(tagdata, room_state, mins, n_delay)
        self.arr_room_state.append(room_state)
    
    def save_to_tagdata(self, tagdata, room_state, mins, delay):
        now = datetime.datetime.now()
        n_day = room_state["day"]
        n_hour = math.floor(mins / 60)
        n_min = mins % 60
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(delay))

        x1,y1 = room_state["patient"].x,room_state["patient"].y
        x2,y2 = simulator_util.get_point_by_position(room_state["room"])
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
        arr_temp = []
        for i in range(0, len(self.arr_room_state)):
            if (mins == self.arr_room_state[i]["to_time"]):
                empty_room.append(self.arr_room_state[i])
            else:
                arr_temp.append(self.arr_room_state[i])

        # charge self.arr_rooms        
        for i in range(0, len(empty_room)):            
            self.arr_rooms.append(empty_room[i]["room"])
        
        # remove assigned room from self.arr_room_state
        self.arr_room_state = arr_temp

        # get completed patients
        return empty_room

    '''
    Nurse Modules
    '''
    def get_patient_waiting_nurse(self):
        arr_patients_waiting_nurse = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["state"] == "waiting nurse"):
                arr_patients_waiting_nurse.append(self.arr_room_state[i])
        return arr_patients_waiting_nurse

    def set_patient_meet_nurse(self, room_state, nurse, tagdata, mins):
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["patient"].id == room_state["patient"].id):
                meet_to_time = random.randint(3, 5) # Nurse work time
                self.arr_room_state[i]["state"] = "meet nurse"
                self.arr_room_state[i]["nurse"] = nurse
                self.arr_room_state[i]["meet_to_time"] = meet_to_time + mins
                self.save_nurse_alert_to_tagdata(tagdata, room_state, nurse, mins, meet_to_time)

    def save_nurse_alert_to_tagdata(self, tagdata, room_state, nurse, mins, delay):
        now = datetime.datetime.now()
        n_day = room_state["day"]
        n_hour = math.floor(mins / 60)
        n_min = mins % 60        
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(delay))
        tagdata.append(alert.get_nurse_alert(room_state["patient"].id,
                                         from_time,
                                         to_time,
                                         delay,
                                         nurse,
                                         room_state["room"]))

    def get_patient_finished_nurse(self, mins):
        arr_pt_finished_nurse = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["meet_to_time"] == mins) and (self.arr_room_state[i]["state"] == "meet nurse"):
                pt_finished_nurse = self.arr_room_state[i]
                self.arr_room_state[i]["state"] = "waiting doctor"
                self.arr_room_state[i]["meet_to_time"] = 0
                arr_pt_finished_nurse.append(pt_finished_nurse)
        return arr_pt_finished_nurse

    '''
    Doctor Modules
    '''
    def get_patient_waiting_doctor(self):
        arr_patients_waiting_doctor = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["state"] == "waiting doctor"):
                arr_patients_waiting_doctor.append(self.arr_room_state[i])
        return arr_patients_waiting_doctor

    def set_patient_meet_doctor(self, room_state, doctor, tagdata, mins):
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["patient"].id == room_state["patient"].id):
                meet_to_time = random.randint(3, 5) # doctor work time
                self.arr_room_state[i]["state"] = "meet doctor"
                self.arr_room_state[i]["doctor"] = doctor
                self.arr_room_state[i]["meet_to_time"] = meet_to_time + mins
                self.save_doctor_alert_to_tagdata(tagdata, room_state, doctor, mins, meet_to_time)

    def save_doctor_alert_to_tagdata(self, tagdata, room_state, doctor, mins, delay):
        now = datetime.datetime.now()
        n_day = room_state["day"]
        n_hour = math.floor(mins / 60)
        n_min = mins % 60        
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(delay))
        tagdata.append(alert.get_doctor_alert(room_state["patient"].id,
                                         from_time,
                                         to_time,
                                         delay,
                                         doctor,
                                         room_state["room"]))

    def get_patient_finished_doctor(self, mins):
        arr_pt_finished_doctor = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["meet_to_time"] == mins) and (self.arr_room_state[i]["state"] == "meet doctor") :
                pt_finished_doctor = self.arr_room_state[i]
                self.arr_room_state[i]["state"] = "waiting equip"
                self.arr_room_state[i]["meet_to_time"] = 0
                arr_pt_finished_doctor.append(pt_finished_doctor)
        return arr_pt_finished_doctor

    '''
    Equip Modules
    '''
    def get_patient_waiting_equip(self):
        arr_patients_waiting_equip = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["state"] == "waiting equip"):
                arr_patients_waiting_equip.append(self.arr_room_state[i])
        return arr_patients_waiting_equip

    def set_patient_meet_equip(self, room_state, equip, tagdata, mins):
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["patient"].id == room_state["patient"].id):
                meet_to_time = random.randint(40, 90) # equip work time
                self.arr_room_state[i]["state"] = "meet equip"
                self.arr_room_state[i]["equip"] = equip
                self.arr_room_state[i]["meet_to_time"] = meet_to_time + mins
                self.save_equip_alert_to_tagdata(tagdata, room_state, equip, mins, meet_to_time)

    def save_equip_alert_to_tagdata(self, tagdata, room_state, equip, mins, delay):
        now = datetime.datetime.now()
        n_day = room_state["day"]
        n_hour = math.floor(mins / 60)
        n_min = mins % 60        
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(delay))
        tagdata.append(alert.get_equip_alert(room_state["patient"].id,
                                            from_time,
                                            to_time,
                                            delay,
                                            equip,
                                            room_state["room"]))

    def get_patient_finished_equip(self, mins):
        arr_pt_finished_equip = []
        for i in range(0, len(self.arr_room_state)):
            if (self.arr_room_state[i]["meet_to_time"] == mins) and (self.arr_room_state[i]["state"] == "meet equip") :
                pt_finished_equip = self.arr_room_state[i]
                self.arr_room_state[i]["state"] = "waiting ivpump"
                self.arr_room_state[i]["meet_to_time"] = 0
                arr_pt_finished_equip.append(pt_finished_equip)
        return arr_pt_finished_equip

    def get_all_rooms(self):
        return self.arr_rooms
    
    def get_all_room_states(self):
        return self.arr_room_state