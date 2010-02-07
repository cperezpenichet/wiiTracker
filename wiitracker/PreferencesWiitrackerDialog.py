# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record

from wiitracker.wiitrackerconfig import getdatapath

class PreferencesWiitrackerDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesWiitrackerDialog"
    prefernces = {}

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a PreferencesWiitrackerDialog requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling PreferencesWiitrackerDialog.finish_initializing().

        Use the convenience function NewPreferencesWiitrackerDialog to create
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

        #set up couchdb and the preference info
        self.__db_name = "wiitracker"
        self.__database = CouchDatabase(self.__db_name, create=True)
        self.__preferences = None
        self.__key = None

        #set the record type and then initalize the preferences
        self.__record_type = "http://wiki.ubuntu.com/Quickly/RecordTypes/Wiitracker/Preferences"
        self.__preferences = self.get_preferences()
        #TODO:code for other initialization actions should be added here
        self.addressEntry = self.builder.get_object("AddressEntry")
        self.addressEntry.set_text(self.__preferences['wiiAddress'])
        self.dampingScale = self.builder.get_object("dampingScale")
        self.dampingScale.set_range(1, 100)
        self.dampingScale.set_value(self.__preferences['filterSize'])

    def get_preferences(self):
        """get_preferences  -returns a dictionary object that contain
        preferences for wiitracker. Creates a couchdb record if
        necessary.
        """

        if self.__preferences == None: #the dialog is initializing
            self.__load_preferences()
            
        #if there were no saved preference, this 
        return self.__preferences

    def __load_preferences(self):
        #TODO: add prefernces to the self.__preferences dict
        #default preferences that will be overwritten if some are saved
        self.__preferences = {"record_type":self.__record_type,
                              "wiiAddress": "00:17:AB:39:49:98",
                              "filterSize": 15}
        
        results = self.__database.get_records(record_type=self.__record_type, create_view=True)
       
#        self.__key = self.__database.put_record(Record(self.__preferences))
        if len(results.rows) == 0:
            #no preferences have ever been saved
            #save them before returning
            self.__key = self.__database.put_record(Record(self.__preferences))
        else:
            self.__preferences = results.rows[0].value
            self.__key = results.rows[0].value["_id"]
        
    def __save_preferences(self):
        self.__database.update_fields(self.__key, self.__preferences)

    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().
        """

        #make any updates to self.__preferences here
        #self.__preferences["preference1"] = "value2"
        self.__preferences["wiiAddress"] = self.addressEntry.get_text()
        self.__preferences["filterSize"] = self.dampingScale.get_value()
        self.__save_preferences()

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """

        #restore any changes to self.__preferences here
        pass

def NewPreferencesWiitrackerDialog():
    """NewPreferencesWiitrackerDialog - returns a fully instantiated
    PreferencesWiitrackerDialog object. Use this function rather than
    creating a PreferencesWiitrackerDialog instance directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'PreferencesWiitrackerDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    dialog = builder.get_object("preferences_wiitracker_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewPreferencesWiitrackerDialog()
    dialog.show()
    gtk.main()

