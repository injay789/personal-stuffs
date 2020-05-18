# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 22:05:26 2020

@author: Injay Lee
"""

# Coursera Problem Solving Python Programming and Video Games
# Hacking Version 03
# This is a text-based password guessing game, made for the Coursera course
# Problem Solving Python Programming and Video Games

#%% FUNCTIONS

# Import modules
import uagame
import time
import random

"""
##############################
NAME:       main
PURPOSE:    This function runs the Hacking game
PARAMETERS: 
RETURNS:    None
##############################
"""
def main():
    # Generate the game window with dimensions 600px by 500px
    gameWindow, stringHeight = generateWindowProperties(600, 500)
    
    # Create the first window and prompt for user guess
    guess, xCoordinate, yCoordinate, correctPassword = displayGuessWindow(gameWindow, stringHeight)
    
    # Close previous window and display program outcome
    displayEndWindow(gameWindow, guess, correctPassword, stringHeight)
    return None

"""
##############################
NAME:       generateWindowProperties
PURPOSE:    This function generates a game window then outputs it for other functions to use
PARAMETERS: gameWindowHeight (I, REQ) - height of the game window in pixels
            gameWindowWidth  (I, REQ) - width of the game window in pixels
RETURNS:    gameWindow - the game window created by this function, used by other functions
##############################
"""
def generateWindowProperties(gameWindowHeight, gameWindowWidth):
    # Create game window that is gameWindowHeight pixels by gameWindowWidth pixels
    gameWindow = uagame.Window('Hacking', gameWindowHeight, gameWindowWidth)
    
    # Set other window properties
    gameWindow.set_font_name('couriernew')          # Set font as courier new
    gameWindow.set_font_size(18)                    # Set font size as 18
    gameWindow.set_font_color('green')              # Set font color as green
    gameWindow.set_bg_color('black')                # Set background color as black
    stringHeight = gameWindow.get_font_height()     # Get height of 18 point font
    
    # Generate list of window properties
    windowProperties = [gameWindow, stringHeight]
    
    return(gameWindow, stringHeight)

"""
##############################
NAME:       calculateEndScreenXCoordinate
PURPOSE:    This function takes in properties of a string (the text, location, string height) and updates
            the game window, then outputs a new set of coordinates for the next string
PARAMETERS: xLocation    (I, REQ) - x coordinate of the text to display
            yLocation    (I, REQ) - y coordinate of the text to display
            stringHeight (I, REQ) - height of the string, used to update the y location for the next string
                                         to be displayed
            stringWidth  (I, OPT) - width of the string, used to update the x location for the next string
                                         to be displayed
RETURNS:    xCoordinate - x-coordinate for centering a line of text
##############################
"""
def calculateEndScreenXCoordinate(gameWindow, string):
    xCoordinate = (gameWindow.get_width() - gameWindow.get_string_width(string)) // 2
    return(xCoordinate)

"""
##############################
NAME:       updateCoordinates
PURPOSE:    This function takes in properties of a string (the text, location, string height) and updates
            the game window, then outputs a new set of coordinates for the next string
PARAMETERS: xLocation    (I, REQ) - x coordinate of the text to display
            yLocation    (I, REQ) - y coordinate of the text to display
            stringHeight (I, REQ) - height of the string, used to update the y location for the next string
                                         to be displayed
            stringWidth  (I, OPT) - width of the string, used to update the x location for the next string
                                         to be displayed
RETURNS:    newXLocation - new x coordinate for the next string to be displayed
            newYLocation - new y coordinate for the next string to be displayed
##############################
"""
def updateCoordinates(xLocation, yLocation, stringHeight, stringWidth=0):
    newXLocation = xLocation + stringWidth
    newYLocation = yLocation + stringHeight
    
    # Generate array of coordinates
    coordinates = [newXLocation, newYLocation]
    
    return(newXLocation, newYLocation)

"""
##############################
NAME:       displayTextInWindow
PURPOSE:    This function takes in properties of a string (the text, location, string height) and updates
            the game window, then outputs a new set of coordinates for the next string
PARAMETERS: gameWindowToEdit (I, REQ) - defines which game window will be updated by the function
            textToDisplay    (I, REQ) - text to display in the window
            xLocation        (I, REQ) - x coordinate of the text to display
            xLocation        (I, REQ) - y coordinate of the text to display
            stringHeight     (I, REQ) - height of the string, used to update the y location for the next string
                                         to be displayed
            stringWidth      (I, OPT) - width of the string, used to update the x location for the next string
                                         to be displayed
RETURNS:    newXLocation - new x coordinate for the next string to be displayed
            newYLocation - new y coordinate for the next string to be displayed
