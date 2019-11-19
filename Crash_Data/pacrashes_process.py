# -*- coding: utf-8 -*-
###################################################################################################
# DAT-129
# Purpose: Use Pandas to extract info from a SQL Server database containing PA accident data
# to answer the following questions:
# 1. Do More Accidents Involving Fatalities Occur in Rural or Urban Areas?
# 2. Do More Accidents Occur on Curved or Straight Pieces of Roads?
# 3. In which PA Counties do the Most Accidents Occur?
# 4. Which Allegheny County Municipalities Have the Highest Number of Fatal Accidents?
# 5. What Type of Driver Impairment is Involved in the Most Accidents?
# 6. What Types of Roads (e.g., State, Local, Interstate, or Turnpike) are Involved in the Most Accidents?
# Author: Lisa Nydick
# Last Modified: 11/18/19
###################################################################################################

from sqlalchemy import create_engine
import urllib
import pandas as pd

###################################################################################################
#  Main Function
###################################################################################################
def main():
    #Establish a connection to SQL Server through SQLAlchemy
    engine = create_db_engine()
    if engine != None:
        
        #Set Pandas display options
        set_pandas_display_options()
        
        #Use Pandas to determine whether more accidents involving fatalities occur in rural or urban areas
        create_area_type_dataframe(engine)
        
        #Use Pandas to determine whether more accidents occur on straight or curved roads
        create_road_shape_dataframe(engine)
        
        #Use Pandas to determine which PA counties have the greatest number of accidents
        create_PA_counties_dataframe(engine)
        
        #Use Pandas to determine which Allegheny County municipalities have the greatest number of fatal accidents
        create_allegheny_county_dataframe(engine)
        
        #Use Pandas to determine which type of impairment is most commonly involved in accidents
        create_impairment_dataframe(engine)
        
        #Use Pandas to determine what type of road is most commonly involved in accidents
        create_road_type_dataframe(engine)

###################################################################################################
#  Creates an SQLAlchemy DB Engine that can be passed to Pandas
###################################################################################################    
def create_db_engine():
   
    try:
        params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=MSI\SQLEXPRESS;DATABASE=Accidents;Trusted_Connection=yes;")
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        print('Successfully created the SQLAlchemy engine.')
        
    except Exception as err:
        print('Error occurred creating thenSQLAlchemy engine', err)
        engine = None
    
    finally:    
        return engine

###################################################################################################
#  Sets Pandas display options
###################################################################################################
def set_pandas_display_options():
    #Floating point number format
    pd.options.display.float_format = '{:,.2f}'.format    

###################################################################################################
#  Use Pandas to determine whether more accidents involving fatalities occur in rural or urban areas
#  1. Execute an SQL Select Query
#  2. Get a total count of accidents
#  3. Group the dataframe by area type (e.g., urban vs rural)
#  4. Count the records in each group
#  5. Add a column to the dataframe that calculates percentage of totals for each group
#  6. Display and plot stats
###################################################################################################    
def create_area_type_dataframe(engine):

    try:
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, urban__rural FROM Crashes WHERE fatal = 1;"
        
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('Do More Accidents Involving Fatalities Occur in Rural or Urban Areas?', 
                      'Total Number of Accidents Involving Fatalities: ', 
                      total_recs)
        
        #Rename columns, group by a column, sort values by counts, and add a percentage of total recs column 
        df = rename_cols_group_sort_df(df, 'Counts', 'Area Type', total_recs)      
           
        #Print the dataframe
        print_dataframe(df)

        #Eliminate percentages from plot
        df = df = df.loc[:, ['Counts']]
        
        #Plot the dataframe in a bar chart
        plot_dataframe(df,'Types of Areas Involved in Accidents with Fatalities', 'Area Type', 'Counts', 'blue' )   

    except Exception as err:
        print('Unexpected Error Occurred in function create_area_type_dataframe: ', err)
        
