# OctoPrint Pan Tilt Camera

Provides support for controlling two servos using GPIO so a pan tilt camera can be controlled.

Based on https://github.com/Salandora/OctoPrint-PanTilt, but instead of calling a script it directly controls two GPIO pins. Also fixed a couple of issues and changed some parts I disliked.

I used this [3D Print](https://www.thingiverse.com/thing:708819), but you can use any design that uses two servos.

## Demo
Click the image below for a short demo.

[![Demo Pan Tilt Plugin](https://raw.githubusercontent.com/antonhensen81/OctoPrint-PanTilt/master/images/demo.png)](https://www.youtube.com/watch?v=HLaBd1Q5k40)


## Wiring

The default wiring looks as shown below. Although other scenarios are possible as well and GPIO pins can be configured to be what you like.

![Wiring](https://raw.githubusercontent.com/antonhensen81/OctoPrint-PanTilt/master/images/wiring.png)


## Setup

Install via the bundled [Plugin Manager](http://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) using this URL: [https://github.com/antonhensen81/OctoPrint-PanTilt/archive/master.zip](https://github.com/antonhensen81/OctoPrint-PanTilt/archive/master.zip)

You will find the plugin manager in OctoPrint under settings. Then select "Get more..." and paste the URL in "... from URL" like shown below and click Install.

![Install](https://raw.githubusercontent.com/antonhensen81/OctoPrint-PanTilt/master/images/install.png)

## Configuration

- Ensure that you have the correct GPIO pins configured for both Pan and Tilt. If you need to change the port numbers you will have to restart.
- Find the limits that work for your servos and configure them accordingly (min, max), just like the initial values for both the pan and tilt servos.
- If needed you can invert the direction either servo.

![Configuration](https://raw.githubusercontent.com/antonhensen81/OctoPrint-PanTilt/master/images/configuration.png)

