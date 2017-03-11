# OctoPrint-LEDmyprinterglow

Howdy Buddies,
This is my first version of "LED my printer glow". It's a small (and at the moment a poor) plugin for OctoPrint to control LED strips.

You can check my page on http://www.rapidforge.de/2016/02/led-my-printer-glow/ to see how it works.

I didn't realized the automatic installer for OctoPrint yet (maybe I'm too stupid).

Feel free to comment or, it's better, try to support this nice little application.

**UPDATE 03/11/2017 - Currently I'm working on another project. So (for me) it's still on hold!**

One problem is that this small addon works just with Raspian Weezy and I don't find the time to fixed that. Sorry for that!

# What do I need for this tool?

The first and most important thing is a LED strip. I'm currently using a LED strip from the big Swedish home center. But there are a lot of other manufactures who can deliver such a thing.
If you got it than you have to hack it and connect it with your pi. Please follow this link for the well explained instruction http://popoklopsi.github.io/RaspberryPi-LedStrip/#/.

**ATTENTION! EVERY WORK ON CIRCUITS HAS TO BE DONE BY TRAINED PERSON(S)! I'M (and the following authors are) NOT RESPONSIBLE FOR DAMAGES! DO THIS ON YOUR OWN RISK!**

Now it's time to prepare your Pi operation system. So you have to install the pigpio daemon from this page http://abyz.co.uk/rpi/pigpio/download.html with these commands:
```bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
```

Sweet but it won't work right now because this isn't ready. Or you have to run the OctoPrint as root. This little detour will start pigpio as daemon. Type `sudo crontab -e` and put the following line at the end of this file:
```
@reboot              /usr/local/bin/pigpiod
```

Now you can clone the plugin into the OctoPrint Plugin folder
```bash
cd ~/.octoprint/plugins
git clone https://github.com/calliconfused/OctoPrint-LEDmyprinterglow
```

After this the plugin is availible under options and plugin.

That's all and have fun!
