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


import cairo

ppi = 72
ppmm = 72/25.4

page_width = 40
page_height = 28

class Page(object):

    '''
    This class defines a pdf page, which can hold vector geometry.
    '''    

    def __init__(self,filename='output.pdf',width=page_width,height=page_height):
        '''
        Initialize a Page class
        
        :param filename: desired output filename.  defaults to 'output.pdf'
        :type filename: string
        :param width: width of the page, in inches
        :type width: float
        :param height: height of the page, in inches
        :type height float
        :rtype: Page instance
        '''    
    
        surface = cairo.PDFSurface(filename, page_width*ppi, page_height*ppi)

        ctx = cairo.Context(surface)
        ctx.scale (1, -1)
        ctx.translate (0, -page_height*ppi)
        
        self._surface = surface
        self._context = ctx

    def draw_poly(self,poly,line_color = (0,0,0,1),line_width=.01,fill_color=(0,0,0,1)):
        '''
        Draw a closed polygon.
        
        :param poly: describes each vertex of the polygon.
        :type poly: list of tuples 
        :param line_color: line color in (r,g,b,a) format.
        :type line_color: tuple of floats
        :param line_width: width of the line
        :type line_width: float
        :param fill_color: color of the polygon interior, in (r,g,b,a) format
        :type line_width: tuple of floats
        :rtype: None
        '''    
        
        pt = poly.pop(0)
        self._context.move_to(*pt)
        
#        lastpt = pt
#        for pt in poly:
#            pt1x = (lastpt[0]*2+pt[0])/3
#            pt1y = (lastpt[1]*2+pt[1])/3
#            pt2x = (lastpt[0]+2*pt[0])/3
#            pt2y = (lastpt[1]+2*pt[1])/3
#            self._context.curve_to(pt1x,pt1y,pt2x,pt2y,*pt)
#            lastpt = pt
        for pt in poly:
            self._context.line_to(*pt)
        
        self._context.close_path ()
        self._context.set_source_rgba(*line_color)
        self._context.set_line_width(line_width)
        self._context.stroke()

    def draw_linestring(self,geom,line_color = (0,0,0,1),line_width=.01,fill_color=(0,0,0,1)):
        '''
        Draw an open linestring.
        
        :param poly: describes each vertex of the linestring.
        :type poly: list of tuples 
        :param line_color: line color in (r,g,b,a) format.
        :type line_color: tuple of floats
        :param line_width: width of the line
        :type line_width: float
        :param fill_color: color of the linestring interior, in (r,g,b,a) format
        :type line_width: tuple of floats
        :rtype: None
        '''    
        coords = list(geom.coords)
        pt = coords.pop(0)
        self._context.move_to(*pt)
        
#        lastpt = pt
#        for pt in poly:
#            pt1x = (lastpt[0]*2+pt[0])/3
#            pt1y = (lastpt[1]*2+pt[1])/3
#            pt2x = (lastpt[0]+2*pt[0])/3
#            pt2y = (lastpt[1]+2*pt[1])/3
#            self._context.curve_to(pt1x,pt1y,pt2x,pt2y,*pt)
#            lastpt = pt
        for pt in geom:
            self._context.line_to(*pt)
        
#        self._context.close_path()
        self._context.set_source_rgba(*line_color)
        self._context.set_line_width(line_width)
        self._context.stroke()
    
    def close(self):
        '''
        close the surface 

        :rtype: None
        '''
        self._surface.finish()
