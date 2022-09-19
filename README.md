## Installation
This project uses Python3. 9
The library [Pygame](https://www.pygame.org) is also used. 
To install pygame:
Windows installation
Make sure you install python with the "Add python to PATH" option selected. This means that python, and pip will work for you from the command line.
There is documentation with python for the "windows installation steps"
py -m pip install -U pygame --user
py -m pygame.examples.aliens
If you get 'PermissionError: [WinError 5] Access is denied', before starting the command prompt right click and "Run as administrator".
Mac installation
Recent versions of Mac OS X require pygame 2
If your examples aren't running and you are using a recent version of Mac OS X; try this line to install pygame instead:
python3 -m pip install -U pygame --user

## Playing the game
run "run.py"

##Game file path
The font files come from the "font" folder
The picture files(enemy,item box,weapon,background) come from the "graphics" folder
The sound files(moving, background_music, system_sound,weapon) come from the "music" folder
The score record is stored in the file "scores.p"
The name of the participant is stored in the file "names.p"

## Gameplay basics
* Use 'W', 'A', 'S', 'D' to move
* Press 'space' to shoot
* Press 'K' to slash
* Press 'J' to throw the grenade
* Press 'Enter' to open the backpack
* Press 'backspace' to delete the item


