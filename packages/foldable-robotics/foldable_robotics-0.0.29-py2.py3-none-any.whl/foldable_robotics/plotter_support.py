# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:34:27 2018

@author: danaukes
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:24:29 2018

@author: danaukes
"""

import math
ppi = 1000

start_string = 'IN;PA;VS30;'
end_string = 'PU;PU0,0;!PG;'

def path_string(path):
    first = True
    # path = list(path)
    s=''
    for point in path:
        if first:
            s+='PU{0:d},{1:d};'.format(int(point[0]),int(point[1]))
        else:
            s+='PD{0:d},{1:d};'.format(int(point[0]),int(point[1]))
        first = False
    # s+='PU;'
    return s

def layer_string(layer):
    layer = layer.rotate(-90)
    layer = layer.scale(ppi,ppi)
    s = start_string
    for path in layer.get_paths():
        s+=path_string(path)
    s += end_string
    return s

class Plotter(object):
    pass
