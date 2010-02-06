# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk

from wiitracker.wiitrackerconfig import getdatapath

class AboutWiitrackerDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutWiitrackerDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a AboutWiitrackerDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling AboutWiitrackerDialog.finish_initializing().
    
        Use the convenience function NewAboutWiitrackerDialog to create 
        NewAboutWiitrackerDialog objects.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutWiitrackerDialog object with it in order to finish
        initializing the start of the new AboutWiitrackerDialog instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here

def NewAboutWiitrackerDialog():
    """NewAboutWiitrackerDialog - returns a fully instantiated
    AboutWiitrackerDialog object. Use this function rather than
    creating a AboutWiitrackerDialog instance directly.
    
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'AboutWiitrackerDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_wiitracker_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutWiitrackerDialog()
    dialog.show()
    gtk.main()

