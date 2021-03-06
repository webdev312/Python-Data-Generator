def get_registration_alert(patient_id, from_time, to_time, delay, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data= {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = "registration"

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in registration"
    command_data["alert_text"] = "Registration (" + str(delay) + " mins)," + str(from_time) + ""
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_triage_alert(patient_id, from_time, to_time, delay, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = "triage"

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in triage"
    command_data["alert_text"] = "Triage (" + str(delay) + " mins)," + str(from_time) + ""
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_nurse_alert(patient_id, from_time, to_time, delay, nurse, room, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "Nurse in Room,meet " + nurse + " : " + repr(delay) + " mins"
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_doctor_alert(patient_id, from_time, to_time, delay, doctor, room, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "Doctor in Room,meet " + doctor + " : " + repr(delay) + " mins"
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_equip_alert(patient_id, from_time, to_time, delay, equip, room, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = room

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in room"
    command_data["alert_text"] = "" + equip + " in Room,Infusion : " + repr(delay) + " mins"
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_image_alert(patient_id, from_time, to_time, delay, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = "image"

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in image"
    command_data["alert_text"] = "Imaging (" + str(delay) + " mins)," + str(from_time) + ""
    
    tag_movement["command_data"] = command_data
    return tag_movement

def get_discharge_alert(patient_id, from_time, to_time, delay, x, y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag alert"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["zone"] = "discharge"

    command_data["x"] = x
    command_data["y"] = y

    command_data["alert_type"] = "patient in discharge"
    command_data["alert_text"] = "Discharge (" + str(delay) + " mins)," + str(from_time) + ""
    
    tag_movement["command_data"] = command_data
    return tag_movement
