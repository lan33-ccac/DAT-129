# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Dictionary Editor
# Author: Lisa Nydick
# Last Modified: 09/16/2019
#####################################

#Define global constants
CMD_ALL = 'all'
CMD_CURR = 'curr'
CMD_DOWN= 'down'
CMD_UP = 'up'
CMD_CHANGE = 'change'
CMD_DEL = 'del'
CMD_ADD = 'add'
CMD_QUIT = 'quit'

KEY_NOT_FOUND = 'Key Not Found'
LEVEL_0 = 0
ROOT = 'ROOT'

#Global variables used by recursive functions
currlevel = LEVEL_0
dict_count = 0
key_count = 0
key_count_list = []
quit = False


###################################################################################################
# Main Function
###################################################################################################    
def main():
    schematext = ''
    infilepath = ''
    outfilepath = ''
    schemadict = {}
    fatal_err = False
    parentkey = ROOT
    save_changes = False

    
    #Dictionary input
    #More complex 3-Level Dictionary
    #schemadict = {"uid": "MAS2912941190", "type": "Journal article", "title": "Publication Title1", "author": {"name": "Maurizio Fava", "degrees": ["MD","PhD"], "affiliation": {"affname": "Harvard University", "city": "Boston"}, "department":{"Dept": "Dept of Psychiatry", "Div": "Div. of Experimental Medicine"}}, "source": "Molecular Psychiatry", "year": 2019}
    
    
    #Simpler 3-Level dictionary
    #schemadict = {"uid": "MAS2912941190", "type": "Journal article", "title": "Publication Title1", "author": {"name": "Maurizio Fava", "affiliation": {"affname": "Harvard University", "city": "Boston"}}, "source": "Molecular Psychiatry", "year": 2019}
    
    #2-Level Dictionary
    #schemadict = {"uid": "MAS2912941190", "type": "Journal article", "title": "Publication Title1", "author": {"name": "Maurizio Fava", "affname": "Harvard University"}, "source": "Molecular Psychiatry", "year": 2019}
    
    #1-Level dictionary
    #schemadict = {"uid": "MAS2912941190", "type": "Journal article", "title": "Publication Title1", "author": "Maurizio Fava", "source": "Molecular Psychiatry", "year": 2019}
 
    #Prompt user for the schema input file and attempt to read it
    infilepath = input('Enter the path for the schema input file:')
    schematext, fatal_err = read_schema(infilepath)
    
    #Ensure that schema can be read as a dictionary
    if fatal_err == False:
        schemadict, fatal_err = validate_dict(schematext)
    
    #Print basic stats    
    if fatal_err == False:
        #get the total number of dictionaries and keys
        get_stats(schemadict)
        print()
        print('BASIC STATS')
        print('Number of dictionaries = ' + str(dict_count))
        print('Total number of keys in the dictionaries = ' + str(key_count))
 
    
    #Gather user input, perform editing, and display results
    if fatal_err == False:
        interact(schemadict, parentkey)
    
    if fatal_err == False: 
        #See if the user wants to save their changes to the schema to a file
        save_changes = input('Save changes to schema in a file before quitting (Y or N)?')
        if save_changes.lower() == 'y' or save_changes.lower() == 'yes':
            outfilepath = input('Enter the output file path:')
            fatal_err = write_schema(outfilepath, schemadict)

    #else don't save the changes

###################################################################################################
# Reads a schema from a text file
###################################################################################################
def read_schema(filepath):
    schematext = ''
    fatal_err = False    
    #open the input file containing the schema string
    try:
        with open(filepath, 'r') as schemafile:
            schematext = schemafile.readline()
            print('**** Changes were written successfully to the output file. ****')
    except IOError:
        print('**** Error occured trying to open input file "' + filepath + '". ****')
        print('**** The pathname or filename probably does not exist.')
        fatal_err = True
        print('**** Changes could not be read from the input file due to error. ****')
        
    except Exception as err:
        print('**** Error in read_schema function: ****')
        print(err)
        fatal_err = True
        print('**** Changes could not be read from the input file due to error. ****')
    
    return schematext, fatal_err

###################################################################################################
# Writes the current schema to a text file
###################################################################################################
def write_schema(filepath, schema):
    
    fatal_err = False    
    #open the input file containing the schema string
    try:
        with open(filepath, 'w') as schemafile:
            schemafile.write(str(schema))
            print('**** Schema was successfully written to output file. ****')
    except IOError:
        print('**** Error occured trying to create output file "' + filepath + '". ****')
        print('**** Path probably does not exist. ****')
        print('**** Schema was NOT written successfully to output file. ****')
        fatal_err = True
    except Exception as err:
        print('**** Error in write_schema function: ****')
        print(err)
        print('**** Schema was NOT written successfully to output file. ****')
        fatal_err = True
    
    return fatal_err
