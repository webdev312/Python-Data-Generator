class Waiting:
    arr_waiting = []   

    def __init__(self):
        self.arr_waiting = []

    def make_patient_waiting_room(self, arr_patients):
        for i in range(0, len(arr_patients)):
            self.arr_waiting.append(arr_patients[i])

    def get_first_waiting_patient(self):
        first_patient = self.arr_waiting[0]
        self.arr_waiting = self.arr_waiting[1:]
        return first_patient

    def check_waiting_patient(self):
        number_of_patients = len(self.arr_waiting)
        if (number_of_patients > 0): return True
        else: return False

    def get_all(self):
        return self.arr_waiting