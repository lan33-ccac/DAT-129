# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Sample connection strings for some popular databases
# Author: Lisa Nydick
# Last Modified: 10/25/2019
#####################################


######################
# SQLite Databases
######################
import sqlite3
dbconn = sqlite3.connect('mydbname')

######################
# mySQL Databases
######################
import MySQLdb
dbconn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

######################
# PostgreSQL Databases
######################
import psycopg2
dbconn = psycopg2.connect(database=db, user=user, password=password, host=host, port="5432")

######################
# ODBC Databases
######################
import pyodbc
#SQL Server
dbconn = pyodbc.connect('Driver={odbcdriver};Server=servername;Database=dbname;Trusted_Connection=yes;')

#MS Access
dbconn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=db_file_path;')
######################
# Oracle Databases 
######################
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('Host Name', 'Port Number', service_name='Service Name')
dbconn = cx_Oracle.connect(user='User Name', password='Personal Password', dsn=dsn_tns)

######################
# DB2 Databases
######################
import DB2
dbconn = DB2.connect(dsn='sample', uid='db2inst1', pwd='******')