###################################################################################################
# Function ensures that schema can be read as a dictionary
###################################################################################################   
def validate_dict(schematext):
    schemadict = {}
    fatal_err = False
    #evaluate schema as code (i.e., a dictionary rather than string)
    try:
        schemadict = eval(schematext)
        if type(schemadict) != dict:
            print('**** Input file does not contain a dictionary. ****')
            fatal_err = True
    except Exception as err:
        print('**** Error in validate_dict function: ****')
        print(err)
        fatal_err = True
    
    return schemadict, fatal_err

###################################################################################################
# Recursive function computes stats
###################################################################################################
def get_stats(schemadict):
    global dict_count
    global key_count
    d = schemadict
    #dictionary count
    dict_count += 1
    for k,v in d.items():
        #total key count for all dictionaries
        key_count += 1
        if type(v) == dict:
            new_dict = v
            #call function recursively with the next dictionary
            get_stats(new_dict)
    return
    

###################################################################################################
# Recursive function that collects user input and calls editing functions
###################################################################################################
def interact(current_dict, parentkey):
    global currlevel
    global quit
    while quit == False:
        #Call function to show the current level of the tree
        show_curr_level(current_dict, parentkey)        
        #Call function to get user command
        sel = display_menu()
        if sel == CMD_QUIT:
            quit = True
        elif sel == CMD_CURR:
            #Call function to show the current level of the dictionary
            show_curr_level(current_dict, parentkey)
        elif sel == CMD_DOWN:
            #Increment tree level count
            currlevel += 1
            #call function to prompt for a key and return the dictionary associated with that key (and the key itself)
            child_dict, childkey = get_dict_by_key(current_dict)
            #make sure child dictionary is a dictionary rather than some other value
            #and make sure the dictionary has changed
            if type(child_dict) == dict and child_dict != current_dict:
                #call this again function recursively with the new_dict and key           
                interact(child_dict, childkey)
            else:   #child_dict is empty, so don't go down
                print('*** No more dictionary levels to display. ****')    
        elif sel == CMD_UP:
            #Decrement tree level count so we know when we're at the top
            currlevel -=1
            if currlevel < LEVEL_0:
                print('*** Currently at the Top ****')
            else:
                #return up to previous call of interact function
                return
           
        elif sel == CMD_CHANGE:
            #Call function to change a node at the current level in the dictionary    
            change_entry(current_dict)
        elif sel == CMD_DEL:
            #Call function to delete a key/value pair at the current level in the dictionary
            delete_entry(current_dict)
        elif sel == CMD_ADD:
            #Call function to edit the value of a key at the current level in the dictionary
            add_entry(current_dict)

###################################################################################################
# Display the main menu and validate the user input
###################################################################################################   
def display_menu():
    stoplooping = False
    while stoplooping == False:
        print()
        print("Select an action:")
        print(f'{" ":<5}{"Curr:":<10}{"View Entries at the Current Level":<10}')
        print(f'{" ":<5}{"Down:":<10}{"View or Edit Entries on the Next Level Down":<10}')
        print(f'{" ":<5}{"Up:":<10}{"View or Edit Entries on the Next Level Up":<10}')
        print(f'{" ":<5}{"Change:":<10}{"Edit a Selected Entry Value on the Current Level":<10}')
        print(f'{" ":<5}{"Del:":<10}{"Delete a Selected Key/Value Pair on the Current Level":<10}')
        print(f'{" ":<5}{"Add:":<10}{"Add a Key/Value Pair on the Current Level":<10}')   
        print(f'{" ":<5}{"Quit:":<10}{"Quit the Program":<10}')
    
        sel = str(input('Action:')).lower()
        if sel == CMD_ALL or sel == CMD_CURR or sel == CMD_DOWN or sel == CMD_UP or sel == CMD_CHANGE or sel == CMD_DEL or sel == CMD_ADD or sel == CMD_QUIT:
            stoplooping = True
        else:
            print('**** Invalid Menu Selection.  Try Again. ****')
            stoplooping = False
            
    return sel   

###################################################################################################
# Function shows the key/value pairs at the current level of the dictionary
###################################################################################################
def show_curr_level(current_dict, parentkey):
    d = current_dict
    global currlevel
    if parentkey == ROOT:
        parent = ('(root)')
    else:
        parent = parentkey
    print()
    print('CURRENT LEVEL= ' + str(currlevel + 1))
    print()
    print(f'{"PARENT:":<20}{"KEY:":<20}{"VALUE:":<20}')
    for k,v in d.items():
        # If the value of the current dictionary is another dictionary, tell user to go Down
        if type(v) == dict:
            print(f'{parent:<20}{str(k):<20}{"* Go Down to View/Edit Subvalues *":<30}')
        else:
            print(f'{parent:<20}{str(k):<20}{str(v):<20}')

