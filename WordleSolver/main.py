def getSolutionList():  # Either uses list of possible Wordle solutions or uses list of all possible Wordle guesses
    run = True
    while run:
        run = False
        solutionsOrGuesses = str(input("1. List of solutions\n2. List of guesses\n"))
        if solutionsOrGuesses == '1':
            solutionList = open("wordlesolutions.txt", encoding="utf-8").read().split()
        elif solutionsOrGuesses == '2':
            solutionList = open("wordleguesses.txt", encoding="utf-8").read().replace('"', '').replace(',', '').split()
        else:
            run = True
    return solutionList


def getInput():  # Asks user what word they used from the bank
    run = True
    while run:
        run = False
        word = str((input("Selected word: ").lower()))
        for char in word:
            if char.isalpha() == False or len(word) != 5:
                run = True
    return word


def getColors():  # Gets color values for that word for information to parse
    run = True
    while run:
        run = False
        colors = str((input("Letter colors (ex: yngnn): ").lower()))
        for char in colors:
            if char.isalpha() == False or (char in {'g', 'y', 'n'} == False) or len(colors) != 5:
                run = True
    return colors

def checkDupe(word, colors):  # If the word has a duplicate with green and yellow letters, takes into account that there are two of those letters in the word
    dupe = None
    for i in range(0, 4):
        if word[i] == word[i + 1] and ((colors[i] == 'y' and colors[i + 1] == 'g') or (colors[i] == 'g' and colors[i + 1] == 'y')):
            dupe = word[i]
    for i in range(0, 3):
        if word[i] == word[i + 2] and ((colors[i] == 'y' and colors[i + 2] == 'g') or (colors[i] == 'g' and colors[i + 2] == 'y')):
            dupe = word[i]
    for i in range(0, 2):
        if word[i] == word[i + 3] and ((colors[i] == 'y' and colors[i + 3] == 'g') or (colors[i] == 'g' and colors[i + 3] == 'y')):
            dupe = word[i]
    if word[0] == word[4] and ((colors[0] == 'y' and colors[4] == 'g') or (colors[0] == 'g' and colors[4] == 'y')):
        dupe = word[i]
    return dupe


def parse(word, colors, solutionList):  # Rules out guesses from the list using colors + duplicates
    for i in range(0, 5):
        if colors[i] == 'n':  # If a letter is gray, removes all words with that letter unless the same letter is green earlier in the word
            for solution in list(solutionList):
                for char in solution:
                    for j in range(0,5):
                        if colors[j] != 'g' and char == solution[j] and char == word[i] and solution in solutionList: solutionList.remove(solution)
        if colors[i] == 'g':  # If a letter is green, removes all words without that letter in that specific position
            for solution in list(solutionList):
                greencheck = True
                if solution[i] != word[i]: greencheck = False
                if greencheck == False and solution in solutionList: solutionList.remove(solution)
        if colors[i] == 'y':  # If a letter is yellow, removes all words without the letter in them at all.
            for solution in list(solutionList):
                yellowcheck = False
                for char in solution:
                    if char == word[i]: yellowcheck = True
                if (yellowcheck == False or solution[i] == word[i]) and solution in solutionList: solutionList.remove(solution)
        if dupe != None: #  If there is a duplicate letter, removes all words with only one of the duplicate letter
            for solution in solutionList:
                count = 0
                for char in solution:
                    if char == dupe: count += 1
                if count < 2: solutionList.remove(solution)

def fancyprint(List):
    print('\033[2J')
    str = ''
    for solution in solutionList:
        str += solution + '   '
    print(str)

# solutionList = open("wordlesolutions.txt", encoding="utf-8").read().split()
solutionList = getSolutionList()
fancyprint(solutionList)
for i in range(0, 7):
    word = getInput()
    colors = getColors()
    dupe = checkDupe(word, colors)
    parse(word, colors, solutionList)
    if len(solutionList) == 1:
        print('\033[2J')
        print("Your word is " + "\033[1;32;32m" + solutionList[0] + '\033[0m')
        break
    if len(solutionList) == 0:
        print('\033[2J')
        print("No solutions remaining!")
        break
    fancyprint(solutionList)
