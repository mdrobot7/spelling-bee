def solve(hint):
    #dict is the array of dictionary lines
    #dictFile is the file object
    dict = dictFile.readlines() #read all lines into a list
    count = 0
    #letters is the game letter string (first char is the center letter, every letter is separated by a space)

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
