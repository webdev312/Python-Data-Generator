import random
import math
import datetime

import simulator_util
import location

class Register:
    # Register JSON Format
    '''
    {
        patient: Patient Class Object
        day: 1
        from_time: 130 (minutes)
        to_time: 145 (minutes)
    }
    '''
    arr_register= []   

    def __init__(self):
        self.arr_register = []

    def register_patient(self, patient, day, mins, tagdata):
        n_delay = random.randint(10,20)
        n_from = mins
        n_to = mins + n_delay

        patient_info = {
            "patient": patient,
            "day": day,
            "from_time": n_from,
            "to_time": n_to,
        }        
        self.save_to_tagdata(tagdata, patient_info)
        self.arr_register.append(patient_info)

    def save_to_tagdata(self, tagdata, patient_info):
        # append REGISTRATION to tag_data
        now = datetime.datetime.now()
        n_day = patient_info["day"]
        n_hour = math.floor(patient_info["from_time"] / 60)
        n_min = patient_info["from_time"] % 60
        n_seq = patient_info["to_time"] - patient_info["from_time"]
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))

        p1,q1,p2,q2 = 1075,324,408,451
        x1,y1 = simulator_util.get_random_point(p1,q1, p2,q2)
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(location.get_patient_location(patient_info["patient"].id,
                                         "REGISTRATION",
                                         from_time,
                                         to_time,
                                         x1,y1 ,x2,y2))

        patient_info["patient"].x = x2
        patient_info["patient"].y = y2

    def get_registered_patient(self, cur_time):
        arr_registered_patients = []

        for i in range(0, len(self.arr_register)):
            if (cur_time == self.arr_register[i]["to_time"]):
                arr_registered_patients.append(self.arr_register[i])

        # remove registered patients from self.arr_register
        arr_temp = []
        for i in range(0, len(self.arr_register)):
            b_is_exist = False
            for j in range(0, len(arr_registered_patients)):
                if (self.arr_register[i]["patient"].id == arr_registered_patients[j]["patient"].id):
                    b_is_exist = True
                    break
            if (b_is_exist == False):
                arr_temp.append(self.arr_register[i])
        self.arr_register = arr_temp
        return arr_registered_patients

    def get_all(self):
        return self.arr_register