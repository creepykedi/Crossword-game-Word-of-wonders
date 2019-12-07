#! py3
# wordsofwonders - program analogue of iphone game
# makes a scrabble like puzzle of words
from collections import Counter
import random
# passing all words as string to mwords variable
with open('wordlist.txt', 'r') as myfile:
    mwords = myfile.read()

# putting all words into list to work with
mlist = mwords.split()


# clue generator with words >6 chars
listlength = len(mlist)
clue = []
while len(clue) < 6:
    rand = random.randint(0, listlength)
    clue = mlist[rand]
clue_letters = (list(clue))

alphabet = 'abcdefghijklmnopqrstvwuxyz'


# making list of all the letters that are NOT in clue word
for letter in clue:
    alphabet = alphabet.replace(letter, '')
#print(alphabet)
#print(len(alphabet))

# checking how many of each letter clue word has
table = []
for letter in clue_letters:
    table.append(clue_letters.count(letter))

# words as part of riddle will be added here
riddlewords = []

k = len(alphabet)
add = None
# checking if word has any of the letters it shouldn't have
for word in mlist:
    add = True
    for letter in alphabet:
        if letter in word:
            # if they do boolean value is set to false
            add = False
    # if they don't then add the word with matching index
    if add:
        riddlewords.append(word)


# now we need to check how many of each letter the clue word has, and delete all that have more from riddlewords
# print(riddlewords)
table2 = []
riddlewords1 = []

# looking for repeating letters in clue word
clueDict = {}
clueDict.update(Counter(clue))

repeatedLettersClue = []
# this function will add all repeated letters from clue word to the list above
for value in clueDict:
    reapeated = clueDict[value]
    if reapeated > 1:
        repeatedLettersClue.append(value)
      #  if reapeated > 2:
      #   repeatedLettersClue.append(value)
#print('\n')
#print('These letters are doubled :' + str(repeatedLettersClue))


repeatedRiddle = {}
repeatedRiddlelist = []

# repeatedLettersClue - the list of letters we need to check against
repeatedLettersRiddle = []
# repeatedLettersRiddle -  the list of letters of checked word

# riddlewords2 - the list of all words that have double letter in common
riddlewords2 = []

# if we have repeated letters in clue, this function runs
# checks if repeated letters in clue words and the one from list coincide
# if they do, the word is added to new list
if len(repeatedLettersClue) > 0:
    for word in riddlewords:
        # adding doubled letters to dictionary to check from
        repeatedRiddle.update(Counter(word))
    #    print(repeatedRiddle)
        for value in repeatedRiddle:
        # value is number of letters
            numOfLetters = repeatedRiddle[value]
            if numOfLetters > 1:
                repeatedLettersRiddle.append(value)
               # print(word + ' doubled ' + str(repeatedLettersRiddle))
               # print('clue word doubled ' + str(repeatedLettersClue))
                if len(set(repeatedLettersRiddle).difference(set(repeatedLettersClue))) == 0:
                    # if any duplicated letters from riddle list are in clue list, but not more letters, we add it
                    riddlewords2.append(word)
                    #print(word + ' is added')
                    # clearing the list for next word
                    repeatedLettersRiddle.clear()

                    break
                repeatedLettersRiddle.clear()
                break
        repeatedRiddle.clear()
                # checking if it has same repeated letters as clue letter
    #print(repeatedRiddle)
#print('\n')
#print('The list of riddle words with repeated letters is:')
#print(set(riddlewords2))

newlist = []
riddlewords2_dic = {}
for word in riddlewords2:
    riddlewords2_dic.update(Counter(word))
    for value in riddlewords2_dic:
        valuefromfirst = riddlewords2_dic[value]
        if valuefromfirst > 1:
            newlist.append(word)
#print(newlist)
# deleting all words that have duplicate letters:

for word in riddlewords:
    for letter in word:
        table2.append(word.count(letter))
    if 2 not in table2 and len(word) > 2 and word.islower():
        riddlewords1.append(word)
    table2.clear()


# adding all words with double letters to list of riddlewords
riddlewords1 = riddlewords1 + riddlewords2
# removing clue word from list
if clue in riddlewords1:
    riddlewords1.remove(clue)

maximum = len(set(riddlewords1))
#print(set(riddlewords1))
play = []

# getting three random words to play

for i in range(4):
    play.append(riddlewords1[random.randint(0, maximum-1)])
# deleting any repeated words
    play = list(set(play))
# if less than 4 words adding one more
while len(play) < 3:
    play.append(riddlewords1[random.randint(0, maximum - 1)])

#print(clue)
#print(play)
print('Welcome to Word of Wonders game!')
print('Good luck!')
print('\n'*5)
print("Find all words in crossword which contain these letters:")
# printing the random letters to make up the clue word from
print(' '.join(random.sample(clue, len(clue))).upper())





clueguessed = [clue]
play.append(clue)
guessWords = play

playwords = []
wordsGuessed = []
# visual aid to how many letters are in words
for word in play:
    playwords.append((('.') * len(word)))
print(playwords)
print('\n')

#for word in playwords:
   # print(word)
hintnum = random.randint(2, len(play[0]))
remaining_letters = len(play[0]) - hintnum
def guessGame():

    guess = input('Find a word\n')
    condition = len(guess) == len(clue)
    if guess in guessWords:
        wordsGuessed.append(guess)
        print('Good job! You found these words:')
        play.remove(guess)
        # changing dots to guessed words
        for word in playwords:
            if len(word) == len(guess):
                playwords.remove(word)
                playwords.append(guess)
                break
        print(playwords)
    elif guess in clue and condition:
        playwords.append(guess)
        print('Good job! You found the main word!' + str(playwords))
        clueguessed.remove(guess)
        play.remove(guess)
    elif guess in riddlewords1:
        print('You found a word that is not in a crossword')
        riddlewords1.remove(guess)
    elif guess != 'hint':
        print("There isn't such word")
        print("If you're stuck, write 'hint' to get a hint")
    if guess == 'hint':
        print('Your hint: ')
        print(play[0][0:hintnum] + '.'*remaining_letters)
while len(play) != 0:
    guessGame()
else:
    print('You won! Congrats!')

