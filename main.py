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

allowProfane = False
#clearConsole = lambda: os.system("cls") #for clearing the terminal screen
#clearConsole = lambda: os.system("clear") #for Unix systems

vowels = "aeiou"
ranks = ["Beginner", "Good Start", "Moving Up", "Good", "Solid", "Nice", "Great", "Amazing", "Genius", "Queen Bee"]
solutions = []
foundWords = []
hintFlag = False #true means the last inputted word was a /hint and not a solved word

try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is allowed
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

#====================================================================================================================================================================================#

#dict is the array of dictionary lines
#dictFile is the file object
#letters is the game letter string (first char is the center letter, NO SPACES!)

def solve(): #returns a list of all solution words (requires letters (str), foundWords (LIST)) ------ returns LIST
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is allowed
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

        try: #check if the current word is in the solved list
            foundWords.index(dict[count])
        except ValueError: #throws an exception when dict[count] cannot be found in the list by .index(). Means that the dict word is NOT in the found list (SUCCESS)
            for i in range(len(dict[count])): #range(length of the current count'th line of the dictionary)
                if letters.find(dict[count][i]) == -1: #if the i'th letter of the current line isn't in the word, delete the line from the dict and break the loop
                    dict.pop(count)
                    break
            else: #only increments the index if the for loop runs successfully
                count += 1
        else:
            dict.pop(count) #if NO EXCEPTION (the word was already found), REMOVE IT (aka FAIL)
    return dict


def hint(): #get one random solution word that ISN'T in the solved words list (requires FULL solutions list, foundWords (LIST)) ---- returns str
    _solutions = solutions #local instance of solutions LIST
    for i in range(len(solutions)):
        try:
            _index = random.randrange(0, len(_solutions))
        except ValueError: #if len(_solutions) = 0
            _index = 0

        try:
            foundWords.index(_solutions[_index])
        except ValueError: #throws an exception when the value cannot be found in the list by .index(). Means that the dict word is NOT in the found words list
            return _solutions[_index]
        else: #if the solution HAS been found (no exception thrown), get rid of that solution word
            _solutions.pop(_index)


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
    _solutions = solve()
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
            if i == 0:
                return 0 #in the case of a negative score, aka if the first word is hinted
            else:
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

#NYT SPELLING BEE SOLVER (SEPARATE FROM THE GAME CODE)

if len(sys.argv) != 1: #if there are arguments
    if len(sys.argv) != 3: #if there are multiple arguments, but not exactly 3 (main.py, -h/-s, [letters]), raise exception
        raise "Too many/too few arguments, see README for help!"

    if sys.argv[1] == "-h": #if the first arg after main.py is -h (hint)
        letters = sys.argv[2]
        letters = letters.lower()
        foundWords = []
        solutions = solve()
        print(hint())
    elif sys.argv[1] == "-s": #if the first arg after main.py is -s (solve)
        letters = sys.argv[2]
        letters = letters.lower()
        foundWords = []
        solutions = solve()
        for i in solutions:
            print(i) #to put a newline after every word
    else:
        raise "Unsupported arguments. See README for help!"
    raise SystemExit

#====================================================================================================================================================================================#

letterFile = open("letters.txt", 'r') #read the letters from the last day played from the file
lastDate = letterFile.readline()
lastDate = lastDate.strip()
letterFile.close()

today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY, put into a string

if lastDate == "" or (int(d1[0:2]) > int(lastDate[0:2])) or (int(d1[3:5]) > int(lastDate[3:5])): #if the dates are greater or the months are greater, regen the letters and redo setup
    print("Generating letters...")
    letterFile = open("letters.txt", 'w')

    letterFile.write(d1 + "\n") #write the date to the file

    while True:
        lettersList = [random.choice(vowels)] #make sure there's at least one vowel
        while len(lettersList) != 7:
            nextLetter = random.choice(string.ascii_lowercase)
            for i in range(len(lettersList)):
                if nextLetter == lettersList[i]: #check for duplicate letters (if duplicate found, break the for loop and throw away the letter choice)
                    break
            else: #if no duplicates found
                lettersList.append(nextLetter)

        for i in range(len(lettersList)):
            if lettersList[i] == 'q':
                for ii in range(len(lettersList)):
                    if lettersList[ii] == 'u':
                        break
                else: #if no u's are found, but q's are:
                    lettersList[random.randrange(0, 7)] = 'u'
                break #get out of the q-checking for loop

        for i in range(3): #randomize the letters 3 times, check each combo each time. this might save some processing time.
            random.shuffle(lettersList) #shuffle the letter order to mix the vowel in

            letters = ""
            for i in range(len(lettersList)): #convert the list to a string
                letters += lettersList[i]

            if maxScore() > 30: break #wait for a letter combo with a max score over 30
        if maxScore() > 30: break #break out of the while True loop (optimize, if needed)


    letters = letters.capitalize() #make the first letter uppercase
    for i in range(len(letters)):
        letterFile.write(letters[i] + " ")
    letters = letters.lower() #re-lowercase all of the letters

    letterFile.write("\n" + calculateRanks() + "\n")
    letterFile.close()

#====================================================================================================================================================================================#

