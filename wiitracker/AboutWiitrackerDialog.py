# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Carlos M. Pérez Penichet <cperezpenichet@gmail.com>
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
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

