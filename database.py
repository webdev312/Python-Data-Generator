#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:05:41 2019

@author: anmol
"""

def get_tag_name(tag_id) :
    pump_map = { 
        1 : "IV PUMP 1", 
        2 : "Surgital Tools 1", 
        3 : "Surgical Tray 2",
        4 : "IV PUMP 2",
        5 : "IV PUMP 3"
    }
    return pump_map.get(tag_id, "Error")


def get_svg(tag_id) :
    pump_image_map = { 
        1 : "ivpump1.svg", 
        2 : "surgicaltools1.svg", 
        3 : "surgicaltray2.svg",
        4 : "ivpump2.svg",
        5 : "ivpum3.svg"
    }
    return pump_image_map.get(tag_id, "Error")

def get_popuptext(tag_id) :
    return "<h2>Pump : " + str(get_tag_name(tag_id)) + "</h2><p>Tag Id : " + str(tag_id) + "</p>"

def get_zone(to_x, to_y) :
    return "Room1"

def get_hour_par_map(hour) :
    if hour >= 6 :
        hour_range = reversed(range(hour))
    else :
        hour_range = [hour, hour-1, hour-2, hour-3, hour-4, hour-5, hour-6]
        
    hour_range_map = {}
    for hour in hour_range :
        hour_range_map[hour] = hour*2
    return hour_range_map

def get_patient_map(hour) :
    if hour >= 6 :
        hour_range = reversed(range(hour))
    else :
        hour_range = [hour, hour-1, hour-2, hour-3, hour-4, hour-5, hour-6]
        
    hour_range_map = {}
    for hour in hour_range :
        hour_range_map[hour] = hour*5
    return hour_range_map