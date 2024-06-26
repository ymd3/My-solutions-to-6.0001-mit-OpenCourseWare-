# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    def __str__(self):
        x = self.get_message_text()
        return x
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        a = self.valid_words[:]
        return a

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        dict_upper = {}
        dict_lower = {}
        lower = 'abcdefghijklmnopqrstuvwxyz'
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for letters in lower:
            dict_lower[letters] = letters

        for letters in upper:
            dict_upper[letters] = letters

        if shift == 0:
            dict_upper = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
            return dict_upper

        while shift > 0:
            x = []
            for values in dict_lower.values():
                x.append(values)
            new = x[1:]
            x = [x[0]]
            lower_values = new + x
            x = 0
            for keys in dict_lower.keys():
                dict_lower[keys] = lower_values[x]
                x += 1

            y = []
            for values in dict_upper.values():
                y.append(values)
            new = y[1:]
            y = [y[0]]
            upper_values = new + y
            x = 0
            for keys in dict_upper.keys():
                dict_upper[keys] = upper_values[x]
                x += 1
            shift -= 1
        dict_upper.update(dict_lower)
        return dict_upper


    def build_shift_dict_recursion(self, shift):  #look into this one again
        if shift == 0:
            dict_upper = {}
            dict_lower = {}
            lower = 'abcdefghijklmnopqrstuvwxyz'
            upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

            for letters in lower:
                dict_lower[letters] = letters

            for letters in upper:
                dict_upper[letters] = letters

            dict_upper.update(dict_lower)
            return dict_upper

        if shift > 0:
            upper_values = []
            previous = Message.build_shift_dict_recursion(self, shift - 1)

            for values in previous.values():
                upper_values.append(values)

            lower_values = upper_values[26:]

            upper_values = upper_values[:26]


            new = lower_values[1:]
            lower_values = [lower_values[0]]
            lower_values = new + lower_values

            new = upper_values[1:]
            upper_values = [upper_values[0]]
            upper_values = new + upper_values

            x = 0
            y = 0
            for keys in previous.keys():
                if x < 26:
                    previous[keys] = upper_values[x]
                    x += 1

                else:
                    previous[keys] = lower_values[y]
                    y += 1

            return previous



    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        listed_message = []
        cipher = Message.build_shift_dict_recursion(self, shift)

        for characters in Message.get_message_text(self):
            if characters not in cipher:
                listed_message.append(characters)
            else:
                encoded = cipher.get(characters)
                listed_message.append(encoded)


        listed_message = ''.join(listed_message)
        return listed_message




class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def __str__(self):
        the = self.message_text
        return the
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift = {}
        messages = []
        for shifts in range(27):
            attempt = Message.build_shift_dict_recursion(self, shifts)
            keys = []
            values = []
            msg = []
            for key in attempt.values():
                keys.append(key)

            for value in attempt.keys():
                values.append(value)
            x = 0

            while x < len(keys):
                attempt[keys[x]] = values[x]
                x += 1

            for char in CiphertextMessage.get_message_text(self):
                if char in attempt:
                    msg.append(attempt.get(char))
                else:
                    msg.append(char)

            msg = ''.join(msg)
            messages.append(msg)
            msg = msg.split(' ')
            valid_words = 0
            for words in msg:
                if words in Message.get_valid_words(self):
                    valid_words += 1


            best_shift[shifts] = valid_words

        number_of_valid_words = []
        for value in best_shift.values():
            number_of_valid_words.append(value)
        shifts = []
        for keys in best_shift.keys():
            shifts.append(keys)
        highest = max(number_of_valid_words)
        the_best_shift = shifts[number_of_valid_words.index(highest)]
        return (the_best_shift, messages[number_of_valid_words.index(highest)])

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    k = 'I love programming'
    k = Message(k)
    k = k.apply_shift(4)
    print(k)
    k = CiphertextMessage(k)
    k = k.decrypt_message()
    print(k)

    k = 'I am just a kid'
    k = Message(k)
    k = k.apply_shift(18)
    print(k)
    k = CiphertextMessage(k)
    k = k.decrypt_message()
    print(k)



    #TODO: best shift value and unencrypted story
    why = Message("Don't cry, this is very fun")
    x = 0

    cry = CiphertextMessage(get_story_string())
    print(cry.decrypt_message())
