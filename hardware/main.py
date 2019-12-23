#!/usr/bin/env python3
import os
import json
import sys
import threading

from agt import AlexaGadget
from time import sleep
from queue import Queue

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_1 
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.console import Console

class MindstormsGadget(AlexaGadget):
    def __init__(self):
        super().__init__(gadget_config_path='./auth.ini')

        # order queue
        self.queue = Queue()

        self.button = Button()
        self.leds = Leds()
        self.sound = Sound()
        self.console = Console()
        self.console.set_font("Lat15-TerminusBold16.psf.gz", True)

        self.dispense_motor = LargeMotor(OUTPUT_A)
        self.pump_motor = LargeMotor(OUTPUT_B)
        self.touch_sensor = TouchSensor(INPUT_1)

        # Start threads
        threading.Thread(target=self._handle_queue, daemon=True).start()
        threading.Thread(target=self._test, daemon=True).start()

    def on_connected(self, device_addr):
        self.leds.animate_rainbow(duration=3, block=False)
        self.sound.play_song((('C4', 'e3'),('C5', 'e3')))

    def on_disconnected(self, device_addr):
        self.leds.animate_police_lights('RED', 'ORANGE', duration=3, block=False)
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        self.sound.play_song((('C5', 'e3'),('C4', 'e3')))

    def _test(self):
        while 1:
            self.button.wait_for_pressed('up')
            order = {
                'name': 'Test', 
                'tea': 'Jasmine',
                'sugar': 100,
                'ice': 100
            }
            self.queue.put(order)
            sleep(1)

    def _handle_queue(self):
        while 1:
            if self.queue.empty(): continue

            order = self.queue.get()
            self._make(name=order['name'], tea=order['tea'], sugar=order['sugar'], ice=order['ice'])

    def _send_event(self, name, payload):
        self.send_custom_event('Custom.Mindstorms.Gadget', name, payload)

    def _affirm_receive(self):
        self.leds.animate_flash('GREEN', sleeptime=0.25, duration=0.5, block=False)
        self.sound.play_song((('C3', 'e3'),('C3','e3')))

    def on_custom_mindstorms_gadget_control(self, directive):
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload), file=sys.stderr)
            control_type = payload["type"]

            # regular voice commands
            if control_type == "automatic":
                self._affirm_receive()
                order = {
                    "name": payload["name"] or "Anonymous",
                    "tea": payload["tea"] or "Jasmine Milk Tea",
                    "sugar": payload["sugar"] or 100,
                    "ice": payload["ice"] or 100,
                }
                self.queue.put(order)
            
            # series of voice commands
            elif control_type == "manual": # Expected params: [command] 
                control_command = payload["command"]

                if control_command == "dispense":
                    self._affirm_receive()
                    if payload['num']:
                        self._dispense(payload['num'])
                    else: 
                        self._dispense()

                elif control_command == "pour":
                    self._affirm_receive()
                    if payload['num']:
                        self._pour(payload['num'])
                    else: 
                        self._pour()

        except KeyError:
            print("Missing expected parameters: {}".format(directive), file=sys.stderr)
    
    def _make(self, name=None, tea="Jasmine Milk Tea", sugar=100, ice=100):
        if not self.touch_sensor.is_pressed:
            # cup is not in place
            self._send_event('CUP', None)
            self.touch_sensor.wait_for_pressed()
            sleep(3) # cup enter delay

        # mid_col = console.columns // 2
        # mid_row = console.rows // 2
        # mid_col = 1
        # mid_row = 1
        # alignment = "L"

        process = self.sound.play_file('mega.wav', 100, Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        # dispense boba
        self._dispense()

        # dispense liquid
        self._pour(tea=tea)

        # self.console.text_at(
        #     s, column=mid_col, row=mid_row, alignment=alignment, reset_console=True
        # )
        # notify alexa that drink is finished
        payload = {
            "name": name,
            "tea": tea,
            "sugar": sugar,
            "ice": ice,
        }
        self._send_event("DONE", payload)

        process.kill() # kill song
        self.sound.play_song((('C4', 'q'),('C4', 'q'),('C4', 'q')), delay=0.1)
        self.touch_sensor.wait_for_released()

    # dispense liquid
    def _pour(self, time_in_s=10, tea="Jasmine Milk Tea"):
        # send event to alexa
        payload = {
            "time_in_s": time_in_s,
            "tea": tea
        }
        self._send_event("POUR", payload)
        self.pump_motor.run_forever(speed_sp=1000)
        sleep(time_in_s)
        self.pump_motor.stop()

    # dispense boba
    def _dispense(self, cycles=10):
        # send event to alexa
        payload = {
            "cycles": cycles
        }
        self._send_event("DISPENSE", payload)

        # ensure the dispenser resets to the correct position everytime
        if cycles % 2:
            cycles += 1

        # agitate the boba to make it fall
        for i in range(cycles):
            deg = 45 if i % 2 else -45
            self.dispense_motor.on_for_degrees(SpeedPercent(75), deg)
            sleep(0.5)

if __name__ == '__main__':
    print('Starting')
    gadget = MindstormsGadget()

    # Set LCD font and turn off blinking LEDs
    os.system('setfont Lat7-Terminus12x6')
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")

    # Startup sequence
    gadget.sound.play_song((('C4', 'e3'),('E4', 'e3')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('C4', 'e3'), ('E3', 'e3')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
