# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:27:10 2021

@author: jacob
"""
"""

Storyline:
    
Due to the Covid-19 pandemic, we have seen an unfortunate shortage in computer chips, graphics cards, gaming consoles, and other PC components.

This is due to the extreme cost and time it takes to both produce these components and to build new plants, as well as due to resellers buying up all the stock and scalping consumers.

Your goal is to build a brand new gaming PC, which will be a big challenge considering these circumstances.

You will spawn at the entrance of a massive computer shop and you need to purchase the components with which you will build your PC.

However, to discourage bulk buying, there is a 5 minute time limit inside the shop.

If you have not successfully bought your items at the checkout by this time, you will be booted out of the shop empty handed.

And as you can imagine, you are also not the only one shopping for these scarce components.

You will encounter many enemies on your journey throughout the shop who will try to beat you up and grab the components in your basket.

Good luck with your shopping, and happy PC building!
    
"""

from game import * # In this python file, we only directly communicate with an object of 'Game' method

g=Game() # Generate an object of class 'Game'
g.gamemap() # Use the 'gamemap' method to fully populate the initial game map


while True: # This is called the 'game loop': it keeps the game running forever until we exit this loop
    
    if g.remaining_time==0 or g.p.end or not g.p.alive: # These are the two scenarios where the game needs to end (either you ran out of time or you completed the level)
        g.slide="endscreen" # When the game ends, we want to go to the 'endscreen'

    if g.slide=="menu": # This conditional statement will run the menu
        g.event_loop_menu() # This 'Game' method will run the event loop for the menu screen
        g.menu_refresh() # This 'Game' method will run the rest of the code for the menu screen inside the game loop

    if g.slide=="playing": # This conditional statement will run the main game
        g.event_loop_playing() # This 'Game' method will run the event loop for the main game
        g.playing_refresh() # This 'Game' method will run the rest of the code for the main game inside the game loop

    if g.slide=="instructions": # Accesses the instructions menu
        g.event_loop_instructions()
        g.instructions_refresh()

    if g.slide=="leaderboard": # Accesses the leaderboard
        g.event_loop_leaderboard()
        g.leaderboard_refresh()

    elif g.slide=="endscreen": # This conditional statement will run the game over screens
        g.event_loop_endscreen() # This 'Game' method will run the event loop for the game over screens
        g.endscreen_refresh() # This 'Game' method will run the rest of the code for the game over screens inside the game loop

    pygame.display.update() # This function will update the pygame display every frame
    clock.tick(FPS) # Sets the frame rate of the game (60FPS in this case)
    