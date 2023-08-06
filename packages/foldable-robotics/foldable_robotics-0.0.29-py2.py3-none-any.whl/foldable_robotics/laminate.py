# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from .class_algebra import ClassAlgebra
from . import geometry
import matplotlib.pyplot as plt
#from .iterable import Iterable
from .layer import Layer
import numpy
from idealab_tools.iterable import Iterable
import foldable_robotics
import foldable_robotics.jupyter_support as fj

class WrongNumLayers(Exception):
    '''Custom exception for when two laminates of the wrong number of layers interact.'''
    pass

class Laminate(Iterable,ClassAlgebra):
    '''The Laminate class holds a list of layers and can be operated upon with CSG-style functions.'''
    
    def __init__(self, *layers):
        '''
        Initializes the class
        
        :param layers: A list of layers which compose the laminate
        :type layers: list
        :rtype: Laminate
        '''
        self.layers = list(layers)
        self.id = id(self)

    def copy(self,identical = True):
        '''
        creates a copy of the instance
        
        :param identical: whether to use the same id or not.
        :type identical: boolean
        :rtype: Laminate
        '''        
        new = type(self)(*[layer.copy(identical) for layer in self.layers])
        if identical:        
            new.id = self.id
        return new

    def export_dict(self):
        '''
        converts the laminate to a dict.
        
        :rtype: dict
        '''        

        d = {}
        d['layers'] = [layer.export_dict() for layer in self.layers]
        d['id'] = self.id
        return d

    @classmethod
    def import_dict(cls,d):
        '''
        converts a dict to a Laminate class
        
        :param d: the laminate in dict form
        :type d: dict
        :rtype: Laminate
        '''        
        
        new = cls(*[Layer.import_dict(item) for item in d['layers']])
        new.id = d['id']
        return new
    
    def is_null(self):
        results = [item.is_null() for item in self]
        return all(results)

    def plot(self,new=False):
        '''
        plots the laminate using matplotlib.
        
        :param new: whether to create a new figure
        :type new: boolean
        '''   
        colors = self.gen_colors(.25)

        try:
            d,e=self.bounding_box_coords()
            if new:
                plt.figure()
            for layer,color in zip(self.layers,colors):
                layer.plot(color = color)
            ax = plt.gca()
            ax.axis([d[0],e[0],d[1],e[1]])
        except foldable_robotics.layer.NoGeoms:
            pass
    def gen_colors(self,alpha=None):
        import matplotlib.cm
        cm = matplotlib.cm.plasma
        l = len(self.layers)     
        if l>1:
            colors = numpy.array([cm(ii/(l-1)) for ii in range(l)])
        else:
            colors = numpy.array([cm(1)])
        if alpha is not None:
            colors[:,3] = alpha
        colors = [tuple(item) for item in colors]
        return colors
    
    def plot_layers(self):
        '''
        plots each layer of the laminate in a new figure using matplotlib.
        '''   

        colors = self.gen_colors()
        
        for color,geom in zip(colors,self.layers):
            plt.figure()
            geom.plot(color = color)

    def _repr_svg_(self):
        return self.make_svg()

    def make_svg(self):
        try:
            repr_height = foldable_robotics.display_height
            line_width=foldable_robotics.line_width
            fill_opacity = foldable_robotics.fill_opacity
    
            hh = repr_height-line_width
            
            colors = self.gen_colors()
    
            min1,max1 = self.bounding_box_coords()
            min1=numpy.array(min1)
            width,height = self.get_dimensions()
    
            self = self.translate(*(-min1))
            self = self.scale(1,-1)
            self = self.scale(hh/height,hh/height)
            self = self.translate(line_width/2,hh+line_width/2)
    
            paths = []        
            for layer,color in zip(self,colors):
                fill_color = fj.color_tuple_to_hex(color[:3])
                paths.append(layer.make_svg_path(line_width,fill_opacity,fill_color))
            paths = '\n'.join(paths)
    
            width,height = self.get_dimensions()
    
            svg_string = fj.make_svg(paths,width+line_width,height+line_width)
        except foldable_robotics.layer.NoGeoms:
            svg_string = None
        return svg_string

    def get_dimensions(self):
        min1,max1 = self.bounding_box_coords()
        min1=numpy.array(min1)
        max1=numpy.array(max1)
        width,height = max1-min1
        return width, height

    def plot_3d(self,material_properties=None):
        import idealab_tools.plot_tris as pt
        material_properties = self.create_material_properties()
        mi = self.mesh_items(material_properties)
        pt.plot_mi(mi)

    def create_material_properties(self):
        colors = self.gen_colors()
        m = []
        for color,layer in zip(colors,self):
            m.append(layer.create_material_property(color=color))
        return m

    @property
    def list(self):
        '''converts the laminate to a list.'''
        return self.layers

    def binary_operation(self,function_name,other,*args,**kwargs):
        '''
        performs a binary operation between self and other.
        
        :param function_name: the layer-based function to be performed
        :type function_name: string
        :param other: the layer-based function to be performed
        :type other: Laminate
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''

        if len(self.layers)!=len(other.layers):
            raise(WrongNumLayers())
        else:
            layers = []
            for layer1,layer2 in zip(self.layers,other.layers):
                function = getattr(layer1,function_name)
                layers.append(function(layer2,*args,**kwargs))
            return type(self)(*layers)

    def unary_operation(self,function_name,*args,**kwargs):
        '''
        performs a unary operation on the laminate.
        
        :param function_name: the layer-based function to be performed
        :type function_name: string
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        layers = []
        for layer1 in self.layers:
            function = getattr(layer1,function_name)
            layers.append(function(*args,**kwargs))
        return type(self)(*layers)
        
    def union(self,other):
        '''
        unions two laminates together.
        
        :param other: the other laminate
        :type other: Laminate
        :rtype: Laminate
        '''
        return self.binary_operation('union',other)

    def difference(self,other):
        '''
        takes the difference of self - other.
        
        :param other:the other laminate
        :type other: Laminate
        :rtype: Laminate
        '''
        return self.binary_operation('difference',other)

    def symmetric_difference(self,other):
        '''
        takes the symmetric difference of self and other.
        
        :param other: the other laminate
        :type other: Laminate
        :rtype: Laminate
        '''
        return self.binary_operation('symmetric_difference',other)

    def intersection(self,other):
        '''
        takes the intersection of self and other.
        
        :param other: the other laminate
        :type other: Laminate
        :rtype: Laminate
        '''
        return self.binary_operation('intersection',other)
    
    def buffer(self,*args,**kwargs):
        '''
        dilate or erode the laminate based on the arguments sent.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('buffer',*args,**kwargs)

    def dilate(self,*args,**kwargs):
        '''
        dilate the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('dilate',*args,**kwargs)

    def erode(self,*args,**kwargs):
        '''
        erode the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('erode',*args,**kwargs)

    def translate(self,*args,**kwargs):
        '''
        translate the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('translate',*args,**kwargs)
        
    def rotate(self,*args,**kwargs):
        '''
        rotate the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('rotate',*args,**kwargs)

    def scale(self,*args,**kwargs):
        '''
        scale the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('scale',*args,**kwargs)

    def affine_transform(self,*args,**kwargs):
        '''
        affine transform the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('affine_transform',*args,**kwargs)

    def simplify(self,*args,**kwargs):
        '''
        simplify the laminate.
        see the corresponding layer function for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        return self.unary_operation('simplify',*args,**kwargs)

    def map_line_stretch(self,*args,**kwargs):
        '''
        transform the laminate based on two lines.
        see foldable_robotics.manufacturing.map_line_stretch for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        import foldable_robotics.manufacturing
        return foldable_robotics.manufacturing.map_line_stretch(self,*args,**kwargs)
    def map_line_scale(self,*args,**kwargs):
        '''
        transform the laminate based on two lines.
        see foldable_robotics.manufacturing.map_line_stretch for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        import foldable_robotics.manufacturing
        return foldable_robotics.manufacturing.map_line_scale(self,*args,**kwargs)
    def map_line_place(self,*args,**kwargs):
        '''
        transform the laminate based on two lines.
        see foldable_robotics.manufacturing.map_line_stretch for arguments and keyword-arguments
        
        :param args: tuple of arguments passed to subfunction
        :type args: tuple
        :param kwargs: keyword arguments passed to subfunction
        :type kwargs: dict
        :rtype: Laminate
        '''
        import foldable_robotics.manufacturing
        return foldable_robotics.manufacturing.map_line_place(self,*args,**kwargs)
        
    def export_dxf(self,name):
        '''
        export the laminate to a .dxf file
        see the corresponding layer function for arguments and keyword-arguments
        
        :param name: filename to export
        :type name: string
        '''
        for ii,layer in enumerate(self.layers):
            layername = name+str(ii)
            layer.export_dxf(layername)
            
    def mesh_items(self,material_properties):
        '''
        create a mesh for 3d rendering using pyqtgraph
        
        :param material_properties: tuple of arguments passed to subfunction
        :type material_properties: foldable_robotics.dynamics_info.MaterialProperty
        :rtype: GLMeshItem
        '''
        
        import matplotlib.cm as cm
        import pyqtgraph.opengl as gl

        z = 0
        vs = []
        cs = []

        for ii,(layer,mp) in enumerate(zip(self,material_properties)):
            v,c = layer.mesh_items_inner(z+mp.thickness/2,mp.color)
            vs.append(v)
            cs.append(c)
            z+=mp.thickness
            
        verts_outer = numpy.vstack(vs)
        colors_outer = numpy.vstack(cs)

        mi= gl.GLMeshItem(vertexes=verts_outer,vertexColors=colors_outer,smooth=False,shader='balloon',drawEdges=False)

        return mi

    def mass_properties(laminate,material_properties):
        '''
        calculate mass properties
        
        :param material_properties: tuple of arguments passed to subfunction
        :type material_properties: foldable_robotics.dynamics_info.MaterialProperty
        :rtype: tuple of mass properties
        '''        
        volume = 0
        mass = 0
        z=0
        centroid_x=0
        centroid_y=0
        centroid_z=0
        for ii,layer in enumerate(laminate):
            bottom = z
            top = z+material_properties[ii].thickness
            area=0
    
            area_i,volume_i,mass_i,centroid_i = layer.mass_props(material_properties[ii],bottom,top)

            centroid_x_i,centroid_y_i,centroid_z_i = centroid_i
            area+=area_i
            volume+=volume_i
            mass+=mass_i

            centroid_x += centroid_x_i*mass_i
            centroid_y += centroid_y_i*mass_i
            centroid_z += centroid_z_i*mass_i

            z=top
        
        centroid_x /= mass
        centroid_y /= mass
        centroid_z /= mass
        centroid = (centroid_x,centroid_y,centroid_z)
        
        I=numpy.zeros((3,3))
        bottom = 0
        for ii,layer in enumerate(laminate):
            cn = numpy.array(centroid)                
            I+=layer.inertia(cn,bottom,material_properties[ii])
            bottom += material_properties[ii].thickness
            
        return mass,volume,centroid,I
        
    def bounding_box(self):
        '''create a bounding box of the layer and return as a layer'''
        import foldable_robotics.manufacturing
        l = foldable_robotics.manufacturing.unary_union(self)
        box = l.bounding_box()
        box = box.to_laminate(len(self))
        return box
        
    def bounding_box_coords(self):
        '''compute the lower left hand and upper right coordinates for computing a bounding box of the layer'''
        import foldable_robotics.manufacturing
        l = foldable_robotics.manufacturing.unary_union(self)
        val = l.bounding_box_coords()
        return val

    def unary_union(self,*others):
        l = [len(item) for item in [self]+list(others)]
        if len(set(l))!=1:
            raise(WrongNumLayers())
        l = l[0]
        layers = []
        for ii in range(l):
            other_ii = [item[ii] for item in others]
            layer = self[ii].unary_union(*other_ii)
            layers.append(layer)
        return type(self)(*layers)

    def to_mesh(self,layer_thickness,characteristic_len_min = None,characteristic_len_max = None):
        '''create a mesh object with gmsh'''
        import foldable_robotics.gmsh_support as gs
        geofile= gs.laminate_to_geo(self,layer_thickness,characteristic_len_min,characteristic_len_max)
        mesh_data = geofile.make_mesh()
        return mesh_data
        

if __name__=='__main__':
    from layer import Layer
    import shapely.geometry as sg
    l=Layer(sg.Polygon([(0,0),(1,0),(0,1)]))
    l2 = l | l.translate(2,0)
    lam=Laminate(l,l.translate(.1,.1))
    l1 = Layer(sg.LineString([(0,0),(1,0),(0,1)]))
    l1.plot(new=True)
    lam._repr_svg_()
        