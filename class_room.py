class RoomManagement:
    arr_rooms = []

    def __init__(self):
        self.arr_rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6"]
    
    def is_available_room(self):
        if (len(self.arr_rooms) > 0):
            return True
        return False
    
    def get_room(self):
        available_room = self.arr_rooms[0]
        self.arr_rooms = self.arr_rooms[1:]
        return available_room

    def empty_room(self, room):
        self.arr_rooms.append(room)

    def get_all_rooms(self):
        return self.arr_rooms