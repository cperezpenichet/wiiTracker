'''
Created on Jan 9, 2010

@author: carlos
'''

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
