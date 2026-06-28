import pyray as pr
from tracker.head_tracker import HeadTracker
import numpy as np


view = 16
window_width = 1920


# haed tracker
tracker = HeadTracker()


monitor = pr.get_current_monitor()

width = pr.get_monitor_width(monitor)
height = pr.get_monitor_height(monitor)

pr.set_config_flags(pr.FLAG_WINDOW_UNDECORATED)

pr.init_window(1900, 1000, "Holocore")
pr.set_target_fps(60)
# pr.toggle_fullscreen()
camera = pr.Camera2D()

v1 = pr.Vector2(0, 0)
v2 = pr.Vector2(0, 450)
pos = pr.Vector2(0, 0)

img = pr.load_image(r"./../test/interlaced.png")
bg = pr.load_image(r"./../test/test.png")
#pr.image_resize(img, window_width, 450)
#pr.image_draw_line_ex(img, v1 , v2, 16,  pr.WHITE)
texture = pr.load_texture_from_image(img)
bg_texture = pr.load_texture_from_image(bg)
pr.set_texture_filter(texture, pr.TEXTURE_FILTER_POINT)

px =  window_width //( img.width // view)
print(px)
current_view =0
while not pr.window_should_close():
    
    # pr.update_camera(camera, pr.CAMERA_ORBITAL)
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

#   DrawTextureRec(Texture2D texture, Rectangle source, Vector2 position, Color tint);
    pr.draw_texture(bg_texture, 0, 0, pr.WHITE)
    

    pose = tracker.update()
    if pose is not None:
        current_view = int(np.interp(pose.yaw,(-30, 30),(0, 15)))    
    for i in range(img.width // view):

        source = pr.Rectangle(i * view + current_view,0, 1,img.height)

        dest = pr.Rectangle(i * view,0,view,img.height)

        pr.draw_texture_pro(texture,source,dest,pr.Vector2(0, 0),0,pr.WHITE)
    
    pr.end_drawing()
    
pr.close_window()