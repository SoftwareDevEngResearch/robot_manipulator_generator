
from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from tracemalloc import start
from bpy import data, context
import bpy
import mathutils
import bmesh
import numpy as np
import os
#test

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


def test_bezier():


    bottom_bezier_verts = bezier_curve([-1.0,0.0,0.0],[-1.0,1.0,0.0],[1.0,1.0,0.0],[1.0,0.0,0.0])

    faces1 = tuple(range(len(bottom_bezier_verts)))

    top_bezier_verts = bezier_curve([-1.0,0.0,1.0],[-1.0,1.0,1.0],[1.0,1.0,1.0],[1.0,0.0,1.0])

    #   verts3


    verts = bottom_bezier_verts + top_bezier_verts
    faces2 = tuple(range(len(bottom_bezier_verts),len(verts)))
    #   faces2 = tuple(range(len(verts)-1, len(bottom_bezier_verts)-1, -1))
    face_back = (0, len(bottom_bezier_verts)-1, len(verts)-1, len(bottom_bezier_verts))
    faces = [faces1, faces2,face_back]

    #   side_faces = [tuple(range(0, len(verts),1))]
    offset = len(bottom_bezier_verts)

    side_faces = []
    for i in range(len(bottom_bezier_verts) -1):
        side_faces.append((i+1, i, offset+i, offset + 1+i))
    #   
    faces += side_faces
    return  verts, faces

def triangle():

    verts = [(1,0,0), (.5,.75,0), (0,1,0), (-.5,.75,0), (-1,0,0),(-1,0,1), (-.5,.75,1), (0,1,1), (.5,.75,1), (1,0,1)]
    #    faces = [(0,1,2,3,4,5)]
    faces = [tuple(range(len(verts)))]
    return verts, faces


def export_part(name):
    """
    export the object as an obj file
    Input: name: name of object you wish to export
    """
    name += '.obj'
    target_file = os.path.join('./test_obj', name)
    bpy.ops.export_scene.obj(filepath=target_file, use_triangles=True, path_mode='COPY')


class JointGenerator:
    def __init__(self):
        pass



