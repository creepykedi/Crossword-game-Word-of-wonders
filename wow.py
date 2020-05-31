#! py3
# wordsofwonders - program analogue of iphone game
# makes a scrabble like puzzle of words
from collections import Counter
import random


def generate_word_set(filename):
    # clue word generator with words >6 chars
    def generate_clue(words):
        mlist = words.split()
        listlength = len(mlist)
        clue = []
        while len(clue) < 6:
            rand = random.randint(0, listlength)
            clue = mlist[rand]
            if '-' in clue:
                generate_word_set(filename)
        clue_letters = (list(clue))
        return clue, clue_letters, mlist

    alphabet = 'abcdefghijklmnopqrstvwuxyz'


    # making list of all the letters that are NOT in clue word, to exclude words that contain them
    def get_letters_missing(clue, alphabet):
        for letter in clue:
            alphabet = alphabet.replace(letter, '')
        return alphabet


    def open_dictionary():
        with open(filename, 'r') as myfile:
            # passing all words as string to words variable
            words = myfile.read()
            clue, clue_letters, mlist = generate_clue(words)
            restrict_letters = get_letters_missing(clue, alphabet)
            # checking how many of each letter clue word has
            table = [clue_letters.count(letter) for letter in clue_letters]
            return clue, clue_letters, mlist, table, restrict_letters

    clue, clue_letters, mlist, table, restrict_letters = open_dictionary()

    k = len(alphabet)
    add = None

    # words as part of riddle will be added here
    def get_possible_riddlewords(arr):
        riddlewords = []
        for word in mlist:
            add = True
            # checking if word has any of the letters it shouldn't have
            for letter in arr:
                if letter in word:
                    # if they do, boolean value is set to false
                    add = False
            # if they don't then add the word with matching index
            if add:
                riddlewords.append(word)
        return riddlewords


    riddlewords = get_possible_riddlewords(restrict_letters)
    #print(f'Possible riddlewords: ', *riddlewords)


    # now we need to check how many of each letter the clue word has and remove from riddlewords ones with extra letters
    # counting letters in clue
    def count_clue_letters(dict):
        clueDict = {}
        clueDict.update(Counter(dict))
        return clueDict

    clueDict = count_clue_letters(clue)

    # looking for repeating letters in clue word
    # this function will add all repeated letters from clue word to the list above
    def clue_repeated_letters(dict):
        repeatedLettersClue = []
        for value in dict:
            reapeated = dict[value]
            if reapeated > 1:
                repeatedLettersClue.append(value)
        return repeatedLettersClue

    repeatedLettersClue = clue_repeated_letters(clueDict)

    table2 = []

    # if we have repeated letters in clue, this function runs
    # checks if repeated letters in clue words coincide with the one from list
    # if they do, the word is added to new list
    def filterRiddlewords(repeatedLettersClue):

        # add counters of current words here
        repeatedRiddle = {}
        repeatedRiddlelist = []

        # repeatedLettersClue - the list of letters we need to check against
        repeatedLettersRiddle = []

        # riddlewords2 - the list of all words that have double letter in common
        riddlewords2 = []

        if repeatedLettersClue:
            for word in riddlewords:
                # adding doubled letters to dictionary to check from
                repeatedRiddle.update(Counter(word))
                n = 1
                for letter in repeatedRiddle:
                    letter = letter.lower()
                    n += 1

                    if repeatedRiddle[letter] <= clueDict[letter]:
                        if n == len(word):
                            riddlewords2.append(word)
                            n = 1
                            repeatedLettersRiddle.clear()
                    else:
                        break
                repeatedRiddle.clear()
        return riddlewords2

    riddlewords2 = filterRiddlewords(repeatedLettersClue)

    # deleting all words that have duplicate letters, adding the rest to list:
    riddlewords1 = []

    def noRepeatedLeteters():
        for word in riddlewords:
            amount = {}
            amount.update(Counter(word))
            values = amount.values()
            myvalues = [i for i in values if i == 1]
            if sum(myvalues) == len(word):
                riddlewords1.append(word)

    noRepeatedLeteters()
    # getting the final list of words to pick from
    final_riddlewords = list(set(riddlewords1).union(set(riddlewords2)))

    # removing clue word from list
    if clue in final_riddlewords:
        final_riddlewords.remove(clue)

    return final_riddlewords, clue


def setup_game():
    final_riddlewords, clue = generate_word_set('wordlist.txt')
    maximum = len(set(final_riddlewords))
    if maximum < 4:
        generate_word_set('wordlist.txt')

    # getting  random words to play
    def generate_playwords(lst):
        play = []
        if len(lst) > 6:
            while len(play) < random.randint(4, 7):
                if maximum < 7:
                    word = lst[random.randint(2, maximum - 1)]
                else:
                    word = lst[random.randint(3, 6)]
                if word not in play:
                    play.append(word)

        else:
            for word in lst:
                play.append(word)
        return play

    play = generate_playwords(final_riddlewords)
    return play, final_riddlewords, clue


def show(clue, play):
    print('Welcome to Word of Wonders game!')
    print('Good luck!')
    print('\n'*5)
    print("Find all words in crossword which contain these letters:")
    # printing the random letters to make up the clue word from

    theriddle = (' '.join(random.sample(clue, len(clue))).upper())
    print(theriddle)

    clueguessed = [clue]
    if clue not in play:
        play.append(clue)
    play = list(set(play))
    assert len(play) == len(set(play))

    playwords = []
    wordsGuessed = []
    # visual aid to how many letters are in words
    for word in play:
        playwords.append((('.') * len(word)))

    print(playwords)
    print('\n')
    return playwords, clueguessed, wordsGuessed, theriddle


play, final_riddlewords, clue = setup_game()
playwords, clueguessed, wordsGuessed, theriddle = show(clue, play)


def hint(play):
    if '.' not in play[0]:
        hintnum = random.randint(2, len(play[0]))
        remaining_letters = len(play[0]) - hintnum
        print('Your hint: ')
        print(play[0][0:hintnum] + '.' * remaining_letters)
    else:
        hintnum = random.randint(2, len(clue[0]))
        remaining_letters = len(clue[0]) - hintnum
        print('Your hint: ')
        print(clue[0][0:hintnum] + '.' * remaining_letters)


def update(guess):
    for word in playwords:
        if len(word) == len(guess):
            playwords.remove(word)
            playwords.append(guess)
            break


def guessGame():
    guess = input('Find a word\n')
    if guess in play and guess != clue:
        print('Good job! You found these words:')
        play.remove(guess)
        # changing dots to guessed words
        update(guess)
        print(playwords)
        print('\n', theriddle)
    elif guess == clue:
        update(guess)
        print("\n" + 'Good job! You found the main word!' + '\n' + theriddle + '\n'+ str(playwords))
        clueguessed.remove(guess)
        play.remove(guess)
        wordsGuessed.append(guess)
        print('\n', theriddle)
        print(playwords)

    elif guess in final_riddlewords:
        print('You found a word, but it is not in a crossword! Try another!')
        print(playwords)
        final_riddlewords.remove(guess)
        print('\n', theriddle)
    elif guess != 'hint':
        print("There is no such word in crossword")
        print("If you're stuck, write 'hint' to get a hint")
        print('\n', theriddle)
        print(playwords)
    if guess == 'hint':
        hint(play)


while len(play) != 0:
    guessGame()
else:
    print()
    print('Amazing! You found all the words!')
    print('You won! Congratulations!')


