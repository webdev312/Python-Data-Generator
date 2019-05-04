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
def get_patient_location(patient_id, sequence, from_time, to_time, from_x, from_y, to_x, to_y) :
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
    
    command_data["zone"] = database.get_zone(to_x, to_y)
    
    tag_movement["command_data"] = command_data
    return tag_movement
    

'''
Generate JSON feed
'''
json_feed = {}
tagdata = []
json_feed["tagdata"] = tagdata
tagdata.append(send_tag_stat(database.get_patient_map(10)))
tagdata.append(send_par_level(database.get_hour_par_map(14)))

'''
1. Iterate through 30 days
2. for each day assign random number of patient
3. Get all sequences patient moved in the day
4. Assign random coordinates in respective zones for each movement
5. Iterate through 3 and 4 for all patients any given day
'''
for i in range(1,2) :
    no_of_patients_for_day = random.randint(15,23)
    patient_times = simulator_util.get_patient_times(no_of_patients_for_day, i)
    for i in range(no_of_patients_for_day) :
        p1,q1,p2,q2 = 1075,324,408,451
        x1,y1 = simulator_util.get_random_point(p1,q1, p2,q2)
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(i,
                                         "REGISTRATION",
                                         patient_times[i][0],
                                         patient_times[i][1],
                                         x1,y1 ,x2,y2))
        
        p1,q1,p2,q2 = 1483,324,902,451
        x1,y1 = x2,y2
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(i,
                                         "TRIAGE",
                                         patient_times[i][2],
                                         patient_times[i][3],
                                         x1,y1, x2,y2))
        
        p1,q1,p2,q2 = 138,324,937,452
        x1,y1 = x2,y2
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(i,
                                         "ROOM",
                                         patient_times[i][4],
                                         patient_times[i][5],
                                         x1,y1, x2,y2))
        
        if(patient_times[i][6] != 0) :
            p1,q1,p2,q2 = 138,324,937,452
            x1,y1 = x2,y2
            x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
            tagdata.append(get_patient_location(i,
                                             "IMAGING",
                                             patient_times[i][6],
                                             patient_times[i][7],
                                             x1,y1, x2,y2))
            
        p1,q1,p2,q2 = 138,324,937,452
        x1,y1 = x2,y2
        x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
        tagdata.append(get_patient_location(i,
                                            "DISCHARGE",
                                            patient_times[i][8],
                                            patient_times[i][9],
                                            x1,y1, x2,y2))

json_data = json.dumps(json_feed, default=simulator_util.datetime_to_string)
with open('data.json', 'w') as outfile:
    outfile.write(json_data)
print(json_data)