# import library files
import random
import sys

# helper functions
def update():
    """updates guesses made and moves left"""
    global guesses
    guesses += 1
    global moves
    moves -= 1

def movesGone():
    """Check if there are any moves left, if not notify user and quit game"""
    if moves < 1:
        print " You've run out of moves. Game Over! \n"
        printAnswer()
        printScores()
        sys.exit(0)

def printScores():
    """Displays moves left and guesses made"""
    print '\n'
    print 'Moves left until hanging: %s' % moves
    print 'Guesses made: %s \n' % guesses

def printAnswer():
    """print every letter in answer"""
    for letter in answer:
        print letter[0],

def printPartial():
    """prints the portion of answer that has been correctly guessed"""
    for letter in answer:
        if letter[1] == True:
            print letter[0],
        else:
            print '_',

def guessedAll():
    """check if we have guessed the answer"""
    for letter in answer:
        if letter[1] == False:
            return False
    return True

# list containing the players our user will be guessing for
players = ['Ronaldo', 'Messi', 'Rooney', 'Mata', 'Neymar', 'Suarez',
           'Bale', 'Fabregas', 'Cech', 'Hazard', 'Sanchez', 'Ozil', 'Benzema']

# we randomly choose an answer from the list and convert it to lowercase
answer = random.choice(players).lower()

# we convert the answer into a list of chars each with a 'show' boolean attached
answer = list(answer)
answer = [[letter, False] for letter in answer]

# counters for number of guesses and moves that we begin with
guesses, moves = 0, 6

# Announce game and give hint
print 'Famous Soccer Player Hangman \n'
printPartial()
print '\n'

while True:
    # we are taking input from the command prompt
    guess = raw_input('Guess the letter: ')

    # check that the guess is a single letter
    if not guess.isalpha() or len(guess) != 1:
        print 'Please provide a single letter'
    else: # the input is valid
        guess = guess.lower()
        # update stats
        update()

        # boolean variable recording if match has been found
        foundMatch = False

        # iterate through entire answer
        for letter in answer:
            # check if we have found a new match
            if letter[1] == False and guess == letter[0]:
                letter[1] = True
                foundMatch = True

        # if we have found a new match
        if foundMatch == True:
            # check if user has won the game
            if guessedAll() == True:
                print 'You have won the game! \n'
                printAnswer()
                printScores()
                sys.exit(0)
            # if user has not yet won the game
            else:
                print 'Found match! \n'
                # check if they have run out of moves, if not show them clues and stats
                movesGone()
                printPartial()
                printScores()
        # if we didn't find a match
        else:
            print 'No match, try again! \n'
            # check if they have run out of moves
            movesGone()
            printPartial()
            printScores()
            
        

                
                
        

