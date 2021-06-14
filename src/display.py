#!/usr/bin/python3

import pygame
import sys

class Display(object):
    def __init__(self,W,H):
        pygame.init()
        self.W = W
        self.H = H
        self.screen = pygame.display.set_mode((W,H))
        self.surface = pygame.Surface(self.screen.get_size()).convert()

    def paint(self, img):

        surf = pygame.surfarray.make_surface(img.swapaxes(0,1)[:,:, [2,1,0]])
        self.screen.blit(surf, (0,0))
        pygame.display.update()

    def checkExit(self):
            #catch exit calls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
