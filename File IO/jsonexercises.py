# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading and printing a JSON object
# Author: Lisa Nydick
# Last Modified: 09/21/2019
#####################################

import json
import csv
from datetime import datetime

def main():
    infile = 'capital_projects_partial.json'
    jsonoutfile = 'capital_projects_out.json'
    logfile = 'capital_projects_log.csv'
    
    projects_json = {}
    projects_list = []
    unique_area_list = []
    unique_status_list = []
    unique_asset_type_list = []
           
    projects_json = read_json_file(infile)
    projects_list, unique_area_list, unique_status_list, unique_asset_type_list = process_json_dict(projects_json, logfile)
    print_projects(projects_list)
    write_json_file(jsonoutfile, projects_list)
    

def read_json_file(infile):
    with open(infile, 'r') as projects:
        projects_json = json.load(projects)
    return projects_json

def process_json_dict(projects_json, logfile):
    projects_list = []
    unique_area_list = []
    unique_status_list = []
    unique_asset_type_list = []
        
    features_list = projects_json['features']
               
    for i in range(len(features_list)):
        feature_dict = features_list[i]
        properties_dict = feature_dict['properties']
        area = properties_dict['area']
        if area == '':
            logMalformedProject(logfile, properties_dict, 'area')
        else:
            #add unique values for area, status, and asset_types to their respective lists
            unique_area_list = add_unique_value_to_list(unique_area_list, area)
            status = properties_dict['status']
            unique_status_list = add_unique_value_to_list(unique_status_list, status)
            asset_type = properties_dict['asset_type']
            unique_asset_type_list = add_unique_value_to_list(unique_asset_type_list, asset_type)
            
            #append the project to the projects list
            projects_list.append(properties_dict)
        
    return(projects_list, unique_area_list, unique_status_list, unique_asset_type_list)
        
            
def print_projects(projects_list):
    for i in range(len(projects_list)):
        d = projects_list[i]
        print(f'{"PROJECT":<20}{d["name"]}')
          
        for k, v, in d.items():
            print(f'{k:<20}{":":<1} {str(v)}')
        print()    
             
def write_json_file(outfile, projects_list):
    with open(outfile, 'w') as projects:
        #json.dump(projects_list, projects)
        #make a string with indents out of a json object
        s = json.dumps(projects_list, indent=4)
        projects.write(s)
        
def logMalformedProject(logfile, properties_dict, field):
    msg_list = []
    
    format="%Y-%m-%d %H:%M"
    timestamp = datetime.strftime(datetime.now(),format)

    project_id = properties_dict['id']
    project_name = properties_dict['name']
    error_msg = 'Value for field "' + field + '" was missing.  Record skipped.'

    msg_list.append(timestamp)
    msg_list.append(project_id)
    msg_list.append(project_name)
    msg_list.append(error_msg)
    with open(logfile, 'a') as errorfile:
        writer = csv.writer(errorfile)
        writer.writerow(msg_list)
            
def add_unique_value_to_list(unique_list, value):
    value_found = False 
    for i in range(len(unique_list)):
        if unique_list[i] == value:
            value_found = True
            print(unique_list[i])
    if value_found == False:
        unique_list.append(value)
        
    return unique_list
        
                       
    
    
    
main()