###################################################################################################
# Function prompts for a key that the user wants to see/edit at the next level, and makes sure it exists.
# If the key exists, function returns the dictionary value associated with the key and the key itself
###################################################################################################            
def get_dict_by_key(current_dict):
    d = current_dict
    newdict = {}
    v = ''
    selected_key = ''
    selected_key = str(input('Enter the Lower-Level Key you Wish to View/Edit:'))
    v = d.get(selected_key, KEY_NOT_FOUND)
    
    if v != KEY_NOT_FOUND:
        userkey = selected_key
        newdict = d.get(userkey)       
    else:
        userkey = KEY_NOT_FOUND
        print('**** Cannot go Down because key "' + selected_key + '" was not found. ***')
        #key not found so return the old dict
        newdict = d
    
    return newdict, userkey

###################################################################################################
# Function changes the value associated with a dictionary key if it exists.
###################################################################################################
def change_entry(current_dict):
    d = current_dict
    v = ''
    selected_key = ''
    userkey = ''
    oldval = ''
    userval = ''
    
    selected_key = str(input('Enter the Key you wish to Edit:'))
    v = d.get(selected_key, KEY_NOT_FOUND)
    
    if v == KEY_NOT_FOUND:
        userkey = KEY_NOT_FOUND
        print('**** Key "' + userkey + '" was not changed because it does not exist at this level. ****')
    else: #key exists
        userkey = selected_key
        oldval = d[userkey]  #store the old value for the key          

        if type(oldval) == dict:
            print('**** A key with subvalues cannot be changed at this level.  Go Down to edit the subvalues of key: "'  + userkey + '". ****')        
        else:                
            userval = input(str('Enter the new value for key "' + userkey + '":'))
                
            try:
                #convert strings that look like lists, tuples, or dicts to their respective data types
                if userval.startswith('[') == True and userval.endswith(']') == True:
                    probable_datatype = 'list'
                    userval = eval(userval)
                    
                
                elif userval.startswith('(') == True and userval.endswith(')') == True:
                    probable_datatype = 'tuple'
                    userval = eval(userval)
                
                elif userval.startswith('{') == True and userval.endswith('}') == True:
                    probable_datatype = 'dict'
                    userval = eval(userval)
                    userval = dict(userval)
                # Otherwise, string represents a string, int, or float
                d[userkey] = userval
                print('**** Value "' + str(oldval) + '" was changed to value "' + str(userval) + '". ****')
            except Exception as err:
                print(err)
                print('**** Value "' + userval + '" was probably misformatted for datatype "' + probable_datatype + '". ****')              


###################################################################################################
# Function deletes a key/value pair at the current level
# It prevents the user from deleting the last pair at this level
# But the user can delete a parent key (and all of it's children) after navigating UP
###################################################################################################
def delete_entry(current_dict):
    d = current_dict
    v = ''
    selected_key = ''
    selected_key = str(input('Enter the Key you Wish to Delete:'))
    v = d.get(selected_key, KEY_NOT_FOUND)
    if v != KEY_NOT_FOUND:
        userkey = selected_key
        #Check the length of the dictionary at the current level to make sure we're not deleting the last key/value pair      
        if len(d) == 1:
            print('**** Cannot delete the last key/value at this level in the dictionary. ****')
            print('**** To delete all pairs, try deleting the parent key/value up a level. ****')
        else:
            del d[userkey]
            print('**** Key "' + selected_key + '" was deleted. ****')
    else:
        print('**** Cannot delete key "' + selected_key + '" because it does not exist at this level. ****')

###################################################################################################
# Function adds a key/value pair at the current level of the dictionary
# Key must not already exist, and it must be a string or int
###################################################################################################    
def add_entry(current_dict):
    d = current_dict
    v = ''
    probable_datatype = ''
    userkey = input('Enter the name of the key you wish to add at the current level:')   
    #if userkey.startswith('{') != -1 or userkey.startswith('[') != -1 or userkey.startswith('(') != -1: 
    #    print('**** Key not added because key name was not a string or integer. ****')
    #else:
    #Make sure the key doesn't already exist
    v = d.get(userkey, KEY_NOT_FOUND)
    if v != KEY_NOT_FOUND:
        print('**** Key not added because it already exists. ****')
    else:
        #key doesn't exist, so prompt for value
        userval = input('Enter the value you wish to add for key "' + userkey + '":')
            
        try:
            #convert strings that look like lists, tuples, or dicts to their respective data types
            if userval.startswith('[') == True and userval.endswith(']') == True:
                probable_datatype = 'list'
                userval = eval(userval)
                                   
            elif userval.startswith('(') == True and userval.endswith(')') == True:
                probable_datatype = 'tuple'
                userval = eval(userval)
                
            elif userval.startswith('{') == True and userval.endswith('}') == True:
                probable_datatype = 'dict'
                userval = eval(userval)
                userval = dict(userval)
            # Otherwise, string represents a string, int, or float
            d[userkey] = userval
            print('**** Key "' + str(userkey) + '" was added with value "' + str(userval) + '". ****')
        except Exception as err:
            print(err)
            print('**** Value "' + userval + '" was probably misformatted for datatype "' + probable_datatype + '". ****')
                
            
###################################################################################################    
main()