# -*- coding: utf-8 -*-
###################################################################################################
# DAT-129
# Purpose: Preprocesses the 311 CSV file to eliminate requests with "DO NOT USE" request types
# and consolidate similar request type names so there are fewer categories of requests.
# The program reads a translation file and uses it to translate the existing request
# type name into a consolidated name.  The program writes out the translated records to
# a file that can be used as input to the 311.py program.
# It also produces a file that contains a list of deleted records.
# Author: Lisa Nydick
# Last Modified: 12/2/2019
###################################################################################################

import csv
import os

#file types
TYPE_INPUT = 'Input'
TYPE_OUTPUT = 'Output'
TYPE_DELETE = 'Delete'
TYPE_TRANS = 'Translation'

#File Header Constants
FIELD_REQUEST_ID = 'REQUEST_ID'
FIELD_CREATED_ON = 'CREATED_ON'
FIELD_REQUEST_TYPE = 'REQUEST_TYPE'
FIELD_STATUS = 'STATUS'
FIELD_DEPARTMENT = 'DEPARTMENT'
FIELD_ISSUE = 'Issue'
FIELD_CATEGORY = 'Category'

MSG_ENTER_OUTPUT_FILENAME = 'Enter the output file name: '
MSG_ENTER_DELETE_FILENAME = 'Enter the file name for deleted records: '
MSG_ENTER_TRANS_FILENAME = 'Enter the 311 Codebook (category translation) filename: '
MSG_ENTER_INPUT_FILENAME = 'Enter the input file name: '
MSG_INVALID_FILENAME = 'Invalid file name.  Please try again.'
MSG_FILE_DOES_NOT_EXIST = "File name doesn't exist.  Please try again."
MSG_ERROR_OCCURRED = 'Unexpected error occurred: '
MSG_PROGRAM_ENDED_ABNORMALLY = 'Program ended abnormally due to a fatal error.'
MSG_ERROR_IN_ROUTINES = 'Error in routine(s):'
MSG_FILE_NOT_IN_EXPECTED_FORMAT = 'File did not contain the expected column names.'

#Misc Constants
UNKNOWN = 'Unknown'
BLANK = ''
DELETE = 'DELETE'
WORKING_ON_IT = 'Working on it...'


#Use global variables to track error status throughout program
fatal_error = False
routines = []

###################################################################################################
# Main Function
###################################################################################################
def main():
    global routines
    routine_name = 'main'    
    trans_list = []
    inputfile, outputfile, deletefile, translationfile = '', '', '', ''

   
    header = [FIELD_REQUEST_ID, FIELD_CREATED_ON, FIELD_REQUEST_TYPE, FIELD_STATUS, FIELD_DEPARTMENT]
    
    inputfile = getFileName(TYPE_INPUT)
    
    #Get the output file name from console input
    outputfile = getFileName(TYPE_OUTPUT)
    
    #Delete a pre-existing log file and initialize a new log file with a header record
    initializeOutputFile(outputfile, header)
    
    if fatal_error == False:
        deletefile = getFileName(TYPE_DELETE)
        
        if fatal_error == False:
            #Delete a pre-existing deleted record file and initialize a new file with a header record
            initializeDeletedRecordFile(deletefile, header)
        
            if fatal_error == False:
                #Gets the translation file (311 codebook) from console input
                translationfile = getFileName(TYPE_TRANS)
        
                if fatal_error == False:
                    print(WORKING_ON_IT)
                          
                    #reads a request type translation file and stores it in a list
                    trans_list = readTranslationFile(translationfile)
        
                    if fatal_error == False:
                        #Read in the capital projects csv records and processes them
                        readandProcessRequestTypes(inputfile, outputfile, deletefile, trans_list)
                
    if fatal_error == True:
        routines.append(routine_name)
        print(MSG_PROGRAM_ENDED_ABNORMALLY)
        print(MSG_ERROR_IN_ROUTINES)
        print(routines)

###################################################################################################
#  Handles unexpected errors in a variety of routines
###################################################################################################
def handle_unexpected_error(err, routine_name):
    global fatal_error
    global routines
    print()
    print(f'{MSG_ERROR_OCCURRED} {err}')  
    fatal_error = True
    routines.append(routine_name)  

###################################################################################################
# Prompts the user for a filename (output, delete, or translation file)
###################################################################################################
def getFileName(filetype):
    invalid_file = True
    while invalid_file:
        if filetype == TYPE_OUTPUT:
            filename = input(MSG_ENTER_OUTPUT_FILENAME)
        elif filetype == TYPE_DELETE:
            filename = input(MSG_ENTER_DELETE_FILENAME)
        elif filetype == TYPE_TRANS:
            filename = input(MSG_ENTER_TRANS_FILENAME)
        else:   #filetype = TYPE_INPUT
            filename = input(MSG_ENTER_INPUT_FILENAME)
        
        invalid_file = validateFileNames(filetype, filename)
    return filename

