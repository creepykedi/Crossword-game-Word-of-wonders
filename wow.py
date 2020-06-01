#! py3
# wordsofwonders - program analogue of iphone game
# makes a scrabble like puzzle of words
from collections import Counter
import random

alphabet = 'abcdefghijklmnopqrstvwuxyz'

class GamePrep:
    def __init__(self, filename, alphabet, difficulty=2):
        self.filename = filename
        self.alphabet = alphabet
        self.clue = []
        self.difficulty = difficulty
        self.words = ""
        self.clue_letters = None
        self.mlist = []
        self.table = None
        self.restrict_letters = []
        self.add = None
        self.clueDict = {}
        self.riddlewords = []
        self.riddlewords1 = []
        self.riddlewords2 = []
        self.final_riddlewords = []
        self.repeatedLettersClue = []
        self.play = []

    def generate_word_set(self):
        def generate_clue():
            """ clue word generator with words >6 chars """
            self.mlist = self.words.split()
            listlength = len(self.mlist)
            while len(self.clue) < 6:
                rand = random.randint(0, listlength)
                self.clue = self.mlist[rand]
                if '-' in self.clue:
                    self.generate_word_set()
            self.clue_letters = (list(self.clue))
            return self.clue, self.clue_letters, self.mlist

        def get_letters_missing():
            """makes list of all the letters that are NOT in clue word, to exclude words that contain them"""
            self.restrict_letters = list(set(self.alphabet).difference(self.clue))
            return self.restrict_letters

        def open_dictionary():
            """ Opens file to use as a dictionary for game"""
            with open(self.filename, 'r') as myfile:
                # passing all words as string to words variable
                self.words = myfile.read()
                return self.words

        def make_table():
            # checking how many of each letter clue word has
            self.table = [self.clue_letters.count(letter) for letter in self.clue_letters]

        def get_possible_riddlewords():
            for word in self.mlist:
                self.add = True
                # checking if word has any of the letters it shouldn't have
                for letter in self.restrict_letters:
                    if letter in word:
                        # if they do, boolean value is set to false
                        self.add = False
                # if they don't then add the word with matching index
                if self.add:
                    self.riddlewords.append(word)
            return self.riddlewords

        def count_clue_letters():
            """ check how many of each letter the clue word has
             to remove from riddlewords ones with extra letters"""
            self.clueDict = Counter(self.clue)
            return self.clueDict

        # looking for repeating letters in clue word
        # this function will add all repeated letters from clue word to the list above

        def clue_repeated_letters():
            for value in self.clueDict:
                reapeated = self.clueDict[value]
                if reapeated > 1:
                    self.repeatedLettersClue.append(value)
            return self.repeatedLettersClue

        # if we have repeated letters in clue, this function runs
        # checks if repeated letters in clue words coincide with the one from list
        # if they do, the word is added to new list
        def filterRiddlewords():
            """ if we have repeated letters in clue, this function runs
                checks if repeated letters in clue words coincide with the one from list
                if they do, the word is added to new list"""
            # add counters of current words here
            if self.repeatedLettersClue:
                for word in self.riddlewords:
                    currentclue = Counter(self.clueDict)
                    check = Counter(word)
                    currentclue.subtract(check)
                    if any(x < 0 for x in currentclue.values()):
                        continue
                    else:
                        self.riddlewords2.append(word)

            return self.riddlewords2

        # deleting all words that have duplicate letters, adding the rest to list:
        def noRepeatedLeteters():
            for word in self.riddlewords:
                amount = {}
                amount.update(Counter(word))
                values = amount.values()
                myvalues = [i for i in values if i == 1]
                if sum(myvalues) == len(word):
                    self.riddlewords1.append(word)

        def get_final_Words():
            """ getting the final list of words to pick from"""
            self.final_riddlewords = list(set(self.riddlewords1).union(set(self.riddlewords2)))
            # removing clue word from list
            if self.clue in self.final_riddlewords:
                self.final_riddlewords.remove(self.clue)

        open_dictionary()
        generate_clue()
        generate_clue()
        get_letters_missing()
        get_possible_riddlewords()
        make_table()
        count_clue_letters()
        clue_repeated_letters()
        filterRiddlewords()
        noRepeatedLeteters()
        get_final_Words()
        return self.final_riddlewords, self.clue

    def setup_game(self):
        maximum = len(set(self.final_riddlewords))
        if maximum < 4:
            self.generate_word_set()

        # getting  random words to play
        def generate_playwords():
            #print(self.clue)
            #print(self.riddlewords2)
            if len(self.final_riddlewords) > 6:
                while len(self.play) < random.randint(4, 7):
                    if maximum < 7:
                        word = self.final_riddlewords[random.randint(2, maximum - 1)]
                    else:
                        word = self.final_riddlewords[random.randint(3, 6)]
                    if word not in self.play:
                        self.play.append(word)

            else:
                for word in self.final_riddlewords:
                    self.play.append(word)
            return self.play

        generate_playwords()
        return self.play, self.final_riddlewords, self.clue


