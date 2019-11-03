"""Exercise for practicing the use of regular expressions."""

# 1. Using regular expressions, iterate over the list below to pull out
# a few items from the list individually. You will need to use multiple 
# for loops for this. 

# 2. If you are able to accomplish this easily, work on pulling out 
# various combinations of list items.

# 3. If you complete the first two tasks, use sub or other available
# re methods to alter items within the list.

rlist = ['12', '346723', 'banana', 'Mongoose', '02143',
	'bIrds of a feather flock together', '6274', 'MONKEY', '123-45-6789'] 
	
import re
# Your work here:
for item in rlist:
    #Match 1 to 5 digits (12, 02143, 6274)
    if re.fullmatch('\d{1,5}', item):
        print(item)
        
print()        
for item in rlist:
    #Match everything starting with M (Mongoose, MONKEY)
    if re.match('M', item):
        print(item)
        
print()
for item in rlist:
    #Match anything all lowercase (banana)
    if re.fullmatch('[a-z]+', item):
        print(item)
        
print()
for item in rlist:
    #Match anything that starts with an uppercase letter and ends with lowercase letters (Mongoose)
    if re.fullmatch('[A-Z]+[a-z]+', item):
        print(item)

print()        
for item in rlist:
    #Match anything that starts with a lower case letter, has an upper case letter second
    # and non-digit characters for its ending (bIrds of a feather flock together)
    if re.fullmatch('[a-z]+[A-Z]+\D+', item):
        print(item)
        #replace the uppercase I with a lowercase I
        newitem = re.sub('I', 'i', item)
        print(newitem)

print()
for item in rlist:
    #Find all uppercase words (MONKEY)
    if re.fullmatch('[A-Z]+', item):
        print(item)
        #Replace uppercase with lowercase
        newitem = re.sub('[A-Z]+', item.lower(), item)
        print(newitem)
    
print()
for item in rlist:
    #Replace the dashes with empty strings in a string that matches the format ddd-dd-dddd (123-45-6789)
    if re.match('\d{3}-\d{2}-\d{4}', item):
        newphone = re.sub('-','', item)
        print(newphone)