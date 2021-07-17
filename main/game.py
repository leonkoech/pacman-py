#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from player import Player
from enemies import *
from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
import random
from threading import Thread
import sched,time
import sys
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

# def check_time(self):
#     while not check_time.cancelled:
#         Game.self_replicate(self)
#         time.sleep(5)
# check_time.cancelled = False

# t = Thread(target=check_time)
# t.start()

class Game(object):
    
    # this function runs in the background every 30 seconds
    def self_replicate(self):
        print('replicate')
        print(pygame.display.get_init())
        print(self.game_over)
        # check if the game has already started
        if self.game_over == False:
            for i in self.enemies:
                # multiply the existing infections
                self.enemies.add(Infection(i.rect.x,i.rect.y,i.change_x,i.change_y))



    

    def __init__(self):
        self.font = pygame.font.Font(None,40)
        self.about = False
        self.game_over = True
        self.dead_infection = True
        self.game_over_screen = False
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        # Create the menu of the game
        self.menu = Menu(("Start","About","Exit"),font_color = WHITE,font_size=60)
        # Create the player
        self.player = Player(32,128,"player.png")
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen
        self.dots_group = pygame.sprite.Group()
        # Set the enviroment:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Create the enemies
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Infection(288,96,0,2))
        self.enemies.add(Infection(288,320,0,-2))
        self.enemies.add(Infection(544,128,0,2))
        self.enemies.add(Infection(32,224,0,2))
        self.enemies.add(Infection(160,64,2,0))
        self.enemies.add(Infection(448,64,-2,0))
        self.enemies.add(Infection(640,448,2,0))
        self.enemies.add(Infection(448,320,2,0))

        
        # Add the dots inside the game
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.dead_infection_sound = pygame.mixer.Sound("deathinfection.wav")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")

       

    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True
                        elif self.menu.state == 2:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                    
        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks,self.vertical_blocks)

            # dot collision
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            # When the block_hit_list contains one sprite that means that player hit a dot
            if len(block_hit_list) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1
                if len(self.enemies) == 0:
                    print("All enemies Destroyed Vaxman!!")
                    if(len(self.dots_group) == 0):
                        print("you win")
                
               
            # enemy collision
            enemy_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            # if the number of enemy collisions is greater than 1 destroy enemy
            # game over if enemy count is greater than 32 times the original number
            ghost_count= len(self.enemies)
           
            if len(enemy_hit_list) > 0:
              
                   
                
                self.dead_infection_sound.play()
                
                if len(self.enemies) == 0:
                    print("All enemies Destroyed Vaxman!!")
                    if(len(self.dots_group) == 0):
                        print("you win")
                
            if ghost_count == 8*32:
                # when ghosts grow to 32 times the original number
                self.game_over=True
                self.game_over_screen=True
               
                self.enemies.explosion = False
                
                self.game_over_sound.play()
            # self.game_over=self.player.game_over
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)
           # tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))    

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                self.display_message(screen,"Vax-man is an arcade game like pacman")
            elif self.game_over_screen:
                self.display_message(screen,"GAME OVER! Score: "+str(self.score) )
            else:
                self.menu.display_frame(screen)
        else:
            # --- Draw the game here ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            #screen.blit(text, (30, 650))
            # Render the text for the score
            text = self.font.render("Score: " + str(self.score),True,GREEN)
            # Put the text on the screen
            screen.blit(text,[120,20])
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,255,0)):
        label = self.font.render(message,True,color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
       
        # Determine the position of the label
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Draw the label onto the screen
        screen.blit(label,(posX,posY))


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1
