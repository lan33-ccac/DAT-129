# -*- coding: utf-8 -*-
###################################################################################################
# DAT-129
# Purpose: Uses Pandas to Read 311 Data to Help Answer Questions about the
# Nature of 311 Requests.  See the README.MD file for details.
# Design: 
# 1. Reads in initialization values from the console.
# 2. Reads the 311 input .CSV file into a Pandas dataframe.
# 3. Extracts the relavant columns (such as REQUEST_TYPE) from the dataframe.
# 4. Groups and sorts the dataframe according to user preferences (read in from console).
# 5. Displays statistics about the data in the dataframe.
# 6. Displays the data in the dataframe.
# 7. Optionally, writes the contents of the dataframe to an Excel or .CSV file
# 8. If the number of records the user wants to display is less than 30, it plots the
#    results in a bar chart (if higher than that, the chart would be illegible.)
# Author: Lisa Nydick
# Last Modified: 12/05/2019
###################################################################################################

import pandas as pd
import os
from datetime import datetime

#Request Status Constants
STATUS_TYPE_OPEN = 'OPEN'
STATUS_TYPE_CLOSED = 'CLOSED'
STATUS_TYPE_ALL = 'ALL'
STATUS_TYPE_NEW = 'NEW'
STATUS_OPEN = 3
STATUS_CLOSED = 1
STATUS_NEW = 0
STATUS_ALL = 2

#Result Options
RESULT_MODE_COUNT = 1       #Request count mode
RESULT_MODE_ED = 2          #Elapsed days mode

#Group By option constants
GROUP_BY_REQ_TYPE = 1       #Group by REQUEST_TYPE column
GROUP_BY_DEPT = 2           #Group by DEPARTMENT column
GROUP_BY_BOTH = 3           #Group by REQUEST_TYPE, then DEPARTMENT

#Sort by option constants
SORT_BY_REQ_TYPE = 1         #Sort results by REQUEST_TYPE
SORT_BY_DEPT = 2             #Sort results by DEPARTMENT
SORT_BY_REQ_COUNT_OR_ED = 3  #Sort results by Request Count or Elapsed Days, depending on results mode

#Number of results constants
ALL_RESULTS = 999   #Flag to display all results
PLOTTING_MAX = 30   #Maximum number of records to allow to be plotted.  (Too many makes the display unreadable.)

#Column Key Constants
REQUEST_ID = 'REQUEST_ID'
REQUEST_TYPE = 'REQUEST_TYPE'
STATUS = 'STATUS'
DEPARTMENT = 'DEPARTMENT'
REQ_COUNT = 'REQ_COUNT'
PERCENT_TOTAL_REQS = '% TOTAL_REQs'
CREATED_ON = 'CREATED_ON'
MEAN_ELAPSED_DAYS = 'MEAN_ELAPSED_DAYS'

#Prompt/Message Constants
MSG_ENTER_311_CSV = 'Enter the 311 CSV Filename: '
MSG_311_FILE_NOT_FOUND = 'File not found.  Please try again.'
MSG_ENTER_RESULT_MODE = 'Do you want request counts or elapsed days to be displayed? (1 = Counts, 2 = Elapsed Days): '
MSG_ENTER_STATUS_1 = 'Enter the status number of interest. (0 = New, 1 = Closed, 2 = All, 3 = Open): '
MSG_ENTER_STATUS_2 = 'Enter the status number of interest. (0 = New, 3 = Open): '
MSG_ENTER_GROUP_BY_OPTION = 'Do you want to group results by request type or by assigned department or both? (1 = Request Type, 2 = Dept, 3 = Both): '
MSG_INVALID_GROUP_BY_OPTION = 'Invalid group by option.  Please try again.'
MSG_ENTER_SORT_BY_OPTION_FOR_REQ_TYPE_GROUPING_COUNTS = 'Sort Results by Request Type or Request Count (1 = Request Type, 3 = Request Count)? '
MSG_ENTER_SORT_BY_OPTION_FOR_REQ_TYPE_GROUPING_ED = 'Sort Results by Request Type or Elapsed Days (1 = Request Type, 3 = Elapsed Days)? '
MSG_ENTER_SORT_BY_OPTION_FOR_DEPT_GROUPING_COUNTS = 'Sort Results by Department or Request Count (2 = Department, 3 = Request Count)? '
MSG_ENTER_SORT_BY_OPTION_FOR_DEPT_GROUPING_ED = 'Sort Results by Department or Elapsed Days (2 = Department, 3 = Elapsed Days)? '
MSG_ENTER_SORT_BY_OPTION_FOR_BOTH_GROUPING_COUNTS = 'Sort Results by Request Type, Department, or Request Count (1 = Request Type, 2 = Department, 3 = Request Count)? '
MSG_ENTER_SORT_BY_OPTION_FOR_BOTH_GROUPING_ED = 'Sort Results by Request Type, Department, or Elapsed Days (1 = Request Type, 2 = Department, 3 = Elapsed Days)? '
MSG_INVALID_SORT_BY_OPTION =  'Invalid sort option.  Please try again.'
MSG_INVALID_STATUS = 'Invalid status.  Please try again.'
MSG_ENTER_NRESPONSE = 'Enter the number of results you want to display or 999 for all results: '
MSG_INVALID_NRESPONSE = 'Invalid number of results.  Please try again.'
MSG_INVALID_CSV_FILE = 'Input file is not a valid CSV file.  Ending program'
MSG_UNEXPECTED_INPUT_FORMAT = 'Input file does not contain the expected columns.  Ending program.'
MSG_WRITE_TO_FILE = 'Write results to an Excel or CSV file? ("Y" or "N")? '
MSG_INVALID_RESPONSE = 'Invalid response.  Please try again.'
MSG_OUTPUT_FILE_NOT_WRITTEN = 'Output file not written.'
MSG_ENTER_OUTPUT_FILENAME = 'Enter the name of the output file: '
MSG_INVALID_FILE_EXTENSION = 'Invalid file extension.  Must be ".csv", ".xls", or ".xlsx".  Please enter a new filename: '
MSG_FILE_SUCCESSFULLY_WRITTEN = ' file successfully written.'
MSG_FILE_NOT_SUCCESSFULLY_WRITTEN = ' file wes NOT successfully written.'
MSG_FILE_IN_USE = 'File is in use by another user or process.  Try again ("Y" or "N")? '
MSG_ERROR_OCCURRED = 'Unexpected Error occurred: '
MSG_PROGRAM_ENDED_ABNORMALLY = 'Program ended abnormally due to a fatal error.'
MSG_ERROR_IN_ROUTINES = 'Error in routine(s):'