##############################
"""
def displayTextInWindow(gameWindowToEdit, textToDisplay, xLocation, yLocation, stringHeight, stringWidth=0, sleepTime=0.3):
    gameWindowToEdit.draw_string(textToDisplay, xLocation, yLocation) # Write first line
    gameWindowToEdit.update()                                         # Update the game window to show changes
    time.sleep(sleepTime)                                             # Pause for defined number of seconds
    
    # Update x and y coordinates for next string
    newXLocation, newYLocation = updateCoordinates(xLocation, yLocation, stringHeight)
    
    # Return updated x and y locations
    return(newXLocation, newYLocation)

"""
##############################
NAME:       promptGuess
PURPOSE:    This function asks the user for a guess
PARAMETERS: gameWindow  (I, REQ) - the game to write to or take inputs from
            newXLocation (I/O, REQ) - the x coordinate the prompt shoud begin at, then the x coordinate of the next
                                      string in the window
            newYLocation (I/O, REQ) - the y coordinate the prompt shoud begin at, then the y coordinate of the next
                                     string in the window
RETURNS:    
##############################
"""
def promptGuess(gameWindow, string, xCoordinate, yCoordinate, stringHeight, stringWidth=0):
    
    # Ask user to input a guess
    guess = gameWindow.input_string(string, xCoordinate, yCoordinate)
    
    # Update x and y coordinates for next string
    newXLocation, newYLocation = updateCoordinates(xCoordinate, yCoordinate, stringHeight)
    
    # Return guess, updated x and y locations
    return(guess, newXLocation, newYLocation)

"""
##############################
NAME:       embedPassword
PURPOSE:    This function asks the user for a guess
PARAMETERS: password (I, REQ) - password to embed
            size     (I, REQ) - the size, number of characters, of the display block for the embedded password
RETURNS:    embeddedPassword
##############################
"""
def embedPassword(password, size):
    # Filler characters to embed password with   
    fill             = '!@#$%^&*()_+=~[]{}'
    
    # Initialize empty embedded password to fill in
    embeddedPassword = ''
    
    # Start embedding at random integer index
    passwordSize = len(password)                          # Calculate password size
    splitIndex   = random.randint(0, size - passwordSize) # Maximum position password can begin at, otherwise overflow
    
    # Fill in random characters for padding before password
    for index in range(0, splitIndex):
        embeddedPassword += random.choice(fill)
        
    # Add password to embedded password
    embeddedPassword += password
        
    # Fill in random characters for padding after password
    for index in range(splitIndex + passwordSize, size):
        embeddedPassword += random.choice(fill)
    
    return(embeddedPassword)

"""
##############################
NAME:       displayHint
PURPOSE:    Displays a hint for number of characters in the correct position relative to the letters in the
            correct password
PARAMETERS: gameWindow      (I, REQ) - game window to update
            passwordGuess   (I, REQ) - the password guess entered by the user
            correctPassword (I, REQ) - correct password determined earlier
            stringHeight    (I, REQ) - for displaying the password
RETURNS:    None
##############################
"""
def displayHint(gameWindow, passwordGuess, correctPassword, hintYCoordinate, stringHeight):
    # Initialize hint display location
    hintXCoordinate = gameWindow.get_width() // 2 # Start x at the middle of the width of the window
    
    # Break password guess into individual letters, then compare to correct password's letters
    # Count number of correct letters
    passwordGuessList   = list(passwordGuess)   # Use list to break into individual letters
    correctPasswordList = list(correctPassword) # Use list to break into individual letters
    correctLetterCount  = 0
    
    # Compare each letter
    for i in range(0, len(passwordGuessList)):
        print(i)
        if i == len(correctPasswordList):
            break
        if passwordGuessList[i] == correctPasswordList[i]:
            correctLetterCount += 1
    
    # If not all characters match in correct positions, display PASSWORD INCORRECT, and number of correct letters
    if (correctLetterCount != len(correctPassword)) or ((correctLetterCount == len(correctPassword)) and len(passwordGuess) > len(correctPassword)):
        hintDisplayText = [passwordGuess + ' INCORRECT',
                           str(correctLetterCount) + '/7 IN MATCHING POSITIONS']
        
    # Display hint
    for displayText in hintDisplayText:
        hintXCoordinate, hintYCoordinate = displayTextInWindow(gameWindow, displayText, hintXCoordinate, hintYCoordinate, stringHeight)
    
    return(hintXCoordinate, hintYCoordinate)
"""
##############################
NAME:       displayGuessWindow
PURPOSE:    This function generates a game window, asks the user for an input, then outputs it for other
            functions to use
PARAMETERS: gameWindow (I, REQ) - the game to write to or take inputs from
RETURNS:    guess       - the user's password guess
            xCoordinate - new x coordinate for the next string to be displayed
            yCoordinate - new y coordinate for the next string to be displayed