class FingerSegmentGenerator():
    def __init__(self):
        pass


    def finger_segment_generator(selfceneter_location=[0,0,0],
        front_bottom = [[-0.5, 0.0, 0.0], [-0.5, 0.2, 0.0] , [0.5, 0.2, 0.0], [0.5, 0.2, 0.0]], 
        front_top = [[-0.5, 0.0, 1.0], [-0.5, 0.2, 1.0] , [0.5, 0.2, 1.0], [0.5, 0.2, 1.0]]):
        
        start_stop_verts = {}
        verts = []
        faces = []




        return verts, faces


    def distal_segment_generator(self,ceneter_location=[0,0,0],
        front_bottom = [[-0.5, 0.0, 0.0], [-0.5, 0.2, 0.0] , [0.5, 0.2, 0.0], [0.5, 0.2, 0.0]], 
        front_top = [[-0.5, 0.0, 1.0], [-0.5, 0.2, 1.0] , [0.5, 0.2, 1.0], [0.5, 0.2, 1.0]], 
        top = [[0.2, 0.2, 0.2], [0.2, 0.2, 0.2]],
        thickness = 1):

        start_stop_verts = {}
        # bottom_bezier_verts = bezier_curve([-1.0, 0.0, 0.0], [-1.0, front_bottom[0], 0.0], [1.0, front_bottom[1], 0.0], [1.0, 0.0, 0.0])
        # top_bezier_verts = bezier_curve([-1.0, 0.0, 1.0], [-1.0, front[0], 1.0], [1.0, front[1], 1.0], [1.0, 0.0, 1.0])

        verts = []

        bottom_bezier_verts = bezier_curve(front_bottom[0], front_bottom[1], front_bottom[2], front_bottom[3])
        verts += bottom_bezier_verts
        start_stop_verts['bottom_bezier_verts'] = (0, len(verts) - 1)
        
        top_bezier_verts = bezier_curve(front_top[0], front_top[1], front_top[2], front_top[3])
        verts += top_bezier_verts
        start_stop_verts['top_bezier_verts'] = (start_stop_verts['bottom_bezier_verts'][1] + 1, len(verts) - 1)
        # verts = bottom_bezier_verts + top_bezier_verts

        top_verts = []
        for i in top_bezier_verts:
            top_verts.append(bezier_curve(
                [i[0], i[1], i[2]], 
                [i[0] + top[0][0], i[1] + top[0][1], i[2] + top[0][2]], 
                [i[0] + top[1][0], -1.0 + top[1][1], i[2] + top[1][2]], 
                [i[0], -1.0, i[2]]))

        start_points = []
        end_points = []
        for vert_list in top_verts:
            start_points.append(len(verts))
            verts += vert_list
            end_points.append(len(verts)-1)

        start_stop_verts['top_verts'] = (start_stop_verts['top_bezier_verts'][1]+1, len(verts)-1)

        verts += [(front_bottom[0][0], -1 * thickness, front_bottom[0][-1]), (front_bottom[-1][0], -1 * thickness, front_bottom[-1][-1])]
        
        bottom_face = [tuple(range((len(bottom_bezier_verts)-1))) + (len(verts) - 1, len(verts) - 2)]

        side_face1 = tuple(range(end_points[0], start_points[0] -1, -1)) + (0, len(verts)-2)
        side_face2 = tuple(range(start_points[-1], end_points[-1]+1, 1)) + (len(verts) - 1, len(bottom_bezier_verts)-1)
        
        back_face = [(len(verts)-2, len(verts)-1, end_points[-1], end_points[0])]

        top_faces = []
        for i in range(len(top_verts)-1):
            for j in range(len(top_verts[i])-1):
                top_faces.append((j + start_points[i], j + 1 + start_points[i], j + 1 + start_points[i + 1], j + start_points[i + 1]))

        # faces = [faces1, faces2, face_back]

        #   side_faces = [tuple(range(0, len(verts),1))]
        offset = len(bottom_bezier_verts)

        front_faces = []
        for i in range(len(bottom_bezier_verts) -1):
            front_faces.append((i+1, i, offset+i, offset + 1+i))
        
        faces = []
        faces += front_faces
        faces += top_faces
        faces += bottom_face
        faces += [side_face1]
        faces += [side_face2]
        faces += back_face
        
        return  verts, faces

