# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Sample code for manipulating an SQLite Database
# Author: Lisa Nydick
# Last Modified: 10/25/2019
#####################################

import sqlite3
import pandas as pd

###################################################################################################
# 
###################################################################################################
def main():
    
    
    #Create the db connection and cursor
    dbconn, cursor = connect_SQLiteDB()
    
    # If dbconn is something other than None, the database operation completed without error.
    # Don't do subsequent operations if there was a failure in the previous routine.
    if dbconn:
        #Create a table in the database
        dbconn = create_Table(dbconn, cursor)
        if dbconn:
            #Insert a couple of rows into the new table
            dbconn = insert_Rows_Version4(dbconn, cursor)            
            if dbconn:
                #Update a value in a row
                dbconn = update_Row(dbconn, cursor)
                if dbconn:
                    #Select and display all rows in the table
                    dbconn = select_Rows(dbconn, cursor)
                    if dbconn:
                        #Delete all rows in the database
                        dbconn = delete_Rows(dbconn, cursor)
                        if dbconn:
                            #Delete the new table
                            dbconn = drop_Table(dbconn, cursor)
                            if dbconn:
                                #Close the DB connection and cursor
                                close_DB_Resources(dbconn, cursor)
                        
###################################################################################################
# Creates and returns a database connection object and a cursor object
# If the DB doesn't already exist, it will be created.
###################################################################################################    
def connect_SQLiteDB():
    try:
        dbconn = sqlite3.connect('SQLite_Python_Demo2.db')
        cursor = dbconn.cursor()
        print()
        print("Successfully Connected to SQLite Database")
               
    except sqlite3.Error as error:
        print("Error while connecting to SQLite", error)
        dbconn = handle_DB_Error(dbconn, cursor)
        
    return dbconn, cursor

###################################################################################################
# Creates a table called "users" in the database
###################################################################################################       
def create_Table(dbconn, cursor):

    query_create_table ='''CREATE TABLE IF NOT EXISTS
                            users(
                            id INTEGER PRIMARY KEY, 
                            name TEXT,
                            phone TEXT, 
                            email TEXT unique, 
                            password TEXT)'''

# Type Conversions:
# Python Type   SQLite Type
# -----------   -----------
# str           TEXT
# int           INTEGER
# float         REAL
# byte          BLOB
# None          Null

    try:
        #Execute the query
        cursor.execute(query_create_table)
        #Commit the transaction
        dbconn.commit()
        print()
        print('Table created or accessed successfully.')
    
    except sqlite3.Error as error: 
        print('Error occurred when creating table.', error)
        dbconn = handle_DB_Error(dbconn, cursor)        
    
    #This will be None if there was an error
    return dbconn    

###################################################################################################
# Inserts 2 rows into the new table using 2 insert and 2 cursor.execute methods
###################################################################################################
def insert_Rows_Version1(dbconn, cursor):
     
    insert_query1 = '''INSERT INTO users(name, phone, email, password)
                  VALUES('Lisa', '4124018564', 'lisa@nydick.com', 'baseba11')'''
    
    insert_query2 = '''INSERT INTO users(name, phone, email, password)
                  VALUES('Dan', '4129013268', 'dan@nydick.com', 'xrfds4@83')'''

    try: 
        #Use execute method twice, once for each insert query                 
        cursor.execute(insert_query1)
        cursor.execute(insert_query2)
        dbconn.commit()
        print()
        print('Rows added successfully.')

    except sqlite3.IntegrityError:
        print('Record(s) already exist(s).')
        dbconn.rollback()

    except sqlite3.Error as error: 
        print('Error occurred when adding a user.', error)
        dbconn = handle_DB_Error(dbconn, cursor)

    return dbconn

###################################################################################################
# Inserts 2 rows into the new table using 2 insert and 2 cursor.execute methods
###################################################################################################
def insert_Rows_Version2(dbconn, cursor):
  
    sql_script = '''INSERT INTO users(name, phone, email, password)
                        VALUES('Lisa', '4124018564', 'lisa@nydick.com', 'baseba11');
                    INSERT INTO users(name, phone, email, password)
                        VALUES('Dan', '4129013268', 'dan@nydick.com', 'xrfds4@83');'''

    try: 
        #Use executescript method to execute all SQL commands in script                 
        cursor.executescript(sql_script)
        dbconn.commit()
        print()
        print('Rows added successfully.')

    except sqlite3.IntegrityError:
        print('Record(s) already exist(s).')
        dbconn.rollback()

    except sqlite3.Error as error: 
        print('Error occurred when adding a user.', error)
        dbconn = handle_DB_Error(dbconn, cursor)

    return dbconn

