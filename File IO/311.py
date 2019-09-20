# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading 311 Data to Answer Question:
# What type of issue is hardest to fix (or is least prioritized)?
# Author: Lisa Nydick
# Last Modified: 09/17/2019
#####################################

import pandas as pd
#import matplotlib.pyplot as plt


###################################################################################################
# Main Function
###################################################################################################
def main():
    infile = "311_full.csv"
    nresults = 6            #Number of results to be displayed
    #nresults = 999         #999 = Display All results
    status_type = 'OPEN'    #Type of status data you want to see
    #status_type = 'CLOSED'
    #status_type = 'ALL'
    #status_type = 'NEW'
    status = 3     #Open    #Status code used for selection criteria   
    #status = 1    #Closed
    #status = 0    #New

    df = pd.read_csv(infile, ',')
    #Set the dataframe index to be the '_id' column
    df.set_index('REQUEST_ID', inplace = True)
    
    get_stats(df, status_type, status, nresults)    

###################################################################################################
# Manipulates the input dataframe to extract relevant data 
# Calculates statistics based on the data
###################################################################################################        
def get_stats(df, status_type, status, nresults):
    
 
    #Extraxt the REQUEST TYPE and STATUS Columns from the input dataframe
    df_slice = df.loc[:,['REQUEST_TYPE', 'STATUS']]
    
    #Get a total count of all rows in the df slice for use in stats display
    df_total_slice = df_slice.loc[:,['REQUEST_TYPE']]
    total_rec_count = df_total_slice.count()
    total_rec_count= int(total_rec_count)
 
    # use status as selection criteria if status type = CLOSED, OPEN, or NEW 
    if status_type == 'CLOSED' or status_type == 'OPEN' or status_type == 'NEW': 
        status_slice = df_slice['STATUS']
        status_criteria = status_slice == status    #0=new, 1=closed, 3=open  
        reqs = df_slice[status_criteria]

    # Otherwise, the status_type is ALL, so we don't need selection criteria
    else:
        reqs = df_slice.loc[:,['REQUEST_TYPE', 'STATUS']]
       
    #Rename the second column for display purposes
    reqs.columns = ['REQUEST_TYPE', 'REQ_COUNT']
  
    #Get a total count of all requests in the status of interest (open, closed, or all)
    total_req_type_count = int(reqs['REQUEST_TYPE'].count())
    
    #Group the results by REQUEST TYPE
    request_types = reqs.groupby('REQUEST_TYPE')
    
    
    #Get a total count of all open requests within each request type
    count_requests = request_types.count()
    
    #Sort the df by the counts in descending order
    sorted_requests = count_requests.sort_values(by=['REQ_COUNT'], ascending = False)
    
    
    #Collect some statistical stats
    count = int(sorted_requests.count())
    maxval = int(sorted_requests.max())
    minval = int(sorted_requests.min())
    mean = float(sorted_requests.mean())
    std = float(sorted_requests.std())
    
    #Print the stats
    print_stats(total_req_type_count, status_type, count, maxval, minval, mean, std)
    
    #Print the list (dataframe) of counts by request type and print a bar graph
    #of the top n results
    print_results(sorted_requests, nresults, status_type, total_req_type_count, total_rec_count)


###################################################################################################
# Prints stats about the most common open requests 
###################################################################################################    
def print_stats(total_req_type_count, status_type, count, maxval, minval, mean, std):
    print()
    print('****************************************************')
    print('STATISTICS FOR ' + status_type + ' REQUESTS:')
    print()
    print(f'{"Total Reqs":^20}{"Count of Request Types":^25} {"Max":^6}{"Min":^6}{"Mean":^10}{"Std Dev":^10}')
    print(f'{"---------------":^20}{"----------------------":^25} {"---":^6}{"---":^6}{"----":^10}{"-------":^10}')
    print(f'{total_req_type_count:^20d}{count:^25d} {maxval:^6d}{minval:^6d}{mean:^10.2f}{std:^10.2f}')
    
###################################################################################################
# Prints a list of the most comon open requests and displays a bar chart 
###################################################################################################    
def print_results(df, nresults, status_type, total_req_type_count, total_rec_count):
    #set the format of floating point numbers
    pd.options.display.float_format = '{:,.2f}'.format
    #set the maximum num cols that will display in the console
    pd.set_option('display.max_columns', 4)
    print()
    print('Total Requests:' + str(total_rec_count))
    print('Total ' + status_type + ' Status Requests:' + str(total_req_type_count))
    print()
    
    if nresults != 999:
        print('TOP ' + str(nresults) + ' TYPES OF ' + status_type + ' REQUESTS:')
    else:
        print(status_type + ' REQUESTS:')
    
    # Only displaying top results
    if nresults != 999:
        top_requests = df.nlargest(nresults, 'REQ_COUNT')
        
        #Build the bar chart before adding percentage columns    
        p = top_requests.plot(kind='bar', figsize=(10,5), color='blue')
        p.set_title('Count of ' + status_type + ' Requests by Request Type', fontsize = 15)
        p.set_xlabel('Request Type')
        p.set_ylabel('Count')
        #p.legend('Open', loc='best')
    else:   #999 means that we want all records
        top_requests = df
        #Don't display the bar chart because it will be too big


    
    #Add a column for percentage calculation.   
    top_requests['% TOTAL_REQs'] = top_requests['REQ_COUNT'] / total_req_type_count * 100

    print()
    print(top_requests)
    print()

    #send the results to excel
    #top_requests.to_excel('311_out1.xlsx')
        
###################################################################################################
main()    