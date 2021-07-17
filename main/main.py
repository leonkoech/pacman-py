import sys
import pygame
from game import Game
import time
import threading
import multiprocessing
# from twisted.ineternet import task, reactor

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def timer(starttime,game,close):
    while not close:
     
        game.self_replicate()
        # run script every 30 seconds to multiply infections
        time.sleep(30.0 - ((time.time() - starttime)% 30.0))     
   

def main():
    # Initialize all imported pygame modules
    pygame.init()
    starttime = time.time()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("VAXMAN")
    #Loop until the user clicks the close button.
    close = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Create a game object
    game = Game()
    # -------- Main Program Loop -----------
    time_thread  = multiprocessing.Process(target=timer,name="timer",args=(starttime,game,close))

    time_thread.start()

    while not close:
        # --- Process events (keystrokes, mouse clicks, etc)
        close = game.process_events()
        # --- Game logic should go here
        game.run_logic()
        # --- Draw the current frame
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)
        # new loop
    
       
        #tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
    # sys.exit()

if __name__ == '__main__':
    main()
