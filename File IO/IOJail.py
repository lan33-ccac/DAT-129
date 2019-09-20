# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Reading Jail Data and Computing Stats
# Author: Lisa Nydick
# Last Modified: 09/18/2019
#####################################


###################################################################################################
# Main Function
###################################################################################################
def main():
    jailfile = 'jail.csv'
    
    process_records(jailfile)

###################################################################################################
# Reads input file line by line into a header list and a data list
# Zips the two lists into a dictionary
# Computes running stats for each dictionary
# Calls function to display results
###################################################################################################
def process_records(jailfile):
    header_list = []
    data_line = ''
    data_list = []
    zd = {}
    
    m_gender_cnt, f_gender_cnt = 0, 0
    b_race_cnt, w_race_cnt = 0, 0 
    total_agebook, total_agecurr, rec_cnt = 0, 0, 0

    #Loops through the input file records
    with open(jailfile, 'r') as infile:
        infile.read(3)  #skip the initial byte order marker
        #First record is the header
        header = infile.readline().rstrip('\n')
        #splits values by comma and stores them in a list
        header_list = header.split(',')
        
        #Remaining records are the data rows
        for line in infile:
            data_line = line.rstrip('\n')
            #Splits values by command and stores them in a list
            data_list = data_line.split(',')
            
            #Zips the header and data list into a single dictionary
            zd = dict(zip(header_list, data_list))
            
            #Increment counts of values (or totals for numeric values)
            if zd['gender'] == 'M':
                m_gender_cnt += 1
            if zd['gender'] == 'F':
                f_gender_cnt += 1
            if zd['race'] == 'B':
                b_race_cnt += 1
            if zd['race'] == 'W':
                w_race_cnt += 1
           
            total_agebook += int(zd['agebook'])
            total_agecurr += int(zd['agecurr'])
            rec_cnt +=1     #Total number of records read
    
    # Compute and display statistics        
    generate_stats(rec_cnt, f_gender_cnt, m_gender_cnt, b_race_cnt, w_race_cnt, total_agebook, total_agecurr)

###################################################################################################
# Calculates stats and Displays the Output
###################################################################################################
def generate_stats(rec_cnt, f_gender_cnt, m_gender_cnt, b_race_cnt, w_race_cnt, total_agebook, total_agecurr):
    
    total_gender = f_gender_cnt + m_gender_cnt
    total_race = b_race_cnt + w_race_cnt
    percent_f_gender = f_gender_cnt / total_gender * 100
    percent_m_gender = m_gender_cnt / total_gender * 100
    percent_b_race = b_race_cnt / total_race * 100
    percent_w_race = w_race_cnt / total_race * 100
    avg_agebook = total_agebook / rec_cnt 
    avg_agecurr = total_agecurr / rec_cnt
   
    print()
    print('JAIL STATISTICS: JAN 2018')
    print(f'{"Rec Cnt":^10}{"% Males":^10} {"% Females":^10}{"% Blacks":^10}{"% Whites":^10}{"Avg AgeBook":^15}{"Avg AgeCurr":^15}')
    print(f'{"-------":^10}{"-------":^10} {"---------":^10}{"--------":^10}{"--------":^10}{"-----------":^15}{"-----------":^15}')
    print(f'{rec_cnt:^10d}{percent_m_gender:^10.2f} {percent_f_gender:^10.2f}{percent_b_race:^10.2f}{percent_w_race:^10.2f}{avg_agebook:^15.2f}{avg_agecurr:^15.2f}')
    
       

###################################################################################################    
main()