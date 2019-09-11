# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:46:10 2019

@author: lnydi
"""

from dbquery import DBQuery
import pandas as pd
#import getpass
import sys


def main():
    odbcdriver = ''
    dbserver = ''
    dbname = ''
    trusted = 'no'
    uid = ''
    pwd = ''
    fatal_error = False
    
    #Call function to gather db connection values from user input
    odbcdriver, dbserver, dbname, trusted, uid, pwd = get_dbconnection_info()
    
    #Build the ODBC Connection String using the values just collected
    connstr = buildconnstr(odbcdriver, dbserver, dbname, trusted, uid, pwd)
    print(connstr)
    
    #Test the connection
    fatal_error = test_connection(connstr)
  
    #If the connection was successful, call function to get user's SQL string and execute it    
    if fatal_error == False:
        execute_query(connstr)
    
            
def get_dbconnection_info():
    odbcdriver = ''
    dbserver = ''
    dbname = ''
    validtrusted = False
    trusted = ''
    uid = ''
    pwd = ''
    
    odbcdriver = input('Enter the ODBC Driver Name (e.g., SQL Server):')
    dbserver = input('Enter the Database Server Name (e.g., MyPC\SQLEXPRESS):')
    dbname = input('Enter the Database Name:')
    
    validtrusted = False
    while validtrusted == False:
        trusted = input('Is this a Trusted Connection? ("yes" or "no") ')
        if trusted.lower() == 'yes' or trusted.lower() == 'no':
            validtrusted = True
            trusted = trusted.lower()
        else:
            print('Trusted Connection value was invalid.  Must be yes or no.  Try again.')
    
    if trusted == 'no':
        #prompt for uid and pwd
        uid = input('Enter Database Userid:')
        #pwd = getpass.getpass('Enter Database Password:')
        pwd = input('Enter Database Password:')
    
    return odbcdriver, dbserver, dbname, trusted, uid, pwd
 
#Builds the ODBC connection string 
def buildconnstr(odbcdriver, dbserver, dbname, trusted, uid, pwd):
    buildstr = 'Driver={' + odbcdriver +'};Server='+ dbserver + ';Database=' + dbname
    if str(trusted).lower() == 'yes' or str(trusted).lower()== 'true':
        buildstr = buildstr + '; Trusted_Connection=yes;'
    else:
        buildstr = buildstr + ';UID=' + uid + ';PWD=' + pwd + ';'
    connstr = buildstr
    return connstr

def test_connection(connstr):
    sqlstr = ''     #SQL string will be blank.  It's not needed yet, but one has to be passed to the DBQuery class
    fatal_error = False
    try:
        #Call class to test the connection
        myquery = DBQuery(connstr, sqlstr)
        cnxn = myquery.get_connection()
        if cnxn != None:
            print('Database Connection was Successful.')
        else:
            print('Database Connection Failed.  Ending Program.')
            fatal_error = True
    except Exception as err:
        print('Database Connection Failed. Ending program.')
        print(err)
        fatal_error = True
    return fatal_error

def execute_query(connstr):
    excel_out_file = ''       
    keeplooping = 'yes'
    while keeplooping == 'yes':


        sqlstr = input("Enter SQL String to be Executed:")
        #Get a new instance of the class with the updated sql string
        myquery = DBQuery(connstr, sqlstr)
        
        #If the SQL represents a SELECT statement, return data as a pandas dataframe and write to Excel file
        if sqlstr.upper().startswith('SELECT'):
            df = pd.DataFrame()
            try:
                df = myquery.get_dataframe()
                if df.empty == False:
                    print('Dataframe was created Successfully.')
                    excel_out_file = input('Enter Excel Output File Path:')
                    try:
                        df.to_excel(excel_out_file)
                        print('Dataframe Successfully Written to Excel File: ' + excel_out_file)
                    except Exception as err:
                        print('Dataframe was NOT Successfully Written to File.')
                        print(err)
                else:
                    print('Dataframe Creation was Not Successful or Returned No Results.')
                
            except Exception as err:
                print('Dataframe Creation was NOT Successful.')
                #print(err)
                #keeplooping = 'no'
                        
        else:   #execute cursor              
            try:
                myquery.exe_cursor()
                print('SQL Statement was Successfully Executed.')
            except Exception as err:
                print('SQL Statement was Not Successfully Executed.')
                print(err)
              
        #See if the user wants to execute more SQL Statements
        exitstatus = input('Execute Another SQL Statement? ("yes" or "no":) ')
        if exitstatus.lower() != 'yes' and exitstatus != 'y':
            keeplooping = 'no'
            print('Ending Program')
            
            
#def buildsql():
    #sqlstr = "INSERT INTO dbo.Test_Table (TestField1, TestField2) VALUES ('C1', 'C2');"
    #sqlstr = "DELETE FROM dbo.Test_Table WHERE TestField1 = 'C1';"
    #sqlstr = "SELECT Display_Last_Name, Display_First_Name, Pub_Year, Title from dbo.Author_Pubs WHERE Search_Last_Name Like 'Zhan%';"
    #return sqlstr


main()    