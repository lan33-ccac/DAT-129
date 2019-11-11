# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Code for File Tree Exercise
# Author: Lisa Nydick
# Last Modified: 11/9/2019
#####################################
import os
import pandas as pd

##################
# Global Variables
##################
dircount = 1
filecount = 0
depth = 0
total_filesize = 0
breadth = 0
width = []
currdepth = 0
top_node = ''
index = 0
dict_list = []

###################################################################################################
# Main Function
###################################################################################################
def main():
    global index
    global top_node

    #traverse bottom up so root is the last directory processed
    for currdir, dirs, files in os.walk('.', topdown = False):  
        get_dircount(dirs)
        get_filecount(files)
        get_max_depth(currdir, files)
        get_filesize(currdir, files)
        get_currdepth(currdir)
        get_breadth(files)

        # Indicates that we are at the root node
        if len(currdir.split(os.sep)) == 2:
            get_top_node_info(currdir)
            build_tree_dicts()
            reinit_global_vars()
    
    #We have all data for all trees, so it's time to load a pandas dataframe        
    load_pandas()
    
###################################################################################################
# Finds and sets the number of directories in the directory structure
###################################################################################################    
def get_dircount(dirs):
    global dircount
    for d in dirs:
        dircount += 1

###################################################################################################
# Finds and sets the number of files in the file structure
###################################################################################################
def get_filecount(files):
    global filecount
    for f in files:
        filecount += 1

###################################################################################################
# Finds and sets the maximum depth of directories and/or files
# The lowest level might be a directory or a file
###################################################################################################        
def get_max_depth(currdir, files):
    global depth
    currdir_sep_count = 0
    
    # Count the number of separator characters in the current directory
    # This indicates how many directories are represented in the current directory path
    currdir_sep_count = get_num_sep_chars(currdir)
    
    # If the number of separators (dirs in currdir) is greater than current depth
    # set the new depth equal to the number of dirs
    if currdir_sep_count > depth:
        depth = currdir_sep_count
        
    # See if any files are at a lower level than the lowest directory
    # by checking the number of separator characters (directories) in each file name
    for f in files:
        fn_sep_count = 0
        #construct the file name
        fn = currdir + os.sep + f

        fn_sep_count = get_num_sep_chars(fn)
        # If the number of separators (dirs in currdir) is greater than current depth
        # set the new depth equal to the number of dirs
        if fn_sep_count > depth:
            depth = fn_sep_count
            
###################################################################################################
# Counts and returns the number of separator characters (os-dependent) in a string
###################################################################################################
def get_num_sep_chars(string):
    sep_count = 0
    for i in range(len(string)):
        if string[i] == os.sep:
            sep_count += 1
    return sep_count

###################################################################################################
# Uses the os.path.getsize function to get the size of the current file and add it to a running total
###################################################################################################
def get_filesize(currdir, files):
    global total_filesize
    for f in files:
        fn = currdir + os.sep + f
        filesize = os.path.getsize(fn)
        total_filesize += filesize

###################################################################################################
# Gets and sets the current depth level by counting the number of separator characters in
# the current directory path
###################################################################################################
def get_currdepth(currdir):
    global currdepth
    currdepth = get_num_sep_chars(currdir)
   
###################################################################################################
# Breadth is defined as the maximum number of directory and/or file nodes
# at any level of the tree structure
###################################################################################################
def get_breadth(files):
    global breadth
    global width
    
    #Each width list index represents the current depth
    #Make sure there are enough 0's in the list to represent the current depth    
    while len(width) < currdepth + 1:
        width.append(0)
    #Add 1 to the depth count for the current level
    width[currdepth - 1] += 1
    
    #Add the current file count to the width list for the current level
    width[currdepth] += len(files)
    
    #Breadth is the maximim of all values in the width list
    breadth = max(width)

###################################################################################################
# Finds the name of the root node of the tree and increments an index of roots
# This function is called when the current directory is the root node
###################################################################################################
def get_top_node_info(currdir):
    global top_node
    global index
    #root node is the tail 
    top_node = currdir.split(os.sep)[1]
    index += 1

###################################################################################################
# Store global variables in a dictionary of tree info and append the dict to a list
###################################################################################################    
def build_tree_dicts():
    tree_dict = {}
    global dict_list
    
    tree_dict['Tree_Index'] = index
    tree_dict['Root_Name'] = top_node
    tree_dict['Max_Depth'] = depth
    tree_dict['Max_Breadth'] = breadth
    tree_dict['Total_Dirs'] = dircount
    tree_dict['Total_Files'] = filecount
    tree_dict['Total_File_Size'] = total_filesize
    
    dict_list.append(tree_dict)
    
###################################################################################################
# Reset global variable values in preparation for the next tree
###################################################################################################    
def reinit_global_vars():
    global dircount
    global filecount
    global depth
    global total_filesize
    global breadth
    global width
    global top_node
    
    dircount = 1
    filecount = 0
    depth = 0
    total_filesize = 0
    breadth = 0
    width = []
    top_node = ''
   

###################################################################################################
# Load the list of dictionaries into a pandas dataframe, display it + its stats
# Plot a bar chart and a box plot for each dataframe column
###################################################################################################    
def load_pandas():

    df = pd.DataFrame(dict_list)
    df.set_index("Root_Name", inplace = True)
    
    #Set the order of the column names
    df = df[["Max_Depth", "Max_Breadth", "Total_Files", "Total_Dirs", "Total_File_Size"]]
    
    #Set some display options
    pd.options.display.float_format = '{:,.2f}'.format
    pd.options.display.max_columns = 8
    pd.options.display.width = 100
    
    print()
    print(df)
    print()
    #print basic stats
    print(df.describe())
    
    #calculate and print median values
    m_depth = df['Max_Depth'].median()
    m_breadth = df['Max_Breadth'].median()
    m_files = df['Total_Files'].median()
    m_dirs = df['Total_Dirs'].median()
    m_size = df['Total_File_Size'].median()
    print(f'{"median":<5}{m_depth:>10.2f}{m_breadth:>13.2f}{m_files:>13.2f}{m_dirs:>12.2f}{m_size:>17.2f}')
    
    #Draw 2 sets of plots (subplots)
    #First set is a bar chart for each numeric dataframe column, with root names
    #on the x-axis
    df.plot(subplots = True, kind = 'bar', figsize = (15,20))
    #Second is a box plot for each numeric dataframe column
    df.plot(subplots = True, kind = 'box', figsize = (15,10))
            

###################################################################################################
if __name__=='__main__':
    main()   