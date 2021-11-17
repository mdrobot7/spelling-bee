# main
#Author: Michael Drobot
#https://github.com/mdrobot7

#Args: -p = profane; -a = all; -r = random order; -o = output results to file
#Add .txt to the end of the input word to make the output dump to a text file

import time
import sys
import random
import os

result = [] #words that are part of the anagram
c = [0] #a list of counter variables
failFlag = False #flag to check if the main algorithm's for loop completed
word = ""
lastWord = ""
args = "" #new args string, makes processing later easier
resultFileArg = 0

clearConsole = lambda: os.system("cls") #for clearing the terminal screen
#clearConsole = lambda: os.system("clear") #for Unix systems

#====================================================================================================================================================================================#

letters = open("letters.txt", 'w') #write the letters for the day to a file
