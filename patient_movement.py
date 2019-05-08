#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:13:42 2019

@author: anmol
"""
import json
import database
import simulator_util
import random

import class_patient
import mgnt_register
import mgnt_triage
import mgnt_waiting
import mgnt_room
import mgnt_imaging
import mgnt_discharge

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

'''
1. Iterate through 30 days
2. for each day assign random number of patient
3. Get all sequences patient moved in the day
4. Assign random coordinates in respective zones for each movement
5. Iterate through 3 and 4 for all patients any given day
'''

register_room = mgnt_register.Register()
triage_room = mgnt_triage.Triage()
waiting_room = mgnt_waiting.Waiting()
manage_room = mgnt_room.Rooms()
image_room = mgnt_imaging.Imaging()
discharge_room = mgnt_discharge.Discharge()

for i in range(1, 2) :
    # no_of_patients_for_day = random.randint(15,23)
    no_of_patients_for_day = 10
    no_of_curr_patients = 0
    for j in range(0, 60*24) : # loop 24 hours
        arr_registered = register_room.get_registered_patient(j)
        if (len(arr_registered) > 0):
            triage_room.triage_patients(arr_registered, j, tagdata)

        arr_triaged = triage_room.get_triaged_patient(j)
        if (len(arr_triaged) > 0):
            waiting_room.make_patient_waiting_room(arr_triaged)

        arr_completed_patients = manage_room.get_completed_assigned_patients(j)

        b_is_patient_waiting = waiting_room.check_waiting_patient()
        if (b_is_patient_waiting):
            b_is_empty_room = manage_room.is_available_room()
            if (b_is_empty_room):
                waiting_patient = waiting_room.get_first_waiting_patient()                
                empty_room = manage_room.get_room()
                manage_room.assign_room(waiting_patient["patient"], empty_room, i, j, tagdata)

        if (len(arr_completed_patients) > 0):
            if (random.randint(0, 1)): image_room.image_patients(arr_completed_patients, j, tagdata)
            else: discharge_room.discharge_patients(arr_completed_patients, j, tagdata)

        arr_imaged_patients = image_room.get_imaged_patient(j)
        if (len(arr_imaged_patients) > 0):
            discharge_room.discharge_patients(arr_imaged_patients, j, tagdata)

        arr_discharged_patients = discharge_room.get_discharged_patient(j)

        if (no_of_curr_patients < no_of_patients_for_day) :
            # There is an opportunity that new patient would be income every 5 mins
            b_is_new_patient = random.randint(0, 1) if (j % 5 == 0) else 0
            if (b_is_new_patient == 0) : continue
            no_of_curr_patients += 1

            # create new patient
            patient = class_patient.Patient(no_of_curr_patients)
            # register new patient
            register_room.register_patient(patient, i, j, tagdata)
        

json_data = json.dumps(json_feed, default=simulator_util.datetime_to_string)
with open('data.json', 'w') as outfile:
    outfile.write(json_data)