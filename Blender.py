import bpy 
import math


VIEWS = 16
FOV = 45
VIEW_CONE = 35
FOCUS_PLANE = 0
Camera = []


class images():
    
    # Note:  Camera_parameters = json
    def add_camera(FoV, focus_plane, location, name):
        print(f" adding {name} with Fov : {FoV} , Focus_plane : {focus_plane} , location {location}")
        Camera = bpy.ops.object.camera_add()
        camera = bpy.context.object # adding camera to the scene
        camera.name = name
        camera.data.lens_unit = 'FOV' # string
        camera.data.angle = math.radians(FoV) # float radians
        camera.location = location # tuple 
        camera.data.dof.use_dof = True # boolean
        camera.data.dof.focus_distance = focus_plane # int

        return camera

    def track_camera(self, camera, target):
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = target
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

    for i in range(VIEWS):
        angle = (i * 360 / VIEWS) * (math.pi / 180)
        x = VIEW_CONE * math.cos(angle)
        y = VIEW_CONE * math.sin(angle)
        z = FOCUS_PLANE
        location = (x, y, z)
        name = f"Camera_{i+1}"
#        print(name)
        Camera = add_camera(FOV, FOCUS_PLANE, location, name)
        Camera.append(Camera)