###################################################################################################
#  Use Pandas to determine whether more accidents occur on curved or straight pieces of roads
#  1. Execute an SQL Select Query
#  2. Get a total count of accidents
#  3. Map True/False values from the database into text values
#  4. Group the dataframe by road shape (e.g., curved vs. straight)
#  5. Count the records in each group
#  6. Add a column to the dataframe that calculates percentage of totals for each group
#  7. Display and plot stats
################################################################################################### 
def create_road_shape_dataframe(engine):

    try:
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, curved_road FROM Crashes;"
        
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('Do More Accidents Occur on Curved or Straight Pieces of Roads?', 
                      'Total Number of Accidents: ', 
                      total_recs)
        
        df = map_true_false_values(df, 'curved_road', 'Curved', 'Straight')
        
        #Rename columns, group by a column, sort values by counts, and add a percentage of total recs column 
        df = rename_cols_group_sort_df(df, 'Counts', 'Road Shape', total_recs)      
           
        #Print the dataframe
        print_dataframe(df)

        #Eliminate percentages from plot
        df = df = df.loc[:, ['Counts']]
        
        #Plot the dataframe in a bar chart
        plot_dataframe(df,'Accidents Involving Curved vs. Straight Roads', 'Road Shape', 'Counts', 'green' )

    except Exception as err:
        print('Unexpected Error Occurred in function create_county_dataframe: ', err)

###################################################################################################
#  Use Pandas to determine which PA counties have the greatest number of accidents
#  1. Execute an SQL Select Query
#  2. Get a total count of accidents
#  3. Group the dataframe by county
#  4. Count the records in each group
#  5. Add a column to the dataframe that calculates percentage of totals for each group
#  6. Display and plot stats
###################################################################################################
def create_PA_counties_dataframe(engine):

    try:
     
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, county_name FROM Crashes;"
            
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('Which PA Counties Have the Greatest Number of Accidents?', 
                      'Total Number of Accidents: ', 
                      total_recs)
        
            #Rename columns, group by a column, sort values by counts, and add a percentage of total recs column 
        df = rename_cols_group_sort_df(df, 'Counts', 'County', total_recs)      
           
        #Print the dataframe
        print_dataframe(df)
 
        #Eliminate percentages from plot
        df = df = df.loc[:, ['Counts']]
       
        #Plot the dataframe in a bar chart
        plot_dataframe(df,'Number of Accidents by County', 'County', 'Counts', 'orange' )
        
        
    except Exception as err:
        print('Unexpected Error Occurred in function create_PA_counties_dataframe: ', err)


###################################################################################################
#  Use Pandas to determine which Allegheny County municipalities have the greatest number of fatal accidents
#  1. Execute an SQL Select Query
#  2. Get a total count of fatal accidents
#  3. Group the dataframe by county
#  4. Count the records in each group
#  5. Add a column to the dataframe that calculates percentage of totals for each group
#  6. Display and plot stats
###################################################################################################
def create_allegheny_county_dataframe(engine):

    try:
     
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, municipality_name FROM Crashes WHERE county_name = 'Allegheny' AND fatal > 0;"
            
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('Which Allegheny County Municipalities Have the Greatest Number of Fatal Accidents?', 
                      'Total Number of Fatal Accidents: ', 
                      total_recs)
        
        #Rename columns, group by a column, sort values by counts, and add a percentage of total recs column 
        df = rename_cols_group_sort_df(df, 'Counts', 'Municipality', total_recs)      
        

        #Print the dataframe
        print_dataframe(df)
        
        #Eliminate percentages from plot
        df = df = df.loc[:, ['Counts']]
        
        #Return only the top 10 results
        df = df.nlargest(10, 'Counts')
                
        #Plot the dataframe in a bar chart
        plot_dataframe(df,'Top 10 Allegheny County Municipalities with Fatal Accidents', 'Municipality', 'Counts', 'cyan' )
        
        
    except Exception as err:
        print('Unexpected Error Occurred in function create_allegheny_county_dataframe: ', err)

        
###################################################################################################
#  Use Pandas to determine what type of driver impairments are involved in the most accidents
#  1. Execute an SQL Select Query
#  2. Get a total count of accidents
#  3. Call the process_impairment function to collect data about each type of impairment
#  4. Combine the resulting dataframes into a single dataframe
#  5. Add a column to the dataframe that calculates percentage of totals for each impairment
#  6. Display and plot stats
###################################################################################################    
def create_impairment_dataframe(engine):

    try:
     
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, drinking_driver, distracted, cell_phone, fatigue__asleep, drugged_driver FROM Crashes;"
            
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('What Type of Driver Impairment is Involved in the Most Accidents?', 
                      'Total Number of Accidents: ', 
                      total_recs)
        
        #Process each possible type of impairment
        df1 = process_impairment(df, 'drinking_driver', 'Drinking Driver?', 'Drinking Driver', 'Non Drinking Driver')
        df2 = process_impairment(df, 'distracted', 'Distracted Driver?', 'Distracted Driver', 'Non Distracted Driver')
        df3 = process_impairment(df, 'cell_phone', 'On Cell Phone Driver?', 'On Cell Phone Driver', 'Not on Cell Phone Driver')
        df4 = process_impairment(df, 'fatigue__asleep', 'Fatigued Driver?', 'Fatigued Driver', 'Non Fatigued Driver')
        df5 = process_impairment(df, 'drugged_driver', 'Drugged Driver?', 'Drugged Driver', 'Non Drugged Driver')
           
        #concatinate the dataframes
        frames = [df1, df2, df3, df4, df5]
        newdf = pd.concat(frames)
        
       # Sort group counts in descending order
        newdf = sort_by_count(newdf, 'Counts')
        
        #Add a percent of total records column to the dataframe
        newdf = add_percentage_col(newdf, 'Counts', total_recs )
        
        #Print the dataframe
        print_dataframe(newdf)
        
        #Plot the dataframe in a bar chart
        plot_dataframe(newdf, 'Accidents Involving Different Forms of Driver Impairment', 'Impairement Type', 'Counts', 'orange' )  

    except Exception as err:
        print('Unexpected Error Occurred in create_impairment_dataframe function: ', err)   

