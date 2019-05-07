#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:13:42 2019

@author: anmol
"""
import datetime
import json
import database
import simulator_util
import random
import json

import math
import class_nurse
import class_room

'''
Generate stat for last few hours
'''
def send_tag_stat(hour_patient_map) :
    tag_stat = {}
    tag_stat["command_type"] = "Tag stats"
    
    command_data = {}
    command_data["stat_type"] = "No of patients"
    
    stat_values = []
    for key, value in hour_patient_map.items():
        item = {}
        item["No of Patients"] = key
        item["time"] = value
        if value < 100 :
            stat_level = "Low"
        elif value < 150 :
            stat_level = "Normal"
        else :
            stat_level = "High"
        item["stat_level"] = stat_level
        stat_values.append(item)
    command_data["stat_values"] = stat_values
    
    tag_stat["command_data"] = command_data
    return tag_stat

'''
 Generate par level for next few hours
'''
def send_par_level(hour_par_map) :
    tag_par_level = {}
    tag_par_level["command_type"] = "Tag Par level"
    
    command_data = {}
    command_data["stat_type"] = "Par level"
    
    stat_values = []
    for key, value in hour_par_map.items():
        item = {}
        item["hour"] = key
        item["par_lavel"] = value
        if value < 5 :
            stat_level = "Low"
        elif value < 10 :
            stat_level = "Medium"
        else :
            stat_level = "High"
        item["stat_level"] = stat_level
        stat_values.append(item)
    command_data["stat_values"] = stat_values
    
    tag_par_level["command_data"] = command_data
    return tag_par_level

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
    

# initialize Room class
rooms = class_room.RoomManagement()

def process_event(data) :
    event_type = data["type"]
    day_of_month = data["day"]
    n_hour = math.floor(data["from"] / 60)
    n_min = data["from"] % 60    

    now = datetime.datetime.now()
    from_time = datetime.datetime(int(now.year), 
                                   int(now.month),
                                   int(day_of_month),
                                   int(n_hour),
                                   int(n_min))

    if (event_type == "TRIAGE") :
        n_seq = data["from"] + random.randint(20,60)
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))

        p1,q1,p2,q2 = 1483,324,902,451
        x1,y1 = data["p_x"],data["p_y"]
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        # save previous x2, y2 position for next event
        data["p_x"] = x2
        data["p_y"] = y2
        tagdata.append(get_patient_location(data["id"],
                                         "TRIAGE",
                                         from_time,
                                         to_time,
                                         x1,y1, x2,y2))
    elif (event_type == "ROOM") :
        room_id = data["room_id"]
        n_seq = data["from"] + random.randint(60,180)
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))

        p1,q1,p2,q2 = database.get_room_position(room_id)
        x1,y1 = data["p_x"],data["p_y"]
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(data["id"],
                                         "ROOM",
                                         from_time,
                                         to_time,
                                         x1,y1, x2,y2,
                                         room_id))

def register_next_event(data) :
    event_type = data["type"]

    n_id = data["id"]
    n_day = data["day"]    

    if (event_type == "TRIAGE") :
        n_from = data["from"] + random.randint(20,180)
        # Check if there is available ROOM
        if (rooms.is_available_room()) :
            n_room_number = rooms.get_room()
            arr_events.append({"type": "ROOM", "id": n_id, "room_id": n_room_number, "day": n_day, "from": n_from, "p_x": data["p_x"], "p_y": data["p_y"]})
        else:
            arr_events.append({"type": "ROOM", "id": n_id, "room_id": "NOROOM", "day": n_day, "from": n_from, "p_x": data["p_x"], "p_y": data["p_y"]})
    elif (event_type == "ROOM") :
        rooms.empty_room(data["room_id"])

'''
Generate JSON feed
'''
json_feed = {}
tagdata = []
json_feed["tagdata"] = tagdata
#tagdata.append(send_tag_stat(database.get_patient_map(10)))
#tagdata.append(send_par_level(database.get_hour_par_map(14)))

'''
1. 4 Nurses, 4 Doctors, 10 IV Pumps
2. 6 Rooms
3. Every patient can meet only 1 Nurse, 1 Doctor, 1 IV Pumps
4. Every patient should wait if there is no remain Nurses or Doctors
'''
arr_nurses = ["Nurse1", "Nurse2", "Nurse3", "Nurse4"]
arr_doctors = ["Doctor1", "Doctor2", "Doctor3", "Doctor4"]
arr_pumps = ["IV Pump1", "IV Pump2", "IV Pump3", "IV Pump4", "IV Pump5", "IV Pump6", "IV Pump7", "IV Pump8", "IV Pump9", "IV Pump10"]
arr_events = []

'''
1. Iterate through 30 days
2. for each day assign random number of patient
3. Get all sequences patient moved in the day
4. Assign random coordinates in respective zones for each movement
5. Iterate through 3 and 4 for all patients any given day
'''



for i in range(1, 2) :
    # no_of_patients_for_day = random.randint(15,23)
    no_of_patients_for_day = 10
    no_of_curr_patients = 0
    for j in range(0, 60*24) : # loop 24 hours
        if (no_of_curr_patients >= no_of_patients_for_day) and (len(arr_events) == 0): 
            print ("full charged : " + repr(j))
            break

        # Check if there is an registered event
        if (len(arr_events) > 0) :
            arr_events_temp = []
            # Process all avilable events and update events list by new events like TRIAGE, ROOM, ... After REGISTRATION
            for k in range(0, len(arr_events)) :
                if (arr_events[k]["from"] == j) :
                    available_event = arr_events[k]
                    process_event(available_event)
                    register_next_event(available_event)
            # Remove processed events from updated events list.
            for k in range(0, len(arr_events)) :
                if (arr_events[k]["from"] != j) :
                    arr_events_temp.append(arr_events[k])
            arr_events = arr_events_temp

        if (no_of_curr_patients >= no_of_patients_for_day) : continue

        # There is an opportunity that new patient would be income every 5 mins
        b_is_new_patient = random.randint(0, 1) if (j % 5 == 0) else 0
        if (b_is_new_patient == 0) : continue
        no_of_curr_patients += 1

        # append REGISTRATION to tag_data
        now = datetime.datetime.now()
        n_day = i
        n_hour = math.floor(j / 60)
        n_min = j % 60
        n_seq = random.randint(10,20)
        from_time = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(n_min))
        to_time = from_time + datetime.timedelta(minutes = int(n_seq))    

        p1,q1,p2,q2 = 1075,324,408,451
        x1,y1 = simulator_util.get_random_point(p1,q1, p2,q2)
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(no_of_curr_patients,
                                         "REGISTRATION",
                                         from_time,
                                         to_time,
                                         x1,y1 ,x2,y2))

        # register TRIAGE event at REGISTRATION to_time
        arr_events.append({"type": "TRIAGE", "id": no_of_curr_patients, "day": i, "from": j + n_seq, "p_x": x2, "p_y": y2})

        

# for i in range(1,2) :
#     no_of_patients_for_day = random.randint(15,23)
#     patient_times = simulator_util.get_patient_times(no_of_patients_for_day, i)
#     for i in range(no_of_patients_for_day) :
#         p1,q1,p2,q2 = 1075,324,408,451
#         x1,y1 = simulator_util.get_random_point(p1,q1, p2,q2)
#         x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
#         tagdata.append(get_patient_location(i,
#                                          "REGISTRATION",
#                                          patient_times[i][0],
#                                          patient_times[i][1],
#                                          x1,y1 ,x2,y2))
        
#         p1,q1,p2,q2 = 1483,324,902,451
#         x1,y1 = x2,y2
#         x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
#         tagdata.append(get_patient_location(i,
#                                          "TRIAGE",
#                                          patient_times[i][2],
#                                          patient_times[i][3],
#                                          x1,y1, x2,y2))

#         p1,q1,p2,q2 = 138,324,937,452
#         x1,y1 = x2,y2
#         x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
#         tagdata.append(get_patient_location(i,
#                                          "ROOM",
#                                          patient_times[i][4],
#                                          patient_times[i][5],
#                                          x1,y1, x2,y2))
        
#         if(patient_times[i][6] != 0) :
#             p1,q1,p2,q2 = 138,324,937,452
#             x1,y1 = x2,y2
#             x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
#             tagdata.append(get_patient_location(i,
#                                              "IMAGING",
#                                              patient_times[i][6],
#                                              patient_times[i][7],
#                                              x1,y1, x2,y2))
            
#         p1,q1,p2,q2 = 138,324,937,452
#         x1,y1 = x2,y2
#         x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
#         tagdata.append(get_patient_location(i,
#                                             "DISCHARGE",
#                                             patient_times[i][8],
#                                             patient_times[i][9],
#                                             x1,y1, x2,y2))

json_data = json.dumps(json_feed, default=simulator_util.datetime_to_string)
with open('data.json', 'w') as outfile:
    outfile.write(json_data)
# print(json_data)

# nurses = class_nurse.Nurses()
# print (nurses.get_all_nurses())
# print (nurses.is_available_nurse())
# print (nurses.call_nurse())
# print (nurses.get_all_nurses())
# print (nurses.return_nurse("Nurse1"))
# print (nurses.get_all_nurses())