#Display constants
STATISTICS_FOR = 'STATISTICS FOR '
REQUESTS = ' REQUESTS:'
TOTAL_REQS = 'Total Reqs'
COUNT_REQ_TYPES = 'Count of Request Types'
COUNT_DEPTS = 'Count of Departments'
MAX = 'Max'
MIN = 'Min'
MEAN = 'Mean'
STDEV = 'Std Dev'
TOTAL_REQUESTS = 'Total Requests: '
TOTAL = 'Total '
STATUS_REQUESTS = ' Status Requests: '
TOP = 'Top '
TYPES_OF = ' Types of '
TOTAL_REC_COUNT = 'Total Records'
DAYS = 'DAYS'
REQUEST_TYPES_STAYING = ' REQUEST TYPES STAYING IN THE '
STATUS_THE_LONGEST = ' STATUS THE LONGEST: '
DEPARTMENTS_WITH_REQUESTS_STAYING_IN = ' DEPARTMENTS WITH REQUESTS STAYING IN THE '
DEPARTMENTS = " Departments' "
UNKNOWN = 'Unknown'

#Pandas Display option constants
MAX_COL_WIDTH_1 = 40    #Column width when only REQUEST_TYPE or DEPARTMENT will be displayed
MAX_COL_WIDTH_2 = 25    #Column width when both REQUEST_TYPE and DEPARTMENT will be displayed
DISPLAY_WIDTH = 90

#Plotting constants
PLOT_COUNT_OF = 'Count of '
PLOT_REQ_BY_REQ_TYPE = ' Requests by Request Type'
PLOT_REQ_TYPE = 'Request Type'
PLOT_COUNT = 'Count'
PLOT_REQ_BY_DEPT = ' Requests by Department'
PLOT_DEPARTMENT = 'Department'
PLOT_DAYS = 'Days'
PLOT_REQ_BY_REQ_TYPE_AND_DEPT = ' Requests by Request Type and Department'
PLOT_REQ_TYPE_DEPT = 'Request Type, Department'
PLOT_MEAN_DAYS_REQUESTS_HAVE_STAYED_IN = 'Mean Days Requests Have Stayed in '
PLOT_STATUS = ' Status, '
PLOT_BY_REQ_TYPE = 'by Request Type'
PLOT_BY_DEPT = 'by Department'
PLOT_BY_BOTH = 'by Request Type, Department'

#Output File Constants
FILE_TYPE_CSV = 'CSV'
FILE_TYPE_EXCEL = 'EXCEL'
EXT_CSV = '.csv'
EXT_XLS = '.xls'
EXT_XLSX = 'xlsx'

#Global Variables
fatal_error = False
routines = []    #List used to store routine call stack for error message
###################################################################################################
# Main Function
###################################################################################################
def main():
    global routines
    routine_name = 'main'
    total_rec_count, total_req_type_count, count, maxval, minval, mean = 0, 0, 0, 0, 0, 0
    
    #Read in parms that the user might want to change between runs
    infile, results_mode, group_by_option, sort_by_option, status, nresults = get_input_parms()
    
    #Set text version of status number for display purposes
    status_type = set_status_type(status)
            
    print('Working on it...')
    
    #Read the csv file into a Pandas dataframe
    df = read_csvfile(infile)
    if fatal_error == False:
    
        #Process the dataframe and collect statistics
        df, total_rec_count, total_req_type_count, count, maxval, minval, mean = process_dataframe(results_mode, status_type, group_by_option, sort_by_option, status, df)


        if fatal_error == False:
            #Print the stats
            print_stats(group_by_option, total_req_type_count, status_type, count, maxval, minval, mean)
        
            if fatal_error == False:
                #Set some Pandas display options
                set_display_options(group_by_option, nresults)
             
                if fatal_error == False:
                    #Print and plot info about the requests.
                    #Call a different routine if result type is counts versus elapsed days
                    if results_mode == RESULT_MODE_COUNT:
                        df = print_results_counts(df, group_by_option, sort_by_option, nresults, status_type, total_req_type_count, total_rec_count)
                    else:
                        df = print_results_ED(df, group_by_option, sort_by_option, nresults, status_type, total_req_type_count, total_rec_count)
                        
                    if fatal_error == False:
                        #Send the results to an excel file if the user wants to
                        send_results_to_file(df)



    if fatal_error == True:
        routines.append(routine_name)
        print(MSG_PROGRAM_ENDED_ABNORMALLY)
        print(MSG_ERROR_IN_ROUTINES)
        print(routines)        
        