###################################################################################################
#  Processes a single type of impairment and returns a dataframe for that type of impairment
#  with counts
###################################################################################################
def process_impairment(df, col_name, new_col_name, truevalue, falsevalue):
    
    try:
        #Create a dataframe from the crash_record_number and impairement columns
        df = df.loc[:, ['crash_record_number', col_name]] 
        
        # Change True/False values
        df = map_true_false_values(df, col_name, truevalue, falsevalue)
        
        #rename columns for display purposes
        df = rename_cols(df, 'Counts', new_col_name)
        
        #filter on impairment type
        impairment = df[new_col_name] == truevalue
        df_filtered = df[impairment]
        
        #group on filtered value to retain dataframe
        df = group_col(df_filtered, new_col_name)
        
        # Get count of impairments
        df = get_group_count(df)
                
        return df
    
    except Exception as err:
        print('Unexpected Error Occurred in process_impairment function: ', err)  

###################################################################################################
#  Use Pandas to determine what type of driver impairments are involved in the most accidents
#  1. Execute an SQL Select Query
#  2. Get a total count of accidents
#  3. Call the process_impairment function to collect data about each type of impairment
#  4. Combine the resulting dataframes into a single dataframe
#  5. Add a column to the dataframe that calculates percentage of totals for each impairment
#  6. Display and plot stats
###################################################################################################    
def create_road_type_dataframe(engine):

    try:
     
        #Build a SQL SELECT query to select the columns we need
        sql = "SELECT crash_record_number, interstate, state_road, local_road_only, turnpike FROM Crashes;"
            
        #Call function to execute the SQL query
        df = execute_query(sql, engine)
        
        #Get the total count of accident records
        total_recs = get_total_recs(df, 'crash_record_number')
    
        if total_recs == 0:
            return
         
        print_headers('What Type of Road is Involved in the Most Accidents?', 
                      'Total Number of Accidents: ', 
                      total_recs)
        
        #Process each possible type of impairment
        df1 = process_road_type(df, 'interstate', 'Interstate?', 'Interstate', 'Non Interstate')
        df2 = process_road_type(df, 'state_road', 'State Road?', 'State Road', 'Non State Road')
        df3 = process_road_type(df, 'local_road_only', 'Local Road?', 'Local Road', 'Non Local Road')
        df4 = process_road_type(df, 'turnpike', 'Turnpike?', 'Turnpike', 'Non Turnpike')
           
        #concatinate the dataframes
        frames = [df1, df2, df3, df4]
        newdf = pd.concat(frames)
        
       # Sort group counts in descending order
        newdf = sort_by_count(newdf, 'Counts')
        
        #Add a percent of total records column to the dataframe
        newdf = add_percentage_col(newdf, 'Counts', total_recs )
        
        #Print the dataframe
        print_dataframe(newdf)
        
        #Plot the dataframe in a bar chart
        plot_dataframe(newdf, 'Accidents Involving Different Types of Roads', 'Road Type', 'Counts', 'pink' )  

    except Exception as err:
        print('Unexpected Error Occurred in create_road_type_dataframe function: ', err)   