letterFile = open("letters.txt", 'r')
letterFileList = letterFile.readlines()

letters = letterFileList[1] #second line
letters = letters.replace(" ", "") #get rid of the spaces
letters = letters.strip()
letters = letters.lower()

rankVals = letterFileList[2].split(",")
for i in range(len(rankVals)):
    rankVals[i] = int(rankVals[i])

foundWords = letterFileList
for i in range(3):
    foundWords.pop(0) #get rid of the first 4 lines of the list/letters.txt (date, letters, ranks) to get a list of found words
for i in range(len(foundWords)):
    foundWords[i] = foundWords[i].strip() #get rid of the newline chars

currentScore = 0
for i in foundWords: #calculate the score at the start of the game
    if i[0] == '-': #if the found word starts with a dash, that means it was a /hinted or /solved word, so don't count it in the score
        continue
    currentScore += score(i)

for i in range(len(foundWords)):
    if foundWords[i][0] == '-':
        foundWords[i] = foundWords[i][1:] #if the found word starts with a dash, remove it in the list ONLY, not in the file

solutions = solve() #fill the solutions list with all of the possible solution words

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

stdscr.addstr(21, 0, "Input: ") #print this BEFORE EVERYTHING ELSE otherwise it breaks stuff
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

foundWordsPad = curses.newpad(30, 150)
counter = 0
for i in range(len(foundWords)):
    if i % 15 == 0:
        counter += 1
    foundWordsPad.addstr(i % 15, (counter - 1)*15, foundWords[i]) #make columns of 15 found words
try:
    foundWordsPad.refresh(0, 0, 6, 35, 21, 120)
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
ranksPad.refresh(0, 0, 3, 130, 15, 150)

while True:
    hintFlag = False
    input = str(stdscr.getstr(21, 7)) #returns bytes, needs to be converted/casted to string.
    input = input[2:-1] #remove extraneous characters
    input = input.lower()
    for i in range(len(input)):
        stdscr.addstr(21, 7 + i, " ") #clear out the past input (stdscr.clrtoeol() and .clrtobot() didn't work for some reason...)
    stdscr.refresh()

    if input == "/exit": break
    if input == " " or input == "/shuffle":
        lettersGUIPad.addstr(0, 0, printLettersGUI(letters)) #regenerate the letters GUI with shuffled letters
        lettersGUIPad.refresh(0, 0, 2, 2, 17, 30)
        continue
    if input == "/hint":
        input = hint() #set the input to a good word, run it through the rest of the input code as a regular input
        hintFlag = True
        #the rest of the input code still needs to be run because of the GUI stuff
    if input == "/solve":
        temp = solve() #temp = a list of all of the not-already-found solution words
        for i in temp:
            #don't score, since the user didn't input the words
            #because the score didn't change, the rank doesn't either. don't bother calculating it.
            foundWords.append(i)
            counter = 0
            for ii in range(len(foundWords)):
                if ii % 15 == 0:
                    counter += 1
                foundWordsPad.addstr(ii % 15, (counter - 1)*15, foundWords[ii]) #make columns of 15 found words

            letterFile.close()
            letterFile = open("letters.txt", 'a') #reopen the file so the score and words can be appended to it
            letterFile.write("-" + i + "\n")
        foundWordsPad.refresh(0, 0, 6, 35, 21, 120)
        letterFile.close()
        time.sleep(5)
        raise SystemExit #the puzzle is solved, kill the program after 5 sec. the user can restart it if they want to see more.


    for i in solutions:
        if i == input: #if the input matches a word in the solutions list, return true
            for ii in foundWords:
                if ii == input: break #if the input matches a solution, make sure it hasn't already been found
            else: #if it wasn't already found (aka is a good input word)
                if not hintFlag: #if the last word was a real input (not a hint), add to the score
                    currentScore += score(input)

                foundWords.append(input)
                counter = 0
                for ii in range(len(foundWords)):
                    if ii % 15 == 0:
                        counter += 1
                    foundWordsPad.addstr(ii % 15, (counter - 1)*15, foundWords[ii]) #make columns of 15 found words
                foundWordsPad.refresh(0, 0, 6, 35, 21, 120)

                currentScorePad.addstr(0, 0, "Current Score: " + str(currentScore))
                currentScorePad.refresh(0, 0, 3, 35, 3, 70)

                currentRankPad.addstr(0, 0, "Current Rank: ")
                currentRankPad.addstr(" " * 10) #remove the old rank (.clrtoeol and .clrtobot didn't work for some reason)
                currentRankPad.refresh(0, 0, 4, 35, 4, 70)
                currentRankPad.addstr(0, 0, "Current Rank: " + ranks[currentRank(currentScore, rankVals)]) #put the new rank in
                currentRankPad.refresh(0, 0, 4, 35, 4, 70)

                letterFile.close()
                letterFile = open("letters.txt", 'a') #reopen the file so the score and words can be appended to it
                if not hintFlag:
                    letterFile.write(input + "\n")
                else:
                    letterFile.write("-" + input + "\n") #if the last input was a /hint, add a dash in front of the word in the file to denote it
                letterFile.close()


#====================================================================================================================================================================================#

#curses ending stuff
letterFile.close()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