###################################################################################################
#  Gets some runtime parameters from console input
###################################################################################################    
def get_input_parms():
      
    infile = get_infile()
    results_mode = get_results_mode()
    status = get_request_status(results_mode)
    group_by_option = get_group_by_option()
    sort_by_option = get_sort_by_option(group_by_option, results_mode)
    nresults = get_nresults()        
        
    return infile, results_mode, group_by_option, sort_by_option, status, nresults

###################################################################################################
#  Gets the name of the input CSV file and makes sure the file exists
###################################################################################################
def get_infile():
    invalid_infile = True
    
    while invalid_infile:
        infile = input(MSG_ENTER_311_CSV)
        if os.path.exists(infile):
            invalid_infile = False
        else:
            print(MSG_311_FILE_NOT_FOUND)
            invalid_infile = True    

    return infile

###################################################################################################
#  Gets the result mode option, which determines whether request counts or elapsed days will be calculated
###################################################################################################
def get_results_mode():
    
    invalid_option = True
    while invalid_option:
        try:
            results_mode = int(input(MSG_ENTER_RESULT_MODE))
            if results_mode != RESULT_MODE_COUNT and results_mode != RESULT_MODE_ED:
                print(MSG_INVALID_RESPONSE)
                invalid_option = True
            else:
                invalid_option = False
        except ValueError:
            print(MSG_INVALID_RESPONSE)
            invalid_option = True
    
    return results_mode

###################################################################################################
#  Gets the request status of interest and ensures that it is a valid integer value
###################################################################################################
def get_request_status(results_mode):
    
    invalid_status = True
    while invalid_status:
        try:
            #If we will display request counts, all status values will be available
            if results_mode == RESULT_MODE_COUNT:
                status = int(input(MSG_ENTER_STATUS_1))
                if status != 0 and status != 1 and status != 2 and status !=3:
                    print(MSG_INVALID_STATUS)
                    invalid_status = True
                else:
                    invalid_status = False
            else:
                #Displaying elapsed days, so only New and Open statuses make sense to use
                status = int(input(MSG_ENTER_STATUS_2))
                if status != 0 and status !=3:
                    print(MSG_INVALID_STATUS)
                    invalid_status = True
                else:
                    invalid_status = False                
        except ValueError:
            print(MSG_INVALID_STATUS)
            invalid_status = True
    
    return status

###################################################################################################
#  Gets the option to group results by request type or department
###################################################################################################
def get_group_by_option():
    
    invalid_option = True
    while invalid_option:
        try:
            group_by_option = int(input(MSG_ENTER_GROUP_BY_OPTION))
            if group_by_option != GROUP_BY_REQ_TYPE and group_by_option != GROUP_BY_DEPT and group_by_option != GROUP_BY_BOTH:
                print(MSG_INVALID_GROUP_BY_OPTION)
                invalid_option = True
            else:
                invalid_option = False
        except ValueError:
            print(MSG_INVALID_GROUP_BY_OPTION)
            invalid_option = True
    
    return group_by_option

###################################################################################################
#  Gets the option to sort results by request type, department, or request count
###################################################################################################
def get_sort_by_option(group_by_option, results_mode):
    
    invalid_option = True
    while invalid_option:
        try:
            #Make different sorting options available based on the type of grouping the user selected
            #Grouping by REQUEST_TYPE
            if group_by_option == GROUP_BY_REQ_TYPE:
                #Display a different message depending on whether request counts or elapsed days will by displayed
                if results_mode == RESULT_MODE_COUNT:
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_REQ_TYPE_GROUPING_COUNTS))
                else: #results_mode == RESULT_MODE_ED (elapsed days)
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_REQ_TYPE_GROUPING_ED))
                #Validate the input value
                if sort_by_option != SORT_BY_REQ_TYPE and sort_by_option != SORT_BY_REQ_COUNT_OR_ED:
                    print(MSG_INVALID_SORT_BY_OPTION)
                    invalid_option = True
                else:
                    invalid_option = False
                    
            #Grouping by DEPARTMENT        
            elif group_by_option == GROUP_BY_DEPT:
                #Display a different message depending on whether request counts or elapsed days will by displayed
                if results_mode == RESULT_MODE_COUNT:                
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_DEPT_GROUPING_COUNTS))
                else: #results_mode == RESULT_MODE_ED (elapsed days)                
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_DEPT_GROUPING_ED))
                #Validate the input value
                if sort_by_option != SORT_BY_DEPT and sort_by_option != SORT_BY_REQ_COUNT_OR_ED:
                    print(MSG_INVALID_SORT_BY_OPTION)
                    invalid_option = True                              
                else:
                    invalid_option = False
                    
            #Grouping by REQUEST_TYPE, then DEPARTMENT
            elif group_by_option == GROUP_BY_BOTH:
                #Display a different message depending on whether request counts or elapsed days will by displayed
                if results_mode == RESULT_MODE_COUNT:
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_BOTH_GROUPING_COUNTS))
                else:   #results_mode == RESULT_MODE_ED (elapsed days)
                    sort_by_option = int(input(MSG_ENTER_SORT_BY_OPTION_FOR_BOTH_GROUPING_ED))
                #Validate the input value
                if sort_by_option != SORT_BY_REQ_TYPE and sort_by_option != SORT_BY_DEPT and sort_by_option != SORT_BY_REQ_COUNT_OR_ED:
                    print(MSG_INVALID_SORT_BY_OPTION)
                    invalid_option = True
                else:
                    invalid_option = False
                        
        except ValueError:
            print(MSG_INVALID_SORT_BY_OPTION)
            invalid_option = True
    
    return sort_by_option

