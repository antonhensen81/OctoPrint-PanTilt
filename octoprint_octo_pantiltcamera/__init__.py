# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import sarge
import flask
from time import sleep
import RPi.GPIO as GPIO

class Octo_pantiltcameraPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SimpleApiPlugin, octoprint.plugin.StartupPlugin):
    def __init__(self):
        self.panValue = 0
        self.tiltValue = 0

    def on_after_startup(self):
        self.panValue = int(self._settings.get(["pan", "initialValue"]))
        self.tiltValue = int(self._settings.get(["tilt", "initialValue"]))
        self.panPort = int(self._settings.get(["pan", "gpio"]))
        self.tiltPort = int(self._settings.get(["tilt", "gpio"]))

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.panPort, GPIO.OUT)
        GPIO.setup(self.tiltPort, GPIO.OUT)

        self.setAngles(self.panValue, self.tiltValue)

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        return dict(
            pan=dict(
                stepSize=5,
                initialValue=30,
                minValue=0,
                maxValue=50,
                gpio=17,
                invert=True),
            tilt=dict(
                stepSize=5,
                initialValue=95,
                minValue=50,
                maxValue=120,
                gpio=18,
                invert=False,
            ),
        )

    def setServoAngle(self, servo, angle):
        pwm = GPIO.PWM(servo, 50)
        pwm.start(8)
        dutyCycle = angle / 18.0 + 3.0
        pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.3)
        pwm.stop()

    def limitValues(self, panValue, tiltValue):
        self.panValue = min(panValue, int(self._settings.get(["pan", "maxValue"])))
        self.panValue = max(self.panValue, int(self._settings.get(["pan", "minValue"])))
        self.tiltValue = min(tiltValue, int(self._settings.get(["tilt", "maxValue"])))
        self.tiltValue = max(self.tiltValue, int(self._settings.get(["tilt", "minValue"])))

    def setAngles(self, panValue, tiltValue):
        self.limitValues(panValue, tiltValue)
        self._logger.info("pan: {}".format(self.panValue))
        self._logger.info("tilt: {}".format(self.tiltValue))
        self.setServoAngle(self.panPort, self.panValue)
        self.setServoAngle(self.tiltPort, self.tiltValue)

    def get_assets(self):
        return dict(js=["js/octo_pantiltcamera.js"], css=["css/octo_pantiltcamera.css"], less=["less/octo_pantiltcamera.less"])

    def get_api_commands(self):
        return dict(set=[], left=[], right=[], up=[], down=[])

    def on_api_command(self, command, data):
        if command == "set":
            if "panValue" in data:
                panValue = int(data["panValue"])
            if "tiltValue" in data:
                tiltValue = int(data["tiltValue"])
            self.setAngles(panValue, tiltValue)
        elif command == "left" or command == "right":
            panValue = int(self.panValue)

            stepSize = int(self._settings.get(["pan", "stepSize"]))
            if stepSize in data:
                stepSize = int(data["stepSize"])

            if self._settings.get(["pan", "invert"]):
                panValue = panValue - (stepSize if command == "right" else -stepSize)
            else:
                panValue = panValue + (stepSize if command == "right" else -stepSize)

            self.setAngles(panValue, self.tiltValue)
        elif command == "up" or command == "down":
            tiltValue = int(self.tiltValue)

            stepSize = int(self._settings.get(["tilt", "stepSize"]))
            if stepSize in data:
                stepSize = int(data["stepSize"])

            if self._settings.get(["tilt", "invert"]):
                tiltValue = tiltValue - (stepSize if command == "up" else -stepSize)
            else:
                tiltValue = tiltValue + (stepSize if command == "up" else -stepSize)

            self.setAngles(self.panValue, tiltValue)

    def on_api_get(self, request):
        return flask.jsonify(panValue=self.panValue, tiltValue=self.tiltValue)

    def get_update_information(self):
        return dict(
            octo_pantiltcamera=dict(
                displayName="Pan/Tilt Plugin",
                displayVersion=self._plugin_version,
                type="github_release",
                user="antonhensen81",
                repo="OctoPrint-OctoPrint-PanTilt",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/antonhensen81/OctoPrint-PanTilt/archive/{target_version}.zip",
            )
        )

__plugin_name__ = "OctoPrint Pan Tilt Camera"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octo_pantiltcameraPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information}
