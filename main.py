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
ranks = ["Beginner", "Good Start", "Moving Up", "Good", "Solid", "Nice", "Great", "Amazing", "Genius", "Queen Bee"]
solutions = []

try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is in the args
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

def inDictionary(_input, _dict): #checks if a particular word is in the dictionary list (_dict is the SOLUTIONS LIST!)
    for i in range(len(_dict)):
        if _input.lower() == _dict[i]:
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


def score(_input): #calculate the score of a word
    if len(_input) == 4: return 1
    for i in letters: #check for pangrams, and score accordingly
        if _input.find(i) == -1: #if the word doesn't contain every letter, it isn't a pangram, so break
            break
    else: #if the word is a pangram
        return 2*len(_input) #double score
    if len(_input) > 4: return len(_input) #if it isn't a 4 letter word, add the length of the word to score
    return 0 #required to give the function a return type (*sigh*...python)


def maxScore():
    _solutions = solve(False)
    totalScore = 0
    for i in range(len(_solutions)):
        totalScore += score(_solutions[i])
    return totalScore


def calculateRanks(): #the scores corresponding to each of the ranks in spelling bee
    #Order: Beginner, Good Start, Moving Up, Good, Solid, Nice, Great, Amazing, Genius, Queen Bee (all the words)
    _ranks = ""
    percentages = [0, 2.5, 5, 10, 20, 30, 40, 60, 80, 100]
    _maxScore = maxScore()

    for i in percentages:
        _ranks += str(int((i/100)*_maxScore)) + "," #make sure these are ints
    _ranks = _ranks[:-1] #should get everything but the last character, TEST THIS
    return _ranks


def currentRank(_score, _rankValsList): #returns a value 0-9, corresponding to an index in the ranks list
    for i in range(len(_rankValsList)):
        if _score < _rankValsList[i]: #run the for loop until it reaches a rank that is greater than the current score
            return i - 1
    return 0


def printLettersGUI(_letters): #returns the ascii art for the letters (like in spelling bee), with the correct letters inserted AND SHUFFLED
    if not isinstance(_letters, str): return 0 #if _letters isn't a string of letters

    center = _letters[0]
    _letters = _letters[1:] #get the first letter, then remove it (to allow for random distribution in the GUI)

    _lettersList = []
    for i in _letters:
        _lettersList.append(i)
    random.shuffle(_lettersList)

    return """
             /---\\
            /.....\\
           (.. {} ..)
      /---\\ \\...../ /---\\
     /.....\\ \\---/ /.....\\
    (.. {} ..)/---\\(.. {} ..)
     \\.....//.....\\\\...../
      \\---/(.. {} ..)\\---/
      /---\\ \\...../ /---\\
     /.....\\ \\---/ /.....\\
    (.. {} ..)/---\\(.. {} ..)
     \\.....//.....\\\\...../
      \\---/(.. {} ..)\\---/
            \\...../
             \\---/""".format(_lettersList[0], _lettersList[1], _lettersList[2], center, _lettersList[3], _lettersList[4], _lettersList[5])

#====================================================================================================================================================================================#

letterFile = open("letters.txt", 'r') #read the letters from the last day played from the file
lastDate = letterFile.readline()
lastDate = lastDate.strip()
letterFile.close()

today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY, put into a string

if (int(d1[0:2]) > int(lastDate[0:2])) or (int(d1[3:5]) > int(lastDate[3:5])): #if the dates are greater or the months are greater, regen the letters and redo setup
    print("Generating letters...")
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

        if maxScore() > 30: break #wait for a letter combo with a max score over 30


    letters = letters.capitalize() #make the first letter uppercase
    for i in range(len(letters)):
        letterFile.write(letters[i] + " ")
    letters = letters.lower() #re-lowercase all of the letters

    letterFile.write("\n" + calculateRanks() + "\n")
    letterFile.close()

letterFile = open("letters.txt", 'r')
letterFileList = letterFile.readlines()

letters = letterFileList[1]
letters = letters.replace(" ", "") #get rid of the spaces
letters = letters.strip()
letters = letters.lower()

rankVals = letterFileList[2].split(",")
for i in range(len(rankVals)):
    rankVals[i] = int(rankVals[i])

foundWords = letterFileList
for i in range(3):
    foundWords.pop(0) #get rid of the first 4 lines of the list/letters.txt (date, letters, max score, ranks) to get a list of found words
for i in range(len(foundWords)):
    foundWords[i] = foundWords[i].strip() #get rid of the newline chars

currentScore = 0
for i in foundWords: #calculate the score at the start of the game
    currentScore += score(i)

solutions = solve(False) #fill the solutions list with all of the possible solution words