###################################################################################################
#  Gets the number of records the user wants to display and ensures that it is a valid integer value
###################################################################################################
def get_nresults():
    invalid_nresults = True
    while invalid_nresults:
        try:
            nresults = int(input(MSG_ENTER_NRESPONSE))
            invalid_nresults = False
        except ValueError:
            print(MSG_INVALID_NRESPONSE)
            invalid_nresults = True           
    return nresults

###################################################################################################
#  Sets status type names based on input status for display purposes
###################################################################################################
def set_status_type(status):
    if status == STATUS_NEW:
        status_type = STATUS_TYPE_NEW
    if status == STATUS_CLOSED:
        status_type = STATUS_TYPE_CLOSED
    if status == STATUS_ALL:
        status_type = STATUS_TYPE_ALL
    if status == STATUS_OPEN:
        status_type = STATUS_TYPE_OPEN
    return status_type

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
#  Reads the 311 csv file into a Pandas dataframe
###################################################################################################    
def read_csvfile(infile):
    routine_name = 'read_csvfile'
    try:
        df = pd.read_csv(infile, ',')
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None

    return df
###################################################################################################
#  Extracts relevant data from a dataframe and computes statistics
###################################################################################################
def process_dataframe(results_mode, status_type, group_by_option, sort_by_option, status, df):
    routine_name = 'process_dataframe'
    total_rec_count, total_req_type_count, count, maxval, minval, mean = 0, 0, 0, 0, 0, 0
    
    #Reset the default column index to be the REQUEST_ID column 
    df = set_index(df)
    
    if fatal_error == False:    
        #Get a subset of the columns in the dataframe
        df = extract_cols(df)
        
        if fatal_error == False:
            #Replace blank values in the REQUEST_TYPE and DEPARTMENT fields with 'Unknown'
            df = replace_blanks(df)
            
            if fatal_error == False:
                #Get a total count of records in the dataframe for use in statistics
                total_rec_count = get_total_rec_count(df, group_by_option)
                
                if fatal_error == False:
                    #Filter records by selected status type
                    df = filter_by_status(status_type, status, df)
                
                    if fatal_error == False:
                        #if results mode is count, call function to group and sort counts info
                        if results_mode == RESULT_MODE_COUNT:    
                            df, total_req_type_count = group_and_sort_counts(df, group_by_option, sort_by_option)
                        else:
                            #Results mode is elapsed days
                            #Convert string dates in CREATED_ON column to date objects
                            df = apply_date_conversion(df)
                            if fatal_error == False:
                            
                                #Calculate the number of days requests have been open
                                df = get_elapsed_days(df)
                                if fatal_error == False:
                                    #Call function to group and sort elapsed day info
                                    df, total_req_type_count = group_and_sort_ED(df, group_by_option, sort_by_option) 
                                
                        
                        if fatal_error == False:
                            #Calc basic statistics
                            count, maxval, minval, mean = compute_stats(df)
        
        
    if fatal_error == True:
        print(MSG_UNEXPECTED_INPUT_FORMAT)
        df = None
        #Add routine to call stack for error message
        routines.append(routine_name)
          
    return df, total_rec_count, total_req_type_count, count, maxval, minval, mean

###################################################################################################
# Resets the dataframe index from the default to the request id column 
###################################################################################################
def set_index(df):
    routine_name = 'set_index'
    try:
        #Set the dataframe index to be the '_id' column
        df.set_index(REQUEST_ID, inplace = True)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None        
    return df 

###################################################################################################
# Selects the REQUEST_TYPE and STATUS column data and stores it in a new dataframe 
###################################################################################################
def extract_cols(df):
    routine_name = 'extract_cols'
    try:
        #Extraxt the REQUEST TYPE, STATUS, and DEPARTMENT Columns from the input dataframe
        df = df.loc[:,[CREATED_ON, REQUEST_TYPE, STATUS, DEPARTMENT]]
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None            
    return df 

###################################################################################################
# Replaces blank and NaN values in the REQUEST_TYPE and DEPARTMENT fields with 'Unknown'
###################################################################################################
def replace_blanks(df):
    routine_name = 'replace_blanks'
    try:
        #replace blanks
        df = df.replace({REQUEST_TYPE:'', DEPARTMENT:''}, UNKNOWN)
        #Replace NaN (Not a Number) values with Unknown
        df.fillna(UNKNOWN, inplace = True)
        #df = df.replace({REQUEST_TYPE:'NaN', DEPARTMENT:'NaN'}, UNKNOWN)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None            
    return df


