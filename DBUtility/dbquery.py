# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:27:19 2019

@author: lnydi
"""
import pyodbc
import pandas as pd


class DBQuery: 
    
    def __init__(self, connstr, sql):
        self.__connstr = connstr
        self.__sql = sql
        
    def set_connstr(self, connstr):
        self.__connstr = connstr
        
    def set_sql(self, sql):
        self.__sql = sql
        
    def get_connstr(self):
        return self.__connstr
    
    def get_sql(self):
        return self.__sql
    
    def get_connection(self):
        try:
            cnxn = pyodbc.connect(self.get_connstr())
            #Set autocommit so changes get saved to the database
            cnxn.autocommit=True
            #return the connection
            return cnxn
        except Exception as err:
            if str(err).find('IM002') != -1:
                print('Database Connection failed due to an invalid ODBC data source name:')
            elif str(err).find('08001') != -1:
                print('SQL Server Name does not exist, or access to it is denied:')
            elif str(err).find('42000') != -1:
                print('Database name does not exist, or login failed:')
            elif str(err).find('28000') != -1:
                print("User ID does not exist or doesn't haver permissions to the database:")
            print(err)
            #Return None instead in place of a connection
            return None
                
                
        #return cnxn
    
    def exe_cursor(self):   #recordset curser     
        try:
            cnxn = self.get_connection()
            #cnxn = connection
            cursor = cnxn.cursor()
            cursor = cursor.execute(self.get_sql())
        except Exception as err:
            if str(err).find('42000') != -1:
                print('SQL Keyword Error:')               
            elif str(err).find('42S02'):
                print('SQL Table or Field Name Not Found:')             
            elif str(err).find('HY090'):
                print('Missing SQL String:')
            print(err)
  

    
    def get_dataframe(self):    #pandas dataframe
        try:
            cnxn = self.get_connection()
            #cnxn = connection
            df= pd.io.sql.read_sql(self.get_sql(), cnxn)
            #return the dataframe if it executed successfully
            return df
        except Exception as err:
            if str(err).find('42000') != -1:
                print('SQL Keyword Error:')               
            elif str(err).find('42S02'):
                print('SQL Table or Field Name Not Found:')             
            elif str(err).find('HY090'):
                print('Missing SQL String:')
            print(err)
            #Return the None object if the dataframe was not created successfully
            return df.empty
        