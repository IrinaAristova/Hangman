# Problem Set 2, hangman.py
# Name: Aristova Irina
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

MAX_ATTEMPTS = 6
MAX_WARNINGS = 3
VOWEL_LETTER = ["a", "e", "i", "o", "u"]

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
    # Эта функция возвращает булевое значение: ​ True​ ,
    # если ​ secret_word було угадано, и ​ False в обратном случае
    '''
    for s in secret_word:
        if s not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    # Эта функция возвращает рядок, который складывается с букв и подчеркиваний в основании того,
    # какие буквы с ​letters_guessed містяться в ​secret_word​
    '''
    def get_guessed_letter(text, letters_guessed):
        '''
        # Это рекурсивная функция, которая рассматривает первую букву текущего слова
        # и возвращает или текущий символ, или подчеркивание
        '''
        if text != "":
            if text[0] in letters_guessed:
                return text[0]+get_guessed_letter(text[1:], letters_guessed)
            else:
                return '_ '+get_guessed_letter(text[1:], letters_guessed)
        else:
            return ""

    return get_guessed_letter(secret_word, letters_guessed)


def get_available_letters(letters_guessed):
    '''
    # Эта функция возвращает рядок, который имеет буквы английского алфавита
    # в нижнем регистре — все буквы, которые не входят в letters_guessed
    '''
    all_letters = list(string.ascii_lowercase)
    for s in letters_guessed:
        all_letters.remove(s)
    return "".join(all_letters)

def get_unique_letter(secret_word):
    '''
    # Эта функция возвращает количество уникальных букв в слове
    '''
    return len(list(set(list(secret_word))))


def print_div():
    print("-------------------------------------------------")
    
def do_greating(letters_count, attempts):
    '''
    Приветствуем игрока
    '''
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуй угадать слово из %d букв(ы) с %d попыток."%(letters_count, attempts))
    print("Приступим!!!")
    print_div()

def do_win_letter(letter):
    print("Вау, у Вас получилось. Вы угадали букву "+letter)

def do_lose_letter(letter):
    print("Хорошая попытка, но неправильно.")
    print("В этом слове нет буквы "+letter)

def do_use_warning(warnings, text):
    if warnings > 0:
        if warnings == 1:
            print("Предупреждаю в последний раз. "+text)
        elif warnings == MAX_WARNINGS:
            print("Предупреждаю. "+text)
        else:
            print("Предупреждаю еще раз. "+text)
        warnings -= 1
        return True
    else:
        print("Я устал повторять Вам правила игры. "+text)
        return False
    
def get_user_letter(letters_guessed, warnings, with_hint = False):
    print(get_available_letters(letters_guessed))
    if with_hint:
        print("Если Вам нужна помощь введите *.")
    while True:
        s = input("Введите одну из предложеных букв ").strip()
        if len(s) > 1: 
            if do_use_warning(warnings, "Введенных символов больше одного."):
                warnings -= 1
                continue
            else:
                return False, warnings
        if s in letters_guessed:
            if do_use_warning(warnings, "Вы уже угадывали эту букву."):
                warnings -= 1
                continue
            else:
                return False, warnings
        if with_hint and s == "*":
            return s.lower(), warnings
        if str.isalpha(s) and (s in string.ascii_lowercase):
            return s.lower(), warnings
        else:
            if do_use_warning(warnings, "Введите символ английского алфавита."):
                warnings -= 1
            else:
                return False, warnings

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
    attempts = MAX_ATTEMPTS # устанавливаем количество попыток
    warnings = MAX_WARNINGS # устанавливаем количество предупреждений
    letters_guessed = []    # устанавливаем список введеных букв
    do_greating(len(secret_word), attempts)
    in_game = True
    while in_game:
        s, warnings = get_user_letter(letters_guessed, warnings)
        # проверяем введеную пользователем букву (или не букву)
        if s:
            letters_guessed.append(s)
            if s in secret_word:
                do_win_letter(s)
            else:
                do_lose_letter(s)
                if s in VOWEL_LETTER:
                    attempts -= 2
                else:
                    attempts -= 1
        else:
            attempts -= 1
        # проверяем можем ли мы продолжать игру
        if attempts:
            if is_word_guessed(secret_word, letters_guessed):
                print("Вы угадали слово: "+secret_word)
                score = attempts*get_unique_letter(secret_word)
                print("Вы заработали %d очков"%(score))
                in_game = False
            else:
                print("Попробуйте еще. У Вас осталось %d попыток."%(attempts))
                print_div()
                print(get_guessed_word(secret_word, letters_guessed))
        else:
            print("Вы проиграли. Это слово: "+secret_word)
            in_game = False

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(my_word) == len(other_word):
        ascii = []
        for s in (my_word):
            if s != "_":
                ascii.append(s)
        for i in range(len(my_word)):
            if my_word[i] == '_':
                # проверяем чтобы на этом месте была буква, которую еще не угадали
                if other_word[i] in ascii:
                    return False
            else:
                # проверяем одинаковые буквы в двух словах
                if my_word[i] != other_word[i]:
                    return False
        # текущее слово вполне подходит
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end=" ")
    print("")


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
    attempts = MAX_ATTEMPTS # устанавливаем количество попыток
    warnings = MAX_WARNINGS # устанавливаем количество предупреждений
    letters_guessed = []    # устанавливаем список введеных букв
    do_greating(len(secret_word), attempts)
    in_game = True
    while in_game:
        s, warnings = get_user_letter(letters_guessed, warnings, True)
        # проверяем введеную пользователем букву (или не букву)
        if s:
            if s == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed).replace("_ ", "_"))
                #continue
            else:
                letters_guessed.append(s)
                if s in secret_word:
                    do_win_letter(s)
                else:
                    do_lose_letter(s)
                    if s in VOWEL_LETTER:
                        attempts -= 2
                    else:
                        attempts -= 1
        else:
            attempts -= 1
        # проверяем можем ли мы продолжать игру
        if attempts:
            if is_word_guessed(secret_word, letters_guessed):
                print("Вы угадали слово: "+secret_word)
                score = attempts*get_unique_letter(secret_word)
                print("Вы заработали %d очков"%(score))
                in_game = False
            else:
                print("Попробуйте еще. У Вас осталось %d попыток."%(attempts))
                print_div()
                print(get_guessed_word(secret_word, letters_guessed))
        else:
            print("Вы проиграли. Это слово: "+secret_word)
            in_game = False


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
