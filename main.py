# main
#Author: Michael Drobot
#https://github.com/mdrobot7

#curses guide: https://docs.python.org/3/howto/curses.html#the-python-curses-module

import time
import sys
import random
import string
import os
import curses
from datetime import date
import solve

allowProfane = False
clearConsole = lambda: os.system("cls") #for clearing the terminal screen
#clearConsole = lambda: os.system("clear") #for Unix systems


try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

def inDictionary(input): #checks if a particular word is in the dictionary
    dict = dictFile.readlines()
    for i in range(len(dict)):
        if input.lower() == dict[i]:
            return True
    return False

def handleInput(input): #checks the inputted word against spelling bee's rules and the dictionary
    input = input.lower()

    if input[0] == '/': #commands
        if input[1:] == "exit": raise SystemExit #exit command
        if input[1:] == "hint":
            time.sleep(0.1) #temporary -- show a hint word
    if input == " ":
        time.sleep(0.1) #shuffle letters when space is pressed

    if input.find(letters[0]) == -1 :
        return False
    else:
        for i in range(len(input)):
            if letters.find(input[i]) == -1: #if the input word contains letters that aren't in the letters string
                return False
        else:
            if inDictionary(input) :
                return True #the for loop ran correctly, the input word contains only good letters, now check if it's in the dictionary
            else: return False

#====================================================================================================================================================================================#

letterFile = open("letters.txt", 'r') #read the letters from the last day played from the file
lastDate = letterFile.readline()
lastDate = lastDate.strip()
letterFile.close()

today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY, put into a string

if (int(d1[0:2]) > int(lastDate[0:2])) or (int(d1[3:5]) > int(lastDate[3:5])): #if the dates are greater or the months are greater, regen the letters and redo setup
    letterFile = open("letters.txt", 'w')
    letterFile.write(d1 + "\n") #write the date to the file
    letterFile.write(random.choice(string.ascii_uppercase) + " ") #write the center letter
    for i in range(6):
        letterFile.write(random.choice(string.ascii_lowercase) + " ") #write the additional 6 letters
    letterFile.write("\n" + maxScore() + "\n")
    letterFile.write(calculateRanks() + "\n")
    letterFile.close()

letterFile = open("letters.txt", 'r')
letterFileList = letterFile.readlines()

letters = letterFileList[1]
letters = letters.replace(" ", "") #get rid of the spaces
letters = letters.lower()

foundWords = letterFileList
for i in range(4):
    foundWords.pop(0) #get rid of the first 4 lines of the list/letters.txt (date, letters, max score, ranks) to get a list of found words

letterFile.close()
letterFile = open("letters.txt", 'a') #reopen the file so the score and words can be appended to it
raise SystemExit

#====================================================================================================================================================================================#

stdscr = curses.initscr()
curses.start_color()
curses.noecho() #don't type keypresses on the screen
curses.cbreak() #don't require the enter key to be pressed to parse inputs
stdscr.keypad(True) #handle special input codes

#curses.LINES = y dimension of the screen
#curses.COLS = x dimension
#.refresh updates the screen

stdscr.addstr(0, 0, "curses, foiled again")
stdscr.refresh()
time.sleep(10)

#====================================================================================================================================================================================#

#curses ending stuff
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
