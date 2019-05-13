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
import datetime

from classes import class_patient
from classes import class_nurse
from classes import class_doctor
from classes import class_equip

from management import mgnt_register
from management import mgnt_triage
from management import mgnt_waiting
from management import mgnt_room
from management import mgnt_imaging
from management import mgnt_discharge

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

def get_tagstats_no_of_patients(data) :
    tag_stats = {}
    tag_stats["command_type"] = "Tag stats"
    
    command_data = {}
    command_data["stat_type"] = "No of patients"    
    command_data["stat_values"] = []

    for i in range(0, len(data)):
        command_data["stat_values"].append(data[i])
    
    tag_stats["command_data"] = command_data
    return tag_stats

def get_tagstats_no_of_assets(data) :
    tag_stats = {}
    tag_stats["command_type"] = "Tag stats"
    
    command_data = {}
    command_data["stat_type"] = "No of assets"    
    command_data["stat_values"] = []

    for i in range(0, len(data)):
        command_data["stat_values"].append(data[i])
    
    tag_stats["command_data"] = command_data
    return tag_stats

def get_tagstats_len_of_stay(data) :
    tag_stats = {}
    tag_stats["command_type"] = "Tag stats"
    
    command_data = {}
    command_data["stat_type"] = "Length of stay"    
    command_data["stat_values"] = []

    for i in range(0, len(data)):
        command_data["stat_values"].append(data[i])
    
    tag_stats["command_data"] = command_data
    return tag_stats
    
'''
Generate JSON feed
'''
json_feed = {}
tagdata = []
json_feed["tagdata"] = tagdata
#tagdata.append(send_tag_stat(database.get_patient_map(10)))
#tagdata.append(send_par_level(database.get_hour_par_map(14)))

'''
1. Iterate through 30 days
2. for each day assign random number of patient
3. Get all sequences patient moved in the day
4. Assign random coordinates in respective zones for each movement
5. Iterate through 3 and 4 for all patients any given day
'''

register_room = mgnt_register.Register()
triage_room = mgnt_triage.Triage()
waiting_room = mgnt_waiting.Waiting() # This is used like stack only right now
manage_room = mgnt_room.Rooms()
image_room = mgnt_imaging.Imaging()
discharge_room = mgnt_discharge.Discharge()

manage_nurse = class_nurse.Nurses()
manage_doctor = class_doctor.Doctors()
manage_equip = class_equip.Equips()

arr_tagstate_no_of_patients = []
arr_tagstate_no_of_assets = []
arr_tagstate_len_of_stay = []

