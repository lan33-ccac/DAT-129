# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading Capitol Project csv records,
# allowing users to enter search criteria stored in json,
# and writing selected records back out to json.
# Author: Lisa Nydick
# Last Modified: 10/2/2019
#####################################

import json
import csv
from datetime import datetime
import os

quit_program = False
fatal_error = False


def main():
    global fatal_error
    csv_infile = 'capital_projects.csv'
    criteria_infile = 'search_criteria.json'
    mgmt_cost_infile = 'mgmt_costs.json'
    
    jsonoutfile = 'capital_projects_out.json'
    
    logfile = 'capital_projects_log.csv'
    
    projects_list = []   
    json_criteria = {}
    mgmt_costs_list = ()
    
    
    #delete the old log file if it exists
    if os.path.exists(logfile):
        try:
            os.remove(logfile)
        except PermissionError:
            print('Log file could not be deleted for new entries because it is open by another user or process.')
            fatal_error = True
            
    #Create the log file
    if fatal_error == False:
        create_log_file(logfile)
        
    #Read the input csv file and store the project records in a list       
    if fatal_error == False:
        projects_list = read_csv_file(csv_infile)

    
    #Discard records that have missing values for criteria fields and log the error
    if fatal_error == False:
        projects_list = look_for_missing_criteria_values(projects_list, logfile)
    
    #Read in the json criteria fields
    if fatal_error == False:
        json_criteria = read_json_criteria(criteria_infile)
    
    #Read in the json management costs scheme
    if fatal_error == False:
        mgmt_costs_list = read_json_mgmt_costs(mgmt_cost_infile)
           
    #Display the main menu until the user quits
    if fatal_error == False:
        while quit_program == False:
            projects_list = display_menu(json_criteria, projects_list)

            if quit_program == False: 
                if projects_list:
                    print_projects(projects_list)
                    #Compute total cost of selected capital projects given mgmt scheme read from json file
                    projects_list = compute_management_costs(mgmt_costs_list, projects_list)
 
                            
            else: 
                if projects_list:                
                    print_projects(projects_list)
                    projects_list = compute_management_costs(mgmt_costs_list, projects_list)     
                    #Write the results out to a json file of the user's choosing if project's list isn't empty
                    write_json_file(jsonoutfile, projects_list)
    
###################################################################################################
# Reads the capital projects csv file into a projects list dictionary
###################################################################################################
def read_csv_file(infile):
    d = {}
    projects_list = []
    global fatal_error
    
    try:
        with open(infile, 'r') as csv_file:
    
            dict_reader = csv.DictReader(csv_file)
            for d in dict_reader:
 
                #append the dictionary to a list of projects
                projects_list.append(d)
    except Exception as err:
        print(err)
        fatal_error = True
        
                       
    return projects_list      

###################################################################################################
# Reads in search criteria fields from a JSON file
###################################################################################################        
def read_json_criteria(criteria_infile):
    global fatal_error
    json_criteria = {}
    
    try:
        with open(criteria_infile, 'r') as criteria:
            json_criteria = json.load(criteria)
    except Exception as err:
        print(err)
        fatal_error = True
        
    return json_criteria

###################################################################################################
# Looks for missing criteria field values in the input records and logs them if they're missing
###################################################################################################
def look_for_missing_criteria_values(projects_list, logfile):
    d = {}
    

    #Make sure there are no blank values in search criteria fields.
    #Delete the dictionary entry if there is a blank so it's not included in search results
    
    #n adjusts index each time a project is deleted
    n = 0
    
    for i in range(len(projects_list) - n):

        d = projects_list[i - n]

        for k,v in d.items():
            if k == 'fiscal_year' or k == 'start_date' or k == 'area' or k == 'asset_type' or k == 'status':
                if v == '':
                    #log the error
                    logMalformedProject(logfile, d, k)
                    #delete the project from the projects list
                    del projects_list[i - n]                    
                    n += 1 
                    
    return projects_list    



###################################################################################################
# Reads the management cost schema from a JSON file
###################################################################################################
def read_json_mgmt_costs(cost_infile):
    global fatal_error
    mgmt_costs_list = []
    with open(cost_infile, 'r') as costs:
       try:
           mgmt_costs_list = json.load(costs)
       except Exception as err:
           print(err)
           fatal_error = True
           
    return mgmt_costs_list

