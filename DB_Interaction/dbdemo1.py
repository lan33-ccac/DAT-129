# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Sample code for basic database operations using an SQLite database
# Author: Lisa Nydick
# Last Modified: 10/25/2019
#####################################
import sqlite3

try:
    #Make the connection object
    dbconn = sqlite3.connect('SQLite_Python_Demo1.db')
    
    #Make the cursor object
    cursor = dbconn.cursor()
    print("Database created and Successfully Connected to SQLite")

    #Build a query to select the version number from SQLie
    select_Query = "select sqlite_version();"
    
    #Execute the query with the cursor object
    cursor.execute(select_Query)
    
    #Fetch the first record (there will only be one)
    record = cursor.fetchone()      #use fetchall or fetchmany to retrieve multiple records
    print("SQLite Database Version is: ", record)
    
except sqlite3.Error as error:
    print("Error while connecting to SQlite", error)
finally:
    #Always close the cursor and database connection
    if dbconn:
        cursor.close()
        dbconn.close()
        print("The SQLite connection is closed.")

