#dict is the array of dictionary lines
#dictFile is the file object
#letters is the game letter string (first char is the center letter, NO SPACES!)

def solve(hint):
    dict = dictFile.readlines() #read all lines into a list
    count = 0

    while True: #"rough cut" of the dictionary - remove any dict words without the center letter, that are too short, or single letters
        if count >= len(dict):
            break
        dict[count] = dict[count].strip("\n")
        if len(dict[count]) <= 3: #get rid of less than 4 character words (rules of spelling bee)
            dict.pop(count)
            continue
        if dict[count].find(letters[0]): #get rid of words that don't contain the center letter
            dict.pop(count)
            continue

        for i in range(len(dict[count])): #range(length of the current count'th line of the dictionary)
            if letters.find(dict[count][i]) == -1: #if the i'th letter of the current line isn't in the word, delete the line from the dict and break the loop
                dict.pop(count)
                break
        else: #only increments the index if the for loop runs successfully
            count += 1

    if hint:
        return dict[random.randint(0, len(dict))]
    else:
        return dict

def maxScore():
    solutions = solve(False)
    score = 0
    for i in range(len(solutions)):
        if len(solutions[i]) = 4: score += 1
        for ii in range(len(letters)): #check for pangrams, and score accordingly
            if(solutions[i].find(letters[ii]) == -1: #if the word doesn't contain every letter, it isn't a pangram, so break
                break
        else: #if the word is a pangram
            score += 2*len(solutions[i]) #double score
            continue
        if len(solutions[i]) > 4: score += len(solutions[i]) #if it isn't a 4 letter word, add the length of the word to score\

    return score

def calculateRanks(): #the scores corresponding to each of the ranks in spelling bee
    #Order: Beginner, Good Start, Moving Up, Good, Solid, Nice, Great, Amazing, Genius, Queen Bee (all the words)
    ranks = ""
    percentages = [0, 2.5, 5, 10, 20, 30, 40, 60, 80]
    score = maxScore()

    for i in percentages:
        ranks += i*score + ","

    return ranks
