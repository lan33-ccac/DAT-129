# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Runs various looping-related exercises
# Last Modified: 09/11/2019
#####################################

def main():
    ex1()
    ex2('KABOOM')
    ex3("askaliceithinkshe'llknow")
    ex4()
    ex5()
    
    
def ex1():
    for i in range(0, 101):
        if i%2 == 0:
            print(i, end=' ')
            
def ex2(str):
    strlen = len(str)
    c = ''
    newstr = ''
    for i in range(0, strlen):
        c = str[i]
        newstr += c*3
    print(newstr)

def ex3(str):
    newstr=''
    strlen=len(str)
    for i in range(0, strlen):
        if i % 2 == 0:
            newstr += str[i]
    print(newstr)
    
def ex4():
    for x in range(1, 5):
        for y in range(5, 8):
            product = x * y
            print(str(x) + ' | ' + str(y) + ' | ' + str(product))
            
def ex5():
    listoflists = [['mn','pa','ut'],['b','p','c'],['echo','charlie','tango']]
    labels = {"state":"US State Abbr: ", "element":"Chemical Element: ", "alpha":"Phonetic Call: "}
    
    labellist = []
    for value in labels.values():
        labellist.append(value)
        
    for i in range(0, len(listoflists)):
        val = listoflists[i]
        for j in range(0, len(val)):
            print(labellist[i] + val[j])
        
 
            
            
main()           
