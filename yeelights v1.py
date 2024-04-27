import os
from pyclbr import Function
import time
import threading
from ast import FunctionDef, arg
from concurrent.futures import thread
from ipaddress import ip_address
from os import name
from unittest.util import three_way_cmp
from warnings import catch_warnings
from flask import Flask, request
from yeelight import *
from yeelight.transitions import *
from yeelight import Bulb
from yeelight import LightType
from threading import Thread

app = Flask(__name__)

# Ustawienie pulsowania 
#===============================
def GreenPulse():
    transitions = [
        HSVTransition(120,100,2000,100),
        HSVTransition(120,20,2000,1),
    ]
    return transitions

def RedPulse():
    transitions = [
        HSVTransition(0,100,2000,100),
        HSVTransition(0,100,2000,1),
    ]
    return transitions

def YellowPulse():
    transitions = [
        HSVTransition(39,100,2000,100),
        HSVTransition(39,20,2000,1),
    ]
    return transitions
#================================

#Ustawienie flow dla pulsowania
#================================
flow_blue = Flow(count=30,transitions= pulse(0, 0, 255))
flow_Green = Flow(transitions= GreenPulse())
flow_Red = Flow(transitions= RedPulse())
flow_Yellow = Flow(transitions= YellowPulse())
#================================

@app.route('/main/', methods=['POST'])

def main():
    
    get_ip = request.args.get('yeelight_ip')
    get_colour = request.args.get('colour')
    get_process = request.args.get('process')
    #Sprawdzenie czy funkcja istnieje + wywolanie jezeli tak.
#================================
    try:
    #Zamiana STR nazwy procesu na obiekt function - globals()[nazwa funkcji]
        function_process_name = globals()[get_process]
    except (Exception,NameError,KeyError):
        print('Error - process ' + get_process + ' not exist')
        return 'Error - process ' + get_process + ' not exist'    
    else:    
        Thread(name=get_ip, target=function_process_name,args=(get_ip,get_colour,get_process,),daemon=True).start()

        return 'Ok'
#================================

def CountThread(get_ip_address):
    """Liczennie ilosci watkow dla danego IP zeby 
    wiedziec czy nie wisza jakies poprzednie zadania dla IP"""
    
    counthreads = 0     
    for thread in threading.enumerate():
        if thread.name == get_ip_address:
            counthreads += 1
    return counthreads
    
def LOCO(get_ip,get_colour,get_process):

    print(get_ip,get_process, get_colour)

    bulb_ip = Bulb(get_ip)
    
    if get_colour == 'GREEN':
        
        bulb_ip.turn_on()
        bulb_ip.set_hsv(120,100,100)
        bulb_ip.set_brightness(10)
        time.sleep(60)
            
        if CountThread(get_ip) == 1:
            bulb_ip.start_flow(flow_Green)
            time.sleep(30)
            if CountThread(get_ip) == 1:             
                bulb_ip.stop_flow()
                bulb_ip.turn_off()
        return 'ok'
        
    elif get_colour == 'RED':
            
        bulb_ip.turn_on()
        bulb_ip.set_hsv(0,100,100)
        bulb_ip.set_brightness(10)
        #time sleep zeby nie zamykac watku, potrzebne do liczenia watkow CountThread
        time.sleep(60)

        return 'ok'
        
    elif get_colour == 'YELLOW':
            
        bulb_ip.turn_on()
        bulb_ip.set_hsv(39,100,100)
        bulb_ip.set_brightness(10)
        #time sleep zeby nie zamykac watku, potrzebne do liczenia watkow CountThread
        time.sleep(60)
        return 'ok'
        
    elif get_colour == 'OBA':
            
        bulb_ip.turn_on()
        bulb_ip.set_hsv(240,100,100)
        bulb_ip.set_brightness(10)
        #bulb_ip.set_rgb(0, 0, 255)
        time.sleep(60)
        #bulb_ip.turn_off()
        
        return 'ok'

if __name__ == "__main__":
    #IP DOMENA
    app.run(host='172.16.4.100', port= 5001, threaded=True)
    #IP SERWIS, SIEC ENG
    #app.run(host='192.168.100.245', port= 5001)