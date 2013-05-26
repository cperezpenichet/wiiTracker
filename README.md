wiiTracker
==========

WiiTracker is a very simple graphical application that tracks the position of a Wii remote based on the accelerometer readings and draws it on the screen.

Dependencies
------------

You need to install the cwiid driver from [here](http://abstrakraft.org/cwiid/#Download) or from your distribution's package manager.

It is also possible that you need to install [Glade](http://abstrakraft.org/cwiid/#Download).

Configuration
-------------

You will have to set the address of your particular Wii remote in the Preferences dialog before the application can correctly pair with your remote. The `lswm` command, which is part of the cwiid distribution, can be used to find out the address.

