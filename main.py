# main
#Author: Michael Drobot
#https://github.com/mdrobot7

#Args: -p = profane; -a = all; -r = random order; -o = output results to file
#Add .txt to the end of the input word to make the output dump to a text file

import time
import sys
import random
import string
import os
from datetime import date
import solve.py

allowProfane = False
clearConsole = lambda: os.system("cls") #for clearing the terminal screen
#clearConsole = lambda: os.system("clear") #for Unix systems


try:
    dict = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dict = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

lines = dict.readlines() #read all lines into a list

def inDictionary(input): #checks if a particular word is in the dictionary
    for i in range(len(lines)):
        if input.lower() == lines[i]:
            return True
    return False

#====================================================================================================================================================================================#

letterFile = open("letters.txt", 'r') #read the letters from the last day played from the file
lastDate = letterFile.readline()

today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY, put into a string

if(int(d1[0:2]) > int(lastDate[0:2]) or int(d1[3:5]) > int(lastDate[3:5])): #if the dates are greater or the months are greater, regen the letters
    letterFile.close()
    letterFile = open("letters.txt", 'w')
    letterFile.write(d1 + "\n") #write the date to the file
    letterFile.write(random.choice(string.ascii_uppercase) + " ") #write the center letter
    for i in range(6):
        letterFile.write(random.choice(string.ascii_lowercase) + " ") #write the additional 6 letters
    letterFile.close()
    letterFile = open("letters.txt", 'r')

letters = letterFile.read()
letters = letters.split("\n")
letters = letters[1] #get the line of letters

#====================================================================================================================================================================================#
