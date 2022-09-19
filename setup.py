# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 23:00:25 2021

@author: jacob
"""
import pygame

from data import *

# Initialising pygame (needed here for initialising fonts and will be used throughout the other python files that import 'setup')

pygame.init()
pygame.display.set_caption('You Know Who') # Displays the game title
clock=pygame.time.Clock() # Necessary for the basic set up of the frame rate
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # Sets up the pygame display that allows us to load images and print them onto the screen

# Loading images-- character, enemy, component

player_spritesheet=pygame.image.load("graphics/main.png").convert() # Load player spritesheet and use convert() to import more efficiently
player_spritesheet=pygame.transform.scale(player_spritesheet,(144,192)) # This will enlarge the player spritesheet by a factor of 1.5 (this size provides a balance between readability and mobility)
object_spritesheet=pygame.image.load("graphics/objects.png").convert() # Load sheet containing walls and furniture
component_spritesheet=pygame.image.load("graphics/components.png").convert() # Load sheet containing PC components that will be randomly scattered around the map

# Loading and configuring ALL enemy spritesheets

enemy1_spritesheet = pygame.image.load("graphics/Enemy/Enemy1.png").convert()
enemy1_spritesheet = pygame.transform.scale(enemy1_spritesheet, (144, 192))
enemy2_spritesheet = pygame.image.load("graphics/Enemy/Enemy2.png").convert()
enemy2_spritesheet = pygame.transform.scale(enemy2_spritesheet, (144, 192))

# Loading images-- weapon

slash_image = pygame.image.load("graphics/weapon/attack.png")
bullet_img = pygame.image.load('graphics/weapon/bullet.png').convert_alpha() # 'alpha' makes the image backgrounds invisible
bullet_img = pygame.transform.scale(bullet_img,(int(bullet_img.get_width() * 2), int(bullet_img.get_height()*2)))
grenade_img = pygame.image.load('graphics/weapon/grenade.png').convert_alpha()
grenade_img = pygame.transform.scale(grenade_img,(int(grenade_img.get_width() * 2), int(grenade_img.get_height()*2)))

# Background images for the menu screen

bg_img = pygame.image.load('graphics/bg_img.png').convert_alpha()
ld_bg_img = pygame.image.load('graphics/ld_bg_img.png').convert_alpha()
end_bg_img = pygame.image.load('graphics/end_bg_img.png').convert_alpha()
title_img = pygame.image.load('graphics/Computer_Quest.png').convert_alpha()
title_img=pygame.transform.scale(title_img,(1013*0.8,106*0.8)) # 'pygame.transform.scale' resizes images

# Box of health, bullet and grenade

health_box_img = pygame.image.load('graphics/Item box/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('graphics/Item box/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('graphics/Item box/grenade_box.png').convert_alpha()

# the dictionary of item_boxes

item_boxes = {

	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
	'Grenade'	: grenade_box_img

}

# Loading fonts - initialises the font style that will be used in this game

medium_font=pygame.font.Font("font/Exo-Bold.ttf",FONT_SIZE[1])
small_font=pygame.font.Font("font/Exo-Bold.ttf",FONT_SIZE[0])
large_font=pygame.font.Font("font/Exo-Bold.ttf",FONT_SIZE[2])
giant_font=pygame.font.Font("font/Exo-Bold.ttf",FONT_SIZE[3])
menu_font=pygame.font.Font("font/ccoverbyteoffregular.ttf", FONT_SIZE[3])
option_font=pygame.font.Font("font/ccoverbyteoffregular.ttf", FONT_SIZE[4])
l_font=pygame.font.Font("font/ccoverbyteoffregular.ttf", FONT_SIZE[2])
font = pygame.font.SysFont('Futura', 30)
futura_large = pygame.font.SysFont('Futura', 50)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Loading music

pygame.mixer.init()
pygame.mixer.set_num_channels(20) #set channels to avoid the confict

# Background music

music = pygame.mixer.music.load('music/background music/background_music.mp3')
pygame.mixer.music.play(-1)

# Weapon Sounds

grenade_music = pygame.mixer.Sound("music/weapon/grenade.wav")
throw_music = pygame.mixer.Sound("music/weapon/throw.mp3")
slash_music = pygame.mixer.Sound("music/weapon/slash.wav")
bullet_music = pygame.mixer.Sound("music/weapon/pistol.ogg")

# Action sounds

moving_music = pygame.mixer.Sound("music/action/moving.mp3")

# System sounds

getitem_music = pygame.mixer.Sound("music/system_sound/Get the item1.wav")
getitem_music1 = pygame.mixer.Sound("music/system_sound/Get the item.mp3")
delete_music = pygame.mixer.Sound("music/system_sound/delete.mp3")
select_music = pygame.mixer.Sound("music/system_sound/select.mp3")
select2_music = pygame.mixer.Sound("music/system_sound/select2.mp3")
select3_music = pygame.mixer.Sound("music/system_sound/select3.mp3")
death_music = pygame.mixer.Sound("music/system_sound/death.mp3")
death1_music = pygame.mixer.Sound("music/system_sound/death1.mp3")
death2_music = pygame.mixer.Sound("music/system_sound/death2.mp3")
win_music = pygame.mixer.Sound("music/system_sound/win.mp3")

pygame.mixer.music.set_volume(0.5)
bullet_music.set_volume(0.2)
moving_music.set_volume(0.6)
grenade_music.set_volume(0.2)
death1_music.set_volume(0.5)
getitem_music1.set_volume(0.2)


# Initialising sprite groups

sprites=pygame.sprite.Group() # This group is the union of all below groups (contains all sprites)

characters=pygame.sprite.Group() # These are the separated groups of sprites
enemies=pygame.sprite.Group()
walls=pygame.sprite.Group()
floors=pygame.sprite.Group()
components=pygame.sprite.Group()
player_bullets=pygame.sprite.Group()
chests=pygame.sprite.Group()
checkouts=pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
player_slash = pygame.sprite.Group()
enemy_slash = pygame.sprite.Group()
ItemBox_group = pygame.sprite.Group()


