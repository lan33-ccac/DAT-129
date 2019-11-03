# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Exercises for List Comprehensions
# Author: Lisa Nydick
# Last Modified: 11/03/2019
#####################################

#Exercise 1: Make a list out of the word "KABOOM" where each element is a letter of the word repeated three times. 
L = [x * 3 for x in "KABOOM"]
print(L)

#Exercise 2: Make a list that counts backwards from 10 to 0
L = [x for x in range (10, -1, -1)]
print(L)

#Exercise 3
#With the 'example.txt' file open, make a list of lines that have the words 'Purple' or 'purple' in it
# and perform at least 2 string methods of your choosing on said lines.
lines = [line.rstrip().upper() for line in open('example.txt') if 'Purple' in line or 'purple' in line]
print(lines)
