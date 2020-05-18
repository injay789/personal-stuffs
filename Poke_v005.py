import uagame
import pygame
import random
import math

#%% FUNCTIONS

"""
##############################
NAME:       main
PURPOSE:    This function runs the Poke the Dots game
PARAMETERS: 
RETURNS:    None
##############################
"""
def main():
    # Create game
    game = Game()

    # Play game
    game.playGame()
    
    return(None)

# An object in this class represents a complete game
class Game:
    
    def __init__(self):
        # Create window with fixed height of 500px, fixed width of 400px
        self.gameWindow = uagame.Window('Poke the Dots', 500, 400)
        self._adjustWindowProperties()

        # Define game properties
        self._closeButtonSelected = False               # Define the default close button object
        self._gameClock           = pygame.time.Clock() # Create the clock
        self._score               = 0                   # Initialize game _score to be zero
        self._frameRate           = 90                  # Higher frame rate is faster game, vice versa
        self._collision             = False               # Define the default object to determine if dots have come into contact
        
        # Define dot properties
        self.smallDotColor    = 'red'      # Dot color
        self.smallDotRadius   = 30         # Dot radius in px
        self.smallDotCenter   = [50, 75]   # Where the small dot will be spawned
        self.smallDotVelocity = [1, 2]     # The velocity [xVelocity, yVelocity]
        self.bigDotColor      = 'blue'     # Dot color
        self.bigDotRadius     = 40         # Dot radius in px
        self.bigDotCenter     = [200, 100] # Where the big dot will be spawned
        self.bigDotVelocity   = [2, 1]     # The velocity [xVelocity, yVelocity]
    
        # Create the dots
        self.smallDot = Dot(self.smallDotColor, self.smallDotCenter, self.smallDotRadius, self.smallDotVelocity, self.gameWindow)
        self.bigDot   = Dot(self.bigDotColor, self.bigDotCenter, self.bigDotRadius, self.bigDotVelocity, self.gameWindow)

        # Randomize the dots' positions
        self.smallDot.randomizeDotPosition()
        self.bigDot.randomizeDotPosition()

        # Play the game
        self.playGame()

        return(None)

    """
    ##############################
    NAME:       _adjustWindowProperties
    PURPOSE:    This method defines windows properties
    PARAMETERS: self (I, REQ) - attribute containing all objects required for the game
    RETURNS:    None
    ##############################
    """
    def _adjustWindowProperties(self):
        # Set window properties
        self.gameWindow.set_bg_color('black')       # Set black background
        self.gameWindow.set_font_name('couriernew') # Set font as courier new
        self.gameWindow.set_font_size(64)           # Set font size as 64
        self.gameWindow.set_font_color('white')     # Set font color as white

        return(None)

    """
    ##############################
    NAME:       playGame
    PURPOSE:    This method plays the game
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def playGame(self):
        # Keep running game as long as player has not selected close
        while not self._closeButtonSelected:
            # Check if user closed the game window
            self.handleEvents()

            # If the dots have not collided, continue the game
            if self._collision == False:
                self.drawGame()   # Draw the next frame
                self.updateGame() # Update the next frame

            # If the dots have collided
            else:
                self.displayGameOver()                # Display game over
                self.gameWindow.update()              # Update window
                self._gameClock.tick(self._frameRate) # Refresh the game, so the user can click X to quit

        # Once the loop is stopped, the game should be closed
        self.gameWindow.close()

        return(None)

    """
    ##############################
    NAME:       handleEvent
    PURPOSE:    Check if the player has performed any actions that should close the game window
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def handleEvents(self):
        # Handle user's actions, i.e. mouse click, key press
        eventList = pygame.event.get() # Get list of user actions
    
        for event in eventList:
            if event.type == pygame.QUIT:              # Check one event, if equal to user clicking quit button, do the following:
                self._closeButtonSelected = True       #     Update _closeButtonSelected object in game class
            elif event.type == pygame.MOUSEBUTTONDOWN: # Check one event, if equal to user clicking down on mouse button, do the following:
                self.smallDot.randomizeDotPosition()   # Call function to randomize dots' positions and velocities
                self.bigDot.randomizeDotPosition()
        
        return(None)

    """
    ##############################
    NAME:       drawGame
    PURPOSE:    Draw the next frame
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def drawGame(self):
        # Clear window before displaying next frame
        self.gameWindow.clear()
    
        # Draw things in the game window
        self.smallDot.draw()                                            # Draw small dot
        self.bigDot.draw()                                              # Draw big dot
        self.gameWindow.draw_string('Score: ' + str(self._score), 0, 0) # Draw _scoreboard
    
        # Update window
        self.gameWindow.update()
    
        return(None)

    """
    ##############################
    NAME:       updateGame
    PURPOSE:    Calculate the next positions of the dots
    PARAMETERS: game (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def updateGame(self):
        # Move dots
        self.smallDot.moveDot()
        self.bigDot.moveDot()
    
        # Every second (1,000 ms) increase the _score by 1
        self._score = pygame.time.get_ticks() // 1000

        # Check if the dots have collided
        self.checkCollision()

        # Control frame rate
        self._gameClock.tick(self._frameRate) # Refresh game at set refresh rate
    
        return(None)

    """
    ##############################
    NAME:       checkCollision
    PURPOSE:    Check if dots have touched each other
    PARAMETERS: game (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def checkCollision(self):
        # Compute distance between the dots
        distanceVector = [i - j for i, j in zip(self.smallDot.centerOfDot(), self.bigDot.centerOfDot())]
        distance       = math.sqrt((distanceVector[0])**2 + (distanceVector[1])**2)

        # If the distance between the dots' centers are less than or equal to the sum of their radii, the dot's have come into contact
        if distance <= (self.smallDot.radiusOfDot() + self.bigDot.radiusOfDot()):
            self._collision = True

        return(None)

    """
    ##############################
    NAME:       displayGameOver
    PURPOSE:    Check if dots have touched each other
    PARAMETERS: game (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def displayGameOver(self):
        # Get original text and background colors
        originalTextColor       = self.gameWindow.get_font_color()
        originalBackgroundColor = self.gameWindow.get_bg_color()

        # Get game over pop up colors
        gameOverBackground = self.bigDot.colorOfDot()
        gameOverForeground = self.smallDot.colorOfDot()
        
        # Get the game surfac and pygame color
        gameSurface           = self.gameWindow.get_surface()    # Get game window surface to modify
        pygameBackgroundColor = pygame.Color(gameOverBackground) # Get the background color

        # Set the coordinates, length, and width of display text
        x      = 0
        y      = self.gameWindow.get_height() - self.gameWindow.get_font_height()
        width  = 300
        height = self.gameWindow.get_font_height()

        # Set the text's color as the small dot's color, background color as the big dot's color
        self.gameWindow.set_font_color(gameOverForeground)
        self.gameWindow.set_bg_color(gameOverBackground)

        # Write the string in the game window at the bottom left corner
        self.gameWindow.draw_string('GAME OVER', x, y)

        # Reset text and background color to original colors
        self.gameWindow.set_font_color(originalTextColor)
        self.gameWindow.set_bg_color(originalBackgroundColor)

        return(None)

    pass

# An object in this class represents a complete dot
class Dot:
    
    def __init__(self, color, center, radius, velocity, gameWindow):
        self._color      = color
        self._center     = center
        self._radius     = radius
        self._velocity   = velocity
        self._gameWindow = gameWindow

    """
    ##############################
    NAME:       draw
    PURPOSE:    This method draws the dot
    PARAMETERS: self (I, REQ) - attribute containing all objects required to draw the dot
    RETURNS:    None
    ##############################
    """
    def draw(self):
        gameSurface    = self._gameWindow.get_surface() # Get game window surface to modify
        pygameDotColor = pygame.Color(self._color)      # Get the dot color
    
        # Draw the dots
        pygame.draw.circle(gameSurface, pygameDotColor, self._center, self._radius)    

        return(None)

    """
    ##############################
    NAME:       randomizeDotPosition
    PURPOSE:    This method randomizes the dot's position
    PARAMETERS: game (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def randomizeDotPosition(self):
        # Compute the height and width of the game window
        gameWindowSize = [self._gameWindow.get_width(), self._gameWindow.get_height()]

        # Randomize the position and velocity
        for i in range(0, len(self._center)):
            self._center[i] = random.randint(self._radius, gameWindowSize[i] - self._radius)

        return(None)

    """
    ##############################
    NAME:       moveDot
    PURPOSE:    Modify a dot's position
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    None
    ##############################
    """
    def moveDot(self):
        # Compute the height and width of the game window
        gameWindowSize = [self._gameWindow.get_width(), self._gameWindow.get_height()]

        # Update position
        for i in range(0, len(self._center)):
            self._center[i] += self._velocity[i]
        
        # Check if edge of dot has touched edge of game window
        for i in range(0, len(gameWindowSize)):
            if (self._center[i] + self._radius >= gameWindowSize[i]) or (self._center[i] - self._radius <= 0):
                self._velocity[i] = -(self._velocity[i])

        return(None)

    """
    ##############################
    NAME:       colorOfDot
    PURPOSE:    Return the dot's color
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    dotColor - the dot's color, in a string
    ##############################
    """
    def colorOfDot(self):
        dotColor = self._color

        return(dotColor)

    """
    ##############################
    NAME:       centerOfDot
    PURPOSE:    Return the dot's center
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    dotColor - the dot's color, in a string
    ##############################
    """
    def centerOfDot(self):
        dotCenter = self._center

        return(dotCenter)

    """
    ##############################
    NAME:       cradiusOfDot
    PURPOSE:    Return the dot's center
    PARAMETERS: self (I, REQ) - contains attributes that will be used by the function
    RETURNS:    dotColor - the dot's color, in a string
    ##############################
    """
    def radiusOfDot(self):
        dotRadius = int(self._radius)
        
        return(dotRadius)

    pass

#%% RUN PROGRAM

main()