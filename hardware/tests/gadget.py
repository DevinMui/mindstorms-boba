#!/usr/bin/env python3
import os

from agt import AlexaGadget

from ev3dev2.led import Leds
from ev3dev2.sound import Sound

class MindstormsGadget(AlexaGadget):
	"""
	A Mindstorms gadget that performs movement based on voice commands.
	Two types of commands are supported, directional movement and preset.
	"""

	def __init__(self):
		"""
		Performs Alexa Gadget initialization routines and ev3dev resource allocation.
		"""
		super().__init__(gadget_config_path='../auth.ini')

		# Ev3dev initialization
		self.leds = Leds()
		self.sound = Sound()

		# Start threads
		# threading.Thread(target=self._patrol_thread, daemon=True).start()

	def on_connected(self, device_addr):
		"""
		Gadget connected to the paired Echo device.
		:param device_addr: the address of the device we connected to
		"""
		self.leds.set_color("LEFT", "GREEN")
		self.leds.set_color("RIGHT", "GREEN")
		self.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))

	def on_disconnected(self, device_addr):
		"""
		Gadget disconnected from the paired Echo device.
		:param device_addr: the address of the device we disconnected from
		"""
		self.leds.set_color("LEFT", "BLACK")
		self.leds.set_color("RIGHT", "BLACK")

	def on_custom_mindstorms_gadget_control(self, directive):
		"""
		Handles the Custom.Mindstorms.Gadget control directive.
		:param directive: the custom directive with the matching namespace and name
		"""

		pass

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
