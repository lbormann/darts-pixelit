# AUTODARTS-PIXELIT
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-pixelit/total.svg)](https://github.com/lbormann/autodarts-pixelit/releases/latest)

Autodarts-pixelit controls your pixelit-installation(s) https://github.com/pixelit-project/PixelIt accordingly to the state of an https://autodarts.io game. A running instance of https://github.com/lbormann/autodarts-caller is needed that sends thrown points from https://autodarts.io to this application.

Special thanks to user [Sini](https://discordapp.com/users/935394843625156688). He came up with the funny idea and developed the core code for controlling a Pixelit installation.



## COMPATIBILITY

| Variant | Support |
| ------------- | ------------- |
| X01 | :heavy_check_mark: |
| Cricket | :heavy_check_mark: |
| Bermuda | |
| Shanghai | |
| Gotcha | |
| Around the Clock | |
| Round the World | |
| Random Checkout | :heavy_check_mark: |
| Count Up | |
| Segment Training | |

## Showcase

#### Videos (Click to play):
<!-- [![IMAGE_ALT](https://img.youtube.com/vi/fDXomw55vhI/hqdefault.jpg)](https://youtu.be/fDXomw55vhI) -->
COMING SOON

#### Images:
<!-- <img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/1.jpg?raw=true">
<p float="left">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/2.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/3.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/4.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/5.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/6.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/7.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/8.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/9.jpg?raw=true" width="49%">
<img src="https://github.com/lbormann/autodarts-pixelit/blob/main/showcase/10.jpg?raw=true" width="49%">
</p> -->
COMING SOON

## Hardware

Here is my currrent Hardware-Setup (You can google prices yourself):
* Controller: 1x AZDelivery ESP32 D1 Mini
* Led-Matrix: 1x COMING SOON
* Power adapter: 1x Mean Well LPV-100-5 40W 5V DC
* Connector: COMING SOON
* Connector: COMING SOON



## INSTALL INSTRUCTION

### Desktop-OS: 

- If you're running a desktop-driven OS it's recommended to use [autodarts-desktop](https://github.com/lbormann/autodarts-desktop) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source: 

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/autodarts-pixelit.git

Go to download-directory and type:

    pip3 install -r requirements.txt



## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/autodarts-caller - (latest version)
* You need to have a running PIXELIT-Installation (2.5.0 at minimum required)

### Run by executable

#### Example: Windows 

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-pixelit.exe -PEPS "your-first-pixelit-ip" "your-second-pixelit-ip"

Save changes.
Click on the shortcut to start the application.


### Run by source

#### Example: Linux

    python3 autodarts-pixelit.py -PEPS "your-pixelit-ip"



### Arguments

- -CON / --connection [OPTIONAL] [Default: "127.0.0.1:8079"] 
- -PEPS / --pixel_endpoints [REQUIRED] [MULTIPLE ENTRIES POSSIBLE] 
- -TP / --templates_path [REQUIRED] 
- -BRI / --effect_brightness [OPTIONAL] [Default: 175] [Possible values: 1 .. 255] 
- -HFO / --high_finish_on [OPTIONAL] [Default: None] [Possible values: 2 .. 170] 
- -HF / --high_finish_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -AS / --app_start_effects [OPTIONAL] [Default: None] [Possible values: See below] 
- -IDE / --idle_effect [OPTIONAL] [Default: None] [Possible values: See below] 
- -G / --game_won_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -M / --match_won_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -B / --busted_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -PJ / --player_joined_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -PL / --player_left_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -S{0-180} / --score_{0-180}_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -A{1-12} / --score_area_{1-12}_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 



*`-CON / --connection`*

Host address to data-feeder (autodarts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address / usually you do NOT need to change this)
    
*`-PEPS / --pixelit_endpoints`*

IP to your PIXELIT. You can define multiple entries. For example: '192.168.3.200' '192.168.3.201'.

*`-TP / --templates_path`*

Setup an absolute path where your json-templates are located.
Make sure the given path doesn't reside inside main-directory (autodarts-caller).

*`-BRI / --effect_brightness`*

Brightness for PIXELIT-effects. You can choose a value between '1' and '255'. By default this is 10.

*`-HFO / --high_finish_on`*

Define what a highfinish means for you. Choose a score-value between '2' and '170'. This value is relevant for argument '-HF'. By default this is not set = no effects for 'Highfinishes'.

*`-HF / --high_finish_effects`*

Controls your pixelit(s) when a high-finish occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-AS / --app_start_effects`*

Controls your pixelit(s) when the application starts
Define an effect/preset/playlist that gets triggered. For examples see below!

*`-IDE / --idle_effect`*

Controls your pixelit(s) when dart-pulling occurs or a configurated duration pasts.
Define an effect/preset/playlist that gets triggered. For examples see below!

*`-G / --game_won_effects`*

Controls your pixelit(s) when a game won occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-M / --match_won_effects`*

Controls your pixelit(s) when a match won occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-B / --busted_effects`*

Controls your pixelit(s) when a bust occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-PJ / --player_joined_effects`*

Controls your pixelit(s) when a player-join occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-PL / --player_left_effects`*

Controls your pixelit(s) when a player-left occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-S{0-180} / --score_{0-180}_effects`*

Controls your pixelit(s) when a specific score occurs. You can define every score-value between 0 and 180.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

*`-A{1-12} / --score_area_{1-12}_effects`*

Besides the definition of single score-values you can define up to 12 score-areas.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!


_ _ _ _ _ _ _ _ _ _


#### Examples: 


| Argument | [condition] | template 1 | template 2 | template 3 | ... |
| --  | -- | -- | --  | -- | -- | 
|-B |  | dart\\|d:200\\|b:10 | dart0\\|d:200\\|b:20 | dart1\\|d:200\\|b:30 | dart2\\|b:50 | |
|-A1 | 0-15 | points-bad | | | | |
|-A2 | 16-60 | points-ok | | | | |

The first argument-definition shows the event 'Busted': Busting will result in playing templates (dart, dart0, dart1, ...) in this order. The value 'd:200' defines 200ms delay between current and next template. The value 'b:10' defines custom brightness for a template.

The second argument-definition shows a 'score-area': recognized scores between 0 and 15 will result in playing template 'points-bad' 
The third argument-definition shows a 'score-area': recognized scores between 16 and 60 result in playing template 'points-ok'


* If don't understand have a look at the example file!

    learn at: **start.bat**




## Community-Profiles

| Argument | USER#1234 | USER#1234 | USER#1234
| --  | -- | -- | -- |
COMING SOON

Moreover you can find ready-to-go pixelit-templates in the community-folder.



## !!! IMPORTANT !!!

This application requires a running instance of autodarts-caller https://github.com/lbormann/autodarts-caller