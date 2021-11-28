# Spelling Bee
A terminal version of the New York Times Spelling Bee game, with a built-in solver!

## NYT Spelling Bee Solver
This function is used as follows through terminal arguments. In the examples, [letters] denotes the puzzle letters, where the center letter is **first**.
- To get a hint, type the following command: `py main.py -h [letters]`
  - This will get a random hint word from the solutions list, not necessarily a word that you have not found already on the NYT site. If you get one you have already found, re-run until you get a hint you can use.
  - The hints are completely random (not alphabetical, not by points)

- To get the full puzzle solution: `py main.py -s [letters]`
  - The solution is ordered alphabetically, and pangrams are not marked. Stuff for a future update.

## Game
The Spelling Bee game itself follows the exact same rules as the New York Times version. If you have never played, the rules are below.

***To start the game***, run `py main.py`. It will regenerate letters the first time you start the program that day. Once the clock passes midnight, if the program is re-launched, `letters.txt` will clear and the letters will be regenerated.

Regenerating letters takes a minute, and the game will launch immediately afterwards. After that, every time the game is started, it will start significantly faster because the letter generation is skipped.

The words used in the game are dependent on `dictionary.txt` and `dictionary-profane.txt`. Any words put inside these files is fair game for Spelling Bee, and they are completely customizable. If the user wants to modify them to exclude certain words, include other ones that aren't already present, or change them in any way, they can. The program will still work, as long as the two text files `dictionary.txt` and `dictionary-profane.txt` exist (in any form) in the directory. The dictionaries are case-sensitive, however, they must be all lower-case for the program to work.

### Game Commands
These are *NOT ARGUMENTS*, these can be typed into the input area once the game is launched.

Words are inputted by typing in the word and hitting `Enter`. Commands also require `Enter` to be pressed.

- `/exit`: Exit the game.
- `/shuffle` or `[Space]`: Shuffle the letters in the grid.
- `/hint`: Give the player a word. It will be added to the found words area onscreen, but it will not count towards ranks or point totals.
- `/solve`: Solve the entire puzzle. The words will be added to the found words area, but will not count for points or ranks (like hints).

### How to Play
The aim of Spelling Bee is to use the letters in the grid to make as many words as you can. There is no time limit, other than the letters resetting at midnight every night.
- You may only use the letters in the grid.
- Every word must use the center letter, and be at least 4 characters long.
- All letters can be re-used as many times as you want.
- The game gives one point per character in a word (i.e. `letters` would get 7 points), except:
  - 4 letter words only get 1 point
  - Words that use all 7 letters in the grid at least once are called "pangrams", and they get double the points of a normal word (i.e. an 8 character pangram would get 16 points)

# Credits
The word lists are from the SCOWL (and Friends) project, and they can be found here: http://wordlist.aspell.net/ . The main dictionary file is the combination of the English and American English files, with a complexity/frequency of 0-70. They were assembled by me, and sorted alphabetically in Windows Command Prompt. The dictionary-profane.txt list is the same as the dictionary.txt list, but with all of the words in the profane SCOWL dictionaries.
