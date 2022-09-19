# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:28:42 2021

@author: jacob
"""
import pickle # For storing leaderboards permanently

hs = pickle.load(open("scores.p","rb")) # Open current state of leaderboards as two lists
hs_name = pickle.load(open("names.p", "rb"))

# Defining screen size
SCREEN_WIDTH=960
SCREEN_HEIGHT=720

# Defining the frame rate
FPS=60

# To position the map correctly on the screen
X_SHIFT=7
Y_SHIFT=-3

# Define color (RGB)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 223, 0)
METALLIC_GOLD = (212, 175, 55)

# Defining player global variables
PLAYER_SPEED= 3
PLAYER_SIZE=48
PLAYER_X=14.6-X_SHIFT # This is where the player should spawn on the map
PLAYER_Y=3-Y_SHIFT
PLAYER_HEALTH=128

# Defining enemy global variables
ENEMY_SPEED = 4
ENEMY_HEALTH=100

# Defining weapon global variables
STARTING_GRENADES=1
STARTING_AMMO=30

MAX_AMMO=40
MAX_GRENADE=10

PLAYER_SLASH_DAMAGE=25 # Damage done by player slash attacks
ENEMY_SLASH_DAMAGE=10 # Damage done by enemy slash attacks

PLAYER_BULLET_DAMAGE=25 # Damage done by player shots
ENEMY_BULLET_DAMAGE=25 # Damage done by player shots

GRENADE_TIMER=100 # to control the time of tractory of parabola
GRENADE_VEL_Y=-11 # the highest point of parabola
GRENADE_SPEED=3 # the x speed of grenade
GRENADE_GRAVITY=0.5 # gravity will control the drop of grenade
GRENADE_EXPLOSION_SPEED = 4 # control the time of start of explosion
GRENADE_PLAYER_DAMAGE=50 # Grenades do damage to players as well as enemies
GRENADE_ENEMY_DAMAGE=50

BULLET_SPEED = 10

# Other global variables 
MONEY_LIMIT=1500
TIME_LIMIT=300

FONT_SIZE=[15,20,30,50, 90] # Small, medium, large and giant font sizes

TILE_SIZE=64

COMPONENT_RARITY=40 # The probability of a PC component spawning on an empty square of the map is 1/COMPONENT_RARITY

BONUS=1000 # The score bonus for finding all 10 components

# Randomly choosing contents of item boxes
ITEM_LIST = ["Health", "Ammo", "Grenade"]

# Navigating menu screen option
NAVIGATION = ['playing', 'instructions', 'leaderboard']

# This is the game map - it is 30 tiles by 50 tiles (each tile being 64 by 64 pixels)
# Numbers represent different types of walls, dots represent empty tiles
# 'A' represents tiles where we don't want PC components to spawn
# 'E' represents walking enemy
# 'E2' represents stationary enemy


GAMEMAP=[
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'A', 'A', 'A', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 19, 'A', 'A', 'A', '.', 19, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'A', 'A', 'A', 'A', '.', 'A', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5],
 [2, '.', '.', '.', 'E2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E2', '.', '.', '.', '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', '.', '.', 44, 'A', 'A', 'A', '.', '.', '.', '.', '.', '.', '.', '.', 44, 'A', 'A', 'A', '.', '.', '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', 'A', 'A', 'A', 'A', '.', '.', 10, 'A', 'A', 'A', '.', '.', 'A', 'A', 'A', 'A', '.', '.', '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'A', 'A', 'A', 'A', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E2', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', 16, 15, 46, 16, '.', '.', 15, 16, 15, 46, 15, 16, 16, 15, 16, 15, '.', '.', 46, 16, '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', 11, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 43, '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', 13, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 12, '.', '.', '.', '.', 5],
 [2, '.', 'E2', '.', '.', 20, 45, 20, 20, 20, 45, 20, 20, 20, 20, '.', '.', 22, 45, 22, 22, 22, 22, 22, 22, '.', '.', '.', '.', 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 43, '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 14, '.', '.', '.', '.', 5],
 [2, 25, 25, 48, 25, 25, 25, 48, 25, 48, '.', '.', 29, 24, 24, 29, 24, 29, 29, 29, 24, 24, '.', 25, 48, '.', '.', '.', '.', 5], 
 [2, 35, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 26, 26, 5],
 [2, 35, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 39, 5], 
 [2, 30, 27, 30, 27, 27, 30, '.', '.', 40, 41, 41, 45, 41, 40, 40, 41, '.', '.', 27, 30, 27, 27, '.', '.', '.', '.', '.', 39, 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 14, '.', 43, '.', '.', '.', '.', 5],
 [2, 34, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 12, '.', 12, '.', '.', 34, '.', 5],
 [2, 56, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E', '.', '.', '.', 14, '.', 12, '.', '.', 56, 36, 5],
 [2, 34, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 43, '.', 14, '.', '.', 34, 36, 5],
 [2, 56, '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 43, '.', 12, '.', '.', 56, 36, 5],
 [2, 34, '.', '.', 'E', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 14, '.', 43, '.', '.', 34, '.', 5],
 [2, 56, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 29, 29, 24, 24, 29, '.', 12, '.', '.', 56, '.', 5],
 [2, 34, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 12, '.', '.', 34, '.', 5],
 [2, 56, '.', '.', '.', '.', '.', 28, 37, 37, 37, 28, 37, 37, 37, 28, 37, 37, 37, 28, 51, 50, 51, 51, 50, '.', '.', 56, '.', 5],
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 55, '.', '.', '.', '.', '.', '.', '.', 34, '.', 5], 
 [2, 15, 16, 15, 15, '.', '.', '.', '.', '.', '.', '.', '.', 'E2', '.', '.', '.', '.', '.', 55, '.', '.', '.', '.', '.', '.', '.', 56, '.', 5],
 [2, '.', '.', '.', '.', '.', '.', 33, 'A', '.', '.', 31, 'A', '.', '.', 33, 'A', '.', '.', 55, '.', 50, 51, 50, 50, 51, 51, 54, '.', 5], 
 [2, 38, '.', '.', '.', '.', '.', 'A', 'A', '.', '.', 'A', 'A', '.', '.', 'A', 'A', '.', '.', 55, '.', 57, '.', '.', '.', '.', '.', 54, '.', 5], 
 [2, 38, '.', 32, 'A', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 57, '.', '.', '.', '.', '.', 54, '.', 5],
 [2, 38, '.', 'A', 'A', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 55, '.', 51, 51, 50, 51, 50, '.', 54, '.', 5],
 [2, 38, '.', '.', '.', 'E2', '.', 33, 'A', '.', '.', 31, 'A', '.', '.', 33, 'A', '.', '.', 55, '.', '.', '.', '.', '.', '.', '.', 51, 50, 5],
 [2, 38, '.', '.', '.', '.', '.', 'A', 'A', '.', '.', 'A', 'A', '.', '.', 'A', 'A', '.', '.', 55, '.', '.', '.', '.', '.', '.', '.', '.', '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 55, 50, 51, '.', 23, 23, 23, '.', 17, '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 17, '.', 5],
 [2, 16, 15, '.', 21, 47, 21, 21, 49, 47, 47, 21, 21, 47, 21, 49, 49, 21, 21, 47, 21, 47, 47, 49, '.', 26, 26, 17, '.', 5], 
 [2, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 17, '.', 5],
 [2, '.', '.', 24, 24, 29, 24, '.', 52, 52, 52, 53, 52, 52, 53, 52, 52, 52, 52, 53, '.', 30, 27, 27, 30, 27, '.', 17, '.', 5],
 [2, '.', '.', 34, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 5],
 [2, 35, '.', 56, '.', 39, '.', '.', 25, 25, 48, 25, 48, 'E2', '.', '.', 'E2', 40, 41, 41, 40, 45, 40, 40, 45, 41, 13, '.', 36, 5],
 [2, 35, '.', 34, '.', 39, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 13, '.', '.', '.', 11, '.', 36, 5],
 [2, 35, '.', 58, '.', 39, '.', '.', '.', 20, 45, 22, 22, 20, '.', '.', 20, 45, 22, 22, 20, '.', 11, '.', 58, '.', 42, '.', 36, 5],
 [2, 35, '.', 'A', '.', 39, '.', '.', '.', 11, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 12, '.', 42, '.', 'A', '.', 42, '.', 36, 5],
 [2, '.', '.', 'A', '.', '.', '.', '.', '.', 13, '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 43, '.', 11, '.', 'A', '.', 13, '.', '.', 5],
 [2, '.', '.', 'A', '.', '.', '.', '.', '.', 42, '.', '.', '.', '.', 59, 'A', '.', '.', '.', '.', 14, '.', '.', '.', 'A', '.', 11, '.', '.', 5], 
 [4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7], 
 ]

# These are the dimensions of the sprites we want to create when generating each type of 'wall' (inc. furniture)
# In total there are 60 types of wall - the first 10 are used for the sides of the map, and the remaining 50 are used for the map interior


# The following lists are of length 60 with each index position directly corresponding to a number in the above gamemap to represent a 'wall' type

SURFACES=[[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],
          
          
          [TILE_SIZE*4,TILE_SIZE*2],[30,TILE_SIZE],[30,TILE_SIZE],
          [28,TILE_SIZE],[28,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[13,TILE_SIZE],[13,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE*2],[TILE_SIZE,52],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,49],[TILE_SIZE,55],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE*2,TILE_SIZE*2],[TILE_SIZE*2,TILE_SIZE*2],[TILE_SIZE*2,105],
          [37,TILE_SIZE],[40,TILE_SIZE],[40,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [32,TILE_SIZE],[32,TILE_SIZE],[TILE_SIZE,53],[TILE_SIZE,56],
          [32,TILE_SIZE],[32,TILE_SIZE],[TILE_SIZE*4,TILE_SIZE*2],[TILE_SIZE,42],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],
          [TILE_SIZE,TILE_SIZE],[TILE_SIZE,TILE_SIZE],[11,TILE_SIZE],[11,TILE_SIZE],
          [33,TILE_SIZE],[43,TILE_SIZE],[34,TILE_SIZE*4],[TILE_SIZE*2,TILE_SIZE]]

# These are the top left positions of all 60 wall types on the spritesheet (first two numbers in each entry) and the area from these top lefts that should be cut out when spawning the walls (last two numbers in each entry)

POSITIONS=[(512,448,64,64),(576,448,64,64),(512,512,64,64),(640,448,64,64),(512,576,64,64),
           (640,512,64,64),(576,576,64,64),(640,576,64,64),(512,640,64,64),
           (640,640,64,64),(0,0,256,128),(128,448,64,64),(128,448,64,64),(128,512,64,64),
           (128,512,64,64),(256,128,64,64),(320,128,64,64),
            (256,192,64,64),(320,192,64,64),(0,576,64,128),(0,256,64,64),(64,256,64,64),
            (0,320,64,64),(192,320,64,64),(0,384,64,64),(64,384,64,64),(192,384,64,64),
            (128,384,64,64),(64,320,64,64),(192,256,64,64),(128,256,64,64),(0,448,128,128),
            (512,64,128,128),(256,0,128,128),(320,448,64,64),(256,256,64,64),(320,256,64,64),
            (256,320,64,64),(320,384,64,64),(256,384,64,64),(192,448,64,64),(256,448,64,64),
            (126,576,64,64),(126,576,64,64),
            (0,128,256,128),(320,320,64,64),(384,320,64,64),(384,128,64,64),
            (448,320,64,64),(448,128,64,64),(384,256,64,64),(448,256,64,64),(384,64,64,64),
            (448,64,64,64),(384,192,64,64),(384,192,64,64),
            (640,128,64,64),(384,0,64,64),(512,192,64,256),(128,640,128,64)]

# These are the amounts by which each wall needs to be shifted to place it in the correct position on the map (e.g. narrow walls that need to be placed on the right side of the tile will need to be shifted to the right)

SHIFTS=[[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT-34/TILE_SIZE,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT-36/TILE_SIZE,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT-51/TILE_SIZE,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT-24/TILE_SIZE,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT-32/TILE_SIZE,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT-32/TILE_SIZE,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT-8/TILE_SIZE],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT-53/TILE_SIZE,Y_SHIFT],[X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT],
        [X_SHIFT,Y_SHIFT],[X_SHIFT,Y_SHIFT]]


# The CATALOGUE stores all the information about PC components - there are 10 different components in total with each referenced by a letter from 'a' to 'j' in a dictionary

CATALOGUE={
    'a':[['Budget Mouse','Mid-Tier Mouse','Quality Mouse','Elite Mouse'],
         [[10,34],[35,69],[70,119],[120,180]],
         [[10,19],[20,39],[40,79],[80,150]],
         [[21,32],(0,0,64,64)]],
    'b':[['Budget SSD','Mid-Tier SSD','Quality SSD','Elite SSD'],
         [[30,79],[80,139],[140,249],[250,500]],
         [[40,79],[80,139],[140,259],[260,400]],
         [[59,38],(64,0,64,64)]],
    'c':[['Budget Graphics Card','Mid-Tier Graphics Card','Quality Graphics Card','Elite Graphics Card'],
         [[70,159],[160,309],[310,599],[600,900]],
         [[180,299],[300,499],[500,799],[800,1200]],
         [[62,44],(128,0,64,64)]],
    'd':[['Budget CPU','Mid-Tier CPU','Quality CPU','Elite CPU'],
         [[100,149],[150,299],[300,519],[520,750]],
         [[200,289],[290,469],[470,649],[650,1000]],
         [[64,46],(192,0,64,64)]],
    'e':[['Budget Motherboard','Mid-Tier Motherboard','Quality Motherboard','Elite Motherboard'],
         [[30,99],[100,169],[170,269],[270,430]],
         [[150,159],[160,219],[220,299],[300,400]],
         [[62,37],(0,64,64,64)]],
    'f':[['Budget Display','Mid-Tier Display','Quality Display','Elite Display'],
         [[120,199],[200,279],[280,449],[450,700]],
         [[50,179],[180,349],[350,499],[500,800]],
         [[45,64],(64,64,64,64)]],
    'g':[['Budget RAM','Mid-Tier RAM','Quality RAM','Elite RAM'],
         [[40,79],[80,119],[120,219],[220,480]],
         [[100,159],[160,249],[250,349],[350,500]],
         [[63,37],(128,64,64,64)]],
    'h':[['Budget PC Case','Mid-Tier PC Case','Quality PC Case','Elite PC Case'],
         [[15,29],[30,49],[50,79],[80,170]],
         [[5,14],[15,29],[30,79],[80,240]],
         [[40,62],(0,128,64,64)]],
    'i':[['Budget Cooling Fan','Mid-Tier Cooling Fan','Quality Cooling Fan','Elite Cooling Fan'],
         [[2,9],[10,24],[25,49],[50,80]],
         [[10,19],[20,29],[30,59],[60,90]],
         [[49,60],(64,128,64,64)]],
    'j':[['Budget Keyboard','Mid-Tier Keyboard','Quality Keyboard','Elite Keyboard'],
         [[20,39],[40,89],[90,169],[170,260]],
         [[70,99],[100,149],[150,209],[210,260]],
         [[64,64],(128,128,64,64)]],
}
    
    
CHECKOUTS=[59] # This is the index position of the checkout

