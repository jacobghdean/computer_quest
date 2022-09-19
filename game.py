# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:56:27 2021

@author: jacob
"""

import pygame
import time
import sys
from random import *
import pickle

from data import *
from sprites import *
from setup import *


class Game:
    def __init__(self):        
      
        # Initialising the timer
        self.time_limit=TIME_LIMIT # Sets the time limit for the game
        self.elapsed_time=0
        self.remaining_time=self.time_limit
        
        # Initialising the type of screen being displayed
        self.slide="menu" # Ensures the game starts on the 'menu screen'

        self.index = 0 # For navigating the menu options
        self.selection = False # For selecting a menu option

        self.name = "" # Storing player name for saving high scores
        
    # Methods for performing specific actions
        
    def show_time(self): # This method will update the timer in each frame
        self.elapsed_time=time.time()-self.start_time # Finds the difference in UNIX time now versus upon starting the game 
        self.remaining_time=self.time_limit-int(self.elapsed_time) # We want a whole number of seconds to be displayed which is why 'elapsed time' is converted to an integer
        self.minutes=self.remaining_time//60 # Finds the whole number of minutes remaining
        self.seconds=self.remaining_time%60 # Finds the remainder from the previous line in seconds
        self.countdown=futura_large.render(f"{self.minutes} min {self.seconds} sec",False,(255,255,255)) # Renders the time remaining in a textual format with anti-aliasing off and in a white colour
        screen.blit(self.countdown,(0,0)) # Displays the time remaining in the top left of the screen
    
    def show_balance(self): # This method will update the monetary balance in each frame
        self.info=futura_large.render(f"£{self.p.balance}",False,(255,255,255)) # Render the player's balance
        screen.blit(self.info,(850,0)) # Print it onto the screen
        
    def show_score(self):
        self.info=futura_large.render(f"{self.p.points} pts",False,(255,255,255))
        screen.blit(self.info,(440,0))
    
    
    def gamemap(self): # This method will render the full game map, including items, walls, players, enemies, and floors
        for row in range(0,len(GAMEMAP)): # Note that the first and last rows and columns in the game map are reserved for the (literal) walls
            for column in range(0,len(GAMEMAP[row])):
                if row not in [0,len(GAMEMAP)-1] and column not in [0,len(GAMEMAP[row])-1]: # Since we are using transparency, we do not want floor tiles to spill over the edges of the map
                    Floor(column-X_SHIFT,row-Y_SHIFT) # There are no interactions involving floors, so there is no harm in rendering floor on game tiles underneath the other objects
                if GAMEMAP[row][column]=="A": # Larger objects occupy multiple tiles, so this line is necessary to prevent PC components from spawning on top of them
                    pass

                elif GAMEMAP[row][column]=="E": # Renders a moving enemy
                    Enemy(column - X_SHIFT, row - Y_SHIFT)
                elif GAMEMAP[row][column]=="E2": # Renders a stationary enemy
                    Enemy2(column - X_SHIFT, row - Y_SHIFT)
                elif GAMEMAP[row][column]!=".": # This conditional will evaluate as true when objects needs to be placed on a tile (represented by an integer in the game map)
                    index=GAMEMAP[row][column] # Records the number displayed in tile (row,column) on the game map
                    Wall(column-SHIFTS[index][0],row-SHIFTS[index][1],index) # Generates a 'wall' sprite of the correct type in tile (row,column) - note that the shifts are needed so that pygame initially displays the correct part of the map

                else:
                    chance=randint(1,COMPONENT_RARITY)
                    if chance==1: # For every empty tile, we randomly generate a number, and if that number is one, we place a PC component in that tile
                        variety=list(CATALOGUE.keys())[randint(0,9)] # Randomly selects a type of component to go into the chosen tile
                        tier=randint(0, len(list(CATALOGUE.values())[0][0])-1) # Randomly selects the level of the component, ranging from 'budget' to 'elite'
                        lb_price=CATALOGUE[variety][1][tier][0] # These lines will store the upper and lower bounds of price and points for a component of the given variety and tier
                        ub_price=CATALOGUE[variety][1][tier][1]
                        lb_points=CATALOGUE[variety][2][tier][0]
                        ub_points=CATALOGUE[variety][2][tier][1]
                        Component(column-X_SHIFT,row-Y_SHIFT,variety,CATALOGUE[variety][0][tier],randint(lb_price,ub_price),randint(lb_points,ub_points)) # Generate a component with price and points randomly between the upper and lower bounds
                if GAMEMAP[row][column] in CHECKOUTS:
                    Checkout(column-X_SHIFT,row-Y_SHIFT) # The checkout till will already be created as a sprite of 'Wall' class, but we want to overlay an invisible sprite of 'Checkout' class in order to give extra functionality
        self.p=Player(PLAYER_X,PLAYER_Y) # Spawn the player in a predetermined location and store the player sprite under the attribute 'p' so that the player data can be easily accessed later

    def reset(self): # This method will empty all the sprite groups, reset the timer, and then repopulate the game map and hence recreate all sprites in their original positions
        self.slide="playing" # Switch to the 'playing' state (so that the new game runs)
        sprites.empty() # Emptying out all sprite groups so that there is no lingering data when we reset the game
        walls.empty()
        floors.empty()
        characters.empty()
        components.empty()
        player_bullets.empty()
        enemy_bullets.empty()
        chests.empty()
        checkouts.empty()
        explosion_group.empty()
        grenade_group.empty()
        ItemBox_group.empty()
        enemies.empty()
        player_slash.empty()
        enemy_slash.empty()


        self.start_time=time.time() # By resetting the start time, when we call 'show_time', 'elapsed time' will go back to zero and 'remaining time' will go back to 'time limit'
        self.show_time() # We need to call this here so that 'remaining time' gets reset to 'time limit' (otherwise 'remaining time' stays as 0 and the new game immediately ends)
        self.gamemap() # Generate the new game map along with the new player

    # Methods for controlling the game loop while on the menu screen
    
    def event_loop_menu(self): # This method will trigger the event loop every frame when we are on the menu screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Checks if the player is pressing 'down'
                    pygame.mixer.find_channel(True).play(select3_music)

                    if self.index < 2:
                        self.index += 1 # If you are not at the end of the menu, add one to your selection
                    else:
                        self.index = 0 # Otherwise go to the top
                if event.key == pygame.K_UP:  # Checks if the player is pressing 'up'
                    pygame.mixer.find_channel(True).play(select3_music)
                    if self.index > 0:
                        self.index -= 1 # If you are not at the start of the menu, add one to your selection
                    else:
                        self.index = 2 # Otherwise go to the bottom

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # If player presses return, select the option the cursor is on
                    pygame.mixer.find_channel(True).play(select_music)
                    self.selection = True

            if event.type == pygame.QUIT: # Regular code to quit python properly
                pygame.quit()
                sys.exit()

    def menu_refresh(self): # This method will run every frame when we are on the menu screen
        pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Setting background image on each frame
        screen.blit(bg_img, (0, 0))

        screen.blit(title_img, (75, 120)) # Layer title on background
        self.cursor = pygame.Surface([10, 10])
        self.cursor.fill((255, 255, 255))
        self.text1 = menu_font.render("Start Game", False, (255, 255, 255)) # These are the three options on the main menu
        self.text2 = menu_font.render("Instructions", False, (255, 255, 255))
        self.text3 = menu_font.render("Leaderboard", False, (255, 255, 255))
        screen.blits([(self.cursor, (325, 315 + self.index * 100)), (self.text1, (350, 295)), (self.text2, (350, 395)),
                      (self.text3, (350, 495))]) # Print the options plus the cursor (dependent on the value of self.index)
        if self.selection == True:
            self.slide = NAVIGATION[self.index] # Move to the new slide you select
            if NAVIGATION[self.index]=='playing': # Only start the timer when you go to the 'playing' screen
                self.start_time=time.time() # Gets the current time in UNIX time
            self.selection = False
            
    # Methods for controlling the game loop while on the instructions screen       
    
    def event_loop_instructions(self): # This method will trigger the event loop for every frame we are in the instructions screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # SPACE returns you to the main menu
                    pygame.mixer.find_channel(True).play(select_music)
                    self.slide = "menu"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def instructions_refresh(self): # This method will trigger the rest of the game loop for every frame we are in the instructions screen
        screen.fill((0, 0, 0)) # Black screen resets each frame visually
        self.result = option_font.render(f"Instructions", False, (255, 255, 255))
        screen.blit(self.result, (230, 20))
        self.result = medium_font.render(f"Press SPACE to go back to the menu", False, (255, 255, 255))
        screen.blit(self.result, (600, 650))

        self.t1 = l_font.render(f"Controls:", False, (255, 255, 255))
        screen.blit(self.t1, (100, 175))
        self.t4 = l_font.render(f"Objective:", False, (255, 255, 255))
        screen.blit(self.t4, (500, 175))
        self.t2 = small_font.render(f"Player:", False, (255, 255, 255))
        screen.blit(self.t2, (100, 250))
        self.t3 = small_font.render(f"Weapons:", False, (255, 255, 255))
        screen.blit(self.t3, (100, 380))
        self.t5 = small_font.render(f"Basket:", False, (255, 255, 255))
        screen.blit(self.t5, (100, 480))
        self.t6 = small_font.render(f"Checkout:", False, (255, 255, 255))
        screen.blit(self.t6, (100, 580))

        self.s1 = small_font.render(f"W - UP", False, (255, 255, 255))
        self.s2 = small_font.render(f"S - DOWN", False, (255, 255, 255))
        self.s3 = small_font.render(f"A - LEFT ", False, (255, 255, 255))
        self.s4 = small_font.render(f"D - RIGHT", False, (255, 255, 255))
        self.s5 = small_font.render(f"J - GRENADE", False, (255, 255, 255))
        self.s6 = small_font.render(f"SPACE - SHOOT", False, (255, 255, 255))
        self.s7 = small_font.render(f"K - KNIFE", False, (255, 255, 255))
        self.s8 = small_font.render(f"ENTER - BASKET", False, (255, 255, 255))
        self.s9 = small_font.render(f"BACKSPACE - DELETE ITEMS", False, (255, 255, 255))
        self.s19 = small_font.render(f"UP & DOWN - NAVIGATE BASKET", False, (255, 255, 255))
        self.s20 = small_font.render(f"SPACE - PURCHASE ITEMS", False, (255, 255, 255))  
        self.s21 = small_font.render(f"LEFT & RIGHT - NAVIGATE CHECKOUT", False, (255, 255, 255)) 
        self.s22 = small_font.render(f"ENTER - MAKE DECISION", False, (255, 255, 255))
        
        self.s10 = small_font.render("Your goal is to build a brand new gaming PC,", False, (255, 255, 255))
        self.s11 = small_font.render("however the pandemic has caused component shortages.", False, (255, 255, 255))
        self.s12 = small_font.render("So you are only allowed 5 minutes in the shop", False, (255, 255, 255))
        self.s13 = small_font.render("and you have to literally kill the competition!", False, (255, 255, 255))
        
        self.s14 = small_font.render("Collect all 10 types of components in the shop", False, (255, 255, 255))
        self.s15 = small_font.render("to win bonus points for completing your PC.", False, (255, 255, 255))
        self.s16 = small_font.render("Kill the lurking enemies to win even more points", False, (255, 255, 255))
        self.s17 = small_font.render("and gain vital supplies.", False, (255, 255, 255))
        
        self.s18 = small_font.render("Ensure you reach the checkout within the time limit!", False, (255, 255, 255))

        screen.blits([(self.s1, (200, 250)), (self.s2, (200, 280)), (self.s3, (200, 310)), (self.s4, (200, 340)),
                      (self.s5, (200, 380)), (self.s6, (200, 410)), (self.s7, (200, 440)), (self.s8, (200, 480)),
                      (self.s9, (200, 510)), (self.s19, (200, 540)), (self.s20, (200, 580)), (self.s21, (200, 610)),
                      (self.s22, (200, 640)),
                      
                      (self.s10, (500, 250)), (self.s11, (500, 275)), (self.s12, (500, 300)), (self.s13, (500, 325)),
                      (self.s14, (500, 375)), (self.s15, (500, 400)), (self.s16, (500, 425)), (self.s17, (500, 450)),
                      (self.s18, (500, 500))])

    # Methods for controlling the game loop while on the leaderboard screen
    
    def event_loop_leaderboard(self): # This method will trigger the event loop for every frame we are in the leaderboard screen
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # SPACE returns you to the main menu
                    self.slide = "menu"  
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def leaderboard_refresh(self):

        pygame.transform.scale(ld_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(ld_bg_img, (0, 0)) # Resetting each frame visually using the background image
        self.result = option_font.render(f"Leaderboard", False, (255, 255, 255))
        screen.blit(self.result, (200, 20))
        for i, score in enumerate(hs): # We use the index 'i' to set the vertical positions of high scores and we use the iterator 'score' to set the values of high scores
            self.result = l_font.render(f"{score}", False, (255, 255, 255))
            screen.blit(self.result, (600, 175 + 40 * i))

        for x, names in enumerate(hs_name):
            self.result = l_font.render(f"{names}", False, (255, 255, 255))
            screen.blit(self.result, (300, 175 + 40 * x))

        self.result = medium_font.render(f"Press SPACE to go back to the menu", False, (255, 255, 255))
        screen.blit(self.result, (600, 650))
        
    # Methods for controlling the game loop while playing the game
    
    def event_loop_playing(self): # This method will trigger the event loop every frame when we are playing the game
        
        for event in pygame.event.get(): # This is the 'event loop': checks through all the pygame events
            if event.type==pygame.KEYDOWN: # We use the event loop to check for key presses where we need to detect a unique press in a stream of frames
                if event.key==pygame.K_RETURN and not self.p.till: # Provided that the player is not at the checkout, the 'enter' key should toggle the basket menu off and on
                    pygame.mixer.find_channel(True).play(select2_music)
                    self.p.show= not self.p.show
                if self.p.show: # This conditional is used for navigating the basket - we want up and down arrow clicks to only be detected once
                    if event.key==pygame.K_DOWN and self.p.selection<len(self.p.basket)-1:
                        self.p.selection+=1 # 'selection' is an attribute of the player class that records which PC component you may wish to remove from the basket
                    if event.key==pygame.K_UP and self.p.selection>0: # We change this attribute depending on how you navigate the basket
                        self.p.selection-=1
                    if event.key==pygame.K_BACKSPACE: # When you try to remove items from the trolley, we also want this to be recorded only once, which is why we are using the event loop
                        pygame.mixer.find_channel(True).play(delete_music)
                        self.p.deletion=True

                        
                if self.p.till: # This conditional is used for navigating the checkout screen - we want left and right arrow clicks to only be detected once
                    if event.key==pygame.K_LEFT and not self.p.finished: # 'finished' is an attribute of the player class that is recording on the checkout screen whether or not you wish to finish 
                        self.p.finished=True # The player can control whether or not they wish to finish by using the left and right arrows
                    if event.key==pygame.K_RIGHT and self.p.finished:
                        self.p.finished=False
                    if event.key==pygame.K_SPACE: # Space bar is used to show the checkout menu if you are at the till
                        self.p.show=True # We want the player to be able to toggle this menu on and off with a click of the space bar, which is why we need to record unique clicks and hence use the event loop
                        
            if event.type == pygame.QUIT: # Returns true if you click the exit button
                pygame.quit() # The opposite to pygame.init(), closes the pygame engine
                sys.exit() # A method from the 'sys' library - securely breaks out of both the event and game loops            
                
    def playing_refresh(self): # This method will run every frame when we are playing the game
    
        screen.fill((0,0,0)) # For each frame, first reset to an empty black screen so images from the previous frame don't linger
        
        floors.draw(screen) # The draw methods will look for the image and rect (i.e. position) for the sprites in each of the following groups and draw these onto the screen
        walls.draw(screen) # The order in which the draw methods are called is carefully chosen so that the images are layered on top of each other in the right order
        components.draw(screen)
        characters.draw(screen)
        player_bullets.draw(screen)
        enemy_bullets.draw((screen))
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        player_slash.draw(screen)
        enemy_slash.draw(screen)
        enemies.draw(screen)
        ItemBox_group.draw((screen))

        sprites.update() # This 'update' method will call the 'update' methods listed under each class of sprite - we call sprites.update() last because it contains text rendering that needs to be displayed last in each frame
        
        self.show_time() # This updates the timer
        self.show_balance() # This updates the balance
        self.show_score() # Updates the score counter

    # Methods for controlling the game loop while on the game over screen

    def event_loop_endscreen(self):  # This method will trigger the event loop for every frame we are in the game over screen
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.find_channel(True).play(select_music)
                    
                    if self.p.points > hs[9]: # If you get a high score, insert it into the correct position on the leaderboard
                        for i in range(len(hs)):
                            if self.p.points > hs[i]:
                                hs.insert(i, self.p.points) # Add high score
                                hs[:] = hs[:-1] # Remove extra list entry
                                pickle.dump(hs, open("scores.p", "wb")) # Save the updated score leaderboard
                                hs_name.insert(i, self.name) # Add name
                                hs_name[:] = hs_name[:-1] # Remove extra lsit entry
                                pickle.dump(hs_name, open("names.p", "wb")) # Save the updated name leaderboard
                                self.name = "" # Reset the name attribute so that we can use it again
                                break # Once you have reached the first score on the leaderboard that you beat, stop updating the list

                    self.reset() # Resets the game once you click SPACE
                    self.slide = "menu" # Take you back to the menu screen when you click SPACE
                else:
                    alphabet="qwertyuiopasdfghjklzxcvbnm" # Only check for letters when player is entering their name
                    if pygame.key.name(event.key) in alphabet:
                        self.name += pygame.key.name(event.key) # Add the letters the player clicks to their name under their high score
                        self.name = self.name[:10] # Limit name to 10 characters
                    if event.key==pygame.K_BACKSPACE:
                        self.name=self.name[:-1] # BACKSPACE allows you to delete characters from your name

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def endscreen_refresh(self):  # This method will run every frame when we are in the game over screen
    
        pygame.transform.scale(end_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(end_bg_img, (0, 0)) # Load background image every frame
        self.result = medium_font.render(f"Press SPACE to go back to the menu", False, (255, 255, 255))
        screen.blit(self.result, (600, 650))
        if int(self.remaining_time) == 0:  # Print one of three game over messages, either from running out of time or dying or exiting the level from the checkout desk
            self.result = option_font.render(f"You ran out of time!", False, (255, 255, 255))
            screen.blit(self.result, (60, 300))
        elif self.p.alive==False: # Triggers if you die
            self.result = option_font.render(f"You died!", False, (255, 255, 255))
            screen.blit(self.result, (280, 300))
        else: # Triggers if you completed the game
            if self.p.bonus==BONUS: # If you won the bonus by collecting all components
                self.bonus=large_font.render(f"Congrats, you built your PC and won 1000 bonus points!",False,(255,255,255))
                screen.blit(self.bonus,(120,300)) # Print the bonus point message under the regular final score message
                pygame.mixer.find_channel(True).play(win_music)
            else:
                self.bonus=large_font.render(f"No bonus points this time, your PC is incomplete!",False,(255,255,255))
                screen.blit(self.bonus,(120,300))
            self.result = option_font.render(f"Your score is {self.p.points}!", False, (255, 255, 255))
            screen.blit(self.result, (90, 150))
        if self.p.points > hs[9] and self.p.alive and self.remaining_time>0: # If you have a high score, you are still alive, and you haven't run out of time
            self.result = l_font.render(f"NEW HIGH SCORE! Please enter name: {self.name}", False, (255, 255, 255)) # Repeatedly visually update the name as the player enters characters
            screen.blit(self.result, (120, 380))



