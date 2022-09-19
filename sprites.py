# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:29:26 2021

@author: jacob
"""
import math

from setup import *
import random



font = pygame.font.SysFont('Futura', 30)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Player(pygame.sprite.Sprite): # Create a player class that is a subclass of the overall pygame 'Sprite' class
    def __init__(self,x,y):
        super().__init__(sprites,characters) # Automatically adds the 'Player' object to the 'sprites' and 'characters' sprite groups when initialised
        
        self.width=PLAYER_SIZE
        self.height=PLAYER_SIZE
        self.x=TILE_SIZE*x # We want to measure the x and y coordinates in tiles not in pixels (necessary for using loops to generate the game map), so we need to modify values to represent pixels correctly
        self.y=TILE_SIZE*y
                
        self.facing="down" # Makes the player face down initially
        self.pos=[48,0] # 'pos' is measuring the top left point on the player spritesheet from which we would like to cut
        self.count=0 # Will be used in the animation method to cycle between sprites on the spritesheet while the player is moving
        
        # Create surface containing main character image
        
        self.image=pygame.Surface([self.width,self.height]) # Creates a blank pygame surface with dimensions equal to those of the player
        self.image.set_colorkey((0,0,0)) # Any pixels in the player image that are pure black become transparent
        self.image.blit(player_spritesheet,(0,0),(self.pos[0],self.pos[1],self.width,self.height)) # Draws the desired subsection of the player spritesheet onto the pygame surface we created
        
        # Initialise position of player
        
        self.rect=self.image.get_rect() # draws a new rectangle over the surface - used by pygame for positioning the surface on the game display
        self.rect.x=self.x # Insert x and y as rect attributes so that they can used to draw the player in the correct position on the map
        self.rect.y=self.y

        # attributes of player
        self.alive = True  # detect if the player is alive
        self.shoot_cooldown = 0
        self.health = PLAYER_HEALTH  # Players have starting health of 128
        self.max_health = self.health
        self.grenades = STARTING_GRENADES # the number of grenade
        self.ammo = STARTING_AMMO # starting ammo 3
        self.max_ammo = MAX_AMMO
        self.max_grenade = MAX_GRENADE

        # attributes of weapon
        self.shoot_trigger = 0  # detect if shoot is triggered
        self.grenade_trigger = 0  # detect if grenade is triggered
        self.slash_cooldown = 0
        
        # For the wallet
        self.balance=MONEY_LIMIT
        
        # For the score
        self.points=0
        self.bonus=0
        
        # For what you have picked up
        
        self.basket=[]
        self.inside=False
        self.selection=0
        self.deletion=False
        
        self.unique_press=False
        self.cut=False
        
        # for shooting once only
        self.trigger=0
        
        self.till=False
        self.finished=True
        self.show=False
        self.lock=False # player must answer the question from the checkout lady
        self.end=False
        self.first=True
        
    def update(self): # This method will run every frame when we call the sprites.update() in the main game loop - useful for 'Player' methods that need to be executed repeatedly

        self.move() # Check for player movement
        self.animation() # Increment the animation counter to determine which sprite image is displayed
        self.wall_collision() # Call this after the movement method to rectify the position of the player if he ran into a wall
        self.component_collision() # Check if the player has collided with any PC components

        self.lookup() # Checks if your basket is open and if so, displays the contents and allows you to remove items
        self.reveal() # Checks if your mouse is hovering over any PC components, and if so it will display their stats
        #weapon
        if not self.till:
            self.shoot()
            self.grenade()
            self.slash()
        self.StatusBar()
        self.Collision_Enemy2()
        self.finish() # Checks if you are at the checkout, and if so will give you the option of finishing your game

    def move(self):
        if self.lock==False: # When the player is at the checkout, we don't want them to be able to move until they respond to the shopkeeper
            keylist = pygame.key.get_pressed() # Generates a list of all keys where each key is True if pressed and False otherwise
            
            if keylist[pygame.K_a]: # pygame.K_LEFT returns the index of the 'a' key in the 'get_pressed' list, so this statement returns True if and only if the 'a' key is pressed
                self.rect.x-=PLAYER_SPEED # When 'a' is pressed, subtract the distance represented by PLAYER_SPEED from the x position of the player (i.e. move the player left)
                self.facing="left" # Hitting 'a' means the player is facing left
                self.moving=True # Hitting 'a' also means the player is moving
                for sprite in sprites:
                    sprite.rect.x+=PLAYER_SPEED # To keep a centered camera angle, move all sprites in the opposite direction to which the player moved
                    moving_music.play()
                return  # End the method here so that we don't get weird combinations of movements (e.g. left and up)

            if keylist[pygame.K_d]:
                self.rect.x+=PLAYER_SPEED
                self.facing="right"
                self.moving=True
                for sprite in sprites:
                    sprite.rect.x-=PLAYER_SPEED
                    moving_music.play()
                return

            if keylist[pygame.K_w]:
                self.rect.y-=PLAYER_SPEED
                self.facing="up"
                self.moving=True
                for sprite in sprites:
                    sprite.rect.y+=PLAYER_SPEED
                    moving_music.play()
                return

            if keylist[pygame.K_s]:
                self.rect.y+=PLAYER_SPEED
                self.facing="down"
                self.moving=True
                for sprite in sprites:
                    sprite.rect.y-=PLAYER_SPEED
                    moving_music.play()
                return

            
            self.moving=False # If none of the direction keys are pressed, the player must not be moving
    
    def animation(self):
        '''
        The animation method is responsible for facing the enemy towards the player and the movement dynamics when
        they're moving. For each direction it faces, different spritesheet images are called.
        '''
        if self.facing=="left": # If the player is facing left, print the sprites of the player that are also facing left
            if self.moving==False: # If the player is not moving, print the stationary sprite of the player
                self.pos=[48,48]
            else:
                position_list=[[0,48],[48,48],[96,48]] # The full list of left-facing player sprites that we will cycle through to represent animation
                self.pos=position_list[int(self.count)]
                self.count+=0.1 # Changes the value of int(self.count) every 10 frames so that the animations take place at an appropriate speed
                if self.count>=3: # Once 10 frames of the final sprite in the list have been displayed, reset and show the first sprite in the list again
                    self.count=0
                
        if self.facing=="right":
            if self.moving==False:
                self.pos=[48,96]
            else:
                position_list=[[0,96],[48,96],[96,96]]
                self.pos=position_list[int(self.count)]
                self.count+=0.1
                if self.count>=3:
                    self.count=0  
                    
        if self.facing=="up":
            if self.moving==False:
                self.pos=[48,144]
            else:
                position_list=[[0,144],[48,144],[96,144]]
                self.pos=position_list[int(self.count)]
                self.count+=0.1
                if self.count>=3:
                    self.count=0
                    
        if self.facing=="down":
            if self.moving==False:
                self.pos=[48,0]
            else:
                position_list=[[0,0],[48,0],[96,0]]
                self.pos=position_list[int(self.count)]
                self.count+=0.1
                if self.count>=3:
                    self.count=0                
         
        self.image=pygame.Surface([self.width,self.height])
        self.image.set_colorkey((0,0,0))
        self.image.blit(player_spritesheet,(0,0),(self.pos[0],self.pos[1],self.width,self.height)) # Once we have found the sprite image that should be displayed, we blit this onto the screen

    def Collision_Enemy2(self):
        hit_list = pygame.sprite.spritecollide(self, enemies,
                                               False)  # This checks whether the player sprite is inside any of the wall sprites - we include 'False' because we don't want to delete sprite upon collision
        if hit_list:  # True when a collision is taking place between the player and a wall sprite
            if self.facing == "left":  # If the player is facing left, he was trying to move left through a wall
                self.rect.x += PLAYER_SPEED  # Undo the leftward movement by adding back PLAYER_SPEED to the player's 'x' position
                for sprite in sprites:  # When the player is moving, we moved all sprites to keep the camera centered, however if the player is colliding with a wall we no longer want to do this
                    sprite.rect.x -= PLAYER_SPEED  # This will undo the attempt to keep the camera centered (the player is not moving so the camera will be centered anyway)
            if self.facing == "right":
                self.rect.x -= PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.x += PLAYER_SPEED
            if self.facing == "up":
                self.rect.y += PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.y -= PLAYER_SPEED
            if self.facing == "down":
                self.rect.y -= PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.y += PLAYER_SPEED

    def wall_collision(self): # This method prevents the player from walking through walls
        hit_list = pygame.sprite.spritecollide(self,walls,False) # This checks whether the player sprite is inside any of the wall sprites - we include 'False' because we don't want to delete sprite upon collision
        if hit_list: # True when a collision is taking place between the player and a wall sprite
            if self.facing=="left": # If the player is facing left, he was trying to move left through a wall
                self.rect.x+=PLAYER_SPEED # Undo the leftward movement by adding back PLAYER_SPEED to the player's 'x' position
                for sprite in sprites: # When the player is moving, we moved all sprites to keep the camera centered, however if the player is colliding with a wall we no longer want to do this
                    sprite.rect.x-=PLAYER_SPEED # This will undo the attempt to keep the camera centered (the player is not moving so the camera will be centered anyway)
            if self.facing=="right":
                self.rect.x-=PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.x+=PLAYER_SPEED
            if self.facing=="up":
                self.rect.y+=PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.y-=PLAYER_SPEED
            if self.facing=="down":
                self.rect.y-=PLAYER_SPEED
                for sprite in sprites:
                    sprite.rect.y+=PLAYER_SPEED
                    
    def component_collision(self): # This method will allow the player to add PC components to their basket
        if len(self.basket)<=10: # The basket cannot fit more than 11 items
            hit_list = pygame.sprite.spritecollide(self,components,False) # If the player is colliding with a component, delete that component from the map
            if hit_list: # True if the player is colliding with a component

                if self.balance-hit_list[0].price>=0:
                    pygame.mixer.find_channel(True).play(getitem_music)
                    self.points+=hit_list[0].value # Adds the number of points contained by the PC component to your score
                    self.balance-=hit_list[0].price # Subtracts the price of the PC component from your monetary balance
                    self.basket+=[(hit_list[0].name,hit_list[0].price,hit_list[0].value,hit_list[0], # Adds a tuple to your basket representing the PC component data, a spare copy of the component (in case you want to remove it from your basket), and a reference copy of the top left wall position
                                   (walls.sprites()[0].rect.x,walls.sprites()[0].rect.y),hit_list[0].variety)]
                    hit_list[0].kill()
                else:
                    self.warning=giant_font.render("Can't Afford!",False,(255,0,0)) # If you are trying to add an item to your basket but you're out of money, a warning message will be shown
                    screen.blit(self.warning,(270,300))
        elif pygame.sprite.spritecollide(self,components,False): # Don't delete PC component from the map if your basket is full
            self.warning=giant_font.render("Your basket is full!",False,(255,0,0)) # If you are trying to add an item to your basket but your basket is full, a warning message will be shown
            screen.blit(self.warning,(180,300))

    def lookup(self): # This method will allow the player to look inside his basket and remove items
        if self.show and not self.till: # 'show' is the variable that determines whether the basket menu should be showing, its value is controlled from inside the event loop, and if you are at the till, you should not be able to open your basket - this is because the 'enter' key needs to be used for other purposes
            self.outer_box=pygame.Surface([300,360]) # To display the basket menu, we layer a smaller blue box on top of a larger black box to get a framed box
            self.inner_box=pygame.Surface([280,340])
            self.outer_box.fill((0,0,0))
            self.inner_box.fill((0,0,255))
            screen.blits([(self.outer_box,(10,350)),(self.inner_box,(20,360))]) # 'blits' allows us to print multiple objects to the screen in one line of code      
            if len(self.basket)>0: # If the player has PC components in their basket, a smaller grey box is also printed to highlight their text selection
                self.selector_box=pygame.Surface([260,22.5])
                self.selector_box.fill((127,127,127))
                screen.blit(self.selector_box,(30,370+self.selection*30)) # 'self.selection' stores the item that the player is intending to remove from their basket, so the selector box position needs to depend on this variable
            for i in range(len(self.basket)): # Cycle through each item in the player's basket and print the item's stats in the basket menu
                self.info=small_font.render(f"{self.basket[i][0]} £{self.basket[i][1]} {self.basket[i][2]}pts",False,(255,255,255)) 
                screen.blit(self.info,(35,370+i*30)) # We move 30 pixels down every time a new set of item stats needs to be printed - prevents text from layering on top of each other
                
            if self.deletion and len(self.basket)>0: # 'self.deletion' is triggered in the event loop by hitting backspace, and provided that the basket is not empty, the item indexed by 'self.selection' will be deleted
                self.points-=self.basket[self.selection][2] # You lose the points of the PC component if you return it
                self.balance+=self.basket[self.selection][1] # You regain money if you return a PC component
                self.basket[self.selection][3].rect.x+=(walls.sprites()[0].rect.x-self.basket[self.selection][4][0]) # Since the player will have moved from the position where they first picked up the component, we need to add the change in position so that the component is returned to the correct location
                self.basket[self.selection][3].rect.y+=(walls.sprites()[0].rect.y-self.basket[self.selection][4][1]) # We use the top left wall as a reference point to measure how much the player has moved
                components.add(self.basket[self.selection][3]) # Return the component to the sprite group of components and also to the group of all sprites
                sprites.add(self.basket[self.selection][3])
                self.basket.remove(self.basket[self.selection]) # Remove the component from the player's basket
                if self.selection>0: # Prevents selection index from becoming negative
                    self.selection-=1 # Prevent a high selection index from remaining after deletion that would cause an error if you tried to delete again
                self.deletion=False # Immediately makes 'self.deletion' False after one frame to prevent multiple items from being removed from the basket at once
                
    def reveal(self): # This method will allow the player to check the stats of PC components lying around by hovering the mouse over them
        for sprite in components:
            if sprite.rect.collidepoint(pygame.mouse.get_pos()): # Checks whether the mouse is hovering over any of the PC components that are scattered across the map                
                self.outer_box=pygame.Surface([175,70]) # We now create a similar framed box as for the basket menu to display the stats of components when you hover the mouse over them
                self.inner_box=pygame.Surface([165,60])
                self.outer_box.fill((0,0,0))
                self.inner_box.fill((0,0,255))
                screen.blits([(self.outer_box,(sprite.rect.x+50,sprite.rect.y-50)),(self.inner_box,(sprite.rect.x+55,sprite.rect.y-45))]) # The extra numbers prevent the framed box from appearing on top of the components
                self.info1=small_font.render(f"{sprite.name}",False,(255,255,255)) # Display the stats of the component inside the box in small font
                self.info2=small_font.render(f"£{sprite.price}                    {sprite.value}pts",False,(255,255,255))
                screen.blits([(self.info1,(sprite.rect.x+60,sprite.rect.y-40)),(self.info2,(sprite.rect.x+60,sprite.rect.y-40+30))])
                #print((sprite.name,sprite.price,sprite.value))

    def StatusBar(self):
        '''
        Status bar for both the players bullet and grenade ammunition. For each Ammunition status bar it calls the
        sprite image of the ammunition for a visual representation when you're in the game.

        '''
        draw_text('HP: ', font, WHITE, 10, 40)
        health_bar = HealthBar(10+40, 40, self.health, self.max_health)
        health_bar.draw(self.health)

        # show ammo
        draw_text('AMMO: ', font, WHITE, 10, 75)
        for x in range(self.ammo):
            screen.blit(bullet_img, (90 + (x * 20), 75))
        # show grenades
        draw_text('GRENADES: ', font, WHITE, 10, 115)
        for x in range(self.grenades):
            screen.blit(grenade_img, (135 + (x * 30), 109))
        if self.health<=0:
            self.alive=False
            pygame.mixer.find_channel(True).play(death2_music)

    def slash(self):
        # update cooldown
        if self.slash_cooldown > 0:
            self.slash_cooldown -= 1
        keylist = pygame.key.get_pressed()
        # I'm sure there is a more efficient way of checking if someone clicked enter

        if keylist[pygame.K_k] and \
                self.slash_cooldown == 0:
            self.slash_cooldown = 20

            if self.facing == 'up':
                Slash_Player(self.rect.centerx, self.rect.centery,
                      'up')  # does this create multiple bullets since the space input is recorded many times
                pygame.mixer.find_channel(True).play(slash_music)
            elif self.facing == 'down':  # do the coordinates work with self.x or only self.rect.x, check with player position translation as well
                Slash_Player(self.rect.centerx, self.rect.centery,
                      'down')  # does this create multiple bullets since the space input is recorded many times
                pygame.mixer.find_channel(True).play(slash_music)
            elif self.facing == 'left':
                Slash_Player(self.rect.centerx, self.rect.centery,
                      'left')  # does this create multiple bullets since the space input is recorded many times
                pygame.mixer.find_channel(True).play(slash_music)
            elif self.facing == 'right':
                Slash_Player(self.rect.centerx, self.rect.centery,
                      'right')  # does this create multiple bullets since the space input is recorded many times
                pygame.mixer.find_channel(True).play(slash_music)
            self.shoot_trigger = 1

    def shoot(self):
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        keylist = pygame.key.get_pressed()
        if not keylist[pygame.K_SPACE]:
            self.shoot_trigger = 0
        # I'm sure there is a more efficient way of checking if someone clicked enter

        if keylist[pygame.K_SPACE] and self.shoot_trigger == 0 and \
                self.shoot_cooldown == 0 and self.ammo >0:
            self.shoot_cooldown = 20

            if self.facing == 'up':
                Bullet_Player(self.rect.centerx, self.rect.centery,'up')  # does this create multiple bullets since the space input is recorded many times
                self.ammo -= 1
                pygame.mixer.find_channel(True).play(bullet_music)
            elif self.facing == 'down':  # do the coordinates work with self.x or only self.rect.x, check with player position translation as well
                Bullet_Player(self.rect.centerx, self.rect.centery,'down')  # does this create multiple bullets since the space input is recorded many times
                self.ammo -= 1
                pygame.mixer.find_channel(True).play(bullet_music)
            elif self.facing == 'left':
                Bullet_Player(self.rect.centerx, self.rect.centery,'left')  # does this create multiple bullets since the space input is recorded many times
                self.ammo -= 1
                pygame.mixer.find_channel(True).play(bullet_music)
            elif self.facing == 'right':
                Bullet_Player(self.rect.centerx, self.rect.centery,'right')  # does this create multiple bullets since the space input is recorded many times
                self.ammo -= 1
                pygame.mixer.find_channel(True).play(bullet_music)
            self.shoot_trigger = 1

    def grenade(self):
        keylist = pygame.key.get_pressed()
        if not keylist[pygame.K_j]:
            self.grenade_trigger = 0
        # I'm sure there is a more efficient way of checking if someone clicked enter

        if keylist[pygame.K_j] and self.grenade_trigger == 0 \
                and self.grenades >0:
            if self.facing == 'up':
                Grenade(self.rect.centerx, self.rect.centery - 0.5 * self.rect.size[0],
                        'up')  # does this create multiple bullets since the space input is recorded many times
                self.grenades -= 1
                pygame.mixer.find_channel(True).play(throw_music)
            elif self.facing == 'down':  # do the coordinates work with self.x or only self.rect.x, check with player position translation as well
                Grenade(self.rect.centerx, self.rect.centery + 0.5 * self.rect.size[0],
                        'down')  # does this create multiple bullets since the space input is recorded many times
                self.grenades -= 1
                pygame.mixer.find_channel(True).play(throw_music)
            elif self.facing == 'left':
                Grenade(self.rect.centerx - 0.5 * self.rect.size[0], self.rect.centery,
                        'left')  # does this create multiple bullets since the space input is recorded many times
                self.grenades -= 1
                pygame.mixer.find_channel(True).play(throw_music)
            elif self.facing == 'right':
                Grenade(self.rect.centerx + 0.5 * self.rect.size[0], self.rect.centery,
                        'right')  # does this create multiple bullets since the space input is recorded many times
                self.grenades -= 1
                pygame.mixer.find_channel(True).play(throw_music)
            self.grenade_trigger = 1
                

        
    def finish(self): # This method will display the checkout menu and allow you to finish the game if you are at the till and press space bar
        if checkouts.sprites()[0].rect.y-self.rect.y<=80 and 0<=self.rect.x-checkouts.sprites()[0].rect.x<=180: # Condition to check whether you are at the till
            if self.first: # If you have your basket menu open and walk to the checkout, we don't want the checkout message to automatically appear (you should always have to press space bar)
                self.first=False # So 'self.first' is a way of tracking the first frame you are at the checkout, and always sets 'self.show' to first so that you have to press space bar to receive the checkout message
                self.show=False
                
            self.till=True # Records that you are at the till - this turns on the left and right arrow controls in the event loop and allows the basket to be disabled
            if self.show: # True when you have pressed space to open the checkout menu
                keylist = pygame.key.get_pressed()
                self.lock=True # This variable will be used to prevent you from moving when at the till with the checkout menu open (you have to answer the checkout question before continuing)
                self.outer_box=pygame.Surface([600,120]) # We now generate a framed text box to contain the checkout question
                self.inner_box=pygame.Surface([580,100])
                self.outer_box.fill((137,137,137))
                self.inner_box.fill((0,0,255))
                screen.blits([(self.outer_box,(180,580)),(self.inner_box,(190,590))])
                
                
                if self.finished==True: # 'self.finished' will track whether you are currently selecting 'yes' or 'no' to ending the game
                    self.selector_box=pygame.Surface([60,40]) # Draw the selector box to the left to go around 'Yes' if 'finished' is set to True
                    self.selector_box.fill((0,255,0))
                    screen.blit(self.selector_box,(195,645))
                    if keylist[pygame.K_RETURN]:# If you hit 'enter' while selecting 'Yes', the game should end  
                        shopping_list=list(CATALOGUE.keys())
                        pygame.mixer.find_channel(True).play(select_music)
                        for item in self.basket: # If you found all varieties of components then your shopping list should be empty after the for loop finishes running
                            if item[5] in shopping_list: # 'item[5] gets the variety of each component in the basket'
                                shopping_list.remove(item[5])
                        if shopping_list==[]: # If you found all varieties of components then your shopping list should be empty after the for loop finishes running
                            self.bonus=BONUS
                            self.points+=self.bonus
                        else:
                            self.bonus=0 # If 'shopping_list' is not empty then this means that you did not find all components
                        self.end=True
                    
                if self.finished==False:               
                    self.selector_box=pygame.Surface([60,40]) # Draw the selector box to the right to go around 'No' if 'finished' is set to False
                    self.selector_box.fill((255,0,0))
                    screen.blit(self.selector_box,(645,645))
                    if keylist[pygame.K_RETURN]: # If you hit 'enter' while selecting 'No', the checkout message should disappear and you should be able to move and continue the game
                        pygame.mixer.find_channel(True).play(select_music)
                        self.show=False
                        self.lock=False
                    
                    
                self.info1=medium_font.render("Have you finished shopping?",False,(255,255,255)) # Writes the checkout message on top of the framed box
                self.info2=medium_font.render("YES",False,(255,255,255))
                self.info3=medium_font.render("NO",False,(255,255,255))
                screen.blits([(self.info1,(200,600)),(self.info2,(200,650)),(self.info3,(650,650))])
                # self.info2=self.font_small.render(f"£{sprite.price}                    {sprite.value}pts",False,(255,255,255))
                
        else:
            self.till=False # If you are no longer in the checkout zone, record this and allow 'self.first' to be true in case you wish to enter the checkout zone again
            self.first=True

'''
ENEMY 1. 
The Enemy class is the "Boss" enemy. It follows the player around the map and has the ability to shoot once in while. 
There are only a couple of these enemies around the map and they are considered the map "Bosses".
'''
class Enemy(pygame.sprite.Sprite):  # inherit from the sprite class to make our main character a sprite
    def __init__(self, x, y):
        super().__init__(sprites, enemies)  # makes player class a sprite and adds it to the sprites list

        self.x = TILE_SIZE * x  # we want to measure the x and y coordinates in tiles not in pixels, so we need to modify our x in tiles to represent pixels correctly
        self.y = TILE_SIZE * y

        # x change and y change variables for movement
        #self.x_change = 0
        #self.y_change = 0

        self.facing = "down" # Starts the game facing downwards
        self.pos = [48, 0]
        self.count = 0

        # TILESIZE = 64. Therefore make player a little smaller than 64 by 64
        # Blit - transfer contents of player onto gamemap surface
        self.image = pygame.Surface([48, 48])  # create a blank surface with area equal to TILE_SIZE
        self.image.set_colorkey((0, 0, 0))  # make any pixels in the player picture that are pure black
        self.image.blit(enemy1_spritesheet, (0, 0),
                        (self.pos[0], self.pos[1], 48, 48))

        # Position of enemy
        self.rect = self.image.get_rect()
        self.rect.x = self.x  # insert x and y as rect attributes so that they can be easily accessed and used in rect methods
        self.rect.y = self.y

        # Transition for the frame rate
        self.transition=0

        self.shoot_cooldown = 0
        self.health = ENEMY_HEALTH  # enemies have 100 health
        self.max_health = self.health
        self.slash_cooldown = 0 # This enemy only has slashing ability.

    def update(self): # This update method will run when we call the sprites.update() in the main program
        for enemy in enemies:
            if enemy.health <=0: # If the enemy health falls below zero
                enemy.kill() # Remove the enemy sprite off the map.
                pygame.mixer.find_channel(True).play(death1_music) # and play the enemy death sound
                characters.sprites()[0].points+=100 # Give 100 points to the player for killing an enemy
                mylist = ["Health", "Ammo", "Grenade"]

                random_box = random.choice(mylist) # Then pick a random perk for the player to pick up when they kill an enemy
                ItemBox(random_box, enemy.rect.x, enemy.rect.y)


        if self.health > 0:
            self.healthbar() # If player health is positive then update the health bar
        self.enemy_slash()
        self.enemy_collision()
        self.enemy_movement()
        self.enemy_animation()

    def healthbar(self):

        self.bar = pygame.Surface([104, 20])
        self.bar2 = pygame.Surface([100, 16])
        self.bar3 = pygame.Surface([self.max_health - self.health, 16])
        self.bar.fill((0, 0, 0))
        self.bar2.fill((0, 255, 0))
        self.bar3.fill((255, 0, 0))
        screen.blits([(self.bar, (self.rect.x - 10, self.rect.y - 30)),
                      (self.bar2, (self.rect.x - 8, self.rect.y - 28)),
                      (self.bar3, (self.rect.x - 8, self.rect.y - 28)),
                      ])

    def enemy_animation(self):
        '''
        This method controls the movement dynamics and facing direction of the Boss enemy.
        '''
        if self.facing == "left":
            position_list = [[0, 48], [48, 48], [96, 48]]
            self.pos = position_list[int(self.count)]
            self.count += 0.1
            if self.count >= 3:  # doesn't work with self.count==3 because of something weird with floats having a small extra decimal component
                self.count = 0

        if self.facing == "right":

            position_list = [[0, 96], [48, 96], [96, 96]]
            self.pos = position_list[int(self.count)]
            self.count += 0.1
            if self.count >= 3:
                self.count = 0

        if self.facing == "up":

            position_list = [[0, 144], [48, 144], [96, 144]]
            self.pos = position_list[int(self.count)]
            self.count += 0.1
            if self.count >= 3:
                self.count = 0

        if self.facing == "down":

            position_list = [[0, 0], [48, 0], [96, 0]]
            self.pos = position_list[int(self.count)]
            self.count += 0.1
            if self.count >= 3:
                self.count = 0

        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(enemy1_spritesheet, (0, 0), (self.pos[0], self.pos[1], 48, 48))

    def enemy_movement(self):
        '''
        This movement method continually tracks the relative position of the player to the enemy so it can follow
        the player around the map. The enemy decides randomly whether to move horizontally first or verticlaly first but
        will try to find the fastest path.
        '''
        player_xpos = characters.sprites()[0].rect.x
        player_ypos = characters.sprites()[0].rect.y # Calculate X and Y positions of main player
        diff_x = player_xpos - self.rect.x
        diff_y = player_ypos - self.rect.y # finding difference in player and enemy x and y positions
        ls = []
        if -300 < diff_x < 300 and -300 < diff_y < 300: # If players are in the range of the walking enemy (Boss enemy)
            if diff_x > 0: # If the player is to the right of the enemy
                ls += ['right'] # Append list with facing right to be fed into the random facing argument
                # Player is right of enemy

            if diff_x < 0:  # was > -1
                ls += ['left']
                # Player is left of the enemy

            if diff_y < 0:  # was 1
                ls += ['up']
                # Player is above enemy

            if diff_y > 0:  # was > -1
                ls += ['down']
                # Player is below enemy

            # Adjusting the frame rate so that the enemy changes direction every 40 frames (4/0.1)=40
            self.transition+=0.1
            if self.transition>=4:
                rand = random.randint(0, len(ls)-1)
                self.facing = ls[rand]
                self.transition=0

            # If statements below change the facing direction of the enemy to always face the main character.
            if self.facing=='right' and diff_x>50:  # diff_x > 50 makes sure the enemy doesn't move inside the player.
                # Player is right of enemy
                self.rect.x += ENEMY_SPEED
                self.facing = "right"  # So we face the enemy to the right since we want the enemy to face the player.
                self.moving = True
            else:
                self.moving = False

            if self.facing=='left' and diff_x<-50:
                # Player is left of the enemy
                self.rect.x -= ENEMY_SPEED
                self.facing = "left"
                self.moving = True
            else:
                self.moving = False

            if self.facing=='up' and diff_y<-50:
                # Player is above enemy
                self.rect.y -= ENEMY_SPEED
                self.facing = "up"
                self.moving = True
            else:
                self.moving = False
            if self.facing=='down' and diff_y>50:
                # Player is below enemy
                self.rect.y += ENEMY_SPEED
                self.facing = 'down'
                self.moving = True
            else:
                self.moving = False

    # Slash ability for the moving enemy (Boss enemy)
    def enemy_slash(self):
        if self.slash_cooldown > 0:
            self.slash_cooldown -= 1
        # I'm sure there is a more efficient way of checking if someone clicked enter
        delta_x = characters.sprites()[0].rect.x - self.rect.x
        delta_y = characters.sprites()[0].rect.y - self.rect.y # Difference in player and enemy position to detect slashing range


        if -70 <delta_x <70 and -70 < delta_y < 70: # Minimum distances for enemy to use slashing ability

            if self.slash_cooldown == 0: # Resetting the cooldown if it reaches zero so it doesn't fight too fast
                self.slash_cooldown = 40

                if delta_y < 0: # If the player is above the enemy
                    Slash_Enemy(self.rect.centerx, self.rect.centery,
                          'up')
                pygame.mixer.find_channel(True).play(slash_music)
                if delta_y > 0: # If the player is below the enemy
                    Slash_Enemy(self.rect.centerx, self.rect.centery,
                          'down')
                    pygame.mixer.find_channel(True).play(slash_music)
                if delta_x < 0: # If the player is to the left of the enemy
                    Slash_Enemy(self.rect.centerx, self.rect.centery,
                          'left')
                pygame.mixer.find_channel(True).play(slash_music)
                if delta_x > 0: # If the player is to the right of the enemy
                    Slash_Enemy(self.rect.centerx, self.rect.centery,
                          'right')
                    pygame.mixer.find_channel(True).play(slash_music)

    def enemy_collision(self):# Enemy collision for colliding interaction with walls and main character
        hit_list_walls = pygame.sprite.spritecollide(self,walls,False)
        hit_list_player = pygame.sprite.spritecollide(self, characters, False)# spritecollide() is an inherited method that checks whether one rectangle (i.e. player sprite itself) is inside another rectangle (i.e. wall sprite) and we include 'False' because we don't want to delete sprite along collision
        if hit_list_player or hit_list_walls: # True when a collision is taking place between the player and an element in the wall group of sprites
            if self.facing=="left":
                self.rect.x+=ENEMY_SPEED # undo the leftward movement by adding back PLAYER_SPEED
            if self.facing=="right":
                self.rect.x-=ENEMY_SPEED
            if self.facing=="up":
                self.rect.y+=ENEMY_SPEED
            if self.facing=="down":
                self.rect.y-=ENEMY_SPEED


'''
Enemy 2 is a stationary enemy that faces the player and shoots when it comes into close proximity. 
'''
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(sprites, enemies)  # makes player class a sprite and adds it to the sprites list

        self.x = TILE_SIZE * x  # we want to measure the x and y coordinates in tiles not in pixels, so we need to modify our x in tiles to represent pixels correctly
        self.y = TILE_SIZE * y

        self.facing = 'down'
        self.pos = [48, 0]

        # TILESIZE = 64. Therefore make player a little smaller than 64 by 64
        # Blit - transfer contents of player onto gamemap surface
        self.image = pygame.Surface([48, 48])  # create a blank surface with area equal to TILE_SIZE
        self.image.set_colorkey((0, 0, 0))  # make any pixels in the player picture that are pure black
        self.image.blit(enemy2_spritesheet, (0, 0),
                        (self.pos[0], self.pos[1], 48, 48))

        # Position of enemy
        self.rect = self.image.get_rect()
        self.rect.x = self.x  # insert x and y as rect attributes so that they can be easily accessed and used in rect methods
        self.rect.y = self.y


        self.shoot_cooldown = 0
        self.health = ENEMY_HEALTH  # player have 100 health
        self.max_health = self.health

        self.shoot_trigger = 0  # This enemy only has a shooting ability

    # Get Enemy 3 to face the player so it can shoot

    def update(self):
        for enemy in enemies: # Same logic as the Boss enemy update function
            if enemy.health <=0:
                enemy.kill() # Remove the enemy sprite if health falls below zero
                pygame.mixer.find_channel(True).play(death1_music)
                characters.sprites()[0].points += 100


                random_box = random.choice(ITEM_LIST) # Spawn random perk for the main character when the enemy dies
                ItemBox(random_box, enemy.rect.x, enemy.rect.y)

        if self.health > 0:
            self.healthbar() # Otherwise if health is still positive, update it.

        self.shoot()
        self.face_player()

    def healthbar(self):
        # Same logic as the boss enemey health bar
        self.bar = pygame.Surface([104, 20])
        self.bar2 = pygame.Surface([100, 16])
        self.bar3 = pygame.Surface([self.max_health - self.health, 16])
        self.bar.fill((0, 0, 0))
        self.bar2.fill((0, 255, 0))
        self.bar3.fill((255, 0, 0))
        screen.blits([(self.bar, (self.rect.x - 10, self.rect.y - 30)),
                      (self.bar2, (self.rect.x - 8, self.rect.y - 28)),
                      (self.bar3, (self.rect.x - 8, self.rect.y - 28)),
                      ])

    def shoot(self):
        '''
        Creating a specific shooting function for this type of enemy
        The enemy can shoot in any direction by constantly shooting towards the main players position when it gets
        within a certain radius of the enemy.
        '''
        player_xpos = characters.sprites()[0].rect.centerx
        player_ypos = characters.sprites()[0].rect.centery
        delta_x = player_xpos - self.rect.centerx
        delta_y = player_ypos - self.rect.centery
        radians = math.atan2(delta_x, delta_y)

        if -250 < delta_x < 250 and -250 < delta_y < 250: # Determining Stationary enemy shooting range
            if radians < math.pi/2: # Converting degrees to radians so we can use sin and cosine to calculate shooting trajectory
                d_final = radians + 3*math.pi/2
            else:
                d_final = radians-math.pi/2

            bullet_x = BULLET_SPEED * math.cos(d_final) # X speed of bullet
            bullet_y = -BULLET_SPEED * math.sin(d_final) # Y speed of bullet

            if self.shoot_cooldown > 0: # Adjusting shooting framerate
                self.shoot_cooldown -= 1 # Choosing how fast we allow another shot

            if self.shoot_cooldown == 0:
                self.shoot_cooldown = random.randrange(20, 100) # Randomising shooting pattern of Enemy2
                Bullet_Enemy(self.rect.centerx, self.rect.centery, bullet_x, bullet_y) # Creating a bullet
                pygame.mixer.find_channel(True).play(bullet_music) # Bullet sound FX

    def face_player(self): # Enemy faces player when shooting.
        delta_x = characters.sprites()[0].rect.x - self.rect.x
        delta_y = characters.sprites()[0].rect.y - self.rect.y
        # Try and except method because when player is in vertical plane of enemy delta_y/delta_x is dividing by zero.
        try:
            if -1< (delta_y/delta_x) <1 and delta_x >0: # Player to the right of the enemy
                self.pos = [48, 96]

            if -1< (delta_y/delta_x) <1 and delta_x <0: # Player to the left of the enemy
                self.pos = [48, 48]

            if ((delta_y/delta_x) >1 or (delta_y/delta_x) < -1) and delta_y <0: # Player above the enemy
                self.pos = [48, 144]

            if ((delta_y/delta_x) >1 or (delta_y/delta_x) < -1) and delta_y >0: # Below
                self.pos = [48, 0]
        except ZeroDivisionError: # Catch the error and so we give the y deltas manually
            if delta_y >0:
                self.pos = [48, 0]
            elif delta_y < 0:
                self.pos = [48, 144]

        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(enemy2_spritesheet, (0, 0), (self.pos[0], self.pos[1], 48, 48))

class Wall(pygame.sprite.Sprite): # Creates a Wall class that is a subclass of the overall Sprite class (note that furniture is also represented by this class)
    def __init__(self,x,y,style): # 'style' is an attribute that represents the type of wall to be created (there are 60 different types of wall in total) 
        super().__init__(sprites,walls) # When a 'wall' sprite is initialised, add this to the group of wall sprites and the group of all sprites

        self.x=TILE_SIZE*x
        self.y=TILE_SIZE*y
        
        self.style=style

        self.image=pygame.Surface(SURFACES[self.style]) # 'SURFACES' is a list containing the dimensions of each type of wall, we use 'self.style' to select the correct entry
        self.image.set_colorkey((0,0,0))
        self.image.blit(object_spritesheet,(0,0),POSITIONS[self.style]) # 'POSITIONS' is a list containing the part of the object spritesheet we would like to cut out, we use 'self.style' to select the correct coordinates
        
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Floor(pygame.sprite.Sprite): # Creates a Floor class that is also a type of sprite
    def __init__(self,x,y):
        super().__init__(sprites,floors) # Adds Floor objects to the 'sprites' and 'floors' sprite groups

        self.x=TILE_SIZE*x
        self.y=TILE_SIZE*y
        
        self.image=pygame.Surface([TILE_SIZE,TILE_SIZE])
        self.image.blit(object_spritesheet,(0,0),(576,512,TILE_SIZE,TILE_SIZE)) # The floor image is also contained in the object spritesheet and we cut these out here
        
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
class Component(pygame.sprite.Sprite): # Creates a class to represent PC components, this is also a type of sprite
    def __init__(self,x,y,variety,name,price,value):
        super().__init__(sprites,components) # Adds Component objects to the 'sprites' and 'components' sprite groups

        self.x=TILE_SIZE*x
        self.y=TILE_SIZE*y
        
        self.variety=variety
        self.name=name
        self.price=price
        self.value=value
        
        self.image=pygame.Surface(CATALOGUE[self.variety][3][0]) # CATALOGUE holds all the component parameters and we use indexing to find the dimensions of the component represented by self.variety
        self.image.set_colorkey((0,0,0))
        self.image.blit(component_spritesheet,(0,0),CATALOGUE[self.variety][3][1]) # Cuts out the correct part of component spritesheet to obtain the image of the component
        
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        
        
class Checkout(pygame.sprite.Sprite): # Creates a class to represent the checkout till - the purpose of this is to overlay an invisble surface on top of the checkout till image in order to detect when the player is nearby
    def __init__(self,x,y):
        super().__init__(sprites,checkouts)
                
        self.x=TILE_SIZE*x
        self.y=TILE_SIZE*y
        self.image=pygame.Surface(SURFACES[-1]) # The last entry in the SURFACES list represents the dimensions of the checkout till

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health # update with new health
        ratio = self.health / self.max_health #calculate health ratio
        pygame.draw.rect(screen, METALLIC_GOLD, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

# Item : health , ammo, and grenade package
class ItemBox(pygame.sprite.Sprite): # Item box randomises between health, ammo and grenade packages spawning.
    def __init__(self, item_type, x, y):
        super().__init__(sprites, ItemBox_group)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):

        if pygame.sprite.collide_rect(self, characters.sprites()[0]): # Check if Itembox collides with character
            #check what kind of box it was
            if self.item_type == 'Health':
                characters.sprites()[0].health += 35 # Players get +35 health when they pick up a health box
                if characters.sprites()[0].health > characters.sprites()[0].max_health:
                    characters.sprites()[0].health = characters.sprites()[0].max_health

            elif self.item_type == 'Ammo':
                characters.sprites()[0].ammo += 5 # Player gets +5 ammo when they pick up ammunition from a dead enemy
                if characters.sprites()[0].ammo > characters.sprites()[0].max_ammo:
                    characters.sprites()[0].ammo = characters.sprites()[0].max_ammo
            elif self.item_type == 'Grenade':
                characters.sprites()[0].grenades += 3 # Player gets +3 Grenades when they pick up grenades from dead enemy
                if characters.sprites()[0].grenades > characters.sprites()[0].max_grenade:
                    characters.sprites()[0].grenades = characters.sprites()[0].max_grenade
            pygame.mixer.find_channel(True).play(getitem_music)
            self.kill()

# if the picture in the same png, you can use it to split into a animation
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite


"""

    character can use this class to use the slash to attack enemies
