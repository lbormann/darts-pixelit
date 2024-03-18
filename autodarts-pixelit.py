import os
import sys
import json
import platform
import argparse
from pathlib import Path
from urllib.parse import urlparse
import requests
import websocket
import ssl
import threading
import logging
import time
import ast
import re

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)



VERSION = '1.1.0'

DEFAULT_EFFECT_BRIGHTNESS = 20

EFFECT_PARAMETER_SEPARATOR = "|"
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]
SUPPORTED_CRICKET_FIELDS = [15, 16, 17, 18, 19, 20, 25]
SUPPORTED_GAME_VARIANTS = ['X01', 'Cricket', 'Random Checkout']



def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if DEBUG:
        logger.exception("\r\n" + str(error_object))

def get_executable_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(os.path.realpath(__file__))
    else:
        raise RuntimeError("Unable to determine executable directory.")

def same_drive(path1, path2):
    drive1 = os.path.splitdrive(path1)[0]
    drive2 = os.path.splitdrive(path2)[0]
    return drive1 == drive2

def check_paths(main_directory, templates_path):
    try:
        main_directory = get_executable_directory()
        errors = None

        templates_path = os.path.normpath(templates_path)
        
        if same_drive(templates_path, main_directory) == True and os.path.commonpath([templates_path, main_directory]) == main_directory:
            errors = 'TEMPLATES_PATH (-M) is a subdirectory of MAIN_DIRECTORY.'

    except Exception as e:
        errors = f'Path validation failed: {e}'

    if errors is not None:
        ppi("main_directory: " + main_directory)
        ppi("templates_path: " + str(templates_path))

    return errors


def control_pixelit(effect_list, ptext, variables = {}, wake_up = False):    
    ppi(ptext + ' - PIXELIT!')

    if wake_up:
        broadcast({"sleepMode": False})

    if effect_list is None:
        return

    for effect in effect_list:
        em = effect["template"].copy()
        # ppi("HALLLLO???? " + em["template"]["text"]["textString"])

        if "brightness" not in em:
            em["brightness"] = EFFECT_BRIGHTNESS

        if "text" in em and "textString" in em["text"] and em["text"]["textString"] and em["text"]["textString"] != "":
            user_text = em["text"]["textString"]
            user_text = user_text.replace("{" + "}", " ")
            for key, value in variables.items():
                user_text = user_text.replace("{" + key + "}", value)
            em["text"]["textString"] = user_text
        broadcast(em)
        if effect["delay"] != 0:
            time.sleep(effect["delay"] / 1000)
  
def broadcast(data):
    global PIXELIT_ENDPOINTS
    for pixelit_ep in PIXELIT_ENDPOINTS:
        try:
            # ppi("Broadcasting to " + str(pixelit_ep))
            threading.Thread(target=broadcast_intern, args=(pixelit_ep, data)).start()
        except:  
            continue

def broadcast_intern(endpoint, data):
    try: 
        displayData = json.dumps(data, ensure_ascii=False).encode('utf8')
        # ppi("PIXEL IT DATA: ", displayData)
        r = requests.post('http://' + endpoint + '/api/screen', displayData, headers={'Content-Type': 'application/data'})
        # ppi("display return: " + r.text)
    except Exception as e:
        ppe("Error while sending to display.", e)
        return


def load_template(template_name):
    fp = open(os.path.join(TEMPLATES_PATH, template_name + ".json"), "r")
    data = json.load(fp)
    data["screen"] = template_name
    fp.close()
    return data