###################################################################################################
# Gets a total count of the records in the dataframe for use in statistics 
###################################################################################################
def get_total_rec_count(df, group_by_option):
    routine_name = 'get_total_rec_count'
    total_rec_count = 0    
    try:
        
        if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_BOTH:
            #Get a total count of all rows in the df for use in stats display
            df_total = df.loc[:,[REQUEST_TYPE]]
        else:
            df_total = df.loc[:,[DEPARTMENT]]
        total_rec_count = df_total.count()
        total_rec_count= int(total_rec_count)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        total_rec_count = 0
        
    return total_rec_count 

###################################################################################################
#  If the status is open, closed, or new, filter records by status
###################################################################################################
def filter_by_status(status_type, status, df):
    routine_name = 'filter_by_status'
    try:
        # use status as selection criteria if status type = CLOSED, OPEN, or NEW 
        if status_type == STATUS_TYPE_CLOSED or status_type == STATUS_TYPE_OPEN or status_type == STATUS_TYPE_NEW:
            status_slice = df[STATUS]
            status_criteria = status_slice == status    #0=new, 1=closed, 3=open  
            df = df[status_criteria]
        # Otherwise, the status_type is ALL, so we don't need selection criteria
        else:
            df = df.loc[:,[CREATED_ON, REQUEST_TYPE, STATUS, DEPARTMENT]]    
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None
    return df 

###################################################################################################
# Applies a date conversion function to string dates in the CREATED_ON column 
###################################################################################################
def apply_date_conversion(df):
    routine_name = 'apply_date_conversion'
    try:
        df[CREATED_ON] = df[CREATED_ON].apply(convert_date)
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None     
    return df

###################################################################################################
# Strips off extraneous text that would be displayed with elapsed days 
###################################################################################################
def strip_days(days):
    routine_name = 'strip_days'
    try:
        days = str(days)
        days_pos = days.find('days')
        if days_pos != -1:
            day_portion = int(days[0:days_pos])
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        day_portion = 0
    return day_portion
    
###################################################################################################
# Converts a date string to a date object in YYYY-mm-dd format 
###################################################################################################
def convert_date(date_time_str):
    routine_name = 'convert_date'
    try:
        datestr = date_time_str[0:10]
        dateobj = datetime.strptime(datestr, "%Y-%m-%d")
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        dateobj = None        
    return dateobj

###################################################################################################
# Calculates how many days a request has been open based on the CREATED_ON value and today's date 
###################################################################################################
def get_elapsed_days(df):
    routine_name = 'get_elapsed_days'
    try:
        now = datetime.now()
        elapsed_days = now - df[CREATED_ON]
        #call function to strip off extraneous text and just save the integer number of days
        elapsed_days_col = elapsed_days.apply(strip_days)
        df[MEAN_ELAPSED_DAYS] = elapsed_days_col    
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        df = None    
    return df

   
###################################################################################################
# Groups dataframe records by REQUEST_TYPE or DEPARTMENT (depending on user-specified group by option), 
# gets counts of each type or department,
# and sorts the results by request count (in descending order)
###################################################################################################        
def group_and_sort_counts(df, group_by_option, sort_by_option):
    routine_name = 'group_and_sort_counts'
    total_req_type_count = 0    
    try: 
 
        if group_by_option == GROUP_BY_REQ_TYPE:
            df = df.loc[:, [REQUEST_TYPE, STATUS]]
            #Rename the second column for display purposes
            df.columns = [REQUEST_TYPE, REQ_COUNT]
            #Get a total count of all requests in the status of interest (open, closed, or all)
            total_req_type_count = int(df[REQUEST_TYPE].count())
            group = df.groupby([REQUEST_TYPE])
            
        elif group_by_option == GROUP_BY_DEPT:
            df = df.loc[:, [DEPARTMENT, STATUS]]
            #Rename the second column for display purposes
            df.columns = [DEPARTMENT, REQ_COUNT]
            #Get a total count of all requests in the status of interest (open, closed, or all)
            total_req_type_count = int(df[DEPARTMENT].count())
            group = df.groupby([DEPARTMENT])
            
        else:   #group_by_option == GROUP_BY_BOTH:
            df = df.loc[:, [REQUEST_TYPE, DEPARTMENT, STATUS]]
            #Rename the last column for display purposes
            df.columns = [REQUEST_TYPE, DEPARTMENT, REQ_COUNT]
            #Get a total count of all requests in the status of interest (open, closed, or all)
            total_req_type_count = int(df[REQUEST_TYPE].count())
            group = df.groupby([REQUEST_TYPE, DEPARTMENT])            
        
        count_requests = group.count()

        #Sort the dataframe based on the user's sorting preference
        if sort_by_option == SORT_BY_REQ_TYPE:
            #Sort first by REQUEST_TYPE (in ascending order), then by REQUEST_COUNT(in descending order)
            sorted_requests = count_requests.sort_values(by=[REQUEST_TYPE, REQ_COUNT], ascending = [True, False])
        elif sort_by_option == SORT_BY_DEPT:
                  #Sort first by DEPARTMENT (in ascending order), then by REQUEST_COUNT(in descending order)
            sorted_requests = count_requests.sort_values(by=[DEPARTMENT, REQ_COUNT], ascending = [True, False])
        else:   #sort_by_option == SORT_BY_REQ_COUNT   
            #sort by REQ_COUNT (in descending order)
            sorted_requests = count_requests.sort_values(by=[REQ_COUNT], ascending = False)            
    
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        sorted_requests = None 
        
    return sorted_requests, total_req_type_count

