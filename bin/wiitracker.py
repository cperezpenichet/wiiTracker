#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk

# Check if we are working in the source tree or from the installed 
# package and mangle the python path accordingly
if os.path.dirname(sys.argv[0]) != ".":
    if sys.argv[0][0] == "/":
        fullPath = os.path.dirname(sys.argv[0])
    else:
        fullPath = os.getcwd() + "/" + os.path.dirname(sys.argv[0])
else:
    fullPath = os.getcwd()
sys.path.insert(0, os.path.dirname(fullPath))

from wiitracker import AboutWiitrackerDialog, PreferencesWiitrackerDialog
from wiitracker.wiitrackerconfig import getdatapath

class WiitrackerWindow(gtk.Window):
    __gtype_name__ = "WiitrackerWindow"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation a WiitrackerWindow requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling WiitrackerWindow.finish_initializing().

        Use the convenience function NewWiitrackerWindow to create
        WiitrackerWindow object.

        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a WiitrackerWindow object with it in order to finish
        initializing the start of the new WiitrackerWindow instance.

        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #uncomment the following code to read in preferences at start up
        #dlg = PreferencesWiitrackerDialog.NewPreferencesWiitrackerDialog()
        #self.preferences = dlg.get_preferences()

        #code for other initialization actions should be added here

    def about(self, widget, data=None):
        """about - display the about box for wiitracker """
        about = AboutWiitrackerDialog.NewAboutWiitrackerDialog()
        response = about.run()
        about.destroy()

    def preferences(self, widget, data=None):
        """preferences - display the preferences window for wiitracker """
        prefs = PreferencesWiitrackerDialog.NewPreferencesWiitrackerDialog()
        response = prefs.run()
        if response == gtk.RESPONSE_OK:
            #make any updates based on changed preferences here
            pass
        prefs.destroy()

    def quit(self, widget, data=None):
        """quit - signal handler for closing the WiitrackerWindow"""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """on_destroy - called when the WiitrackerWindow is close. """
        #clean up code for saving application state should be added here

        gtk.main_quit()

def NewWiitrackerWindow():
    """NewWiitrackerWindow - returns a fully instantiated
    WiitrackerWindow object. Use this function rather than
    creating a WiitrackerWindow directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'WiitrackerWindow.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    window = builder.get_object("wiitracker_window")
    window.finish_initializing(builder)
    return window

if __name__ == "__main__":
    #support for command line options
    import logging, optparse
    parser = optparse.OptionParser(version="%prog %ver")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show debug messages")
    (options, args) = parser.parse_args()

    #set the logging level to show debug messages
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('logging enabled')

    #run the application
    window = NewWiitrackerWindow()
    window.show()
    gtk.main()

