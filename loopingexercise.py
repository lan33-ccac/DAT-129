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
        
        
            
            
main()           