def parse_effects_argument(effects_argument):
    if effects_argument is None:
        return effects_argument

    parsed_list = list()
    for effect in effects_argument:
        try:
            
            effect_params = effect.split(EFFECT_PARAMETER_SEPARATOR)
            state = {"template": None, "delay": 0}

            # template-name
            effect_template_name = effect_params[0].strip().lower()
            state["template"] = load_template(effect_template_name)

            pattern = r'(?:t:(?P<t>[^\|]+))|(?:d:(?P<d>\d+))|(?:b:(?P<b>\d+))'
            matches = re.finditer(pattern, effect)

            t_value = None
            d_value = None
            b_value = None

            for match in matches:
                group_dict = match.groupdict()
                if group_dict['t']:
                    t_value = group_dict['t']
                elif group_dict['d']:
                    d_value = int(group_dict['d'])
                elif group_dict['b']:
                    b_value = int(group_dict['b'])

            if t_value is not None:
                state["template"]["text"]["textString"] = t_value
                # ppi("t:", t_value)
            if d_value is not None:
                state["delay"] = d_value
                # ppi("d:", d_value)
            if b_value is not None:
                state["template"]["brightness"] = b_value
                # ppi("b:", b_value)
                    
            parsed_list.append(state)
        except Exception as e:
            ppe("Failed to parse event-configuration: ", e)
            continue

    return parsed_list   

def parse_score_area_effects_argument(score_area_effects_arguments):
    if score_area_effects_arguments == None:
        return score_area_effects_arguments

    area = score_area_effects_arguments[0].strip().split('-')
    if len(area) == 2 and area[0].isdigit() and area[1].isdigit():
        return ((int(area[0]), int(area[1])), parse_effects_argument(score_area_effects_arguments[1:]))
    else:
        raise Exception(score_area_effects_arguments[0] + ' is not a valid score-area')

    

def process_lobby(msg):
    if msg['action'] == 'player-joined' and PLAYER_JOINED_EFFECTS != None:
        variables = {'playername': msg['player']}
        control_pixelit(PLAYER_JOINED_EFFECTS, 'Player joined!', variables)    
    
    elif msg['action'] == 'player-left' and PLAYER_LEFT_EFFECTS != None:
        variables = {'playername': msg['player']}
        control_pixelit(PLAYER_LEFT_EFFECTS, 'Player left!', variables)    

def process_variant_x01(msg):
    if msg['event'] == 'darts-thrown':
        val = str(msg['game']['dartValue'])
        variables = {'score': val}

        if SCORE_EFFECTS[val] is not None:
            control_pixelit(SCORE_EFFECTS[val], 'Darts-thrown: ' + val, variables)
        else:
            area_found = False
            ival = int(val)
            for SAE in SCORE_AREA_EFFECTS:
                if SCORE_AREA_EFFECTS[SAE] is not None:
                    ((area_from, area_to), AREA_EFFECTS) = SCORE_AREA_EFFECTS[SAE]
                    if ival >= area_from and ival <= area_to:
                        control_pixelit(AREA_EFFECTS, 'Darts-thrown: ' + val, variables)
                        area_found = True
                        break
            if area_found == False:
                ppi('Darts-thrown: ' + val + ' - NOT configured!')

    elif msg['event'] == 'darts-pulled' and IDLE_EFFECTS is not None:
        variables = {'playername': msg['player'], 
                    'points-left': msg['game']['pointsLeft'], 
                    }
        control_pixelit(IDLE_EFFECTS, 'Darts-pulled', variables)

    elif msg['event'] == 'busted' and BUSTED_EFFECTS is not None:
        control_pixelit(BUSTED_EFFECTS, 'Busted!')

    elif msg['event'] == 'game-won' and GAME_WON_EFFECTS is not None:
        score = msg['game']['dartsThrownValue']
        variables = {'playername': msg['player'], 'score': score}
        if HIGH_FINISH_ON is not None and int(score) >= HIGH_FINISH_ON and HIGH_FINISH_EFFECTS is not None:
            control_pixelit(HIGH_FINISH_EFFECTS, 'Game-won - HIGHFINISH', variables)
        elif GAME_WON_EFFECTS is not None:
            control_pixelit(GAME_WON_EFFECTS, 'Game-won', "GAME WON", variables)

    elif msg['event'] == 'match-won' and MATCH_WON_EFFECTS is not None:
        score = msg['game']['dartsThrownValue']
        variables = {'playername': msg['player'], 'score': score}
        if HIGH_FINISH_ON is not None and int(score) >= HIGH_FINISH_ON and HIGH_FINISH_EFFECTS is not None:
            control_pixelit(HIGH_FINISH_EFFECTS, 'Match-won - HIGHFINISH', variables)
        elif MATCH_WON_EFFECTS is not None:
            control_pixelit(MATCH_WON_EFFECTS, 'Match-won', "MATCH WON", variables)

    elif msg['event'] == 'match-started' and MATCH_START_EFFECTS is not None:
        variables = {'playername': msg['player'], 
                     'game-mode': msg['game']['mode'], 
                     'game-mode-extra': msg['game']['pointsStart']
                     }
        control_pixelit(MATCH_START_EFFECTS, 'Match-started', variables)

    elif msg['event'] == 'game-started' and GAME_START_EFFECTS is not None:
        variables = {'playername': msg['player'], 
                    'game-mode': msg['game']['mode'], 
                    'game-mode-extra': msg['game']['pointsStart']
                    }
        control_pixelit(GAME_START_EFFECTS, 'Game-started', variables)
    

