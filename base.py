import sys
from startup import Startup
import pygame
import os
# This class is a base for a graphics pipeline it creates a pygame window and sets its
# parameters
class Base(object):

    def __init__(self):
        startUp = Startup()
        startUp.run()
        pygame.init()
        # change position of the window on the screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 100)
        # w and h of window
        screenSize = (512, 512)

        # indicate rendering options
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL

        # initialize buffers to perform intialiasting
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        # use core profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)

        # create and display the window
        self.screen = pygame.display.set_mode(screenSize, displayFlags)

        # set the Title of the window
        pygame.display.set_caption("After")

        # determine if the main loop is active
        self.running = True

        # mangage time related operations and data
        self.clock = pygame.time.Clock()

        # manage user inout

        self.quit = False

    # implement by extending class
    def initialize(self):
        pass

    # implement by extending class
    def update(self):
        pass

    def run(self):
        ## startup ##

        self.initialize()

        ## main loop ##
        while self.running:
            ##process input##

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.quit = True

            if self.quit:
                self.running = False

            ## update ##
            self.update()

            # display on screen
            pygame.display.flip()

            # pause if necessary to achieve 60FPS
            self.clock.tick(60)

        ## shutdown ##
        pygame.quit()
        sys.exit()
