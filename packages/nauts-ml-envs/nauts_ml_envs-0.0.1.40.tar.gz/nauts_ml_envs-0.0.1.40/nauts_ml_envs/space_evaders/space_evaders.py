# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:42:02 2020

@author: Richard Hamilton
"""
import numpy as np
import pygame
from pygame.locals import *
import random
import os

pygame.init()


ENV_WIDTH = 10  #width of the window
ENV_HEIGHT = 10 #height of the window
SCREEN_WIDTH = ENV_WIDTH * 50 #width of the window
SCREEN_HEIGHT = ENV_HEIGHT * 50 #height of the window

#NUM_ENEMIES = 4


#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

#NUM_ROUNDS = 10
OFF_SCREEN_LIMIT = 10

#create a player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, player_file):
        # create a plain rectangle for the sprite image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.img = pygame.image.load(player_file)
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.imgrect = self.img.get_rect()
        self.rect.centerx = ENV_WIDTH/2
        self.rect.bottom = ENV_HEIGHT
        self.x_speed=0
        
    def update(self):            
        self.rect.x += self.x_speed
        if self.rect.right > ENV_WIDTH:
            self.rect.right = ENV_WIDTH
        if self.rect.left <0:
            self.rect.left =0

#create a player sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, meteorite_file):
        # create a plain rectangle for the sprite image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill(RED)
        self.img = pygame.image.load(meteorite_file)
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.rect = self.image.get_rect()
        self.imgrect = self.img.get_rect()
        self.rect.x = random.randint(0, ENV_WIDTH - self.rect.width)
        self.rect.y = random.randint(-OFF_SCREEN_LIMIT, 0)
        self.y_speed = 1
        self.round = 0
    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > ENV_HEIGHT:
            self.rect.x = random.randint(0, ENV_WIDTH - self.rect.width)
            self.rect.y = random.randint(-OFF_SCREEN_LIMIT, 0)
            self.round+=1

class env:
    def __init__(self, background_file, player_file, meteorite_file, num_enemies = 4, num_rounds = 10):
        #Set up screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(background_file)
        self.player_file = player_file
        self.meteorite_file = meteorite_file
        
        #setup player
        self.all_sprites = pygame.sprite.Group()
        self.img = pygame.sprite.Group()
        self.player = Player(player_file)
        self.num_enemies = num_enemies
        self.num_rounds = num_rounds
        
        #setup meteroids
        self.enemy_sprites = pygame.sprite.Group()
        for i in range(self.num_enemies):
            self.enemy = Enemy(meteorite_file)
            self.enemy_sprites.add(self.enemy)
            self.all_sprites.add(self.enemy)
    
        self.all_sprites.add(self.player)
        
        self.done = 0

    def get_objs_observation_space_high(self):
        obs = [ENV_WIDTH]+([ENV_WIDTH]*self.num_enemies)
        return np.array(obs, dtype=float)
    
    def get_objs_observation_space_low(self):
        obs = [0]+([-ENV_WIDTH]*self.num_enemies)
        return np.array(obs, dtype=float)
        
    def sortSecond(self, List):
        return List[1]
    
    def get_state(self):
        #update raw state
        self.state=[self.player.rect.centerx]
        obj_rounds = []
        for obj in self.enemy_sprites:
            obj_rounds.append(obj.round)
            self.state.append(obj.rect.centerx-self.player.rect.centerx) #),obj.y_speed\
        
        for rounds in obj_rounds:
            self.done = True
            if rounds < self.num_rounds:
                self.done = False
                break
        return self.state
    
    def get_flags(self, action):
        #check for collisions
        collisions = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        self.col = False
        if collisions:
             self.done = True
             self.col = True
        
        return [self.col, action]
    
    def reset(self):
        #setup player
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.player_file)
        
        #setup meteroids
        self.enemy_sprites = pygame.sprite.Group()
        for i in range(self.num_enemies):
            self.enemy = Enemy(self.meteorite_file)
            self.enemy_sprites.add(self.enemy)
            self.all_sprites.add(self.enemy)
    
        self.all_sprites.add(self.player)
        
        self.done = 0
        
        return self.get_state()
        
    def step(self, action):
        #set horizontal speed of player
        if action ==1:
            self.player.x_speed = -1
        elif action == 2:
            self.player.x_speed = 1
        else:
            self.player.x_speed = 0
        self.all_sprites.update()
        
        return self.get_state(), self.get_flags(action), self.done
        
    def render(self):
        pygame.event.get()
        self.screen.blit(self.background, (0,0))
        self.player.imgrect.left = self.player.rect.centerx*50
        self.player.imgrect.bottom = self.player.rect.bottom*50
        self.screen.blit(self.player.img, (self.player.imgrect))
        for enemy in self.enemy_sprites:
            enemy.imgrect.left = enemy.rect.centerx*50
            enemy.imgrect.bottom = enemy.rect.bottom*50
            self.screen.blit(enemy.img, (enemy.imgrect))
        pygame.display.flip()

    def quit(self):
        pygame.quit()