###################################################################################################
# Ensures that the user entered a file name with a csv extension
# and that the input file and translation file paths exist.
###################################################################################################
def validateFileNames(filetype, filename):
    invalid_file = True
    #File must be of type .csv
    if filename.endswith('.csv'):
        #The Input and Translation files must already exist
        if filetype == TYPE_TRANS or filetype == TYPE_INPUT:
            if os.path.exists(filename):
                invalid_file = False
            else:
                invalid_file = True
                print(MSG_FILE_DOES_NOT_EXIST)
        else: #filetype is Output or Delete, so it doesn't need to exist
            invalid_file = False
    else:
        invalid_file = True
        print(MSG_INVALID_FILENAME)
   
    return invalid_file

###################################################################################################
# Creates an output file with a header record
###################################################################################################
def initializeOutputFile(outputfile, header):
    routine_name = 'initializeOutputFile'
    try:
        with open(outputfile, 'w', newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
###################################################################################################
# Creates a deleted record file with a header record
###################################################################################################
def initializeDeletedRecordFile(deletefile, header):
    routine_name = 'initializeDeletedRecordFile'
    try:
        with open(deletefile, 'w', newline = '') as delfile:
            writer = csv.writer(delfile)
            writer.writerow(header)
    except Exception as err:
        handle_unexpected_error(err, routine_name)

###################################################################################################
# Reads in a list of translated (i.e., consolidated) request types
###################################################################################################
def readTranslationFile(translationfile):
    routine_name = 'readTranslationFile'
    trans_list = []
    try:
        with open(translationfile, 'r') as transfile:
            transfile.read(3)
            translations = csv.DictReader(transfile)
            for translation in translations:
                trans_list.append(translation)
        
    except Exception as err:
        handle_unexpected_error(err, routine_name)
    
    return trans_list

###################################################################################################
# Reads the input CSV file line by line and tests whether its Issue value
# matches the Request_Type value in a translation list.
# If there's a match, it replaces the request type with the category value
# and writes it out to a file that can be used as input to the 311.py program.
# If the translated version says "DELETE" the request type represents a "DO NOT USE" and so it is deleted
# and the deleted record is logged.
###################################################################################################    
def readandProcessRequestTypes(inputfile, outputfile, deletefile, trans_list):
    routine_name = 'readandProcessRequestTypes'
    
    try:
        with open(inputfile, 'r') as infile:
            request_types = csv.DictReader(infile)
            for request_type in request_types:
                delete = False
                rid = request_type[FIELD_REQUEST_ID]
                rdate = request_type[FIELD_CREATED_ON]
                rtype = request_type[FIELD_REQUEST_TYPE]
                rstatus = request_type[FIELD_STATUS]
                rdept = request_type[FIELD_DEPARTMENT]
                #Substitute Unknown for blank department fields
                if rdept == BLANK:
                    rdept = UNKNOWN
                
                for i, v in enumerate(trans_list):
    
                    request_type = v[FIELD_ISSUE]
                    if rtype == request_type:
                        category = v[FIELD_CATEGORY]
                        if category != UNKNOWN and category != BLANK:
                            #Use the category as the request type
                            rtype = category
                        else:
                            #Use original request type as the category
                            rtype = request_type
                            
                        # If the translation says "DELETE" this is a flag that indicates this request
                        # type should not be included in the results
                        if category == DELETE:
                             delete = True
                             rtype = request_type   #use the original request type in the deleted request log
                    
                    # else no match, so leave rtype alone
                if delete == False:                    
                    writeOutputRecord(outputfile, rid, rdate, rtype, rstatus, rdept)
                else:
                    writeDeletedRequestRecord(deletefile, rid, rdate, rtype, rstatus, rdept)
                    
                if fatal_error == True:
                    #if an error occured when writing the output file or deleted requests file
                    #append this routine name to the error call stack
                    routines.append(routine_name)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        print(MSG_FILE_NOT_IN_EXPECTED_FORMAT)

###################################################################################################
# Writes a record to an output file that can be used as input to 311.py or 311_Elapsed_Days.py
###################################################################################################            
def writeOutputRecord(outputfile, rid, rdate, rtype, rstatus, rdept):
    routine_name = 'writeOutputFile'
    req_list = []
    req_list.append(rid)
    req_list.append(rdate)
    req_list.append(rtype)
    req_list.append(rstatus)
    req_list.append(rdept)
    
    try:
        with open(outputfile, 'a', newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(req_list)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        
    
###################################################################################################
# Writes a record to an deleted request file
###################################################################################################
def writeDeletedRequestRecord(deletefile, rid, rdate, rtype, rstatus, rdept):
    routine_name = 'writeDeletedRequestFile'
    req_list = []
    req_list.append(rid)
    req_list.append(rdate)
    req_list.append(rtype)
    req_list.append(rstatus)
    req_list.append(rdept)
    
    try:
        with open(deletefile, 'a', newline = '') as deletedfile:
            writer = csv.writer(deletedfile)
            writer.writerow(req_list)
    except Exception as err:
        handle_unexpected_error(err, routine_name)

###################################################################################################
if __name__=='__main__':
    main()