#import appdaemon.plugins.hass.hassapi as hass
import requests
import json
import time
import argparse
import logging

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)

def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if debug:
        logger.exception("\r\n" + str(error_object))
        
def load_template(name):
    try: 
      fp = open(args["path"]+name,"r")
      data = json.load(fp)
      data["screen"] = name.replace(".json","")
      fp.close()
      return data
    except Exception as e:
      ppe("Template not found: ", e)
      return None

def push_config():
    try: 
      fp = open(args["path"]+"pixelit_config.json","r")
      data = json.load(fp)
      requests.post('http://' + args["IP"] + '/api/config',data=json.dumps(data), headers={'Content-Type': 'application/data'})
      if debug: ppi("Hardware Initialized")
    except Exception as e:
      ppe("Hardware Initialized failed", e)
      return None

def rest_add(kwargs):
    if debug: ppi("pixelit_add: " +str(kwargs))
      
    try:
      data = load_template(kwargs["title"])
      if len(kwargs["message"]) and (kwargs["title"] != "clock.json"):
        data["text"]["textString"] = kwargs["message"]

      display(data)
      response = {"length playlist": len(playlist)}

    except Exception as e:
      ppe("Unable to add screen", e)
      response = {"error": "message or title missing"}


def rest_delete(kwargs):
    if debug: ppi("rest_delete: "+str(kwargs))
    if alertMsg != None:
      if debug: ppi("rest_delete: alert")
      if alertMsg["screen"] == kwargs["title"]: alertMsg = None
    if warningMsg != None:
      if debug: ppi("rest_delete: warning")
      if warningMsg["screen"] == kwargs["title"]: warningMsg = None
    try:
      for msg in playlist:
        if msg["screen"] == kwargs["title"]:
          if msg.get("target") == "alert": alertMsg = None
          playlist.remove(msg)
      response = {"playlist": len(playlist)}
    except:
      ppe("Unable to delete screen",e)
      response = {"error": "screen not deleted"}

def rest_update(kwargs):
    found = False
    if debug: ppi("rest_update: " + str(kwargs))
    try:
      for msg in playlist:
        if msg["screen"] == kwargs["title"]:
          found = True
          template = load_template(kwargs["title"]+".json")
          if template != None:
            for key in kwargs:
              if key=="message":
                template["text"]["textString"] = kwargs["message"]
          else:
            if debug: ppi("screen not found: " + kwargs["title"])
      response = {"playlist": len(playlist)}
      if found:
        return response, 200
      else:
        rest_add(kwargs)
        return response, 200
    except:
      ppi("Unable to update screen",e)
      response = {"error": "screen not deleted"}
      return response, 400  

def display(msg):
    #if debug: ppi("display: " + json.dumps(msg))
    try: 
      r = requests.post(url,data=json.dumps(msg, ensure_ascii=False).encode('utf8'), headers={'Content-Type': 'application/data'})
      if debug: ppi("display return: " +r.text)
    except Exception as e:
      ppe("Error while sending to display.", e)
      
      
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-CON", "--connection", default="127.0.0.1:8079", required=False, help="Connection to data feeder")
    ap.add_argument("-IP", "--IP", default="192.168.3.55", required=True, help="IP to LED Matrix")
    ap.add_argument("-PATH", "--path", default="template/", required=True, help="Path to templates")

    args = vars(ap.parse_args())

#def initialize():
    url = 'http://' + args["IP"] + '/api/screen'
    playlist = []
    debug = True
    sleepMode = False
    pointer = 0
    showAlert = True
    alertMsg = None
    warningMsg = None
    # push_config()

    #Pixelit templates
    text='data.json'
    call='call.json'
    clock='clock.json'
    default='default.json'
    temperature='temperature.json'
    xmas = 'xmas.json' 
    alarm = 'alarm.json'
    dart = 'dart.json'
    points = 'points.json'
    board = 'board.json'

    #test use template points.json with dynamic message
    message = "Game on Player"
    kwargs ={"title": board, "message": message}
    rest_add(kwargs)
    time.sleep(10)
    
    #test use template points.json with dynamic message
    message = "180"
    kwargs ={"title": points, "message": message}
    rest_add(kwargs)
    time.sleep(5)
    
    #test use template call.json with dynamic message
    message = "Lets play Darts -==-<"
    kwargs ={"title": call, "message": message}
    rest_add(kwargs)
    time.sleep(10)

    #test endless loop busted animation
    i = 0
    while i <= 12:
        message = ""
        kwargs = {"title": 'dart' + str(i) + '.json', "message": message}
        rest_add(kwargs)
        time.sleep(0.2)
        i += 1
        if i == 12:
            i = 0
      
time.sleep(30)