###################################################################################################
# Groups dataframe records by REQUEST_TYPE or DEPARTMENT (depending on user-specified group by option), 
# gets counts of each type or department,
# and sorts the results by elapsed days (ED) (in descending order)
###################################################################################################        
def group_and_sort_ED(df, group_by_option, sort_by_option):
    routine_name = 'group_and_sort_ED'
    total_req_type_count = 0    
    try:
        #We only need the request type, department, and mean elapsed days columns
        df = df.loc[:, [REQUEST_TYPE, DEPARTMENT, MEAN_ELAPSED_DAYS]]
        
        if group_by_option == GROUP_BY_REQ_TYPE:
            #Group the results by REQUEST TYPE
            total_req_type_count = int(df[REQUEST_TYPE].count())
            group = df.groupby([REQUEST_TYPE])
        elif group_by_option == GROUP_BY_DEPT:
            #Group the results by assigned department
            total_req_type_count = int(df[DEPARTMENT].count())
            group = df.groupby([DEPARTMENT])
        else:
            #Group by both fields
            total_req_type_count = int(df[REQUEST_TYPE].count())
            group = df.groupby([REQUEST_TYPE, DEPARTMENT])
            
        #Get the mean number of open requests within each request type or department
        mean_elapsed_days = group.mean()
        
        #Sort the dataframe based on the user's sorting preference
        if sort_by_option == SORT_BY_REQ_TYPE:
            #Sort first by REQUEST_TYPE (in ascending order), then by MEAN_ELAPSED_DAYS (in descending order)
            sorted_mean_elapsed_days = mean_elapsed_days.sort_values(by=[REQUEST_TYPE, MEAN_ELAPSED_DAYS], ascending = [True, False])
        elif sort_by_option == SORT_BY_DEPT:
                  #Sort first by DEPARTMENT (in ascending order), then by MEAN_ELAPSED_DAYS (in descending order)
            sorted_mean_elapsed_days = mean_elapsed_days.sort_values(by=[DEPARTMENT, MEAN_ELAPSED_DAYS], ascending = [True, False])
        else:   #sort_by_option == SORT_BY_REQ_COUNT_OR_ED   
            #sort by REQ_COUNT (in descending order)
            sorted_mean_elapsed_days = mean_elapsed_days.sort_values(by=[MEAN_ELAPSED_DAYS], ascending = False)

    
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        sorted_mean_elapsed_days = None
        total_req_type_count = 0
        
    return sorted_mean_elapsed_days, total_req_type_count


###################################################################################################
# Gathers basic statistics 
###################################################################################################
def compute_stats(df):
    routine_name = 'compute_stats'
    count, maxval, minval, mean = 0,0,0,0
    try:    
        count = int(df.count())
        maxval = int(df.max())
        minval = int(df.min())
        mean = float(df.mean())
    except Exception as err:
        handle_unexpected_error(err, routine_name)
    return count, maxval, minval, mean 
   
###################################################################################################
# Prints stats about the most common requests 
###################################################################################################    
def print_stats(group_by_option, total_req_type_count, status_type, count, maxval, minval, mean):
    print()
    print('****************************************************')
    print(STATISTICS_FOR + status_type + REQUESTS)
    print()
    if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_BOTH:
        print(f'{TOTAL_REC_COUNT:^15}{COUNT_REQ_TYPES:^25} {MAX:^6}{MIN:^6}{MEAN:^6}')
    else:
        print(f'{TOTAL_REC_COUNT:^15}{COUNT_DEPTS:^25} {MAX:^6}{MIN:^6}{MEAN:^6}')
    print(f'{"---------------":^15}{"----------------------":^25} {"----":^6}{"----":^6}{"------":^6}')
    print(f'{total_req_type_count:^15d}{count:^25d} {maxval:^6d}{minval:^6d}{mean:^6.2f}')

