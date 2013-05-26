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

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

from math import sin, cos

ARROW_1 =  [(0, -75),
          (15, -45),
          (10, -45),
          (10, 75),
          (-10, 75),
          (-10, -45),
          (-15, -45)]

ARROW_15 =  [(0, -75),
          (15, -45),
          (10, -45),
          (10, 75),
          (0, 50),
          (-10, 75),
          (-10, -45),
          (-15, -45)]

ARROW_2 = [(0, -75),
          (10, 75),
          (0, 50),
          (-10, 75),
          (0, -75)]

ARROW = ARROW_2

def moveTo(what, where):
    ret = []
    for point in what:
        ret.append((point[0] + where[0],
                    point[1] + where[1]))
    return ret

def rotate(what, angle):
    ret = []
    matrix = ((cos(angle), -sin(angle)),
              (sin(angle), cos(angle)))
    for point in what:
        ret.append((point[0] * matrix[0][0] + point[1] * matrix[0][1],
                    point[0] * matrix[1][0] + point[1] * matrix[1][1]))
    return ret

def scale(what, scale):
    ret = []
    for point in what:
        ret.append((point[0] * scale[0],
                    point[1] * scale[1]))
    return ret

def rotateMove(what, angle, where):
    ret = []
    matrix = ((cos(angle), -sin(angle)),
              (sin(angle), cos(angle)))
    for point in what:
        ret.append((int(point[0] * matrix[0][0] + point[1] * matrix[0][1] + where[0]),
                    int(point[0] * matrix[1][0] + point[1] * matrix[1][1] + where[1])))
    return ret

def rotateMoveScale(what, angle, where, scale):
    ret = []
    matrix = ((cos(angle), -sin(angle)),
              (sin(angle), cos(angle)))
    for point in what:
        ret.append((int(point[0] * scale[0] * matrix[0][0] + 
                        point[1] * scale[1] * matrix[0][1] + where[0]),
                    int(point[0] * scale[0] * matrix[1][0] + 
                        point[1] * scale[1] * matrix[1][1] + where[1])))
    return ret
