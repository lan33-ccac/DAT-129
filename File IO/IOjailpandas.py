# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading Jail Data and Computing Stats (Pandas version)
# Author: Lisa Nydick
# Last Modified: 09/17/2019
#####################################


import pandas as pd

###################################################################################################
# Main Function
###################################################################################################
def main():
    infile = "jail.csv"

    df = pd.read_csv(infile, ',')
    #Set the dataframe index to be the '_id' column
    df.set_index('_id', inplace = True)
    get_stats(df)    

###################################################################################################
# Calculates statistics based on data in the input Pandas dataframe
###################################################################################################        
def get_stats(df):
    
    # Get avg of agebook series
    agebook = df['agebook']
    avg_agebook = agebook.mean()
    
    #get avg of agecurr series
    agecurr = df['agecurr']
    avg_agecurr = agecurr.mean()
    
    #Count the number of females in the gender series
    gender = df['gender']
    female = gender  == 'F'
    female_count = gender[female].count()    

    #Count the number of males in the gender series    
    male = gender == 'M'
    male_count = gender[male].count()
    
    #Get a total count of gender rows
    total_gender_count = gender.count()

    #Calc % of males and females
    percent_m_gender = male_count/total_gender_count * 100
    percent_f_gender = female_count/total_gender_count * 100
    
    #Count number of blacks in race series
    race = df['race'] 
    black = race == 'B'
    black_count = race[black].count()
    
    #Count number of whites in race series
    white = race == 'W'
    white_count = race[white].count()
    
    #Get a total count of race rows
    total_race_count = race.count()
    
    #Calc % of blacks and whites
    percent_b_race = black_count/total_race_count * 100
    percent_w_race = white_count/total_race_count * 100
    
    #Call function to print the statistics
    print_stats(avg_agebook, avg_agecurr, percent_m_gender, percent_f_gender, percent_b_race, percent_w_race)

###################################################################################################
# Prints the statistics
###################################################################################################
def print_stats(avg_agebook, avg_agecurr, percent_m_gender, percent_f_gender, percent_b_race, percent_w_race):    
    print()
    print('JAIL STATISTICS: JAN 2018')
    print(f'{"% Males":^10} {"% Females":^10}{"% Blacks":^10}{"% Whites":^10}{"Avg AgeBook":^15}{"Avg AgeCurr":^15}')
    print(f'{"-------":^10} {"---------":^10}{"--------":^10}{"--------":^10}{"-----------":^15}{"-----------":^15}')
    print(f'{percent_m_gender:^10.2f} {percent_f_gender:^10.2f}{percent_b_race:^10.2f}{percent_w_race:^10.2f}{avg_agebook:^15.2f}{avg_agecurr:^15.2f}')
    
        
###################################################################################################
main()