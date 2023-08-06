# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
import numpy
import math


def distance(p1,p2):
    p1 = numpy.array(p1)
    p2 = numpy.array(p2)
    v = p2-p1
    return(length(v))
def length(v1):
    '''
    finds the length of a vector
    
    :param v1: the vector
    :type v1: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1).flatten()
    l = (v1.dot(v1))**.5
    return l
    
def inner_angle(v1,v2):
    '''
    finds the interior angle between two vectors
    
    :param v1: the first vector
    :type v1: tuple or list of floats
    :param v2: the second vector
    :type v2: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1).flatten()
    l1 = length(v1)
    v2 = numpy.array(v2).flatten()
    l2 = length(v2)
    cost = numpy.dot(v1,v2)/l1/l2
    t = math.acos(cost)
    return t
    
def total_angle(v1,v2,v3=None):
    '''
    finds the interior angle between two vectors
    
    :param v1: the first vector
    :type v1: tuple or list of floats
    :param v2: the second vector
    :type v2: tuple or list of floats
    :rtype: float
    '''

    v1 = numpy.array(v1).flatten()
    if len(v1)==2:
        v1 = numpy.r_[v1,0]
        v3 = numpy.array([0,0,1])

        v2 = numpy.array(v2).flatten()
    if len(v2)==2:
        v2 = numpy.r_[v2,0]
        v3 = numpy.array([0,0,1])

    costheta = numpy.dot(v1,v2)
    sintheta  = numpy.cross(v1,v2)
    l_sintheta = length(sintheta)
    neg = sintheta.dot(v3)
    if neg<0:
        neg = -1
    else:
        neg=1
    theta = math.atan2(neg*l_sintheta,costheta)
    return theta    

def heal_polylines(lines, tolerance=1e-3):
    polylines=[]
    while len(lines)>0:
        polyline = []
        polyline.append(lines.pop(0))
        finding = True
        while finding:
            finding = False
            for ii in range(len(lines)):
                item = lines[ii]
                if distance(polyline[-1][1],item[0])<tolerance:
                    polyline.append(item)
                    lines.pop(ii)
                    finding = True
                    break
                elif  distance(polyline[-1][1],item[-1])<tolerance:
                    polyline.append(item[::-1])
                    lines.pop(ii)
                    finding = True
                    break
        polyline2 = numpy.array([item[0] for item in polyline]+[polyline[-1][-1]])
        # polyline = numpy.array([item for segment in polyline for item in segment])
        polylines.append(polyline2)
        print(len(lines))
    return polylines