###################################################################################################
# Sets display options for terminal output 
###################################################################################################
def set_display_options(group_by_option, nresults):
    routine_name = 'set_display_options'
    try:
        #set the format of floating point numbers
        pd.options.display.float_format = '{:,.2f}'.format
        #set the maximum num cols that will display in the console based on how many records
        #the user wants to display.  Otherwise Pandas might not display all of them.
        pd.options.display.max_rows = nresults
        if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_DEPT:
            pd.options.display.max_colwidth = MAX_COL_WIDTH_1
        else: #use shorter column widths when req type and department need to be displayed
            pd.options.display.max_colwidth = MAX_COL_WIDTH_2    
        pd.options.display.width = DISPLAY_WIDTH            
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        
###################################################################################################
# Prints a list of request count info and displays a bar chart 
###################################################################################################    
def print_results_counts(df, group_by_option, sort_by_option, nresults, status_type, total_req_type_count, total_rec_count):
    routine_name = 'print_results_counts'    
    try:

        #Add a column for percentage calculation.
        df[PERCENT_TOTAL_REQS] = df[REQ_COUNT] / total_req_type_count * 100

        print()
        print(TOTAL_REQUESTS + str(total_rec_count))
        print(TOTAL + status_type + STATUS_REQUESTS + str(total_req_type_count))
        print()
        
        # 999 means print all results.  Anything else means print the top nresults
        if nresults != ALL_RESULTS:
            #If the results are sorted by REQUEST_COUNT, display appropriate message
            if sort_by_option == SORT_BY_REQ_COUNT_OR_ED:    
                if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_BOTH: 
                    print(TOP + str(nresults) + TYPES_OF + status_type + REQUESTS)
                else:
                    print(TOP + str(nresults) + DEPARTMENTS + status_type + REQUESTS)
            else:
                #Results are sorted by REQUEST_TYPE or DEPARTMENT, so print a generic message
                print(status_type + REQUESTS)
        else:
            print(status_type + REQUESTS)
        
        # Only displaying top results
        if nresults != ALL_RESULTS:
            top_requests = df.head(nresults)
 
            #plot the bar chart if nresults less than 31.  Otherwise it would be unreadable.            
            if nresults < PLOTTING_MAX + 1:
                plot_results_counts(top_requests, group_by_option, status_type)
    
        else:   #999 means that we want all records
            top_requests = df
            #Don't display the bar chart because it will be too big
          
        print()
        print(top_requests)
        print()
        
    except Exception as err:
        handle_unexpected_error(err, routine_name)
        top_requests = None
    
    return top_requests

###################################################################################################
# Prints a list of elapsed day info and displays a bar chart 
###################################################################################################
def print_results_ED(df, group_by_option, sort_by_option, nresults, status_type, total_req_type_count, total_rec_count):
    routine_name = 'print_results_ED'
    try:    
        print()
        print(TOTAL_REQUESTS + str(total_rec_count))
        print(TOTAL + status_type + STATUS_REQUESTS + str(total_req_type_count))
        print() 
        
        
        # 999 means print all results.  Anything else means print the top nresults
        if nresults != ALL_RESULTS:
            #If the results are sorted by elapsed days, display appropriate message
            if sort_by_option == SORT_BY_REQ_COUNT_OR_ED:            
                if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_BOTH:
                    print(TOP + str(nresults) + REQUEST_TYPES_STAYING + status_type + STATUS_THE_LONGEST)
                else:
                    print(TOP + str(nresults) + DEPARTMENTS_WITH_REQUESTS_STAYING_IN + status_type + STATUS_THE_LONGEST)    
            else:
                #Results are sorted by REQUEST_TYPE or DEPARTMENT, so print generic message
                print(status_type + REQUESTS)
        else:
            if sort_by_option == SORT_BY_REQ_COUNT_OR_ED:
                if group_by_option == GROUP_BY_REQ_TYPE or group_by_option == GROUP_BY_BOTH:
                    print(REQUEST_TYPES_STAYING + status_type + STATUS_THE_LONGEST)
                else:
                    print(DEPARTMENTS_WITH_REQUESTS_STAYING_IN + status_type + STATUS_THE_LONGEST)
            else:
                print(status_type + REQUESTS)
                
        # Only displaying top results
        if nresults != ALL_RESULTS:
            top_requests = df.head(nresults)
            
            #plot the bar chart if nresults less than 31.  Otherwise it would be unreadable.            
            if nresults < PLOTTING_MAX + 1:
                plot_results_ED(top_requests, group_by_option, status_type)
    
        else:   #999 means that we want all records
            top_requests = df
            #Don't display the bar chart because it will be too big
           
        print()
        print(top_requests)
        print()

    except Exception as err:
        handle_unexpected_error(err, routine_name)
        top_requests = None
    
    return top_requests

###################################################################################################
#  Plots the dataframe results in a bar chart (in Counts mode)
###################################################################################################
def plot_results_counts(df, group_by_option, status_type):
    routine_name = 'plot_results_counts'
    try:
        
        #Eliminate percentages from plot and just use the Request Count
        df = df.loc[:, ['REQ_COUNT']]
          
        p = df.plot(kind='bar', figsize=(12,7), color='blue', grid = True)
        if group_by_option == GROUP_BY_REQ_TYPE:
            p.set_title(PLOT_COUNT_OF + status_type + PLOT_REQ_BY_REQ_TYPE, fontsize = 15)
            p.set_xlabel(PLOT_REQ_TYPE)
        elif group_by_option == GROUP_BY_BOTH:
            p.set_title(PLOT_COUNT_OF + status_type + PLOT_REQ_BY_REQ_TYPE_AND_DEPT, fontsize = 15)
            p.set_xlabel(PLOT_REQ_TYPE_DEPT)            
        elif group_by_option == GROUP_BY_DEPT:
            p.set_title(PLOT_COUNT_OF + status_type + PLOT_REQ_BY_DEPT, fontsize = 15)
            p.set_xlabel(PLOT_DEPARTMENT)            
        p.set_ylabel(PLOT_COUNT)    

    except Exception as err:
        handle_unexpected_error(err, routine_name)

        
