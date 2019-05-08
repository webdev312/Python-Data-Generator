def get_nurse_alert(patient_id, from_time, to_time, delay, nurse, room) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "<div>Nurse in Room</div><p>meet " + nurse + " : " + repr(delay) + " Mins</p>"
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_doctor_alert(patient_id, from_time, to_time, delay, doctor, room) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "<div>Doctor in Room</div><p>meet " + doctor + " : " + repr(delay) + " Mins</p>"
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_equip_alert(patient_id, from_time, to_time, delay, equip, room) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "<div>IV Pump in Room</div><p>infusion " + equip + " : " + repr(delay) + " Mins</p>"
    
    tag_movement["command_data"] = command_data
    return tag_movement