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

def send_tag_movement(tag_id, sequence, from_time, to_time, from_x, from_y, to_x, to_y) :
    tag_movement = {}
    tag_movement["command_type"] = "Tag movement"
    
    command_data = {}
    command_data["tag_id"] = tag_id
    command_data["tag"] = database.get_tag_name(tag_id)
    command_data["icon"] = database.get_svg(tag_id)
    command_data["popup_text"] = database.get_popuptext(tag_id)
    
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
    

json_feed = {}
tagdata = []
json_feed["tagdata"] = tagdata
tagdata.append(send_tag_stat(database.get_patient_map(10)))
tagdata.append(send_par_level(database.get_hour_par_map(14)))

zones = ["REGISTRATION", "PRE-OP", "PROCEDURE", "STERIZATION", "HALLWAY"]

for i in range(1,6) :
    p1,q1,p2,q2 = 1075,324,408,451
    x1,y1 = simulator_util.get_random_point(p1,q1, p2,q2)
    x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
    tagdata.append(send_tag_movement(i,"REGISTRATION",14,15,x1,y1 ,x2,y2))
    
    p1,q1,p2,q2 = 1483,324,902,451
    x1,y1 = x2,y2
    x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
    tagdata.append(send_tag_movement(i,"PRE-OP",15,16,x1,y1, x2,y2))
    
    p1,q1,p2,q2 = 138,324,937,452
    x1,y1 = x2,y2
    x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
    tagdata.append(send_tag_movement(i,"PROCEDURE",17,18,x1,y1, x2,y2))
    
    p1,q1,p2,q2 = 138,324,937,452
    x1,y1 = x2,y2
    x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
    tagdata.append(send_tag_movement(i,"STERIZATION",18,19,x1,y1, x2,y2))
    
    p1,q1,p2,q2 = 138,324,937,452
    x1,y1 = x2,y2
    x2,y2 = simulator_util.get_random_point(p1,q1, p2,q2)
    tagdata.append(send_tag_movement(i,"HALLWAY",19,20,x1,y1, x2,y2))

with open('data.json', 'w') as outfile:
    json.dump(json_feed, outfile)
print(json.dumps(json_feed))