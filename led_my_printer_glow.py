# coding=utf-8
from __future__ import absolute_import

import pigpio
import time
import octoprint.plugin
from octoprint.events import Events

pi = pigpio.pi()

__plugin_name__ = "LED my printer glow"
__plugin_version__ = "0.1.0"
__plugin_description__ = "Handle LED strips in your printers box"
__plugin_author__ = "Pascal Burbach <alpenmaxx@gmx.de>"
__plugin_license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__plugin_url__ = "http://www.rapidforge.de"

# Set GPIO with color
PIN_RED = 17	# GPIO 17 = pin 11 with color red
PIN_GRN = 22	# GPIO 22 = pin 15 with color green
PIN_BLU = 24	# GPIO 24 = pin 18 with color blue

class LEDprinterglow(octoprint.plugin.StartupPlugin,
					 octoprint.plugin.ShutdownPlugin,
					 octoprint.plugin.EventHandlerPlugin):
	
	def on_after_startup(self):
		self._logger.info("Start LED my printer glow")
		COLOR_SWITCH(  0,   0,   0, 255, 255, 255, 1.00)
		COLOR_SWITCH(255, 255, 255,   0,   0,   0, 0.50)
		COLOR_SWITCH(  0,   0,   0, 255,   0,   0, 0.10)
		time.sleep(0.5)
		COLOR_SWITCH(255,   0,   0, 255, 255,   0, 0.10)
		time.sleep(0.5)
		COLOR_SWITCH(255, 255,   0,   0, 255,   0, 0.10)
		time.sleep(0.5)
		COLOR_SWITCH(  0, 255,   0,   0, 255, 255, 0.10)
		time.sleep(0.5)
		COLOR_SWITCH(  0, 255, 255,   0,   0, 255, 0.10)
		time.sleep(0.5)
		COLOR_SWITCH(  0,   0, 255, 255, 255, 255, 1.00)
		
	def on_shutdown(self):
		COLOR_SWITCH(255, 255, 255,   0,   0,   0, 1.00)
		self._logger.info("Shutdown LED my printer glow")
	
	def on_event(self, event, payload):
		if event == Events.PRINT_STARTED:
			COLOR_SWITCH(255, 255, 255, 255,   0,   0, 1.00)
			
		if event == Events.PRINT_PAUSED:
			COLOR_SWITCH(255,   0,   0,   0, 255, 255, 1.00)	

		if event == Events.PRINT_RESUMED:
			COLOR_SWITCH(  0, 255, 255, 255,   0,   0, 1.00)			
		
		if event == Events.PRINT_CANCELLED:
			COLOR_SWITCH(255,   0,   0, 255, 128,   0, 1.00)
			time.sleep(25)
			COLOR_SWITCH(255, 128,   0, 255, 255, 255, 1.00)
			
		if event == Events.PRINT_DONE:
			COLOR_SWITCH(255,   0,   0,   0, 255,   0, 1.00)
			time.sleep(25)
			COLOR_SWITCH(  0, 255,   0, 255, 255, 255, 1.00)
			
__plugin_implementation__ = LEDprinterglow()

def COLOR_SWITCH(SOURCE_RED, SOURCE_GRN, SOURCE_BLU, TARGET_RED, TARGET_GRN, TARGET_BLU, STP_SEC):
	NOLOOPS = 100
	for x in range(1, NOLOOPS + 1):
	
		# check if numbers are in range of 0 to 255
		if SOURCE_RED > 255:
			SOURCE_RED = 255
		elif SOURCE_RED < 0:
			SOURCE_RED = 0
			
		if SOURCE_GRN > 255:
			SOURCE_GRN = 255
		elif SOURCE_GRN < 0:
			SOURCE_GRN = 0	
			
		if SOURCE_BLU > 255:
			SOURCE_BLU = 255
		elif SOURCE_BLU < 0:
			SOURCE_BLU = 0
			
		if TARGET_RED > 255:
			TARGET_RED = 255
		elif TARGET_RED < 0:
			TARGET_RED = 0
			
		if TARGET_GRN > 255:
			TARGET_GRN = 255
		elif TARGET_GRN < 0:
			TARGET_GRN = 0
			
		if TARGET_BLU > 255:
			TARGET_BLU = 255	
		elif TARGET_BLU < 0:
			TARGET_BLU = 0
		
		if TARGET_RED - SOURCE_RED < 0:
			CURRENT_RED = SOURCE_RED - (int((SOURCE_RED - TARGET_RED) / float(NOLOOPS) * x))
		elif TARGET_RED - SOURCE_RED == 0:
			CURRENT_RED = TARGET_RED
		elif TARGET_RED - SOURCE_RED > 0:
			CURRENT_RED = int((SOURCE_RED - TARGET_RED) / float(NOLOOPS) * x) * -1
	
		if TARGET_GRN - SOURCE_GRN < 0:
			CURRENT_GRN = SOURCE_GRN - (int((SOURCE_GRN - TARGET_GRN) / float(NOLOOPS) * x))
		elif TARGET_GRN - SOURCE_GRN == 0:
			CURRENT_GRN = TARGET_GRN
		elif TARGET_GRN - SOURCE_GRN > 0:
			CURRENT_GRN = int((SOURCE_GRN - TARGET_GRN) / float(NOLOOPS) * x) * -1

		if TARGET_BLU - SOURCE_BLU < 0:
			CURRENT_BLU = SOURCE_BLU - (int((SOURCE_BLU - TARGET_BLU) / float(NOLOOPS) * x))
		elif TARGET_BLU - SOURCE_BLU == 0:
			CURRENT_BLU = TARGET_BLU
		elif TARGET_BLU - SOURCE_BLU > 0:
			CURRENT_BLU = int((SOURCE_BLU - TARGET_BLU) / float(NOLOOPS) * x) * -1

		pi.set_PWM_dutycycle(PIN_RED, CURRENT_RED)
		pi.set_PWM_dutycycle(PIN_GRN, CURRENT_GRN)
		pi.set_PWM_dutycycle(PIN_BLU, CURRENT_BLU)

		time.sleep(float(STP_SEC) / NOLOOPS)
