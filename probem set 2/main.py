# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    x = 0
    for letters in secret_word:
        if letters in letters_guessed:
            x += 1
    if x == len(secret_word):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    revealed = ''
    for letters in secret_word:
        if letters in letters_guessed:
            revealed += letters
        else:
            revealed += '_ '
    return revealed



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    import string
    import string
    letters = list(string.ascii_lowercase)
    for a in letters_guessed:
        if a in letters:
            letters.remove(a)
    letters = ''.join(letters)
    return letters

def unique_letters(secret_word):
    # gets the unique letters of the secret word and returns its as a string
    a = list(secret_word)
    for letters in a:
        if a.count(letters) > 1:
            a.remove(letters)
    a = ''.join(a)
    return a

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    x = 6
    letters_guessed = []
    y = 3
    print('Welcome to the game of Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long')
    print(f'You have {y} warnings left.')

    while x > 0:
        print('-------------')
        print(f'you have {x} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        a = input('Please guess a letter: ').lower()

        if is_word_guessed(secret_word, letters_guessed) == True:
            print('congratulations, you won!')
            print(f'You total score for this game is: {x*len( unique_letters(secret_word) )}')
            break

        elif a in letters_guessed:
            y-=1
            if y >= 0:
                print(f"Oops! You've already guessed that letter. You now have {y} warnings: ")
                print(get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left:")
                print('so you lose one guess: ', get_guessed_word(secret_word, letters_guessed))
                y = 1
                x -= 1

        elif a in secret_word:
            letters_guessed.append(a)
            print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')

        elif a not in secret_word:
            if a not in 'qwertyuiopasdfghjklzxcvbnm':
                if y>0 :
                    y -= 1
                    print(
                        f'Oops! That is not a valid letter. You have {y} warnings left: {get_guessed_word(secret_word, letters_guessed)}')
                if y == 0:
                    x -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:")
                    print('so you lose one guess: ', get_guessed_word(secret_word, letters_guessed))
                    y = 1

            elif a in 'aeiou':
                x-=2
                letters_guessed.append(a)
                print(f'Oops! that letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')

            else:
                x-=1
                letters_guessed.append(a)
                print(f'Oops! that letter is not in my word: {get_guessed_word(secret_word,letters_guessed)}')
        if is_word_guessed(secret_word, letters_guessed) == True:
            print('congratulations, you won!')
            print(f'You total score for this game is: {x*len( unique_letters(secret_word) )}')
            break
        if x <= 0:
            print("----------- ")
            print(f"Sorry, you ran out of guesses. The word was {secret_word}.")




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------
def space_remover(my_word):
    #takes in a guessed word ans removes the spaces
    my_word = list(my_word)
    k = my_word.count(' ')
    for num in range(k):
        my_word.remove(' ')
    my_word = ''.join(my_word)
    return my_word


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    match = []
    my_word = space_remover(my_word)
    if len(my_word) == len(other_word):
        for letters in my_word:
            if letters in 'qwertyuiopasdfghjklzxcvbnm':
                if letters in other_word:
                    if my_word.index(letters) == other_word.index(letters):
                        match.append(True)
                    else:
                        match.append(False)
                else:
                    match.append(False)
    if not len(my_word) == len(other_word):
        match.append(False)
    if False in match:
        match = False
    else:
        match = True
    return match


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    list = []
    for other_word in load_words():
        if match_with_gaps(my_word, other_word) == True:
            list.append(other_word)
    if list == []:
        print("No matches found")
    else:
        print(' '.join(list))

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    x = 6
    letters_guessed = []
    y = 3
    print('Welcome to the game of Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long')
    print(f'You have {y} warnings left.')

    while x > 0:
        print('-------------')
        print(f'you have {x} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        a = input('Please guess a letter: ').lower()

        if is_word_guessed(secret_word, letters_guessed) == True:
            print('congratulations, you won!')
            print(f'You total score for this game is: {x * len(unique_letters(secret_word))}')
            break

        if a == '*':
            my_word = get_guessed_word(secret_word, letters_guessed)
            show_possible_matches(my_word)

        elif a in letters_guessed:
            y -= 1
            if y >= 0:
                print(f"Oops! You've already guessed that letter. You now have {y} warnings: ")
                print(get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left:")
                print('so you lose one guess: ', get_guessed_word(secret_word, letters_guessed))
                y = 1
                x -= 1

        elif a in secret_word:
            letters_guessed.append(a)
            print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')

        elif a not in secret_word:
            if a not in 'qwertyuiopasdfghjklzxcvbnm':
                if y > 0:
                    y -= 1
                    print(
                        f'Oops! That is not a valid letter. You have {y} warnings left: {get_guessed_word(secret_word, letters_guessed)}')
                if y == 0:
                    x -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:")
                    print('so you lose one guess: ', get_guessed_word(secret_word, letters_guessed))
                    y = 1

            elif a in 'aeiou':
                x -= 2
                letters_guessed.append(a)
                print(f'Oops! that letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')

            else:
                x -= 1
                letters_guessed.append(a)
                print(f'Oops! that letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
        if is_word_guessed(secret_word, letters_guessed) == True:
            print('congratulations, you won!')
            print(f'You total score for this game is: {x * len(unique_letters(secret_word))}')
            break
        if x <= 0:
            print("----------- ")
            print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints("apple")

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

# secret_word = choose_word(wordlist)
# hangman_with_hints(secret_word)
