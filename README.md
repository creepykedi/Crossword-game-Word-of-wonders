# Word of wonders

A crossword game that works in a command line.

######Description: 

Upon running, game creates a random long secret word(selected from the list of nouns from .txt file), and several more shorter words that use the same letters. 
All letters that this word uses are then displayed to the user in a random order, along with boxes indicating other words and their letters, like this:

```
Find all words in crossword which contain these letters:
A U L E C G E O L
['...', '...', '...', '.........']
```

######Objective
Player has to guess all the words to win the game. Unguessed words are obscured with dots like that: 
'....' - a four letter word. Guessed words are displayed normally.

```
Find a word
>cue
Good job! You found these words:
['...', '...', '.........', 'cue']
```

Player can get a hint, to randomly get part of word or whole word discovered:

```
>hint
Your hint: 
al.
```

This example uncovered two letters of 3 letter word (ale).

Some words that satisfy the conditions aren't in crossword. The player is displayed 'You found a word that is not in a crossword' if he finds such a word.
Upon guessing all words correctly, player gets congratulations message and the game ends.
