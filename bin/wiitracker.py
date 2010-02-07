#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk
from gtk.gdk import threads_init

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
from wiitracker.Wii3DTracker import Wii3DTracker
from wiitracker.WiiConnectionMaker import WiiConnectionMaker
from wiitracker.util import ARROW, rotateMoveScale, rotateMove
import gobject
from math import pi

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

    def finish_initializing(self, builder, wiiAddress):
        """finish_initalizing should be called after parsing the ui definition
        and creating a WiitrackerWindow object with it in order to finish
        initializing the start of the new WiitrackerWindow instance.

        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)
        self.tracker = Wii3DTracker(wiiAddress)

        #uncomment the following code to read in preferences at start up
        #dlg = PreferencesWiitrackerDialog.NewPreferencesWiitrackerDialog()
        #self.preferences = dlg.get_preferences()

        #code for other initialization actions should be added here
        self.statusBar = builder.get_object("statusbar")
        self.status_context = self.statusBar.get_context_id('')
        self.rollDrawing = builder.get_object('rollDrawing')
        self.pitchDrawing = builder.get_object('pitchDrawing')

        self.menuConnect = builder.get_object('menuitem_Connect')
        self.menuTrack = builder.get_object('menuitem_Track')
        self.menuConnectTrack = builder.get_object('menuitem_ConnectTrack')
        self.menuRumble = builder.get_object('menuitem_Rumble')
        

        self.__connectTrack_source = 0
        
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
        self.set_sensitive(False)
        self.tracker.stopping = True
        if self.tracker.wiiMote:
            gobject.timeout_add(10, self.tracker.wiiMote.close)
        gobject.timeout_add(20, gtk.main_quit)
        
    def __connectCallback(self, connectionMaker):
        if connectionMaker.connected:
            self.menuTrack.set_sensitive(True)
            self.menuRumble.set_sensitive(True)
            self.tracker.wiiMote = connectionMaker.wiiMote
            self.tracker.acc_cal = connectionMaker.acc_cal
            self.tracker.connected = True
        else:
            self.menuConnect.set_sensitive(True)
            self.menuConnectTrack.set_sensitive(True)
            if self.__connectTrack_source:
                gobject.source_remove(self.__connectTrack_source)
        
    def on_menuitem_Connect(self, widget, data=None):
        """called when the menuitem_Connect is clicked"""
        self.menuConnect.set_sensitive(False)
        self.menuConnectTrack.set_sensitive(False)
        connectionMaker = WiiConnectionMaker(self.tracker.wiiAddress,
                                             self.statusBar,
                                             self.__connectCallback)
        connectionMaker.start()
        
    def on_menuitem_Track(self, widget, data=None):
        """called when the menuitem_Tack is clicked"""
        if not self.tracker.connected:
            return True
        
        self.roll_gdkWindow = self.rollDrawing.window
        self.pitch_gdkWindow = self.pitchDrawing.window
        self.gc = self.roll_gdkWindow.new_gc()        
        self.__CENTER = (self.roll_gdkWindow.get_geometry()[2]/2,
                         self.roll_gdkWindow.get_geometry()[3]/2)
        
        self.menuTrack.set_sensitive(False)
        gobject.timeout_add(9, self.__paint)
        return False
    
    def on_menuitem_ConnectTrack(self, widget, data=None):
        self.on_menuitem_Connect(widget, data)
        self.__connectTrack_source = gobject.timeout_add(100,
                                                         self.on_menuitem_Track,
                                                         widget, data)
        
    def on_menuitem_Rumble(self, widget, data=None):
        self.tracker.wiiMote.rumble = widget.active
        
    def __paint(self):
        angles = self.tracker.getAngles()
            
        self.statusBar.pop(self.status_context)     
        self.statusBar.push(self.status_context,
#                                     "R:%6.0f°\tP:%6.0f°\tSd (angles[0] *0 / pi, 
#                                                              gles[1] * 180 / pi,
#                                                         self.tracker.filt_state))
                            "R:%6.0f°\tP:%6.0f°" % (angles[0] * 180 / pi, 
                                                    (angles[1]+pi/2) * 180 / pi,))
            
        self.roll_gdkWindow.clear()
        self.roll_gdkWindow.draw_polygon(self.gc,
                                         True,
                                         rotateMoveScale(ARROW, 
                                                    angles[0], 
                                                    self.__CENTER,
                                                    (1, 0.5))
                                        )
        self.pitch_gdkWindow.clear()
        self.pitch_gdkWindow.draw_polygon(self.gc,
                                          True,
                                          rotateMove(ARROW, 
                                                     angles[1]+pi/2, 
                                                     self.__CENTER)
                                          )
        
        #=======================================================================
        # 3D stuff
        #=======================================================================
#        THETA = 0
#        self.transform.RotateY(THETA * 180 / pi)
#
#        # Pitch
#        self.transform.RotateWXYZ(-angles[1] * 180 / pi,
#                             cos(THETA),
#                             0,
#                             sin(THETA))
#
##        Roll
#        self.transform.RotateWXYZ(-angles[0] * 180 / pi,
#                             sin(THETA) * -sin(angles[1] - pi/2),
#                             cos(-angles[1] - pi/2),
#                             cos(THETA) * -sin(angles[1] - pi/2))
#        self.renWin.Render()
#        
#        self.transform.Identity()
        #=======================================================================
        # 3D stuff ends
        #=======================================================================
        
        return not self.tracker.stopping

def NewWiitrackerWindow(wiiAddress):
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
    window.finish_initializing(builder, wiiAddress)
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
    window = NewWiitrackerWindow("00:17:AB:39:49:98")
    window.show()
    threads_init()
    gtk.main()
    