letterFile.close()
letterFile = open("letters.txt", 'a') #reopen the file so the score and words can be appended to it

#====================================================================================================================================================================================#

stdscr = curses.initscr()
curses.start_color()
curses.echo() #type keypresses on the screen
curses.cbreak() #don't require the enter key to be pressed to parse inputs
stdscr.keypad(True) #handle special input codes

#curses.LINES = y dimension of the screen
#curses.COLS = x dimension
#.refresh updates the screen
#everything is y, x!!!!!

stdscr.addstr(20, 0, "Input: ") #print this BEFORE EVERYTHING ELSE otherwise it breaks stuff
stdscr.refresh()

lettersGUIPad = curses.newpad(100, 100) #a part of the screen for the letters GUI
lettersGUIPad.addstr(0, 0, printLettersGUI(letters))

# (0,0) : coordinate of upper-left corner of pad area to display.
# (2,2) : coordinate of upper-left corner of window area to be filled with pad content.
# (17, 30) : coordinate of lower-right corner of window area to be filled with pad content.
try:
    lettersGUIPad.refresh(0, 0, 2, 2, 17, 30) #0, 0, 2, 2, 17, 30
except:
    print("\nMake your terminal window bigger, and restart the program.\n") #curses freaks out because the terminal window is too small for the desired pad dimension
    raise SystemExit

foundWordsPad = curses.newpad(100, 100)
counter = 0
for i in range(len(foundWords)):
    if i % 15 == 0:
        counter += 1
    foundWordsPad.addstr(i, (counter - 1)*20, foundWords[i]) #make columns of 15 found words
try:
    foundWordsPad.refresh(0, 0, 6, 35, 30, 70)
except:
    print("\nMake your terminal window bigger, and restart the program.\n") #curses freaks out because the terminal window is too small for the desired pad dimension
    raise SystemExit

currentScorePad = curses.newpad(1, 100)
currentScorePad.addstr(0, 0, "Current Score: " + str(currentScore))
currentScorePad.refresh(0, 0, 3, 35, 3, 70)

currentRankPad = curses.newpad(1, 100)
currentRankPad.addstr(0, 0, "Current Rank: " + ranks[currentRank(currentScore, rankVals)])
currentRankPad.refresh(0, 0, 4, 35, 4, 70)

ranksPad = curses.newpad(100, 100)
for i in range(len(ranks)):
    ranksPad.addstr(i, 0, ranks[i] + ": " + str(rankVals[i]))
ranksPad.refresh(0, 0, 3, 80, 15, 100)

while True:
    input = str(stdscr.getstr(20, 7)) #returns bytes, needs to be converted/casted to string.
    input = input[2:-1] #remove extraneous characters
    input = input.lower()
    for i in range(len(input)):
        stdscr.addstr(20, 7 + i, " ") #clear out the past input (stdscr.clrtoeol() and .clrtobot() didn't work for some reason...)
    stdscr.refresh()

    if input == "/exit": break
    if input == " " or input == "/shuffle":
        lettersGUIPad.addstr(0, 0, printLettersGUI(letters)) #regenerate the letters GUI with shuffled letters
        lettersGUIPad.refresh(0, 0, 2, 2, 17, 30)
        continue

    for i in solutions:
        if i == input: #if the input matches a word in the solutions list, return true
            for ii in foundWords:
                if ii == input: break #if the input matches a solution, make sure it hasn't already been found
            else: #if it wasn't already found (aka is a good input word)
                currentScore += score(input)

                foundWords.append(input)
                counter = 0
                for i in range(len(foundWords)):
                    if i % 15 == 0:
                        counter += 1
                    foundWordsPad.addstr(i, (counter - 1)*20, foundWords[i]) #make columns of 15 found words
                foundWordsPad.refresh(0, 0, 6, 35, 30, 70)

                currentScorePad.addstr(0, 0, "Current Score: " + str(currentScore))
                currentScorePad.refresh(0, 0, 3, 35, 3, 70)

                currentRankPad.addstr(0, 0, "Current Rank: ")
                for i in range(len(ranks[currentRank(currentScore - score(input), rankVals)])): #clear out the old rank from the line (.clrtoeol doesn't work for some reason)
                    currentRankPad.addstr(" ")
                currentRankPad.refresh(0, 0, 4, 35, 4, 70)
                currentRankPad.addstr(0, 0, "Current Rank: " + ranks[currentRank(currentScore, rankVals)]) #put the new rank in
                currentRankPad.refresh(0, 0, 4, 35, 4, 70)

                letterFile.close()
                letterFile = open("letters.txt", 'a') #reopen the file so the score and words can be appended to it
                letterFile.write(input + "\n")

#====================================================================================================================================================================================#

#curses ending stuff
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
