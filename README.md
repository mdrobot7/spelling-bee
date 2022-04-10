# Spelling Bee
A terminal version of the New York Times Spelling Bee game, with a built-in solver!

**This program uses a Python terminal UI package called Curses, which will have to be installed before running.**

## NYT Spelling Bee Solver
This function is used as follows through terminal arguments. In the examples, [letters] denotes the puzzle letters, where the center letter is **first**.
- To get a hint, type the following command: `py main.py -h [letters]`
  - This will get a random hint word from the solutions list, not necessarily a word that you have not found already on the NYT site. If you get one you have already found, re-run until you get a hint you can use.
  - The hints are completely random (not alphabetical, not by points)

- To get the full puzzle solution: `py main.py -s [letters]`
  - The solution is ordered alphabetically, and pangrams are marked with an `*` before the word.

- To get the full puzzle solution, sorted by word length: `py main.py -S [letters]`
  - The solution is ordered by word length, with pangrams marked with an `*` and listed first.

DISCLAIMER: **Not all words** outputted by the solver are guaranteed to be solutions to the New York Times Spelling Bee game. The NYT edits the game's solution list, and sometimes excludes certain words (often times particularly rare, specific, jargon-y, or scientific terms). The dictionary files included in this repository are intended to include as many words as possible, not specifically the words used by NYT.

## Game
The Spelling Bee game itself follows the exact same rules as the New York Times version. If you have never played, the rules are below.

***To start the game***, run `py main.py`. It will regenerate letters the first time you start the program that day. Once the clock passes midnight, if the program is re-launched, `letters.txt` will clear and the letters will be regenerated.

Regenerating letters takes a minute, and the game will launch immediately afterwards. After that, every time the game is started, it will start significantly faster because the letter generation is skipped.

The words used in the game are dependent on `dictionary.txt` and `dictionary-profane.txt`. Any words put inside these files is fair game for Spelling Bee, and they are completely customizable. If the user wants to modify them to exclude certain words, include other ones that aren't already present, or change them in any way, they can. The program will still work, as long as the two text files `dictionary.txt` and `dictionary-profane.txt` exist (in any form) in the directory. The dictionaries are case-sensitive, however, they must be all lower-case for the program to work.

### Overriding Letters
The user may override the auto-generated letters for the game and replace them with their own (or the current day's New York Times letters!). To override the letters, run the following command: `py main.py [letters]`, where `[letters]` are the new letters, with the center letter first. Read the warning, and enter `Y` if you want to proceed.

This only needs to be done **ONCE**. Once the letters are overriden, they will stay that way. For example, if you override the letters, play for a while, exit, and come back, start the game with the regular `py main.py` command, and it will restore your solved words and score. If you use the `py main.py [letters]` command, **it will clear your solved words and score**.

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

# Common Errors
- `_curses.error: addwstr() returned ERR`: This seems to be MS Powershell-specific, and simply means the Powershell window is not big enough to play the game. Expand the window and start the game again. (This does not happen in Windows Command Prompt, in CMD it throws the correct user-readable exception. Fix for a future patch)

# Credits
The word lists are from the SCOWL (and Friends) project, and they can be found here: http://wordlist.aspell.net/ . The main dictionary file is the combination of the English and American English files, with a complexity/frequency of 0-70. They were assembled by me, and sorted alphabetically in Windows Command Prompt. The dictionary-profane.txt list is the same as the dictionary.txt list, but with all of the words in the profane SCOWL dictionaries.
