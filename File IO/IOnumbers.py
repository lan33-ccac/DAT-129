# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: I/O Exercise in Writing Formatted Numbers to a File
# Author: Lisa Nydick
# Last Modified: 09/16/2019
#####################################


###################################################################################################
# Main Function
###################################################################################################
def main():
    num_list = [0,1,2,3,4,5,6,7,8,9]
    outfile = 'IOnumbers_out.txt'
    outstring = ''
    
    #Build the output string
    outstring = format_num_list(num_list)
    #Write the numbers to an output file
    write_nums(outstring, outfile)

###################################################################################################
# Function formats the input number list
###################################################################################################
def format_num_list(num_list):
    outstring = ''
    for r in range(9, -1, -1):
        for c in range(0, len(num_list)):
            #forces a line break if we are at the end of the list
            if c == len(num_list) - 1:
                outstring += str(num_list[c]) + '\n'
            else:
                outstring += str(num_list[c])
        num_list.remove(r)
    return outstring
        
###################################################################################################
# Function writes the formatted numbers to an output text file
###################################################################################################        
def write_nums(outstring, outfile):
    try:
        with open(outfile, 'w') as textfile:
            textfile.write(outstring)
    except IOError:
        print('Output filepath "' + outfile + '" is invalid.')
    except Exception as err:
        print(err)
        print('Output file could not be written due to error.')
    
        
###################################################################################################
main()