##############################
"""
def displayGuessWindow(gameWindow, stringHeight, stringWidth=0):
    xCoordinate = 0 # Initialize x location at x = 0
    yCoordinate = 0 # Initialize y location at y = 0
    attempts    = 4 # Initialize the number of attempts
    
    # Initialize fixed text
    enterGuessText = 'ENTER PASSWORD >'
    
    # Store lockout warning
    lockoutText        = '*** LOCKOUT WARNING ***'
    lockoutXCoordinate = gameWindow.get_width() - gameWindow.get_string_width(lockoutText)
    lockoutYCoordinate = gameWindow.get_height() - stringHeight

    #Display header
    headerList = ['DEBUG MODE', str(attempts) + ' ATTEMPT(S) LEFT']
    
    # Store location to display number of attempts left
    attemptsXCoordinate = 0
    attemptsYCoordinate = stringHeight
    
    for header in headerList:
        xCoordinate, yCoordinate = displayTextInWindow(gameWindow, header, xCoordinate, yCoordinate, stringHeight)
    
    # Display empty line
    xCoordinate, yCoordinate = displayTextInWindow(gameWindow, '', xCoordinate, yCoordinate, stringHeight)
    
    # Display password list
    passwordList = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE', 'HEARING', 
                    'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING']

    # Set HUNTING as the correct password
    correctPassword = passwordList[7]
    
    # Set maximum embedded password size as 20 characters
    size = 20

    for password in passwordList:
        # Embed password with random characters
        embeddedPassword = embedPassword(password, size)
        
        # Display password in game window
        xCoordinate, yCoordinate = displayTextInWindow(gameWindow, embeddedPassword, xCoordinate, yCoordinate, stringHeight)
    
    # Display empty line
    xCoordinate, yCoordinate = displayTextInWindow(gameWindow, '', xCoordinate, yCoordinate, stringHeight)
    
    # Initialize y coordinate of hint at 0
    hintYCoordinate = 0
    
    # Prompt for guess, as long as there are between 4 and 1 attempts remaining
    getUserGuess = True
    while getUserGuess:
        # Ask for guess
        guess, xCoordinate, yCoordinate = promptGuess(gameWindow, enterGuessText, xCoordinate, yCoordinate, stringHeight)
        
        # Check if guess is correct
        if guess == correctPassword:
            getUserGuess = False
        # If guess is not correct, prompt for another
        else:
            # Decrement number of attempts
            attempts -= 1
            
            # Display hint
            hintXCoordinate, hintYCoordinate = displayHint(gameWindow, guess, correctPassword, hintYCoordinate, stringHeight)
            
            # Quit if number of attempts is 0
            if attempts == 0:
                getUserGuess = False
            elif attempts == 1:
                displayTextInWindow(gameWindow, lockoutText, lockoutXCoordinate, lockoutYCoordinate, stringHeight, sleepTime=0)

            # Display new number of attempts     
            displayText = str(attempts) # Change display text to show number of attempts
            displayTextInWindow(gameWindow, displayText, attemptsXCoordinate, attemptsYCoordinate, stringHeight, sleepTime=0)

    return(guess, xCoordinate, yCoordinate, correctPassword)

"""
##############################
NAME:       displayEndWindow
PURPOSE:    This function generates the last game window, then asks the user to press Enter to end the game
PARAMETERS: gameWindow   (I, REQ) - the game to write to or take inputs from
            guess        (I, REQ) - the guess from the previous window
            stringHeight (I, REQ) - string height, used to update new string location
            stringWidth  (I, OPT) - string width, used to update new string location
RETURNS:    
##############################
"""
def displayEndWindow(gameWindow, guess, correctPassword, stringHeight, stringWidth=0):
    # Clear window
    gameWindow.clear()
    
    # Compute new y-coordinate
    outcome_height = stringHeight * 7                             
    yCoordinate = (gameWindow.get_height() - outcome_height) // 2      

    # Compute new x-coordinate
    xCoordinate = calculateEndScreenXCoordinate(gameWindow, guess)

    # Display centered guess, line 1/7 of final screen
    xCoordinate, yCoordinate = displayTextInWindow(gameWindow, guess, xCoordinate, yCoordinate, stringHeight)
    
    # Determine next lines based on user input
    if guess == correctPassword:
        endMessageList = ['', 'EXITING DEBUG MODE', '', 'LOGIN SUCCESSFUL - WELCOME BACK', '']
        prompt         = 'PRESS ENTER TO CONTINUE'
    else:
        endMessageList = ['', 'LOGIN FAILURE - TERMINAL LOCKED', '', 'PLEASE CONTACT AN ADMINISTRATOR', '']
        prompt         = 'PRESS ENTER TO EXIT'

    # Display next lines
    for message in endMessageList:
        # Display Text
        xCoordinate              = calculateEndScreenXCoordinate(gameWindow, message)
        xCoordinate, yCoordinate = displayTextInWindow(gameWindow, message, xCoordinate, yCoordinate, stringHeight)
    
    # Prompt user to press enter to end the program
    xCoordinate                     = calculateEndScreenXCoordinate(gameWindow, prompt)
    guess, xCoordinate, yCoordinate = promptGuess(gameWindow, prompt, xCoordinate, yCoordinate, stringHeight)
    
    # Close window
    gameWindow.close()
    
    return()

#%% RUN PROGRAM

main()