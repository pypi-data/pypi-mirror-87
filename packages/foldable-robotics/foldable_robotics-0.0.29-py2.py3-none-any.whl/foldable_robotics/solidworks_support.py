# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:23:36 2019

@author: daukes
"""

import yaml
import numpy
import matplotlib.pyplot as plt
import os
import shapely.geometry as sg
from foldable_robotics.layer import Layer
import foldable_robotics.layer
import foldable_robotics.dxf

class obj(object):
    pass
    
from idealab_tools.data_exchange.generic_data import GenericData

def objectify(var):
    if isinstance(var,dict):
#        new_var = GenericData(**var)
        new_var = obj()
        for key,value in var.items():
            setattr(new_var,key,objectify(value))
        return new_var
    elif isinstance(var,list):
        new_var = [objectify(item) for item in var]
        return new_var
    else: 
        return var    
        
class Component(object):
    pass

class Face(object):
    pass

def create_loops(filename,prescale):
#    plt.figure()
    with open(filename) as f:
        data1 = yaml.load(f,Loader=yaml.FullLoader)
    data = objectify(data1)
    global_transform = numpy.array(data.transform)
    components = []
    for component in data.components:
        new_component = Component()
        local_transform = numpy.array(component.transform)
        T = local_transform.dot(global_transform)
        faces = []
        for face in component.faces:
            new_face = Face()
            loops = []
            for loop in face.loops:
                loop = numpy.array(loop)
                loop_a = numpy.hstack([loop,numpy.ones((len(loop),1))])
                loop_t = loop_a.dot(T)
                loop_t*=prescale
                loop_out = loop_t[:,:2].tolist()
                loops.append(loop_out)
#                plt.fill(loop_t[:,0],loop_t[:,1])
            new_face.loops = loops
            faces.append(new_face)
        new_component.faces = faces
        components.append(new_component)
    return components

def component_to_layer(component):
    faces = []
    for face in component.faces:
        loops = []
        for loop in face.loops:
            loops.append(Layer(sg.Polygon(loop)))
        if not not loops:
            face_new = loops.pop(0)            
            for item in loops:
                face_new^=item
            faces.append(face_new)
    if not not faces:
        component_new = faces.pop(0)
        for item in faces:
            component_new|=item
        return component_new
            
def get_joints(*component_layers,round_digits):
    segments = []
    for layer in component_layers:
        segments.extend(layer.get_segments())
    
    segments = [tuple(sorted(item)) for item in segments]
    segment_array = numpy.array(segments)
    segment_array = segment_array.round(round_digits)
    segments2 = [(tuple(a),tuple(b)) for a,b in segment_array.tolist()]    
    segments3 = list(set(segments2))
    
    ii = [segments3.index(item) for item in segments2]
    jj = list(set(ii))
    kk = [ii.count(item) for item in jj]
    ll = [segments3[aa] for aa,bb in zip(jj,kk) if bb>1]

    mm = []
    for item in ll:
        mm.append(segments2.index(item))
        
    nn = [segments[ii] for ii in mm]
    
    return nn

def length(segment):
    segment = numpy.array(segment)
    v = segment[1]-segment[0]
    l=((v**2).sum())**.5
    return l

def filter_segments(segments,round_digits):
    lengths = [length(item) for item in segments]
    segments = [item for item,l in zip(segments,lengths) if l>(10**(-round_digits))]
    return segments

def create_layered_dxf(elements,filename):
    import ezdxf
    dwg = ezdxf.new('R2010')
    msp = dwg.modelspace()

    import foldable_robotics.dxf

    for info,items in elements:
#        items = element.pop('items')
        
        layer = dwg.layers.new(**info)
        for item in items.get_paths():
            msp.add_lwpolyline(item,dxfattribs={'layer': info['name']})
        
    dwg.saveas(filename)     

def process(filename,output_file_name,prescale,round_digits):

    components = create_loops(filename,prescale)
    layers = [component_to_layer(item) for item in components]
    layer2 = Layer()
    layer2 = layer2.unary_union(*layers)
    # layer2.plot(new=True)
    
    segments = get_joints(*layers,round_digits=round_digits)
    segments = filter_segments(segments,round_digits)
    
    linestrings = [sg.LineString(item) for item in segments]
    joints = Layer(*linestrings)
#    joints.plot()
    
    elements = []
    elements.append(({'name':'body','dxfattribs':{'color': foldable_robotics.dxf.to_index[0xff0000]}},layer2))
    elements.append(({'name':'joints','dxfattribs':{'color': foldable_robotics.dxf.to_index[0x0000ff]}},joints))
    
    create_layered_dxf(elements,output_file_name)
    return layer2,joints,components
       
    
if __name__=='__main__':
    user_path = os.path.abspath(os.path.expanduser('~'))
    # folder = os.path.join(user_path,'C:/Users/danaukes/projects/papers_2019_foldable_textbook/_cad/spherical_example')

    # folder=r'C:\Users\danaukes\Dropbox (Personal)\projects\2020-12-06 Knife holder'
    # filename='knife_holder - Sheet1_Drawing View1.yaml'

    folder = r'C:\Users\danaukes\Dropbox (Personal)\projects\2019-12-27 silverware'
    filename = 're-assembled - Sheet1_Drawing View1.yaml'

    filename_simple = os.path.splitext(filename)[0]
    full_path = os.path.normpath(os.path.join(folder,filename))
    
    # output_file_name = os.path.join(user_path,'desktop','design.dxf')
    output_file_name = os.path.join(folder,filename_simple+'.dxf')
    
    
    round_digits = 2
    a,b,c = process(full_path,output_file_name,1,round_digits)

    for item in c:
        component_to_layer(item).plot(new=True)
        
    a.plot(new=True)