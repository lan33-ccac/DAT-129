# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Writing Formatted Names to a File
# Author: Lisa Nydick
# Last Modified: 09/16/2019
#####################################

#Global Consts
GREETING = 'Good Evening Dr. '
MIND_IF = ', would you mind if I call you '

###################################################################################################
# Main Function
###################################################################################################
def main():
    infile = 'IOnames_input.txt'
    name_list = []
    
    #get list of names
    name_list = read_rows(infile)
    #compose greeting
    greeting(name_list)
    
###################################################################################################
# Function reads rows containing first and last names from an input file and returns the name list
###################################################################################################   
def read_rows(infile):
    name_list = []
    with open(infile, 'r') as file:
        for row in file:
            name = row
            name = name.rstrip('\n')
            name_list.append(name)

    return name_list

###################################################################################################
# Function takes a list of first and last names and prints the appropriate greeting
###################################################################################################    
def greeting(name_list):
    full_name = ''
    first_name = ''
    last_name = ''
    name_parts = []
    #Loop through the list of names, separating the first name from the last name with .split function
    for i in range(len(name_list)):
        full_name = name_list[i]
        name_parts = full_name.split()
        first_name = name_parts[0]
        last_name = name_parts[1]
        
        print(f'{GREETING}{last_name}{MIND_IF}{first_name}{"?"}')

###################################################################################################        
main()