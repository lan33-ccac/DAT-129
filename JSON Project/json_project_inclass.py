# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading Capitol Project csv records,
# and search criteria from a JSON file, 
# printing well-formed matching records to the console
# Author: Lisa Nydick
# Last Modified: 10/3/2019
#####################################

import json, csv, os
from datetime import datetime


LOG_FILE='malformedProjects.csv'
PROJECT_CSV = 'capital_projects.csv'
CRITERIA_FILE ='search_criteria_2.json'

###################################################################################################
# Main Function
###################################################################################################
def main():
    filters = {}
    
    #Delete a pre-existing log file and initialize a new log file with a header record
    initializeLogFile()
    
    #Read in the JSON file containing search criteria
    filters = readProjectFilters()
    
    #Read in the capital projects csv records and process them
    readandProcessProjects(filters)

###################################################################################################
# Deletes a pre-existing log file and creates a new one with a header record
###################################################################################################
def initializeLogFile():
    #delete the log file if it already exists
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    with open(LOG_FILE, 'w', newline = '') as errorfile:
        writer = csv.writer(errorfile)
        header = ['Timestamp', 'Project ID', 'Project Name', 'Error Msg']
        writer.writerow(header)
###################################################################################################
# Reads the project search criteria (filters) into a dictionary and returns it
###################################################################################################
def readProjectFilters():
    filters = {}
    with open(CRITERIA_FILE, 'r') as criteria:
        filters = json.load(criteria)
    return filters

###################################################################################################
# Reads the projects CSV file line by line into a dictionary and processes each record by
# ensuring the integrity of the record, and making sure it passes the filter tests.
# Records that pass all tests are sent to the output medium    
###################################################################################################    
def readandProcessProjects(filters):
    with open(PROJECT_CSV, 'r') as projFile:
        projects = csv.DictReader(projFile)
        for proj in projects:
            if checkProjectIntegrity(proj):             #Checks for the presence of the area field in the project record
                if passProjectFilter(proj, filters):    #Sees if the project meets the search criteria
                    recordOutputProject(proj)           #Outputs eligible records


###################################################################################################
# Prints a project to the console in an easy to read format
###################################################################################################        
def printProjecttoConsole(proj):
    print()
    print("Project Profile: ")
    for key in proj:
        print(f'{key:<22}{proj[key]}')

###################################################################################################
# Checks whether a project is missing a value for the 'area' field, and if so, calls a function
# to send it to a log file.  Returns a True or False value to indicate whether the integrity
# check succeeded or failed.        
###################################################################################################
def checkProjectIntegrity(proj):
    if proj['area'] == '':
        logMalformedProject(proj, 'area')
        return False
    else:
        return True

###################################################################################################
# Appends project info to a log file for a project that fails its integrity check
###################################################################################################        
def logMalformedProject(proj, field):   
    msg_list = []
        
    format="%Y-%m-%d %H:%M"
    timestamp = datetime.strftime(datetime.now(),format)

    project_id = proj['id']
    project_name = proj['name']
    error_msg = 'Value for field "' + field + '" was missing.  Record skipped.'

    msg_list.append(timestamp)
    msg_list.append(project_id)
    msg_list.append(project_name)
    msg_list.append(error_msg)
    
    try:
        with open(LOG_FILE, 'a', newline = '') as errorfile:
            writer = csv.writer(errorfile)
            writer.writerow(msg_list)
    except PermissionError:
        print('Log file could not be opened to append new entries because it is already open by another user or process.')    
    

###################################################################################################
# Tests whether a project meets all filter criteria and returns a True or False value
###################################################################################################        
def passProjectFilter(proj, filters):
    test_results = []
    passed_all_tests = False
    
    #Loop through all filters, testing whether their values match the input project's values for the same fields
    #Build a list of test results since a record could pass one test but fail another.
    for k, v in filters.items():
        
        if v != '':     #If the value is blank, the current field automatically passes its test
            if k == 'planning_status':  #"planning status" in criteria is "status" in csv file
                k = 'status'

            #If the length of the value list is greater than 1, 
            #send the list to a function that will loop through it's values, looking for a match.
            #Append the test result to a list of test results
            if len(v) > 1:
                if testOrCondition(proj, k, v): 
                    test_results.append(True)
                else:
                    test_results.append(False)
            else:
                #there is only one value in the criterion list, so just test it directly
                if testValue(proj, k, v[0]):
                    test_results.append(True)
                else:
                    test_results.append(False)
        else:
            test_results.append(True)

    #Loop through the test results list looking for at least one failed test.
    #If there's a failed test in the list, the entire record fails
    passed_all_tests = True             #Start out assuming all tests were passed
    for j in range(len(test_results)):
        if test_results[j] == False:    #If one failed, reset the boolean to False
            passed_all_tests = False
                    
    return passed_all_tests
    
###################################################################################################
# Tests the value of a project field against the corresponding filter field value
# Returns True if the field values match, False if they don't match
###################################################################################################        
def testValue(proj, field, filter_value):
    # If the filter value is blank, the field values automatically match
    if str(filter_value) == str(proj[field]) or str(filter_value) == '':
        return True
    else:
        return False

###################################################################################################
# Loops through a list of criteria values, seeing if any one of them matches the project value
# If there's a match, the record passes this test, and True is returned.
# Otherwise, none of the values in the criteria list match the project value, so False is returned
###################################################################################################        
def testOrCondition(proj, key, filter_value_list):
    passed_a_test = False
    for i in range(len(filter_value_list)):
        if testValue(proj, key, filter_value_list[i]):
            passed_a_test = True
    return passed_a_test

###################################################################################################
# Sends a project record to the output of choice
###################################################################################################        
def recordOutputProject(proj):
    printProjecttoConsole(proj)
    
main()