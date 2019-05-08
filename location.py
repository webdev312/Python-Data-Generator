import database

'''
Get present location of patient in hospital
'''
def get_patient_location(patient_id, sequence, from_time, to_time, from_x, from_y, to_x, to_y, spec_id = "") :
    tag_movement = {}
    tag_movement["command_type"] = "Tag movement"
    
    command_data = {}
    command_data["patient_id"] = patient_id
    
    command_data["sequence"] = sequence
    
    command_data["from_time"] = from_time
    command_data["to_time"] = to_time
    
    command_data["from_x"] = from_x
    command_data["from_y"] = from_y

    command_data["to_x"] = to_x
    command_data["to_y"] = to_y
    
    command_data["zone"] = database.get_zone_by_sequence(sequence, spec_id)
    
    tag_movement["command_data"] = command_data
    return tag_movement