###################################################################################################
#  Processes a single type of road and returns a dataframe for that type of road
#  with counts
###################################################################################################
def process_road_type(df, col_name, new_col_name, truevalue, falsevalue):
    
    try:
        #Create a dataframe from the crash_record_number and impairement columns
        df = df.loc[:, ['crash_record_number', col_name]] 
        
        # Change True/False values
        df = map_true_false_values(df, col_name, truevalue, falsevalue)
        
        #rename columns for display purposes
        df = rename_cols(df, 'Counts', new_col_name)
        
        #filter on impairment type
        road_type = df[new_col_name] == truevalue
        df_filtered = df[road_type]
        
        #group on filtered value to retain dataframe
        df = group_col(df_filtered, new_col_name)
        
        # Get count of impairments
        df = get_group_count(df)
                
        return df
    
    except Exception as err:
        print('Unexpected Error Occurred in process_road_type function: ', err)  

###################################################################################################
# Uses Pandas to execute a SQL Query and store the results in a dataframe 
###################################################################################################
def execute_query(sql, engine):    
    try:
        df = pd.read_sql_query(sql, engine)
        return df        
    except Exception as err:
        print('Unexpected Error Occurred in execute_query function: ', err)    

###################################################################################################
# Gets and returns the total number of records returned by a SQL query 
###################################################################################################
def get_total_recs(df, col):
    try:
        total_recs = int(df[col].count())            
    except Exception as err:
        print('Unexpected Error Occurred in get_total_recs function: ', err)    
        total_recs = 0    
    finally:
        return total_recs    

###################################################################################################
# Prints dataframe header info, including the question being asked,
# The type of total being displayed, and the total itself
###################################################################################################    
def print_headers(question, total_description, total_recs):
    print()
    print(question)
    print()
    print(total_description + str(total_recs))

###################################################################################################
# Substitutes string values for True/False values 
###################################################################################################
def map_true_false_values(df, col, trueval, falseval):
    try:
        df[col] = df[col].map({True: trueval, False: falseval})
        return df
    except Exception as err:
        print('Unexpected Error Occurred in map_true_false_values function: ', err)         

###################################################################################################
# 1. Renames columns for display purposes
# 2. Groups the dataframe by a column
# 3. Gets a count for each grouping
# 4. Sort the dataframe by count (in descending order)
# 4. Adds a column to the dataframe with the percentage of total records
###################################################################################################
def rename_cols_group_sort_df(df, col1, col2, total_recs):
    try:       
        #Rename the columns for display purposes
        df = rename_cols(df, col1, col2)
        
        #Group the dataframe by column value
        df = group_col(df, col2)
        
        #Get a count for each group
        df = get_group_count(df)
        
        # Sort the group counts in descending order
        df = sort_by_count(df, col1)
        
        #Add a column to the df for percentage of total values
        df = add_percentage_col(df, col1, total_recs)
        
        return df

    except Exception as err:
        print('Unexpected Error Occurred in rename_cols_group_sort_df function: ', err)

###################################################################################################
# Renames two columns for display purposes 
###################################################################################################
def rename_cols(df, col1, col2):
    try:
        df.columns = [col1, col2]
        return df
    except Exception as err:
        print('Unexpected Error Occurred in rename_cols function: ', err)

###################################################################################################
# Groups records by the value of a column 
###################################################################################################
def group_col(df, col):
    try:
        df = df.groupby(col)
        return df
    except Exception as err:
        print('Unexpected Error Occurred in group_cols function: ', err)

###################################################################################################
# Returns a dataframe containing group counts 
###################################################################################################
def get_group_count(df):
    try:
        df = df.count()
        return df
    except Exception as err:
        print('Unexpected Error Occurred in get_group_count function: ', err)

###################################################################################################
#  Sorts a dataframe by count in descending order
###################################################################################################
def sort_by_count(df, col):
    try:
        df = df.sort_values(by=[col], ascending = False)
        return df
    except Exception as err:
        print('Unexpected Error Occurred in sort_by_count function: ', err)

###################################################################################################
#  Adds a % of total records column to a dataframe
###################################################################################################
def add_percentage_col(df, col, total_recs):
    try:
        df['%_of_Total'] = df[col] / total_recs * 100
        return df
    except Exception as err:
        print('Unexpected Error Occurred in add_percentage_col function: ', err)
        
###################################################################################################
#  Prints a dataframe to console
###################################################################################################
def print_dataframe(df):
    print()
    print(df)
    print()

###################################################################################################
# Plots the dataframe in a bar chart 
###################################################################################################
def plot_dataframe(df, title, xlabel, legend, color):
    
    try:
        p = df.plot(kind='bar', figsize=(12,7), color=color, grid = True)
        p.legend([legend])
        p.set_title(title, fontsize = 18)    
        p.set_xlabel(xlabel) 

    except Exception as err:
        print('Unexpected Error Occurred in plot_dataframe function: ', err)


###################################################################################################
if __name__=='__main__':
    main()   