def build_data_feeder_url():
    server_host = CON.replace('ws://', '').replace('wss://', '').replace('http://', '').replace('https://', '')
    server_url = 'wss://' + server_host
    try:
        ws = websocket.create_connection(server_url, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.close()
    except Exception as e_ws:
        try:
            server_url = 'ws://' + server_host
            ws = websocket.create_connection(server_url)
            ws.close()
        except:
            pass
    return server_url

def connect_data_feeder():
    def process(*args):
        global WS_DATA_FEEDER
        websocket.enableTrace(False)

        WS_DATA_FEEDER = websocket.WebSocketApp(build_data_feeder_url(),
                                on_open = on_open_data_feeder,
                                on_message = on_message_data_feeder,
                                on_error = on_error_data_feeder,
                                on_close = on_close_data_feeder)
        WS_DATA_FEEDER.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    threading.Thread(target=process).start()

def on_open_data_feeder(ws):
    ppi('CONNECTED TO DATA-FEEDER ' + str(ws.url))
    
def on_message_data_feeder(ws, message):
    def process(*args):
        try:
            # ppi(message)
            msg = ast.literal_eval(message)

            if('game' in msg and 'mode' in msg['game']):
                mode = msg['game']['mode']
                if mode == 'X01' or mode == 'Cricket' or mode == 'Random Checkout':
                    process_variant_x01(msg)
                # elif mode == 'Cricket':
                #     process_match_cricket(msg)
            elif(msg['event'] == 'lobby'):
                process_lobby(msg)

        except Exception as e:
            ppe('WS-Message failed: ', e)

    threading.Thread(target=process).start()

def on_close_data_feeder(ws, close_status_code, close_msg):
    try:
        ppi("Websocket [" + str(ws.url) + "] closed! " + str(close_msg) + " - " + str(close_status_code))
        ppi("Retry : %s" % time.ctime())
        time.sleep(3)
        connect_data_feeder()
    except Exception as e:
        ppe('WS-Close failed: ', e)
    
def on_error_data_feeder(ws, error):
    ppe('WS-Error ' + str(ws.url) + ' failed: ', error)

    



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-CON", "--connection", default="127.0.0.1:8079", required=False, help="Connection to data feeder")
    ap.add_argument("-PEPS", "--pixelit_endpoints", required=True, nargs='+', help="Url(s) to pixelit instance(s)")
    ap.add_argument("-TP", "--templates_path", required=True, help="Absolute path to your templates")
    ap.add_argument("-BRI", "--effect_brightness", type=int, choices=range(1, 256), default=DEFAULT_EFFECT_BRIGHTNESS, required=False, help="Brightness of current effect")
    ap.add_argument("-HFO", "--high_finish_on", type=int, choices=range(1, 171), default=None, required=False, help="Individual score for highfinish")
    ap.add_argument("-HF", "--high_finish_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when high-finish occurs")
    ap.add_argument("-AS", "--app_start_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when app starts")
    ap.add_argument("-IDE", "--idle_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when waiting for throw")
    ap.add_argument("-GS", "--game_start_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when game-start occurs")
    ap.add_argument("-MS", "--match_start_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when match-start occurs")
    ap.add_argument("-G", "--game_won_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when game won occurs")
    ap.add_argument("-M", "--match_won_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when match won occurs")
    ap.add_argument("-B", "--busted_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when bust occurs")
    ap.add_argument("-PJ", "--player_joined_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when player-join occurs")
    ap.add_argument("-PL", "--player_left_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition when player-left occurs")
    for v in range(0, 181):
        val = str(v)
        ap.add_argument("-S" + val, "--score_" + val + "_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition for score " + val)
    for a in range(1, 13):
        area = str(a)
        ap.add_argument("-A" + area, "--score_area_" + area + "_effects", default=None, required=False, nargs='*', help="PIXELIT effect-definition for score-area")
    
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=False, required=False, help="If '1', the application will output additional information")

    args = vars(ap.parse_args())

   
    global WS_DATA_FEEDER
    WS_DATA_FEEDER = None



    # ppi('Started with following arguments:')
    # ppi(json.dumps(args, indent=4))

    osType = platform.system()
    osName = os.name
    osRelease = platform.release()
    ppi('\r\n', None, '')
    ppi('##########################################', None, '')
    ppi('       WELCOME TO AUTODARTS-PIXELIT', None, '')
    ppi('##########################################', None, '')
    ppi('VERSION: ' + VERSION, None, '')
    ppi('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease, None, '')
    ppi('SUPPORTED GAME-VARIANTS: ' + " ".join(str(x) for x in SUPPORTED_GAME_VARIANTS), None, '')
    ppi('DONATION: bitcoin:bc1q8dcva098rrrq2uqhv38rj5hayzrqywhudvrmxa', None, '')
    ppi('\r\n', None, '')

    DEBUG = args['debug']
    CON = args['connection']
    PIXELIT_ENDPOINTS = list(args['pixelit_endpoints'])
    PIXELIT_ENDPOINT_PRIMARY = args['pixelit_endpoints'][0]
    TEMPLATES_PATH = Path(args['templates_path'])
    EFFECT_BRIGHTNESS = args['effect_brightness']
    HIGH_FINISH_ON = args['high_finish_on']

    path_status = check_paths(__file__, TEMPLATES_PATH)
    if path_status is not None: 
        ppi('Please check your arguments: ' + path_status)
        sys.exit()  
    
    APP_START_EFFECTS = parse_effects_argument(args['app_start_effects'])
    GAME_START_EFFECTS = parse_effects_argument(args['game_start_effects'])
    MATCH_START_EFFECTS = parse_effects_argument(args['match_start_effects'])
    IDLE_EFFECTS = parse_effects_argument(args['idle_effects'])
    GAME_WON_EFFECTS = parse_effects_argument(args['game_won_effects'])
    MATCH_WON_EFFECTS = parse_effects_argument(args['match_won_effects'])
    BUSTED_EFFECTS = parse_effects_argument(args['busted_effects'])
    HIGH_FINISH_EFFECTS = parse_effects_argument(args['high_finish_effects'])
    PLAYER_JOINED_EFFECTS = parse_effects_argument(args['player_joined_effects'])
    PLAYER_LEFT_EFFECTS = parse_effects_argument(args['player_left_effects'])

    SCORE_EFFECTS = dict()
    for v in range(0, 181):
        parsed_score = parse_effects_argument(args["score_" + str(v) + "_effects"])
        SCORE_EFFECTS[str(v)] = parsed_score
        # ppi(parsed_score)
    SCORE_AREA_EFFECTS = dict()
    for a in range(1, 13):
        parsed_score_area = parse_score_area_effects_argument(args["score_area_" + str(a) + "_effects"])
        SCORE_AREA_EFFECTS[a] = parsed_score_area
        # ppi(parsed_score_area)

    try:
        connect_data_feeder()
    except Exception as e:
        ppe("Connect failed: ", e)


    control_pixelit(APP_START_EFFECTS, "App-started", wake_up=True)


time.sleep(30)