"""
class Slash_Player(pygame.sprite.Sprite): # Slashing class which ONLY the player uses.
    def __init__(self, x, y, direction):
        super().__init__(sprites, player_slash)

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.direction = direction # the facing direction of the charactor
        self.img = Spritesheet('graphics/weapon/attack.png')
        self.image = self.img.get_sprite(0, 0, self.width, self.height)# the variable name must be image, because draw only understand image

        self.animation_loop = 0 #control the animation frame

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # input centerx and centery positions of player

        # save frame of animation in the list
        self.right_animations = [self.img.get_sprite(0, 64, self.width, self.height),
                                 self.img.get_sprite(32, 64, self.width, self.height),
                                 self.img.get_sprite(64, 64, self.width, self.height),
                                 self.img.get_sprite(96, 64, self.width, self.height),
                                 self.img.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.img.get_sprite(0, 32, self.width, self.height),
                                self.img.get_sprite(32, 32, self.width, self.height),
                                self.img.get_sprite(64, 32, self.width, self.height),
                                self.img.get_sprite(96, 32, self.width, self.height),
                                self.img.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.img.get_sprite(0, 96, self.width, self.height),
                                self.img.get_sprite(32, 96, self.width, self.height),
                                self.img.get_sprite(64, 96, self.width, self.height),
                                self.img.get_sprite(96, 96, self.width, self.height),
                                self.img.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.img.get_sprite(0, 0, self.width, self.height),
                              self.img.get_sprite(32, 0, self.width, self.height),
                              self.img.get_sprite(64, 0, self.width, self.height),
                              self.img.get_sprite(96, 0, self.width, self.height),
                              self.img.get_sprite(128, 0, self.width, self.height)]
    
    #change the frame to make the animation of slash
    def update(self):
        if self.direction == 'up':
            #self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 1
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        # when the slash collide with enemies, which will hurt enemies
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, player_slash, False):
                if enemy.health >0:
                    enemy.health -= PLAYER_SLASH_DAMAGE
                    self.kill()

class Slash_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(sprites, enemy_slash)

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.direction = direction # the facing direction of the charactor
        self.img = Spritesheet('graphics/weapon/attack.png')
        self.image = self.img.get_sprite(0, 0, self.width, self.height)# the variable name must be image, because draw only understand image

        self.animation_loop = 0

        self.rect = self.image.get_rect()
        #self.rect.x = self.x
        #self.rect.y = self.y
        self.rect.center = (x, y)  # input centerx and centery of player

        self.right_animations = [self.img.get_sprite(0, 64, self.width, self.height),
                                 self.img.get_sprite(32, 64, self.width, self.height),
                                 self.img.get_sprite(64, 64, self.width, self.height),
                                 self.img.get_sprite(96, 64, self.width, self.height),
                                 self.img.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.img.get_sprite(0, 32, self.width, self.height),
                                self.img.get_sprite(32, 32, self.width, self.height),
                                self.img.get_sprite(64, 32, self.width, self.height),
                                self.img.get_sprite(96, 32, self.width, self.height),
                                self.img.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.img.get_sprite(0, 96, self.width, self.height),
                                self.img.get_sprite(32, 96, self.width, self.height),
                                self.img.get_sprite(64, 96, self.width, self.height),
                                self.img.get_sprite(96, 96, self.width, self.height),
                                self.img.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.img.get_sprite(0, 0, self.width, self.height),
                              self.img.get_sprite(32, 0, self.width, self.height),
                              self.img.get_sprite(64, 0, self.width, self.height),
                              self.img.get_sprite(96, 0, self.width, self.height),
                              self.img.get_sprite(128, 0, self.width, self.height)]
    def update(self):
        if self.direction == 'up':
            #self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 1
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if self.direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


        if pygame.sprite.spritecollide(characters.sprites()[0], enemy_slash, False):
            if characters.sprites()[0].alive and characters.sprites()[0].health >0:
                characters.sprites()[0].health -= ENEMY_SLASH_DAMAGE # Takes 10 off character health
                self.alive = False
                self.kill()

"""
    player can use this class to create instances of bullet to shoot enemies
