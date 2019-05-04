#!/usr/bin/env python3

#- * -coding: utf - 8 - * -
"""
Created on Thu May 2 14: 49: 22 2019

@author: anmol
"""
import random
import datetime as dt

'''
Get a random point between two coordinates
'''
def get_random_point(x1, y1, x2, y2):
    midX = x1 + (x2 - x1) / 2
    midY = y1 - (y1 - y2) / 2
    width = abs(x2 - x1)
    height = abs(y1 - y2)
    if (width == 0):
      width = 1
    if (height == 0):
      height = 1
    
    if (round(width) <= 0):
      wd = 1
    else :
      if (round(width) - 20 <= 0):
          wd = 1
      else :
          wd = round(width) - 10
    if (round(height) <= 0):
        ht = 1
    else :
        if (round(height) - 30 <= 0):
            ht = 1
        else :
            ht = round(height) - 30
    region = random.randint(1, 4)
    coordX = 0
    coordY = 0
    if (wd == 1):
      wd = 2
    if (ht == 1):
      ht = 2
    randWd = random.randint(0,round(wd / 2))
    randHt = random.randint(0,round(ht / 2))
    if region == 1:
      coordX = midX - randWd
      coordY = midY + randHt
    elif (region == 2):
      coordX = midX + randWd
      coordY = midY + randHt
    elif (region == 3):
      coordX = midX - randWd
      coordY = midY - randHt
    elif (region == 4):
      coordX = midX + randWd
      coordY = midY - randHt
    else :
      coordX = x1 + random.randint(0,wd)
      coordY = y1 - 20 - random.randint(0,ht)
    coordX = coordX - 10;
    coordY = coordY - 10;
    return coordX, coordY

'''
Generate patient times for day
'''
def get_patient_times(no_of_patients, day_of_month) :
    patient_times = {}
    now = dt.datetime.now()
    for i in range(no_of_patients) :
        sequences = get_sequence_for_patient(i+1)
        reg_in_hr = i
        reg_in_min = random.randint(0,59)
        
        reg_in_time = dt.datetime(int(now.year), 
                                   int(now.month),
                                   int(day_of_month),
                                   int(reg_in_hr),
                                   int(reg_in_min))
        reg_out_time = reg_in_time + dt.timedelta(minutes = int(sequences[0]))
        
        triage_in_time = reg_out_time
        triage_out_time = triage_in_time + dt.timedelta(minutes = int(sequences[1]))
        
        room_in_time = triage_out_time
        room_out_time = room_in_time + dt.timedelta(minutes = int(sequences[2]))
        
        if sequences[3] !=0 :
            imaging_in_time = room_out_time
            imaging_out_time = imaging_in_time + dt.timedelta(minutes = int(sequences[3]))
            
            discharge_in_time = imaging_out_time
            discharge_out_time = discharge_in_time + dt.timedelta(minutes = int(sequences[4]))
        else :
            imaging_in_time = 0
            imaging_out_time = 0
            
            discharge_in_time = room_out_time
            discharge_out_time = discharge_in_time + dt.timedelta(minutes = int(sequences[4]))
        patient_times[i] = [reg_in_time, reg_out_time,
                   triage_in_time, triage_out_time,
                   room_in_time, room_out_time,
                   imaging_in_time, imaging_out_time,
                   discharge_in_time, discharge_out_time]
    return patient_times
        
'''
Generate sequence patient would spend in hospital
'''
def get_sequence_for_patient(patient_id) :
    zones = ["REGISTRATION", "TRIAGE", "ROOM", "IMAGING", "DISCHARGE"]
    
    min_in_registration = random.randint(10,20)
    min_in_triage = random.randint(20,60)
    min_in_room = random.randint(60,180)
    min_in_imaging = random.randint(60,120)
    min_in_discharge = random.randint(10,20)
    
    if (patient_id%3 == 0) :
        return [min_in_registration, min_in_triage, min_in_room, 0, min_in_discharge]
    else :
        return [min_in_registration, min_in_triage, min_in_room, min_in_imaging, min_in_discharge]
    
'''
Convert datetime to string for json conversion
'''
def datetime_to_string(in_out_time):
    if isinstance(in_out_time, dt.datetime):
        return in_out_time.__str__()
    
# print(json.dumps(get_patient_times(3, 1), default = datetime_to_string))
print(get_patient_times(3, 1))