# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Exercise in webscraing the clinicaltrials.gov website
# Author: Lisa Nydick
# Last Modified: 10/8/2019
#####################################

import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#Constants that can change between program runs
OUT_FILE = 'clinical_trials.csv'
CONDITION_VALUE='Depression'
TERM_VALUE = 'ketamine'
COUNTRY_VALUE = 'US'
STATE_VALUE = ''
CITY_VALUE = ''
DISTANCE_VALUE = ''

#Constant Constants
AMP = '&'
SEP = ';'
SITE = 'https://clinicaltrials.gov/ct2/'
OPER = 'results?'
CONDITION_KEY = 'cond='
TERM_KEY = 'term='
COUNTRY_KEY = 'cntry='
STATE_KEY = 'state='
CITY_KEY = 'city='
DISTANCE_KEY = 'dist='

#Output file header
HEADER = ['Search Date/Time', 'Status', 'Study Number', 'Study Name', 'Conditions', 'Interventions', 'Study Type', 'Phase', 'Location']

#Data column numbers
COL_STATUS = 2
COL_TITLE = 3
COL_CONDITION = 4
COL_INTERVENTIONS = 5
COL_STUDYTYPE = 6
COL_PHASE = 7
COL_LOCATION = 8

#Error Handling
ERROR_PERMISSIONS = 'Log file could not be opened to append new entries because it is already open by another user or process.'
fatal_error = False
###################################################################################################
# Initializes a CSV output file with a header record
###################################################################################################
def initializeCSVFile():
    global fatal_error
    try:
        with open(OUT_FILE, 'w', newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(HEADER)
    except PermissionError:
        print(ERROR_PERMISSIONS)
        fatal_error = True

###################################################################################################
# Builds a dictionary out of url key-value constants.  Returns the dictionary.
###################################################################################################
def buildURLDict():
    d = {}
    d[CONDITION_KEY] = CONDITION_VALUE
    d[TERM_KEY] = TERM_VALUE
    d[COUNTRY_KEY] = COUNTRY_VALUE
    d[STATE_KEY] = STATE_VALUE
    d[CITY_KEY] = CITY_VALUE
    d[DISTANCE_KEY] = DISTANCE_VALUE
    return d

###################################################################################################
# Builds a url based on the web site domain, the operation ("results?"), and the key-value pairs
# in the input dictionary.  Returns the url.
###################################################################################################
def buildURL(d):
    url = SITE + OPER 
    for k, v in d.items():
        url = url + k + v + AMP
    url = stripTrailingAMP(url)
    return url

###################################################################################################
# Strips the trailing ampersand char off the end of the url.  Returns the stripped url.
###################################################################################################
def stripTrailingAMP(url):
    url = url[0:len(url) - 1]
    return url

###################################################################################################
# Issues the http request and returns the web page response.
###################################################################################################
def getHTMLPageText(url):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        #use the resource manager to request the page from the internet
        #and retrieve the HTML from the response for use as the return text
        return response.read()


###################################################################################################
# Gets the study number string from the title text and returns it
###################################################################################################
def getStudyNumber(title):
    study_num = title[11:22]
    return study_num 

###################################################################################################
# Strips the "Show study NCT024884456: " Portion of the title and returns the title.
# This string is a fixed length.
###################################################################################################
def stripStudyNumber(title):
    title = title[24:len(title)]
    return title

###################################################################################################
# Traverses the soup object, looking for status, title, and location information.
# Appends these values to lists and returns the lists.
###################################################################################################
def traverseSoup(soup):
    status_list = []
    title_list = []
    study_num_list = []
    condition_list = []
    intervention_list = []
    studytype_list = []
    phase_list = []
    location_list = []
    
    #start with table containing the data
    table_tags = soup.find_all("table", id="theDataTable")
    for tags in table_tags:
        #Then get the table rows
        trs = tags.find_all("tr")
        for tr in trs:
            #find all of the table data (tds) in the row
            tds = tr.find_all("td")
            
            #Call method to find the status value.  Append the status to a list
            status = findStatus(tds)
            status_list.append(status)
            
            #Call method to find the title.  Don't append it to a list quite yet.
            title = findTitle(tds)
            
            #The study number is part of the title string, so extract it and append it to a list
            study_num = getStudyNumber(title)
            study_num_list.append(study_num)
            
            #Strip the study number from the title string and append it to a list
            title = stripStudyNumber(title)
            title_list.append(title)
            
            #Call method to find the condition info
            condition = findCondition(tds)
            condition_list.append(condition)
            
            #Call method to find the interventions info
            intervention = findIntervention(tds)
            intervention_list.append(intervention)
            
            #Call method to find the study type info
            studytype = findStudyType(tds)
            studytype_list.append(studytype)
            
            #Call method to find the study phase info
            phase = findPhase(tds)
            phase_list.append(phase)
            
            #Call methhod to find the location info. 
            location = findLocation(tds)
            location_list.append(location)
            
   
    return status_list, study_num_list, title_list, condition_list, intervention_list, studytype_list, phase_list, location_list

###################################################################################################
# Extracts the status value from a soup object
###################################################################################################
def findStatus(tds):
    #The status is in the status column inside a span tag

    status_col = tds[COL_STATUS]
    status = status_col.get_text()

    #Make some substitutions to make the status text more readable
    status = status.replace("Has", ", Has")
    status = status.replace("New", ", New")
    return status

###################################################################################################
# Extracts the title value from a soup object
###################################################################################################
def findTitle(tds):
    #The study title is in the title column inside an a tag
    a_tag = tds[COL_TITLE].find("a")
    title = a_tag.attrs.get("title")    
    return title


###################################################################################################
# Extracts the condition(s) info from a soup object
###################################################################################################
def findCondition(tds):
    condition = ''
    lis = tds[COL_CONDITION].find_all("li")
    if len(lis) == 1:
        condition = lis[0].get_text()
    else:
        #concatinate multiple conditions with separator char
        for li in lis:
            condition = condition + SEP + li.get_text()
            #strip the initial separator char off the condition before returning it
            condition = stripInitialChar(condition)
    return condition

###################################################################################################
# Extracts the intervention(s) info from a soup object
###################################################################################################
def findIntervention(tds):
    intervention = ''
    lis = tds[COL_INTERVENTIONS].find_all("li")
    if len(lis) == 1:
        intervention = lis[0].get_text()
    else:
        #concatinate multiple interventions with separator char
        for li in lis:
            intervention = intervention + SEP + li.get_text()
            #strip the initial separator char off the intervention before returning it
            intervention = stripInitialChar(intervention)
    return intervention

###################################################################################################
# Extracts the study type info from a soup object
###################################################################################################
def findStudyType(tds):
    td = tds[COL_STUDYTYPE]
    studytype = td.get_text()
    return studytype           

###################################################################################################
# Extracts the study phase info from a soup object
###################################################################################################
def findPhase(tds):
    td = tds[COL_PHASE]
    phase = td.get_text()
    #Make some substitutions to make the phase text more readable
    phase = phase.replace("Phase 1Phase 2", "Phase 1, Phase 2")
    phase = phase.replace("Phase 2Phase 3", "Phase 2, Phase 3")
    
    return phase
    
    
###################################################################################################
# Extracts the location from a soup object
###################################################################################################
def findLocation(tds):
    location = ''
    lis = tds[COL_LOCATION].find_all("li")
    if len(lis) == 1:
        location = lis[0].get_text()
    else:
        #concatinate multiple locations with separator char
        for li in lis:
            location = location + SEP + li.get_text()
            #strip the initial separator char off the location before returning it
            location = stripInitialChar(location)
    return location
                    
###################################################################################################
# Strips the initial comma off of a string
###################################################################################################
def stripInitialChar(string):
    if string[0] == SEP:
        string = string[1:len(string) + 1]
    return string
      
###################################################################################################
# Loops through the study number list and study title lists, writing out each record to a csv file
###################################################################################################
def outputRecords(status_list, study_num_list, title_list, condition_list, intervention_list, studytype_list, phase_list, location_list):

    #All lists will have the same number of elements
    for i in range(len(title_list)):
        status = status_list[i]
        study_num = study_num_list[i]
        title = title_list[i]
        condition = condition_list[i]
        intervention = intervention_list[i]
        studytype = studytype_list[i]
        phase = phase_list[i]
        location = location_list[i]
        if fatal_error == False:
            writeCSVRecord(status, study_num, title, condition, intervention, studytype, phase, location)    
        
###################################################################################################
# Writes the search timestamp, trial status, study number and title to a csv file
###################################################################################################        
def writeCSVRecord(status, study_num, title, condition, intervention, studytype, phase, location):
    global fatal_error
    msg_list = []

    date_format="%Y-%m-%d %H:%M"
    timestamp = datetime.strftime(datetime.now(), date_format)

    msg_list.append(timestamp)
    msg_list.append(status)
    msg_list.append(study_num)
    msg_list.append(title)
    msg_list.append(condition)
    msg_list.append(intervention)
    msg_list.append(studytype)
    msg_list.append(phase)
    msg_list.append(location)
    
    try:
        with open(OUT_FILE, 'a', newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(msg_list)
    except PermissionError:
        print(ERROR_PERMISSIONS)
        fatal_error = True
        

###################################################################################################
# Main Function
###################################################################################################        
def main():
    status_list = []
    title_list = []
    study_num_list = []
    condition_list = []
    interventions_list = []
    location_list = []
    d = {}
    
    #initialize the CSV outfile with a header record
    initializeCSVFile()
    
    if fatal_error == False:
    
        #Build a dictionary out of URL keys and values
        d = buildURLDict()
    
        #Build the url from the dictionary
        url = buildURL(d)
    
        #Issue get request and receive the response in pagetext
        pageText = getHTMLPageText(url)
    
        #In itialize the BeautifulSoup object
        soup = BeautifulSoup(pageText, 'html.parser')
    
        #Traverse the soup looking for status, study number, title, and location info
        #Append each value to its own list
        status_list, study_num_list, title_list, condition_list, interventions_list, studytype_list, phase_list, location_list = traverseSoup(soup)
    
        #Output the records in the lists to a CSV file
        outputRecords(status_list, study_num_list, title_list, 
                      condition_list, interventions_list, studytype_list, 
                      phase_list, location_list)



    
if __name__=='__main__':
    main()