# AUTODARTS-PIXELIT
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-pixelit/total.svg)](https://github.com/lbormann/autodarts-pixelit/releases/latest)

Autodarts-pixelit controls your pixelit-installation(s) https://github.com/pixelit-project/PixelIt accordingly to the state of an https://autodarts.io game. A running instance of https://github.com/lbormann/autodarts-caller is needed that sends thrown points from https://autodarts.io to this application.


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
TODO

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
TODO

## Hardware

Here is my currrent Hardware-Setup (You can google prices yourself):
* Controller: 1x AZDelivery ESP32 D1 Mini
* Led-Matrix: 1x TODO
* Power adapter: 1x Mean Well LPV-100-8 60W 5V DC
* Connector: TODO
* Connector: TODO



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
- -BRI / --effect_brightness [OPTIONAL] [Default: 175] [Possible values: 1 .. 255] 
- -HFO / --high_finish_on [OPTIONAL] [Default: None] [Possible values: 2 .. 170] 
- -HF / --high_finish_effects [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: None] [Possible values: See below] 
- -IDE / --idle_effect [OPTIONAL] [Default: "solid|lightgoldenrodyellow"] [Possible values: See below] 
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

*`-BRI / --effect_brightness`*

Brightness for PIXELIT-effects. You can choose a value between '1' and '255'. By default this is 10.

*`-HFO / --high_finish_on`*

Define what a highfinish means for you. Choose a score-value between '2' and '170'. This value is relevant for argument '-HF'. By default this is not set = no effects for 'Highfinishes'.

*`-HF / --high_finish_effects`*

Controls your pixelit(s) when a high-finish occurs.
Define one effect/preset/playlist or a list. If you define a list, the program will randomly choose at runtime. For examples see below!

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


| Argument | [condition] | effect 1 | effect 2 | effect 3 | ... |
| --  | -- | -- | --  | -- | -- | 
|-B |  | solid\\|red1 | solid\\|blue2 | | | |
|-A1 | 0-15 | 1\\|s255\\|i255\\|green1\\|red2 | solid\\|red1 | breathe\\|yellow1\\|blue2\\|s170\\|i40 | | |
|-A2 | 16-60 | ps\\|3 | | | 

The first argument-definition shows the event 'Busted': Busting will result in playing one of the 2 defined effects: solid (red) and solid (blue).

The second argument-definition shows a 'score-area': recognized scores between 0 and 15 will result in playing one of the 3 effects: blink (ID: 1), breathe or solid. For every of those effects we defined different colors, speeds and intensities; only the effect-name/effect-ID is required; everything else is an option.

The third argument-definition shows a 'score-area': recognized scores between 16 and 60 result in playing preset (or playlist) 3.

* To set a preset or playlists, use the displayed ID in WLED! Moreover you can set a custom duration (Except -IDE)

    syntax: **"ps|{ID}|{seconds}"**

* To set an effect, use an pixelit-effect-name or the corresponding ID (https://github.com/Aircoookie/WLED/wiki/List-of-effects-and-palettes):

    syntax: **"{'effect-name' or 'effect-ID'}|{primary-color-name}|{secondary-color-name}|{tertiary-color-name}"**

* To set effect- speed, intensity, palette, duration (Except -IDE)

    syntax: **"{'effect-name' or 'effect-ID'}|s{1-255}|i{1-255}|p{palette-ID}|d{seconds}"**

* For color-name usage, validate that the color-name you want is available in the list!

    validate here: **https://github.com/lbormann/autodarts-pixelit/blob/main/colors.txt**

* To set an random effect, use 'x' or 'X' as effect-id

    syntax: **"x"**

* If don't understand have a look at the example file!

    learn at: **start.bat**




## Community-Profiles

| Argument | Tullaris#4778 | wusaaa#0578 | Sini#8190
| --  | -- | -- | -- |
| HF (Highfinish) | fire flicker | 4 87 26 29 93 42 64 | ps\\|1 ps\\|2 |
| IDE (Idle) | solid\\|lightgoldenrodyellow | solid\\|lightgoldenrodyellow | ps\\|10 |
| G (Game-won) | colorloop | 4 87 26 29 93 42 64 | ps\\|9 ps\\|11 |
| M (Match-won) | running\\|orange\\|red1 | 4 87 26 29 93 42 64 | ps\\|3 ps\\|4 |
| B (Busted) | fire 2012 | solid\\|red1 | ps\\|20 ps\\|21 |
| S0 (score 0) | breathe\\|orange\\|red1 | | ps\\|5 ps\\|6 |
| S3 (Score 3) | running | | |
| S26 (Score 26) | dynamic | | ps\\|7 ps\\|8 |
| S135 (Score 135) | | 78 9 | |
| S140 (Score 140) | | 81 | |
| S144 (Score 144) | | 78 9 | |
| S153 (Score 153) | | 78 9 | |
| S162 (Score 162) | | 78 9 | |
| S171 (Score 171) | | 78 9 | |
| S180 (Score 180) | rainbow | 78 9 | ps\\|12 ps\\|13 |
| A1 (Area 1) | 0-14 solid\\|deeppink1 | 0-30 solid\\|orange | 0-25 ps\\|14 ps\\|15 |
| A2 (Area 2) | 15-29 solid\\|blue | 31-60 solid\\|orange1 | 27-59 ps\\|16 ps\\|18 |
| A3 (Area 3) | 30-44 solid\\|deepskyblue1 | 61-90 solid\\|yellow1 | 60-99 ps\\|17 ps\\|19 |
| A4 (Area 4) | 45-59 solid\\|green | 91-120 solid\\|olivedrab4 | 100-179 ps\\|22 ps\\|23 |
| A5 (Area 5) | 60-74 solid\\|chartreuse1 | 121-150 solid\\|olivedrab1 | |
| A6 (Area 6) | 75-89 solid\\|brick | | |
| A7 (Area 7) | 90-104 solid\\|tomato1 | | |
| A8 (Area 8) | 105-119 solid\\|tan1 | | |
| A9 (Area 9) | 120-134 solid\\|yellow1 | | |
| A10 (Area 10) | 135-149 solid\\|purple1 | | |
| A11 (Area 11) | 150-164 solid\\|orange | | |
| A12 (Area 12) | 165-180 solid\\|red1 | | |

Moreover you can find ready-to-go pixelit-presets in the community-folder; You can restore a preset-file in pixelit-ui.



## !!! IMPORTANT !!!

This application requires a running instance of autodarts-caller https://github.com/lbormann/autodarts-caller
