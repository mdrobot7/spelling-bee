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
import solvers

allowProfane = False
clearConsole = lambda: os.system("cls") #for clearing the terminal screen
#clearConsole = lambda: os.system("clear") #for Unix systems
vowels = "aeiou"


try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

def inDictionary(input): #checks if a particular word is in the dictionary
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
    dict = dictFile.readlines()
    for i in range(len(dict)):
        if input.lower() == dict[i]:
            return True
    return False

#====================================================================================================================================================================================#

#dict is the array of dictionary lines
#dictFile is the file object
#letters is the game letter string (first char is the center letter, NO SPACES!)

def solve(hint):
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
    dict = dictFile.readlines() #read all lines into a list
    count = 0

    while True: #"rough cut" of the dictionary - remove any dict words without the center letter, that are too short, or single letters
        if count >= len(dict):
            break
        dict[count] = dict[count].strip("\n")
        if len(dict[count]) <= 3: #get rid of less than 4 character words (rules of spelling bee)
            dict.pop(count)
            continue
        if dict[count].find(letters[0]) == -1: #get rid of words that don't contain the center letter
            dict.pop(count)
            continue

        for i in range(len(dict[count])): #range(length of the current count'th line of the dictionary)
            if letters.find(dict[count][i]) == -1: #if the i'th letter of the current line isn't in the word, delete the line from the dict and break the loop
                dict.pop(count)
                break
        else: #only increments the index if the for loop runs successfully
            count += 1

    if hint:
        while True:
            try:
                temp = dict[random.randint(0, len(dict))]
                foundWords.index(temp)
            except ValueError: #throws an exception when the value cannot be found in the list by .index(). Means that the dict word is NOT in the found words list
                return temp
    else:
        return dict


def score(input): #calculate the score of a word
    if len(input) == 4: return 1
    for i in letters: #check for pangrams, and score accordingly
        if input.find(letters[i]) == -1: #if the word doesn't contain every letter, it isn't a pangram, so break
            break
    else: #if the word is a pangram
        return 2*len(input) #double score
    if len(solutions[i]) > 4: return len(input) #if it isn't a 4 letter word, add the length of the word to score


def maxScore():
    solutions = solve(False)
    score = 0
    for i in range(len(solutions)):
        score(solutions[i])
    return score


def calculateRanks(): #the scores corresponding to each of the ranks in spelling bee
    #Order: Beginner, Good Start, Moving Up, Good, Solid, Nice, Great, Amazing, Genius, Queen Bee (all the words)
    ranks = ""
    percentages = [0, 2.5, 5, 10, 20, 30, 40, 60, 80]
    score = maxScore()

    for i in percentages:
        ranks += str((i/100)*score) + ","
    return ranks


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

    while True:
        lettersList = [random.choice(vowels)]
        for i in range(6):
            lettersList.append(random.choice(string.ascii_lowercase))
        random.shuffle(lettersList) #shuffle the letter order to mix the vowel in

        letters = ""
        for i in range(len(lettersList)): #convert the list to a string
            letters += lettersList[i]

        max = maxScore()
        if max > 30: break #wait for a letter combo with a max score over 30


    letters = letters.capitalize() #make the first letter uppercase
    for i in range(len(letters)):
        letterFile.write(letters[i] + " ")
    letters = letters.lower() #re-lowercase all of the letters

    letterFile.write("\n" + str(maxScore()) + "\n")
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

currentScore = 0
for i in foundWords: #calculate the score at the start of the game
    score(foundWords[i])

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
