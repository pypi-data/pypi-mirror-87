# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:39:00 2018

@author: daukes
"""

from .laminate import Laminate
from .layer import Layer

def rectangular_array(shape,spacing_x, spacing_y, num_x, num_y):
    
#    shapes= shape.copy()
    shapes = []
    
    for ii in range(num_x):
        x_pos = ii*spacing_x
        for jj in range(num_y):
            y_pos = jj*spacing_y
            shapes.append(shape.translate(x_pos,y_pos))
    
    shapes2 = type(shape)()
    shapes2=shapes2.unary_union(*shapes)
    
    return shapes2