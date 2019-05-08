class Doctors:
    arr_doctors = []

    def __init__(self):
        self.arr_doctors = ["Doctor1", "Doctor2", "Doctor3", "Doctor4"]
    
    def is_available_doctor(self):
        if (len(self.arr_doctors) > 0):
            return True
        return False
    
    def call_doctor(self):
        available_doctor = self.arr_doctors[0]
        self.arr_doctors = self.arr_doctors[1:]
        return available_doctor

    def return_doctor(self, doctor):
        self.arr_doctors.append(doctor)

    def get_all_doctors(self):
        return self.arr_doctors