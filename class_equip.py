class Equips:
    arr_equips = []

    def __init__(self):
        self.arr_equips = ["IV Pump1", "IV Pump2", "IV Pump3", "IV Pump4", "IV Pump5", "IV Pump6", "IV Pump7", "IV Pump8", "IV Pump9", "IV Pump10"]
    
    def is_available_equip(self):
        if (len(self.arr_equips) > 0):
            return True
        return False
    
    def call_equip(self):
        available_equip = self.arr_equips[0]
        self.arr_equips = self.arr_equips[1:]
        return available_equip

    def return_equip(self, equip):
        self.arr_equips.append(equip)

    def get_all_equips(self):
        return self.arr_equips