###################################################################################################
# Inserts 2 rows into the new table using a parameterized query
###################################################################################################
def insert_Rows_Version3(dbconn, cursor):
    
    #Build tuples for each set of values
    user1 = ('Lisa', '4124018564', 'lisa@nydick.com', 'baseba11')
    user2 = ('Dan', '4129013268', 'dan@nydick.com', 'xxfds4@83')
    
    #Parameterized query
    insert_query = '''INSERT INTO users(name, phone, email, password)
                  VALUES(?,?,?,?)'''

    try: 
        #Call execute method twice, once for each user
        cursor.execute(insert_query, user1)
        cursor.execute(insert_query, user2)
        dbconn.commit()
        print()
        print('Rows added successfully.')

    except sqlite3.IntegrityError:
        print('Record(s) already exist(s).')
        dbconn.rollback()

    except sqlite3.Error as error: 
        print('Error occurred when adding a user.', error)
        dbconn = handle_DB_Error(dbconn, cursor)

    return dbconn    
###################################################################################################
# Inserts 2 rows into the new table using a list of tuples and a parameterized query
# with the .executemany method
###################################################################################################
def insert_Rows_Version4(dbconn, cursor):

    
    #Build a list of tuples
    users = [('Lisa', '4124018564', 'lisa@nydick.com', 'baseba11'),
             ('Dan', '4129013268', 'dan@nydick.com', 'xxfds4@83')]
    
    #Parameterized query
    insert_query = '''INSERT INTO users(name, phone, email, password)
                  VALUES(?,?,?,?)'''

    try: 
        #Use executemany method to insert the list of tuples                 
        cursor.executemany(insert_query, users)
        dbconn.commit()
        print()
        print('Rows added successfully.')

    except sqlite3.IntegrityError:
        print('Record(s) already exist(s).')
        dbconn.rollback()

    except sqlite3.Error as error: 
        print('Error occurred when adding a user.', error)
        dbconn = handle_DB_Error(dbconn, cursor)

    return dbconn

###################################################################################################
# Updates a field value in the table
###################################################################################################            
def update_Row(dbconn, cursor):
    
    old_email = 'lisa@nydick.com'
    new_email = 'lisa.nydick@gmail.com'
    update_query = '''UPDATE users SET email = ? WHERE email = ? '''
     
    try:
        cursor.execute(update_query, (new_email, old_email))
        dbconn.commit()
        print()
        print('Value updated successfully.')
        
    except sqlite3.Error as error: 
        print('Error occurred when updating a user.', error)
        dbconn = handle_DB_Error(dbconn, cursor)
    
    return dbconn

###################################################################################################
# Selects all rows from the table and displays them with a print statement
# Also loads a pandas dataframe from sql and displays the contents of the dataframe
###################################################################################################
def select_Rows(dbconn, cursor):
    
    select_query = '''Select * from users'''
    
    try:
        cursor.execute(select_query)
        rows = cursor.fetchall()
        print()
        print(f'{"id":<5}{"name":>5}{"phone":>12}{"email":>25}{"password":>10}')
        for row in rows:
            print(f'{row[0]:<5}{row[1]:>5}{row[2]:>12}{row[3]:>25}{row[4]:>10}')
            
        #To store recordset in a Pandas dataframe:
        df= pd.io.sql.read_sql(select_query, dbconn)
        print()
        print('Pandas dataframe containing recordset:')
        pd.set_option('display.max_columns', 5)
        pd.set_option('display.width', 800)
        df.set_index('id', inplace = True)
        print(df)
        
        
    except sqlite3.Error as error: 
        print('Database error occurred when selecting records.', error)
        dbconn = handle_DB_Error(dbconn, cursor)
    except Exception as err:    #in case a Pandas error occurs
        print('Unexpected error occurred when displaying records.', err)
        
    return dbconn

###################################################################################################
# Deletes all rows from the users table
###################################################################################################
def delete_Rows(dbconn, cursor):
    
    delete_query = '''DELETE FROM users'''
    
    try:
        cursor.execute(delete_query)
        dbconn.commit()
        print()
        print('Deleted all users successfully.')

    except sqlite3.Error as error: 
        print('Error occurred when deleting user records.', error)
        dbconn = handle_DB_Error(dbconn, cursor)
        
    return dbconn

###################################################################################################
# Deletes the users table
###################################################################################################            
def drop_Table(dbconn, cursor):
    
    drop_query = '''DROP TABLE users'''
    
    try:
        cursor.execute(drop_query)
        dbconn.commit()
        print()
        print('Dropped table successfully.')
        
    except sqlite3.Error as error: 
        print('Error occurred when dropping table.', error)
        dbconn = handle_DB_Error(dbconn, cursor)        

    return dbconn

###################################################################################################
# Handles sqlite3 errors by rolling back transactions and closing DB resources
###################################################################################################
def handle_DB_Error(dbconn, cursor):
    if dbconn:
        try:
            #rollback changes since the last commit
            dbconn.rollback()
            print('Rolled back transaction.')

        except sqlite3.Error as error:
            print('Error rolling back transaction.', error)
            
        finally:
            #call function to close DB connection and cursor
            close_DB_Resources(dbconn, cursor)        
            dbconn = None
            return dbconn

###################################################################################################
# Closes the DB Connection and Cursor so the DB won't become locked
###################################################################################################    
def close_DB_Resources(dbconn, cursor):
    try:
        cursor.close()
        dbconn.close()
        print()
        print('DB resources were closed successfully.')
    except sqlite3.Error as error:
        print('Error occurred closing DB resources.', error)
        
###################################################################################################
if __name__=='__main__':
    main()




