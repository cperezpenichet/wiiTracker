'''
Created on Jan 15, 2010

@author: carlos
'''
from Queue import Queue
from math import atan, cos, pi
import cwiid

class Wii3DTracker(object):
    '''
    This object represents a WiiMote with position tracking
    capabilities in 3D using the getAngles function. 
    '''

    def __init__(self, wiiAddress):
        '''
        Create and initialize the tracker.
        
        wiiAddress is the address of the WiiMote you intend to track.
        '''
        self.wiiAddress = wiiAddress
        self.wiiMote = None
        
        self.acc_cal = ((128, 128, 128),
                        (255, 255, 255))
        self.acc = [0, 0, 0]
        
        self.FILTER_LENGTH = 15
        self.roll_fltr_1 = Queue()
        self.roll_fltr_2 = Queue()
        self.pitch_fltr = Queue()
        self.filtered_roll_1 = 0
        self.filtered_roll_2 = pi
        self.filtered_pitch = 0
        self.filter_state = 0
        
        self.stopping = False
        self.connected = False
        
    def __del__(self):
        if self.connected:
            self.wiiMote.close()
    
    def connect(self):
        """
        Actually start the connection to the WiiMote.
        The controller should be in discovery mode (set by pressing 1+2)
        """
        try:
            self.wiiMote = cwiid.Wiimote(self.wiiAddress)
            self.connected = True
        except:
            self.connected = False
            return
        
        self.wiiMote.enable(cwiid.FLAG_MESG_IFC)
        self.wiiMote.rpt_mode = cwiid.RPT_ACC
        self.acc_cal = self.wiiMote.get_acc_cal(cwiid.EXT_NONE)
        
    def getAngles(self):
        """
        Get the roll and pitch angles for the current position.
        
        Both angles are measured against the positive vertical axis.
        roll is in the range [-pi, pi] while pitch is in the range
        [-pi/2, pi/2]
        
        Returns a tuple of the form (roll, pitch)
        """
        messages = None
        while messages == None:
            messages = self.wiiMote.get_mesg()
            
        for msg in messages:
            if msg[0] == cwiid.MESG_ACC:
                # Normalize data using calibration info from the controller
                for i in range(3):
                    self.acc[i] = float(msg[1][i]-self.acc_cal[0][i])/(self.acc_cal[1][i]-self.acc_cal[0][i])
                    
                # Calculate roll and pitch based on the 3 acceleration 
                # components. Have to take into account several cases
                # to avoid division by zero and the correct quadrant.
                if self.acc[cwiid.Z] == 0.0:
                    if self.acc[cwiid.X] > 0:
                        tmp = 1
                    else:
                        tmp = -1
                    roll = pi/2 * tmp
                else:
                    roll = atan(self.acc[cwiid.X]/self.acc[cwiid.Z])
                if self.acc[cwiid.Z] < 0.0:
                    if self.acc[cwiid.X] > 0.0:
                        tmp = 1
                    else:
                        tmp = -1
                    roll = roll + pi * tmp
                if self.acc[cwiid.Z] == 0.0:
                    pitch = pi/2
                    if self.acc[cwiid.Y] < 0.0:
                        pitch = -1 * pitch
                else:
                    pitch = atan(self.acc[cwiid.Y]/self.acc[cwiid.Z]*cos(roll))
                
                # Now apply some filtering to avoid noise. Two filtera are 
                # used for roll to avoid problems related to the discontinuity
                # in a full rotation. One filter stores data from the sensor
                # and the other works with the same data rotated by pi.
                roll = float(roll)/self.FILTER_LENGTH
                pitch = float(pitch)/self.FILTER_LENGTH
                if roll >= 0:
                    nu_roll = roll - pi/self.FILTER_LENGTH
                else:
                    nu_roll = roll + pi/self.FILTER_LENGTH
                
                while self.roll_fltr_1.qsize() > self.FILTER_LENGTH:
                    self.roll_fltr_1.get()
                    self.roll_fltr_2.get()
                    self.pitch_fltr.get()
                if self.roll_fltr_1.qsize() == self.FILTER_LENGTH:
                    self.filtered_roll_1 = self.filtered_roll_1 - self.roll_fltr_1.get()
                    self.filtered_roll_2 = self.filtered_roll_2 - self.roll_fltr_2.get()
                    self.filtered_pitch = self.filtered_pitch - self.pitch_fltr.get()
                self.roll_fltr_1.put(roll)
                self.roll_fltr_2.put(nu_roll)
                self.pitch_fltr.put(pitch)
                self.filtered_roll_1 = self.filtered_roll_1 + roll
                self.filtered_roll_2 = self.filtered_roll_2 + nu_roll
                self.filtered_pitch = self.filtered_pitch + pitch
                
                # Depending on the angle data from one filter or the other 
                # is returned. A reverse transformation is applied to 
                # make both filters compatible.
                if self.filter_state == 0:
                    ret = self.filtered_roll_1
                else:
                    if self.filtered_roll_2 > pi:
                        ret = self.filtered_roll_2 - 2 * pi
                    else: 
                        ret = self.filtered_roll_2
                        
                # Finally select which filter to use for the next
                # time based on the current roll angle.
                if abs(ret) > pi/2:
                    self.filter_state = 1
                else:
                    self.filter_state = 0
                
        return (ret, self.filtered_pitch)