###################################################################################################
#  Plots the dataframe results in a bar chart (in Elapsed Days mode)
###################################################################################################
def plot_results_ED(df, group_by_option, status_type):
    routine_name = 'plot_results_ED'

    try:
        #Build the bar chart    
        p = df.plot(kind='bar', figsize=(12,7), color='blue', grid = True)
        if group_by_option == GROUP_BY_REQ_TYPE:
            p.set_title(PLOT_MEAN_DAYS_REQUESTS_HAVE_STAYED_IN + status_type + PLOT_STATUS + PLOT_BY_REQ_TYPE, fontsize = 15)
            p.set_xlabel(PLOT_REQ_TYPE)
        elif group_by_option == GROUP_BY_BOTH:   
            p.set_title(PLOT_MEAN_DAYS_REQUESTS_HAVE_STAYED_IN + status_type + PLOT_STATUS + PLOT_BY_BOTH, fontsize = 15)
            p.set_xlabel(PLOT_REQ_TYPE_DEPT)
        elif group_by_option == GROUP_BY_DEPT:
            p.set_title(PLOT_MEAN_DAYS_REQUESTS_HAVE_STAYED_IN + status_type + PLOT_STATUS + PLOT_BY_DEPT, fontsize = 15)    
            p.set_xlabel(PLOT_DEPARTMENT)
        p.set_ylabel(PLOT_DAYS)
        
    except Exception as err:
        handle_unexpected_error(err, routine_name)
###################################################################################################
#  Calls functions to see if user wants to send results to a file, 
#  collects a filename, make sure the filename has an extension that the dataframe object can output to,
#  and writes the contents of the dataframe out to a csv or excel file
###################################################################################################        
def send_results_to_file(df):
    global routines
    routine_name = 'send_results_to_file'
    output_to_file = False
    filename = ''
    
    output_to_file = prompt_for_output()
    if output_to_file == True:
        filename = get_output_file_name()
        #test the file extension to see if it's csv, xls, or xlxs.
        #The filename may be altered in the get_output_file_type method
        filetype, filename = get_output_file_type(filename)
        write_output_file(df, filename, filetype)
    else:
        print(MSG_OUTPUT_FILE_NOT_WRITTEN)
        print()

    if fatal_error == True:
        #add routine to call stack
        routines.append(routine_name)        

###################################################################################################
#  Asks the user whether to send the dataframe results to a CSV or Excel file
###################################################################################################        
def prompt_for_output():
    valid_response = False
    output_response = ''
    while valid_response == False:
        response = input(MSG_WRITE_TO_FILE)
        if response.lower() == 'y':
            valid_response = True
            output_response = True
        elif response.lower() == 'n':
            valid_response = True
            output_response = False
        else:
            valid_response = False
            output_response = False
            print(MSG_INVALID_RESPONSE)
    return output_response

###################################################################################################
#  Takes in the name of the output file
###################################################################################################
def get_output_file_name():
    filename = ''
    filename = input(MSG_ENTER_OUTPUT_FILENAME)
    return filename

###################################################################################################
#  Examines the output file's extension to see if's a file type supported by a dataframe engine
###################################################################################################
def get_output_file_type(filename):
    fileext_good = False
    filetype = ''

    while fileext_good == False:
        filename = filename.lower()
        if filename.endswith(EXT_CSV):
            filetype = FILE_TYPE_CSV
            fileext_good = True
        elif filename.endswith(EXT_XLS) or filename.endswith(EXT_XLSX):
            filetype = FILE_TYPE_EXCEL
            fileext_good = True
        else:
            fileext_good = False
            filename = input(MSG_INVALID_FILE_EXTENSION)
    return filetype, filename

###################################################################################################
# Attempts to write the output file 
###################################################################################################
def write_output_file(df, filename, filetype):
    global fatal_error
    global routines
    routine_name = 'write_output_file'
    try_again = True
    if filetype == FILE_TYPE_CSV:
        while try_again == True:
            try:
                df.to_csv(filename)
                try_again = False
                print(FILE_TYPE_CSV + MSG_FILE_SUCCESSFULLY_WRITTEN)
                print()
            except PermissionError:
                response_try_again = input(MSG_FILE_IN_USE)
                if response_try_again.lower() == 'y':
                    try_again = True
                else:
                    try_again = False
                    print()
                    print(FILE_TYPE_CSV + MSG_FILE_NOT_SUCCESSFULLY_WRITTEN)
                    fatal_error = True
                    routines.append(routine_name)
                    return
            except Exception as err:
                try_again = False
                handle_unexpected_error(err, routine_name)
                print(FILE_TYPE_CSV + MSG_FILE_NOT_SUCCESSFULLY_WRITTEN)
                print()
                return
    else:   #filetype is Excel
        while try_again == True:
            try:
                df.to_excel(filename)
                try_again = False
                print(FILE_TYPE_EXCEL + MSG_FILE_SUCCESSFULLY_WRITTEN)
                print()
            except PermissionError:
                response_try_again = input(MSG_FILE_IN_USE)
                if response_try_again.lower() == 'y':
                    try_again = True
                else:
                    try_again = False
                    print(FILE_TYPE_EXCEL + MSG_FILE_NOT_SUCCESSFULLY_WRITTEN)
                    print()
                    fatal_error = True
                    routines.append(routine_name)                    
                    return
            except Exception as err:
                try_again = False
                handle_unexpected_error(err, routine_name)
                return                                 
###################################################################################################
if __name__=='__main__':
    main()   