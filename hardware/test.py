#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from ev3dev2.sound import Sound

from time import sleep

import requests

url = 'http://5aaacbd4.ngrok.io'

while True:
    r = requests.get(url+'/state')
    res = r.json()
    if(res['state']==1):
        m = LargeMotor(OUTPUT_A)
        m.on_for_rotations(SpeedPercent(75), 5)

        sound = Sound()
        sound.speak('Your boba drink is finished!')
        
        requests.post(url+'/state', json={ 'state': 0 })

    sleep(1)