class PalmGenerator:
    def __init__(self):

        pass

    def cylinder_palm(self, center_location, dimentions):
        start_stop_verts = {}
        verts = []
        faces = []
        top_verts = []
        top_negative_verts = []
        top_positive_verts = []
        bottom_negative_verts = []
        bottom_positive_verts = []
        step_size = 0.001
        for x in np.arange(-1.0* dimentions[0]/2.0, dimentions[0]/2.0 + step_size, step_size):
            rounded_x = round(x,3)

            y = ((dimentions[1]/2)**2 * (1 - ((rounded_x-center_location[0])**2)/(dimentions[0]/2)**2)) ** 0.5 + center_location[1]
            negative_y = -1 * y
            top_negative_verts.append((rounded_x, negative_y, center_location[2]))
            bottom_negative_verts.append((rounded_x, negative_y, center_location[2] - dimentions[2]))
            
            if -1 * dimentions[0]/2 < rounded_x < dimentions[0]/2: 
                top_positive_verts.insert(0, (rounded_x, y, center_location[2]))
                bottom_positive_verts.insert(0, (rounded_x, y, center_location[2] - dimentions[2]))
        
        verts += top_negative_verts
        verts += top_positive_verts
        start_stop_verts['top_verts'] = (0, len(verts)-1)
        verts += bottom_negative_verts
        verts += bottom_positive_verts
        start_stop_verts['bottom_verts'] = (start_stop_verts['top_verts'][1] + 1, len(verts) - 1)


        top_face = [tuple(range(start_stop_verts['top_verts'][0], start_stop_verts['top_verts'][1] + 1, 1))]
        bottom_face = [tuple(range(start_stop_verts['bottom_verts'][1], start_stop_verts['bottom_verts'][0] - 1, -1))]
        side_faces = []

        top_vertex = range(start_stop_verts['top_verts'][0], start_stop_verts['top_verts'][1] + 1)
        bottom_vertex = range(start_stop_verts['bottom_verts'][0], start_stop_verts['bottom_verts'][1] + 1)

        for vertex in range(start_stop_verts['top_verts'][1] + 1):
            side_faces.append((
                top_vertex[vertex-1],
                bottom_vertex[vertex-1],
                bottom_vertex[vertex],
                top_vertex[vertex]))
    
        faces += top_face
        faces += bottom_face
        faces += side_faces

        return verts, faces


        
    
    def square_palm(self, center_location, dimentions):
        

        start_stop_verts_dict = {}
        verts = []
        top_verts = [
            (center_location[0] + -1*dimentions[0]/2, center_location[1]  + dimentions[1]/2, center_location[2]), 
            (center_location[0] + -1*dimentions[0]/2, center_location[1] + -1*dimentions[1]/2, center_location[2]),
            (center_location[0] + dimentions[0]/2, center_location[1] + -1*dimentions[1]/2, center_location[2]),
            (center_location[0] + dimentions[0]/2, center_location[1] + dimentions[1]/2, center_location[2])]
        
        verts += top_verts
        start_stop_verts_dict['top_verts'] = (0, len(verts)-1)

        bottom_verts = [
            (center_location[0] + -1*dimentions[0]/2, center_location[1] + dimentions[1]/2, center_location[2] - dimentions[2]), 
            (center_location[0] + -1*dimentions[0]/2, center_location[1] + -1*dimentions[1]/2, center_location[2] - dimentions[2]),
            (center_location[0] + dimentions[0]/2, center_location[1] + -1*dimentions[1]/2, center_location[2] - dimentions[2]),
            (center_location[0] + dimentions[0]/2, center_location[1] + dimentions[1]/2, center_location[2] - dimentions[2])]
        verts += bottom_verts
        
        start_stop_verts_dict['bottom_verts'] = (len(top_verts), len(verts)-1)
        
        top_face = [(0, 1, 2, 3)]
        bottom_face = [tuple(range(start_stop_verts_dict['bottom_verts'][1], start_stop_verts_dict['bottom_verts'][0]-1, -1))]


        top_vertex = range(start_stop_verts_dict['top_verts'][0], start_stop_verts_dict['top_verts'][1] + 1)
        bottom_vertex = range(start_stop_verts_dict['bottom_verts'][0], start_stop_verts_dict['bottom_verts'][1] + 1)
        side_faces = []
        for i in range(4):
            side_faces.append((
                top_vertex[i -1],
                bottom_vertex[i -1],
                bottom_vertex[i],
                top_vertex[i]))

        faces = top_face + bottom_face + side_faces
        return verts, faces


def bezier_curve(p1, p2, p3, p4):
    points = []
    for t in np.arange(0.0, 1.01, 0.01):
        points.append([
        (((1 - t) ** 3) * p1[0]) + (3*((1-t)**2) * t * p2[0]) + (3*(1-t) * (t ** 2) *p3[0]) + (t**3 * p4[0]),
        (((1 - t) ** 3) * p1[1]) + (3*((1-t)**2) * t * p2[1]) + (3*(1-t) * (t ** 2) *p3[1]) + (t**3 * p4[1]),
        (((1 - t) ** 3) * p1[2]) + (3*((1-t)**2) * t * p2[2]) + (3*(1-t) * (t ** 2) *p3[2]) + (t**3 * p4[2])])
    return points


# def test_bezier_top(
#     front_bottom = [[-0.5, 0.0, 0.0], [-0.5, 0.2, 0.0] , [0.5, 0.2, 0.0], [0.5, 0.2, 0.0]], 
#     front_top = [[-0.5, 0.0, 1.0], [-0.5, 0.2, 1.0] , [0.5, 0.2, 1.0], [0.5, 0.2, 1.0]], 
#     top = [0.2, 0.2],
#     thickness = 1):
    
#     # bottom_bezier_verts = bezier_curve([-1.0, 0.0, 0.0], [-1.0, front_bottom[0], 0.0], [1.0, front_bottom[1], 0.0], [1.0, 0.0, 0.0])
#     # top_bezier_verts = bezier_curve([-1.0, 0.0, 1.0], [-1.0, front[0], 1.0], [1.0, front[1], 1.0], [1.0, 0.0, 1.0])