for i in range(1, 30) :
    no_of_patients_for_day = random.randint(15,23)    
    no_of_curr_patients = 0
    no_of_discharged_patients = 0
    arr_patient_len_of_stay = []
    for j in range(0, 60*24) : # loop 24 hours
        '''
        Tag Stats
        '''
        if (j % 60 == 0):
            now = datetime.datetime.now()
            n_day = i
            n_hour = j / 60
            time_now = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(0))
            # Number of Patients
            tagstat_no_patient = {
                "time": time_now,
                "number of patients": no_of_curr_patients - no_of_discharged_patients
            }
            arr_tagstate_no_of_patients.append(tagstat_no_patient)
            
            # Number of Assets
            n_using_assets = manage_equip.get_number_of_using_equips()
            tagstat_no_assets = {
                "time": time_now,
                "number of assets": n_using_assets
            }
            arr_tagstate_no_of_assets.append(tagstat_no_assets)
        '''
        Tag Stats End
        '''

        # Check if register is finished
        arr_registered = register_room.get_registered_patient(j)
        # If there are registered patients, triage them
        if (len(arr_registered) > 0):
            triage_room.triage_patients(arr_registered, j, tagdata)

        # Check if triage is finished
        arr_triaged = triage_room.get_triaged_patient(j)
        # If there are triaged patients, make them to wait
        if (len(arr_triaged) > 0):
            waiting_room.make_patient_waiting_room(arr_triaged)

        # Check if there are patients did everything on room
        arr_completed_patients = manage_room.get_completed_assigned_patients(j)

        # If there is waiting patient and rooms are empty, move patient from waiting room to treatment room
        b_is_patient_waiting = waiting_room.check_waiting_patient()
        if (b_is_patient_waiting):
            b_is_empty_room = manage_room.is_available_room()
            if (b_is_empty_room):
                waiting_patient = waiting_room.get_first_waiting_patient()                
                empty_room = manage_room.get_room()
                manage_room.assign_room(waiting_patient["patient"], empty_room, i, j, tagdata)

        # If there is a patient that treated, move to image room or discharge
        if (len(arr_completed_patients) > 0):
            if (random.randint(0, 1)): image_room.image_patients(arr_completed_patients, j, tagdata)
            else: discharge_room.discharge_patients(arr_completed_patients, j, tagdata)

        # If there is a imaged patient, move to discharge
        arr_imaged_patients = image_room.get_imaged_patient(j)
        if (len(arr_imaged_patients) > 0):
            discharge_room.discharge_patients(arr_imaged_patients, j, tagdata)

        # If there is a discharged patient, calculate stay of length and number of patient
        arr_discharged_patients = discharge_room.get_discharged_patient(j)
        if (len(arr_discharged_patients) > 0):
            no_of_discharged_patients += len(arr_discharged_patients)
            for k in range(0, len(arr_discharged_patients)):
                for n in range(0, len(arr_patient_len_of_stay)):
                    if (arr_discharged_patients[k]["patient"].id == arr_patient_len_of_stay[n]["patient_id"]):
                        arr_patient_len_of_stay[n]["to_time"] = j
                        break

        '''
        Alert Modules like Nurses, Doctors and IV Pumps
        '''
        '''
        Nurse Alert Module
        '''
        # Check if there is a patient that has "waiting nurse" state
        arr_pt_waiting_nurse = manage_room.get_patient_waiting_nurse()
        if (len(arr_pt_waiting_nurse) > 0):
            # Check if there is a free nurse
            b_is_free_nurse = manage_nurse.is_available_nurse()
            if (b_is_free_nurse):
                for k in range(0, len(arr_pt_waiting_nurse)):
                    b_is_free_nurse = manage_nurse.is_available_nurse()
                    if not (b_is_free_nurse): break
                    # Call a nurse
                    free_nurse = manage_nurse.call_nurse()
                    manage_room.set_patient_meet_nurse(arr_pt_waiting_nurse[k], free_nurse, tagdata, j)
        # Check if there is a patient that finish meeting nurse
        arr_finished_nurse = manage_room.get_patient_finished_nurse(j)
        for k in range(0, len(arr_finished_nurse)):
            manage_nurse.return_nurse(arr_finished_nurse[k]["nurse"])

        
        '''
        Doctor Alert Module
        '''
        # Check if there is a patient that has "waiting doctor" state
        arr_pt_waiting_doctor = manage_room.get_patient_waiting_doctor()
        if (len(arr_pt_waiting_doctor) > 0):
            # Check if there is a free doctor
            b_is_free_doctor = manage_doctor.is_available_doctor()
            if (b_is_free_doctor):
                for k in range(0, len(arr_pt_waiting_doctor)):
                    b_is_free_doctor = manage_doctor.is_available_doctor()
                    if not (b_is_free_doctor): break
                    # Call a doctor
                    free_doctor = manage_doctor.call_doctor()
                    manage_room.set_patient_meet_doctor(arr_pt_waiting_doctor[k], free_doctor, tagdata, j)
        # Check if there is a patient that finish meeting doctor
        arr_finished_doctor = manage_room.get_patient_finished_doctor(j)
        for k in range(0, len(arr_finished_doctor)):
            manage_doctor.return_doctor(arr_finished_doctor[k]["doctor"])

        
        '''
        Equipment Alert Module
        '''
        # Check if there is a patient that has "waiting equip" state
        arr_pt_waiting_equip = manage_room.get_patient_waiting_equip()
        if (len(arr_pt_waiting_equip) > 0):
            # Check if there is a free equip
            b_is_free_equip = manage_equip.is_available_equip()
            if (b_is_free_equip):
                for k in range(0, len(arr_pt_waiting_equip)):
                    b_is_free_equip = manage_equip.is_available_equip()
                    if not (b_is_free_equip): break
                    # Call a equip
                    free_equip = manage_equip.call_equip()
                    manage_room.set_patient_meet_equip(arr_pt_waiting_equip[k], free_equip, tagdata, j)
        # Check if there is a patient that finish meeting equip
        arr_finished_equip = manage_room.get_patient_finished_equip(j)
        for k in range(0, len(arr_finished_equip)):
            manage_equip.return_equip(arr_finished_equip[k]["equip"])
        '''
        Alert Modules End
        '''

        if (no_of_curr_patients < no_of_patients_for_day) :
            # There is an opportunity that new patient would be income every 5 mins
            b_is_new_patient = random.randint(0, 1) if (j % 5 == 0) and (j > 0) else 0
            if (b_is_new_patient == 0) : continue
            no_of_curr_patients += 1

            # create new patient
            uuid = str(i) + "_" + str(no_of_curr_patients)
            patient = class_patient.Patient(uuid)
            # register new patient
            register_room.register_patient(patient, i, j, tagdata)
            # register regist time for length of stay
            arr_patient_len_of_stay.append({
                "patient_id": uuid,
                "from_time": j,
                "to_time": 0
            })

    # calculate len_of_stay daily for every an hour
    for j in range(0, 24):
        len_of_stay_cur= 0
        len_of_stay_prev = 0
        for k in range(0, len(arr_patient_len_of_stay)):
            if (j*60 <= arr_patient_len_of_stay[k]["to_time"]):
                if (j*60 >= arr_patient_len_of_stay[k]["from_time"]):
                    len_of_stay_cur += j*60 - arr_patient_len_of_stay[k]["from_time"]
            else:
                len_of_stay_cur += arr_patient_len_of_stay[k]["to_time"] - arr_patient_len_of_stay[k]["from_time"]
        if (j > 0):
            for k in range(0, len(arr_patient_len_of_stay)):
                if ((j-1)*60 <= arr_patient_len_of_stay[k]["to_time"]):
                    if ((j-1)*60 >= arr_patient_len_of_stay[k]["from_time"]):
                        len_of_stay_prev += (j-1)*60 - arr_patient_len_of_stay[k]["from_time"]
                else:
                    len_of_stay_prev += arr_patient_len_of_stay[k]["to_time"] - arr_patient_len_of_stay[k]["from_time"]
        len_of_stay = len_of_stay_cur - len_of_stay_prev
        now = datetime.datetime.now()
        n_day = i
        n_hour = j
        time_now = datetime.datetime(int(now.year), int(now.month), int(n_day), int(n_hour), int(0))
        # Number of Patients
        tagstat_length_stay = {
            "time": time_now,
            "length of stay": len_of_stay
        }
        arr_tagstate_len_of_stay.append(tagstat_length_stay)



tagdata.append(get_tagstats_no_of_patients(arr_tagstate_no_of_patients))
tagdata.append(get_tagstats_no_of_assets(arr_tagstate_no_of_assets))
tagdata.append(get_tagstats_len_of_stay(arr_tagstate_len_of_stay))

json_data = json.dumps(json_feed, default=simulator_util.datetime_to_string)
with open('data.json', 'w') as outfile:
    outfile.write(json_data)