def solve(hint = False): #hint = true if it should print one solution, false to print all
    result = [] #words that are part of the anagram
    c = [0] #a list of counter variables
    failFlag = False #flag to check if the main algorithm's for loop completed
    word = ""
    lastWord = ""

    _word = letters

    _word = _word.replace(" ", "") #get rid of all of the spaces
    _word = _word.lower() #make sure the word is all lowercase
    word = _word
    lastWord = [_word] #lastword list

    #====================================================================================================================================================================================#

    #c[0] for the next 2 loops is the line of the dictionary list that the program is on.

    while True: #"rough cut" of the dictionary - remove any dict words with "bad" letters
        if c[0] >= len(lines):
            break
        lines[c[0]] = lines[c[0]].strip("\n")
        if len(lines[c[0]]) == 1: #get rid of 1 character words
            lines.pop(c[0])
            continue
        for i in range(len(lines[c[0]])): #range(length of the current c[0]'th line of the dictionary)
            if word.find(lines[c[0]][i]) < 0: #if the i'th letter of the current line isn't in the word, delete the line from the dict and break the loop
                lines.pop(c[0])
                break
        else: #only increments the index if the for loop runs successfully
            c[0] += 1
    c[0] = 0

    #c[0] is the line of the dictionary list that the program is on
    while True: #"fine cut" of the dictionary - remove any remaining dict words that don't work for other reasons (duplicate letters, etc)
        if c[0] >= len(lines):
            break
        for i in range(len(lines[c[0]])): #range(length of the current word)
            if word.find(lines[c[0]][i]) >= 0: #find the i'th letter of the dictionary line in the input word
                word = word[0:word.find(lines[c[0]][i])] + word[word.find(lines[c[0]][i]) + 1:] #if the letter is found, remove it from the input word
            else:
                lines.pop(c[0])
                word = lastWord[0] #reset the word
                break
        else:
            c[0] += 1

    #at this point, all words in 'lines' should work as a first word in the anagram.

    #====================================================================================================================================================================================#

    c[0] = 0
    if hint:
        c[0] = random.randint(0, len(lines))

    while True:
        ##=============================================================MAIN ALGORITHM================================================================##

        for i in range(len(lines[c[len(result)]])): #range: length of the line at index (appropriate counter depending on how many words have already been found)
            if word.find(lines[c[len(result)]][i]) >= 0: #if the i'th letter of the dictionary line at index (counter) is in the input word
                word = word[0:word.find(lines[c[len(result)]][i])] + word[word.find(lines[c[len(result)]][i]) + 1:] #if the letter is found in the input word, remove it from input word.
            else:
                failFlag = True #if the for loop fails (i.e. the anagram combination doesn't work), set failFlag and break it.
                break
        ##==========================================================================================================================================##

        if failFlag:
            failFlag = False
            if c[len(result)] >= len(lines) - 1: #if the counter reached the end of lines, aka reached the end of the dict (-1 offset because the ++ hasn't happened yet, in else)
                if len(result) > 0: #if a result can be removed, then remove it
                    while c[len(result)] >= len(lines) - 1: #go back to a counter that has space to count up
                        if len(result) > 0: result.pop()
                        else:
                            print("Complete.")
                            if "o" in args:
                                resultFile.close()
                            raise SystemExit
                        c[len(result)] += 1
                        c[len(result) + 1] = 0 #clear the now-vacated counter
                else:
                    print("No anagrams could be found, sorry!")
                    resultFile.close()
                    raise SystemExit
            else:
                c[len(result)] += 1
            word = lastWord[len(result)]
        elif not failFlag:
            result.append(lines[c[len(result)]]) #add the working word to the results list
            if len(c) == len(result): c.append(0) #add another index to the counter list if it is needed
            else: c[len(result)] = 0 #if the counter index exists, reset the counter.
            if hint: c[len(result)] = random.randint(0, len(lines)) #if a random anagram is specified, randomize the indexer
            if len(lastWord) == len(result): lastWord.append(word)
            else: lastWord[len(result)] = word #if the index exists, use it
        if word == "": #if word is empty, meaning all of the letters have been taken out of it (used)
            print(result)
            failFlag = False
            if "a" in args:
                result.pop() #remove the last result to give space in the word
                lastWord.pop() #get rid of the empty string in the last index of lastWord
                word = lastWord[len(result)]
                c[len(result)] += 1 #move on to the next word
                if c[len(result)] >= len(lines): #if increasing the counter hits the end of the dict
                    result.pop() #get rid of the next result back in the list
                    lastWord.pop()
                    word = lastWord[len(result)]
                    c[len(result)] += 1
            else: #if the args don't specify to print all, then exit the program
                raise SystemExit
