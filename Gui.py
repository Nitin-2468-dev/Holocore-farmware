import dearpygui.dearpygui as dpg
import pprint as pp
from PIL import Image
import numpy as np
import math



# ---------------- Image Viewer ----------------

class ImageViewer:
    
    def __init__(self,width, height):
        self.texture_tag = "texture"
        self.image_tag = "preview"
        self.width = width
        self.height = height  
        self.data = [0.0] * (self.width * self.height * 4)  

        with dpg.window(label="Image", tag="image_window"):
            with dpg.texture_registry(tag="texture_registry"):
                # Dummy texture
                dpg.add_dynamic_texture(
                    width=self.width,
                    height=self.height,
                    default_value=self.data,
                    tag=self.texture_tag
                )

            dpg.add_image(self.texture_tag, tag=self.image_tag)

    def load(self, filename):

        # img_w, img_h, channels, pixels = dpg.load_image(filename)
        

        # if img_w != self.width or img_h != self.height:
        #     raise ValueError(
        #         f"Expected {self.width}x{self.height}, "
        #         f"got {img_w}x{img_h}"
        #     )
        
        # self.show(pixels)

        self.load_interlaced(filename ,16, 0)

            
    
    def show(self,data):
        dpg.set_value(self.texture_tag, data)
        self.fit_to_window()

    def fit_to_window(self):
        window_w = dpg.get_item_width("image_window")
        window_h = dpg.get_item_height("image_window") - 10

        scale = min(window_w / self.width, window_h / self.height)

        display_w = int(self.width * scale)
        display_h = int(self.height * scale)

        x = (window_w - display_w) // 2
        y = (window_h - display_h) // 2

        dpg.configure_item(
            self.image_tag,
            texture_tag=self.texture_tag,
            width=display_w,
            height=display_h,
            pos=(x, y)
        )


# ---------------- File Dialog ----------------

class FileDialog:

    def __init__(self , renderer):

        self.renderer = renderer
        self.filename = None

        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=self.callback,
            tag="file_dialog",
            width=400,
            height=400
        ):

            dpg.add_file_extension(".*")
            dpg.add_file_extension(".png")
            dpg.add_file_extension(".jpg")

        with dpg.viewport_menu_bar():
            dpg.add_menu_item(
                label="Open Image",
                callback=lambda: dpg.show_item("file_dialog")
            )

    def callback(self, sender, app_data, user_data):

        self.filename = next(iter(app_data["selections"].values()))

        print(self.filename)

        # self.viewer.load(self.filename)
        self.renderer.load(self.filename)


# ---------------- Main GUI ----------------

class Gui:

    def __init__(self):

        dpg.create_context()
        dpg.create_viewport(
            title="Holocore",
            width=1000,
            height=700
        )

        self.viewer = ImageViewer(width=1920, height=1080)
        self.renderer = self.Renderer()
        self.dialog = FileDialog(self.renderer)

        with dpg.window(label="Controls"):

            dpg.add_slider_int(
                label="Current View",
                min_value=0,
                max_value=15,
                default_value=0,
                callback=self.slider_callback
            )

        dpg.setup_dearpygui()
        dpg.set_primary_window("image_window", True)
        dpg.show_viewport()
        while dpg.is_dearpygui_running():

            self.viewer.fit_to_window()

            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def slider_callback(self, sender, app_data):
            pixels = self.renderer.render(views=16, current_view=app_data)
            self.viewer.show(pixels)

# ---------------- Renderer ----------------

    class Renderer:

        def __init__(self):
            self.image = None
            self.views = 16

        def load(self, filename):
            self.image = np.array(
                Image.open(filename).convert("RGBA")
            )

        def render(self, views, current_view):
            output = np.zeros_like(self.image)
            output[:] = [255, 0, 0, 255]   # red background
            # output[:, current_view::views] = self.image[:, current_view::views]

            stripe = self.image[:, current_view::views]

            output = np.repeat(stripe, views, axis=1)
            output = output[:, :self.image.shape[1]]

            data = output.astype(np.float32) / 255.0
            data = data.flatten().tolist()

            return data



Gui()