# -*- coding: utf-8 -*-
###################################################################################################
# DAT-129
# Purpose: Reads a very large csv file into a Pandas dataframe and loads it into
# a SQL Server database via SQLAlchemy
# Author: Lisa Nydick
# Last Modified: 11/18/19
###################################################################################################
# download and inspect CSV file to anticipate needs in creating a database table to store info
# Convert Yes/No to boolean

# Read in first row of test file and convert polluted header row to clean, pretty, compatible
# database column names


import re
import pandas as pd
from sqlalchemy import create_engine
import urllib

cleancols = []
with open("crashtest.csv", 'r') as ctfile:
    head = ctfile.readlines()[0]    #get column names in header row
    #print(head)
    cols = head.split(',')  #makes a list
    #print(cols)
    exp_space = re.compile('\s+')    #grabs whitespaces
    exp_weird = re.compile('\W+')   #weird character
    for entry in cols:
        prettycol= exp_space.sub('_', entry).lower()    #replace with underscore, lowercase
        #print(prettycol)
        #finalcol = exp_weird.sub('', prettycol)
        
        cleancols.append(exp_weird.sub('', prettycol))
    #print(cleancols)

# Try pandas approach

df = pd.read_csv("crash_data_full.csv", skiprows=1, names=cleancols, true_values = ['Yes'], false_values = ['No'], index_col = 'crash_record_number')
#pd.options.display.max_columns = 10
#pd.options.display.max_colwidth = 20
#pd.options.display.width = 110
#print(df)


    
try:
    params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=MSI\SQLEXPRESS;DATABASE=Accidents;Trusted_Connection=yes;")
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    print('Successfully created the SQLALchemy engine.')
    
except Exception as err:
    print('Error creating the SQLAlchemy engine', err)

try:
    df.to_sql('Crashes', con=engine, if_exists='replace', index_label = 'crash_record_number', chunksize=100)
    print('Successfully added data to table.')

except Exception as err:
    print('Error occured adding data to table.', err)
    