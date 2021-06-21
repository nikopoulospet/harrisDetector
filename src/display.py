#!/usr/bin/python3

import pygame
import numpy as np
import sys

class Display(object):
    def __init__(self,W,H):
        pygame.init()
        self.W = W
        self.H = H
        self.selector = 0
        self.screen = pygame.display.set_mode((W,H))
        self.surface = pygame.Surface(self.screen.get_size()).convert()


    def paint_vid(self,image,count):
        ret = np.empty((300,369,3),dtype=np.uint8)
        ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = image[:,:]
        surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        font = pygame.font.Font('freesansbold.ttf', 10)
        text = font.render(str(count), True, (255,0,0),(0,255,0))
        textRect = text.get_rect()
        textRect.center = (self.W-10, self.H-10)

        self.screen.blit(surf, (0,0))
        self.screen.blit(text, textRect)
        pygame.display.flip()
        pygame.display.update()

    def paint(self,image,gray,img,rMap,L1,L2):
        if(self.selector == 1):
            ret = np.empty((self.H,self.W,3),dtype=np.uint8)
            ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = gray
            surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        elif(self.selector == 2):
            ret = np.empty((self.H,self.W,3),dtype=np.uint8)
            ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = img[:,:]
            surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        elif(self.selector == 3):
            ret = np.empty((self.H,self.W,3),dtype=np.uint8)
            ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = rMap[:,:]
            surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        elif(self.selector == 4):
            ret = np.empty((self.H,self.W,3),dtype=np.uint8)
            ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = L1[:,:]
            surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        elif(self.selector == 5):
            ret = np.empty((self.H,self.W,3),dtype=np.uint8)
            ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = L2[:,:]
            surf = pygame.surfarray.make_surface(ret.swapaxes(0,1))
        elif(self.selector == 6):
            surf = pygame.surfarray.make_surface(image.swapaxes(0,1)[:,:, [2,1,0]])
        else:
            surf = pygame.surfarray.make_surface(image.swapaxes(0,1)[:,:, [2,1,0]])


        for x in range(0,rMap[0,:].size):
            for y in range(0,rMap[:,0].size):
                if(rMap[y][x] > 0):
                    pygame.draw.circle(surf, (0,255,0), (x,y), 2)

        self.screen.blit(surf, (0,0))
        pygame.display.flip()
        pygame.display.update()

    def checkInput(self):
            #catch input calls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #keyboard pressed to change display options
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.selector = 0
                    if event.key == pygame.K_1:
                        self.selector = 1
                    if event.key == pygame.K_2:
                        self.selector = 2
                    if event.key == pygame.K_3:
                        self.selector = 3
                    if event.key == pygame.K_4:
                        self.selector = 4
                    if event.key == pygame.K_5:
                        self.selector = 5
                    if event.key == pygame.K_6:
                        self.selector = 6