#     bottom_bezier_verts = bezier_curve(front_bottom[0], front_bottom[1], front_bottom[2], front_bottom[3])
#     top_bezier_verts = bezier_curve(front_top[0], front_top[1], front_top[2], front_top[3])
#     verts = bottom_bezier_verts + top_bezier_verts

#     top_verts = []
#     for i in top_bezier_verts:
#         top_verts.append(bezier_curve([i[0], i[1], i[2]], [i[0], i[1], i[2] + top[0]], [i[0], -1.0, i[2] + top[1]], [i[0], -1.0, i[2]]))
    
#     start_points = []
#     end_points = []
#     for vert_list in top_verts:
#         start_points.append(len(verts))
#         verts += vert_list
#         end_points.append(len(verts)-1)

#     verts += [(front_bottom[0][0], -1 * thickness, front_bottom[0][-1]), (front_bottom[-1][0], -1 * thickness, front_bottom[-1][-1])]
    
#     bottom_face = [tuple(range((len(bottom_bezier_verts)-1))) + (len(verts) - 1, len(verts) - 2)]

#     side_face1 = tuple(range(end_points[0], start_points[0], -1)) + (0, len(verts)-2)
#     side_face2 = tuple(range(start_points[-1], end_points[-1],)) + (len(verts) - 1, len(bottom_bezier_verts)-1)
    
#     back_face = [(len(verts)-2, len(verts)-1, end_points[-1], end_points[0])]

#     top_faces = []
#     for i in range(len(top_verts)-1):
#         for j in range(len(top_verts[i])-1):
#             top_faces.append((j + start_points[i], j + 1 + start_points[i], j + 1 + start_points[i + 1], j + start_points[i + 1]))

#     # faces = [faces1, faces2, face_back]

#     #   side_faces = [tuple(range(0, len(verts),1))]
#     offset = len(bottom_bezier_verts)

#     front_faces = []
#     for i in range(len(bottom_bezier_verts) -1):
#         front_faces.append((i+1, i, offset+i, offset + 1+i))
    
#     faces = []
#     faces += front_faces
#     faces += top_faces
#     faces += bottom_face
#     faces += [side_face1]
#     faces += [side_face2]
#     faces += back_face
    
#     return  verts, faces

if __name__ == '__main__':

    # verts, faces = test_bezier()


    # verts, faces = test_bezier_top(
        # front_bottom = [[-0.5, 0.0, 0.0], [-0.5, 0.20, 0.0] , [0.5, 0.20, 0.0], [0.5, 0.0, 0.0]], 
        # front_top = [[-0.5, 0.0, 1.0], [-0.5, 0.20, 1.0] , [0.5, 0.20, 1.0], [0.5, 0.0, 1.0]], 
        # top = [2, 1],
        # thickness= 1)

    test = FingerSegmentGenerator()
    verts, faces = test.distal_segment_generator(
        front_bottom=[[-0.5, 0.0, 0.0], [-0.5, 0.20, 0.0] , [0.5, 0.20, 0.0], [0.5, 0.0, 0.0]], 
        front_top = [[-0.5, 0.0, 1.0], [-0.5, 0.20, 1.0] , [0.5, 0.20, 1.0], [0.5, 0.0, 1.0]], 
        top = [[0, 0, .4], [0, 0, .4]],
        thickness= 1)

    # test = PalmGenerator()
    # # verts, faces = test.square_palm([0,0,0], [3,2,1])  # not sure if I want the orgin to be on the top or bottom of the palm leaning towards the top

    # verts,faces = test.cylinder_palm([0,0,0], [3,2,2])

    #   verts, faces = triangle()
    edges = []
    mesh_name = "Cube"
    mesh_data = data.meshes.new(mesh_name)
    mesh_data.from_pydata(verts,edges,faces)
    bm = bmesh.new()
    bm.from_mesh(mesh_data)
    bm.to_mesh(mesh_data)
    bm.free()
    mesh_obj = data.objects.new(mesh_data.name, mesh_data)
    context.collection.objects.link(mesh_obj)

    export_part('testing')