class Game:
    def __init__(self, play, clue, wordsguessed, playwords, theriddle, score, clueguessed):
        # list of words still to be guessed
        self.play = play
        # main word
        self.clue = clue
        # list of all that we guessed
        self.wordsGuessed = wordsguessed
        # [..., ....]
        self.playwords = playwords
        # G N V I I D type of clue repr
        self.theriddle = theriddle
        # bool if we guessed main word
        self.clueguessed = clueguessed
        self.score = score

    def show(self):
        """"Displays beginning of a game"""
        print('Welcome to Word of Wonders game!')
        print('Good luck!')
        print('\n' * 3)
        print("Find all words in crossword which contain these letters:")
        # printing the random letters to make up the clue word from

        self.theriddle = (' '.join(random.sample(self.clue, len(self.clue))).upper())

        print(self.theriddle)

        if self.clue not in self.play:
            self.play.append(self.clue)
        self.play = list(set(self.play))

        for word in self.play:
            self.playwords.append('.' * len(word))
        print(self.playwords)
        return self.play, self.playwords, self.theriddle

    def guess_clue(self):

        self.clueguessed = True
        return self.clueguessed

    def guessGame(self, *args):
        """Main game logic"""
        def show_score():
            if self.score is not None:
                print('Your score: ', self.score)
            else:
                print('Your score: 0')

        def hint():
            """Gives player a hint"""
            if '.' not in self.play[0]:
                hintnum = random.randint(2, len(self.play[0]))
                remaining_letters = len(self.play[0]) - hintnum
                print('Your hint: ')
                print(self.play[0][0:hintnum] + '.' * remaining_letters)
            else:
                hintnum = random.randint(2, len(clue[0]))
                remaining_letters = len(clue[0]) - hintnum
                print('Your hint: ')
                print(clue[0][0:hintnum] + '.' * remaining_letters)

        def update():
            self.wordsGuessed.append(guess)
            self.play.remove(guess)
            for word in self.playwords:
                if guess not in self.playwords:
                    if len(word) == len(guess):
                        self.playwords.remove(word)
                        self.playwords.append(guess)

        #print('play', self.play)

        print('Your score: ', self.score)
        guess = input('Find a word:   ')
        print()
        if guess in self.play and guess != self.clue:
            print('Good job! You found these words:')
            update()
            self.score += 50
        elif guess == self.clue:
            self.guess_clue()
            self.score += 150
            update()
            print("\n" + 'Good job! You found the main word!')

        elif guess in final_riddlewords:
            print('You found a word, but it is not in a crossword! Try another!')
            self.score += 20
            final_riddlewords.remove(guess)

        elif guess != 'hint':
            print("There is no such word in crossword")
            print("If you're stuck, write 'hint' to get a hint")
        if guess == 'hint':
            if 'hint' not in self.play:
                self.score -= 10
            hint()
        return self

    def playGame(self):
        """Run game recursively"""
        self.play, self.playwords, self.theriddle = self.show()
        # recursively pass new values
        game = self.guessGame()
        while len(self.play) != 0 or not self.clueguessed:
            print(self.playwords, '\n')
            print(self.theriddle)
            Game.guessGame(game)
        else:
            print()
            print('Amazing! You found all the words! Your score: ', self.score)
            print('You won! Congratulations!')

# Create instance of game
G = GamePrep('wordlist.txt', alphabet, difficulty=1)
GamePrep.generate_word_set(G)
play, final_riddlewords, clue = GamePrep.setup_game(G)
g = Game(play=play, clue=clue, wordsguessed=[], playwords=[], theriddle="", score=0, clueguessed=False)
Game.playGame(g)

