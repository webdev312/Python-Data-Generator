import random
import datetime
import math

import location
import simulator_util
import alert

class Imaging:
    # Imaging JSON Format
    '''
    {
        patient: patient object
        day: 1
        from_time: 130 (minutes)
        to_time: 145 (minutes)
    }
    '''
    arr_image = []   

    def __init__(self):
        self.arr_image = []

    def image_patients(self, arr_patients, mins, tagdata):
        n_delay = random.randint(60,120)
        n_from = mins
        n_to = mins + n_delay

        for i in range(0, len(arr_patients)):
            arr_patients[i]["from_time"] = n_from
            arr_patients[i]["to_time"] = n_to
            self.save_to_tagdata(tagdata, arr_patients[i])
            self.arr_image.append(arr_patients[i])            

    def save_to_tagdata(self, tagdata, patient_info):
        now = datetime.datetime.now()
        n_day = patient_info["day"]
        n_hour = math.floor(patient_info["from_time"] / 60)
        n_min = patient_info["from_time"] % 60
        n_seq = patient_info["to_time"] - patient_info["from_time"]
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))

        x1,y1 = patient_info["patient"].x,patient_info["patient"].y
        x2,y2 = simulator_util.get_point_by_position("image")
        tagdata.append(location.get_patient_location(patient_info["patient"].id,
                                         "IMAGING",
                                         from_time,
                                         to_time,
                                         x1,y1, x2,y2))
        tagdata.append(alert.get_image_alert(patient_info["patient"].id, from_time, to_time, n_seq, x2, y2))
        
        patient_info["patient"].x = x2
        patient_info["patient"].y = y2

    def get_imaged_patient(self, cur_time):
        arr_imaged_patients = []

        for i in range(0, len(self.arr_image)):
            if (cur_time == self.arr_image[i]["to_time"]):
                arr_imaged_patients.append(self.arr_image[i])

        # remove registered patients from self.arr_triage
        arr_temp = []
        for i in range(0, len(self.arr_image)):
            b_is_exist = False
            for j in range(0, len(arr_imaged_patients)):
                if (self.arr_image[i]["patient"].id == arr_imaged_patients[j]["patient"].id):
                    b_is_exist = True
                    break
            if (b_is_exist == False):
                arr_temp.append(self.arr_image[i])
        self.arr_image = arr_temp
        return arr_imaged_patients

    def get_all(self):
        return self.arr_image