###################################################################################################
# Displays the main menu and performs the record searches
###################################################################################################
def display_menu(json_criteria, projects_list):
    global quit_program
    global fatal_error
    results_list = {}
    count = 1
    
    print()
    print('CAPITAL PROJECTS SEARCH')
    print()
    print('You can search to Capital Projects data by entering values for search criteria.')
    print('Entering multiple search criteria will further limit the results.')
    print()
    print('Available search fields are:')
    print()
    for k in json_criteria.keys(): 
        #'planning_status' in criteria corresponds to 'status' in csv
        if k == 'planning_status':
            print(str(count) + ') status')
        else:
            print(str(count) + ') ' + k)
        count += 1
    sel = input('Enter the number corresponding to your search criterion of choice or Q to quit: ')
    if sel == 'Q' or sel == 'q':
        quit_program = True
        return projects_list
    else:
        try:
            if int(sel) == 1:
                selval = input('Enter the fiscal year in YYYY format: ')
                if selval != '':
                    valid_year_format, year = valid_year(selval)
                    if valid_year_format == True:
                        json_criteria.update({'fiscal_year': year})
                        operator = input('Enter the search operator (=, >, or <): ')
                        if operator == '=' or operator == '>' or operator == '<':
                            results_list = find_records(projects_list, 'fiscal_year', selval, operator)
                        else:
                            print('Invalid operator entry.')
                else:   #Input was blank, so don't filter on it
                    results_list = projects_list
            elif int(sel) == 2:
                selval = input('Enter the start year in YYYY-mm-dd format: ')
                if selval != '':
                    valid_date_format = valid_date(selval)                
                    if valid_date_format == True:
                        json_criteria.update({'start_date': selval})
                        operator = input('Enter the search operator (=, >, or <): ')
                        if operator == '=' or operator == '>' or operator == '<':
                            results_list = find_records(projects_list, 'start_date', selval, operator)
                        else:
                            print('Invalid operator entry.') 
                else:   #Input was blank, so don't filter on it
                    results_list = projects_list
            elif int(sel) == 3:
                selval = input('Enter the area value: ')
                if selval != '':
                    json_criteria.update({'area': selval})
                    results_list = find_records(projects_list, 'area', selval, '=')
                else:   #Input was blank, so don't filter on it
                    results_list = projects_list    
            elif int(sel) == 4:
                selval = input('Enter the asset type value: ')
                if selval != '':
                    json_criteria.update({'asset_type': selval})
                    results_list = find_records(projects_list, 'asset_type', selval, '=')
                else:   #Input was blank, so don't filter on it
                    results_list = projects_list    
            elif int(sel) == 5:
                selval = input('Enter the status value: ')
                if selval != '':
                    json_criteria.update({'planning_status': selval})
                    results_list = find_records(projects_list, 'status', selval, '=')
                else:   #Input was blank, so don't filter on it
                    results_list = projects_list
            else:
                print('Invalid selection.')
        
        except Exception as err:
            print('Error in display_menu: ' + str(err))
            fatal_error = True
    
    
    if results_list:    
        projects_list = results_list
        
        
    return projects_list
        
###################################################################################################
# Prints the current projects list to the console
###################################################################################################            
def print_projects(projects_list):
    print(json.dumps(projects_list, indent=4))

###################################################################################################
# Writes the projects list to a JSON file
###################################################################################################             
def write_json_file(outfile, projects_list):
    global fatal_error
    invalid_filepath = True
    
    while invalid_filepath == True:
        #prompt for output file path
        outfile = input('Enter name of the file you want json records to be written to or Q to quit: ')

        if outfile != 'Q' and outfile != 'q':
            try:
                with open(outfile, 'w') as projects:
                    invalid_filepath = False
                    #make a string with indents out of a json object
                    s = json.dumps(projects_list, indent=4)
                    projects.write(s)
            except IOError:
                invalid_filepath = True
                print('Invalid file path.  Please enter an existing file path.')
            except Exception as err:
                print(err)
                fatal_error = True
        else:   #Exit loop
            invalid_filepath = False

###################################################################################################
# Creates an error log file and writes the header record
###################################################################################################            
def create_log_file(logfile):
    with open(logfile, 'w', newline = '') as errorfile:
        writer = csv.writer(errorfile)
        header = ['Timestamp', 'Project ID', 'Project Name', 'Error Msg']
        writer.writerow(header)

