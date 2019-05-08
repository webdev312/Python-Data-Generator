class Nurses:
    arr_nurses = []

    def __init__(self):
        self.arr_nurses = ["Nurse1", "Nurse2", "Nurse3", "Nurse4"]
    
    def is_available_nurse(self):
        if (len(self.arr_nurses) > 0):
            return True
        return False
    
    def call_nurse(self):
        available_nurse = self.arr_nurses[0]
        self.arr_nurses = self.arr_nurses[1:]
        return available_nurse

    def return_nurse(self, nurse):
        self.arr_nurses.append(nurse)

    def get_all_nurses(self):
        return self.arr_nurses