#!/usr/bin/env python3
import os
import json
import sys

from agt import AlexaGadget
from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.console import Console

class MindstormsGadget(AlexaGadget):
    def __init__(self):
        super().__init__(gadget_config_path='./auth.ini')

        self.leds = Leds()
        self.sound = Sound()
        self.console = Console()
        self.console.set_font("Lat15-TerminusBold16.psf.gz", True)

        self.dispense_motor = LargeMotor(OUTPUT_A)
        self.pump_motor = LargeMotor(OUTPUT_B)

        # Start threads
        # threading.Thread(target=self._patrol_thread, daemon=True).start()

    def on_connected(self, device_addr):
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        self.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))

    def on_disconnected(self, device_addr):
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")

    def on_custom_mindstorms_gadget_control(self, directive):
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload), file=sys.stderr)
            control_type = payload["type"]

            # regular voice commands
            if control_type == "automatic":
                self._make()
            
            # series of voice commands
            elif control_type == "manual": # Expected params: [command] 
                control_command = payload["command"]

                if control_command == "dispense":
                    self._dispense()

                elif control_command == "pour":
                    self._pour()

        except KeyError:
            print("Missing expected parameters: {}".format(directive), file=sys.stderr)
    
    def _make(self, options=None):
        self.sound.speak("Dispensing boba")

        # dispense boba

        # sound.speak("Dispensing " + tea)

        # dispense liquid
        self._pour(10)

        # s = name + ", your boba drink is finished. Please come pick it up"

        # console.text_at(
        #     s, column=mid_col, row=mid_row, alignment=alignment, reset_console=True
        # )

        # sound.speak(s)

    # dispense liquid
    def _pour(self, time_in_s=10):
        self.dispense_motor.run_forever(speed_sp=1000)
        sleep(time_in_s)
        self.pump_motor.stop()

    # dispense boba
    def _dispense(self, cycles=10):
        # ensure the dispenser resets to the correct position everytime
        if cycles % 2:
            cycles += 1

        # agitate the boba to make it fall
        for _ in range(cycles):
            deg = 45 if cycles % 2 else -45
            self.dispense_motor.on_for_degrees(SpeedPercent(75), deg)
            sleep(0.5)

if __name__ == '__main__':

    gadget = MindstormsGadget()

    # Set LCD font and turn off blinking LEDs
    os.system('setfont Lat7-Terminus12x6')
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")

    # Startup sequence
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