"""

class Bullet_Player(pygame.sprite.Sprite): # Class for when player shoots a bullet.
    def __init__(self, x, y, direction):
        super().__init__(sprites,player_bullets)
        self.speed = BULLET_SPEED
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # input centerx and centery of player
        self.direction = direction # facing direction of player

    def update(self): # when you call sprite.update this calls ALL of the bullets so you don't need a loop
        
    #change the direction to change the direction of bullet
        if self.direction == "up":
            self.rect.y -= self.speed
        if self.direction == "down":
            self.rect.y += self.speed
        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "right":
            self.rect.x += self.speed

        #check if bullet has gone off screen
        if self.rect.right < 0+100 or self.rect.left > SCREEN_WIDTH-100 \
                or self.rect.top <0+100 or self.rect.bottom >SCREEN_HEIGHT-100\
                or pygame.sprite.spritecollide(self,walls,False):

            self.kill()

        for enemy in enemies: # check collision with characters
            if pygame.sprite.spritecollide(enemy, player_bullets, False):
                if enemy.health >0:
                    enemy.health -= PLAYER_BULLET_DAMAGE
                    self.kill()

# Bullet_Enemy class added from version 7.
class Bullet_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed):
        super().__init__(sprites,enemy_bullets)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # input centerx and centery of player
        self.x_speed = x_speed
        self.y_speed = y_speed


    def update(self):# when you call sprite.update this calls ALL of the bullets so you don't need a loop

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        #check if bullet has gone off screen
        if self.rect.right < 0+100 or self.rect.left > SCREEN_WIDTH-100 \
                or self.rect.top <0+100 or self.rect.bottom >SCREEN_HEIGHT-100\
                or pygame.sprite.spritecollide(self,walls,False):

            self.kill()

        # check collision with characters

        if pygame.sprite.spritecollide(characters.sprites()[0], enemy_bullets, False):
            if characters.sprites()[0].alive and characters.sprites()[0].health >0:
                characters.sprites()[0].health -= ENEMY_BULLET_DAMAGE
                self.alive = False
                self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(sprites, grenade_group)
        self.timer = GRENADE_TIMER #waiting for explosion
        self.vel_y = GRENADE_VEL_Y  # you throw up the grenade, the start of top is 0, gravity,default is -11
        self.speed = GRENADE_SPEED # default is 7
        self.GRAVITY = GRENADE_GRAVITY # default is 0.75
        self.image = grenade_img
        self.landing = False
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # input centerx and centery of player
        self.direction = direction  # facing direction of player


    def update(self):# when you call sprite.update this calls ALL of the Grenade so you don't need a loop
        self.vel_y += self.GRAVITY
        if self.direction =='up' or self.direction =='down':
            dx = 0
        else:
            dx = self.speed

        if self.direction == "down":
            dy = -self.vel_y
        else:
            dy = self.vel_y

        # check collision with floor
        #use dy to control the dropping time of parabola

        if dy > 7 and self.direction == "up":
            dy =350 - self.rect.bottom      #use 350 to change the position of y of grenade
            self.speed = 0
            self.landing = True
        elif dy < -6 and self.direction == "down":
            dy = 600 - self.rect.bottom
            self.speed = 0
            self.landing = True

        elif dy > 11 and self.direction == "left":
            dy =350 - self.rect.bottom
            self.speed = 0
            self.landing = True

        elif dy > 11 and self.direction == "right":
            dy =350 - self.rect.bottom
            #dy = 350 - self.rect.bottom
            self.speed = 0 #grenade stop in the ground
            self.landing = True

        # update grenade position

        if self.direction == "up" and self.landing == False:
            self.rect.x -= dx
            self.rect.y += dy
        elif self.direction == "down" and self.landing == False:
            self.rect.x += dx
            self.rect.y += dy
        elif self.direction == "left" and self.landing == False:
            self.rect.x -= dx
            self.rect.y += dy
        elif self.direction == "right" and self.landing == False:
            self.rect.x += dx
            self.rect.y += dy

        # countdown timer
        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1.7)
            pygame.mixer.find_channel(True).play(grenade_music)
            explosion_group.add(explosion)

class Explosion(pygame.sprite.Sprite): # Explosion for the grenade
    def __init__(self, x, y, scale):
        super().__init__(sprites, explosion_group)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'graphics/weapon/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) #change the size of frame of explosion
            self.images.append(img)
            self.frame_index = 0 # represent first frame
            self.image = self.images[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0

    def update(self):  # continue to run in while loop by sprite.update()

        # update explosion animation
        self.counter += 1

        if self.counter >= GRENADE_EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):

                self.kill()
            else:
                self.image = self.images[self.frame_index]  # when use draw, it will works
                if self.frame_index == 2:
                    # do damage to anyone that is nearby
                    if abs(self.rect.centerx - characters.sprites()[0].rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - characters.sprites()[0].rect.centery) < TILE_SIZE * 2:
                        characters.sprites()[0].health -= GRENADE_PLAYER_DAMAGE

                    for enemy in enemies:
                        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                            enemy.health -= GRENADE_ENEMY_DAMAGE