###################################################################################################
# Appends malformed input records to the logfile
###################################################################################################        
def logMalformedProject(logfile, d, criteria_field):
    global fatal_error
    msg_list = []
        
    format="%Y-%m-%d %H:%M"
    timestamp = datetime.strftime(datetime.now(),format)

    project_id = d['id']
    project_name = d['name']
    error_msg = 'Value for field "' + criteria_field + '" was missing.  Record skipped.'

    msg_list.append(timestamp)
    msg_list.append(project_id)
    msg_list.append(project_name)
    msg_list.append(error_msg)
    
    try:
        with open(logfile, 'a', newline = '') as errorfile:
            writer = csv.writer(errorfile)
            writer.writerow(msg_list)
    except PermissionError:
        print('Log file could not be opened to append new entries because it is already open by another user or process.')
        fatal_error = True

###################################################################################################
# Validates that dates are entered in YYYY-mm-dd format
###################################################################################################        
def valid_date(datestr):
    valid_date_format = True
    try:
        dateobj = datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        valid_date_format = False
        
    return valid_date_format

###################################################################################################
# Converts a string into a date object so dates can be compared
###################################################################################################
def convert_date_str_to_dateobj(datestr, date_format):
    try:
        dateobj = datetime.strptime(datestr, date_format)
        print(dateobj)
    except Exception as err:
        print('Error in convert_date_str_to_dateobj: ' + str(err))
    return dateobj

###################################################################################################
# Validates that a fiscal year is entered in YYYY format
###################################################################################################        
def valid_year(year_str):
    valid_year_format = False
    if len(year_str) == 4:
        try:
            year = int(year_str)
            valid_year_format = True
        except ValueError:
            print('Year ' + year_str + ' is not a number.')
        except Exception as err:
            print(err)
    else:
        print('Year must be in YYYY format.')
    
    return valid_year_format, year

###################################################################################################
# Computes the total management costs of selected projects based on 
###################################################################################################
def compute_management_costs(mgmt_costs_list, projects_list):
    global fatal_error
    total_cost = 0
    
    try:
        for i in range(len(projects_list)):
            d1 = projects_list[i]
            budget = int(d1['budgeted_amount'])
            #loop through mgmt_costs_list, looking for a criteria match
            for j in range(len(mgmt_costs_list)):
                d2 = mgmt_costs_list[j]
                budget_cutoff = d2['budget_cutoff']
                mgmt_rate = float(d2['mgmt_rate'])
                comparison = d2['criterion']

                if comparison == '<=':
                    if budget <= budget_cutoff:
                        mgmt_cost = mgmt_rate * budget
                        break

                else:   #comparison is >
                    if budget > budget_cutoff:
                        mgmt_cost = mgmt_rate * budget
                        break
         
            total_cost += mgmt_cost
            
        print(f'{"TOTAL MANAGEMENT COSTS OF SELECTED CAPITAL PROJECTS:":<42}{total_cost:> ,.2f}')
 
            
    except Exception as err:
        print(err)
        fatal_error = True
        
    return projects_list
                
            
###################################################################################################
# Finds records that match search criterion value (and operator if applicable)
###################################################################################################        
def find_records(projects_list, field, value, operator):
    results_list = []
    records_found = False

    if field == 'start_date':
        date_format = '%Y-%m-%d'
        value = convert_date_str_to_dateobj(value, date_format)
        #print('criteria start_date = ' + str(value))
        
    for i in range(len(projects_list)):
        d = projects_list[i]

        for k,v in d.items():
                        
            #if the criteria value isn't blank, check whether the criteria field matches the dictionary key
            if value != '':
                if k == field:
                    #If field is start_date, convert record's start date to a date object
                    if k == 'start_date':
                        date_format = '%m/%d/%Y'
                        v = convert_date_str_to_dateobj(v, date_format)
                        print('record date = ' + str(v))

                    
                    #check the operator to determine the type of search.  Text fields will always be =
                    if operator == '=':
                        if v == value:
                            records_found = True
                            #match, so append the dictionary entry to the results list
                            results_list.append(d)
                    elif operator == '>':
                        if v > value:
                            records_found = True
                            #match, so append the dictionary entry to the results list
                            results_list.append(d)
                    else:   #operator is <
                        if v < value:
                            records_found = True
                            #match, so append the dictionary entry to the results list
                            results_list.append(d)                        
                #else skip field
            else:  #Input value was blank, so don't limit records by it (i.e., automatically append the dict entry)
                records_found = True
                results_list.append(d)
                
    if records_found == False:
        print('No records matched the search criteria.')
        
    return(results_list)                           
    
    
    
main()
