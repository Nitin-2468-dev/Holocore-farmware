import json
import pprint

class Metadata:
    def __init__(self,data):
        self.metadata = json.loads(data)
    
    def show(self):
        pprint.pprint(self.metadata.items())

    def write(self , filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.metadata, file, indent=4, ensure_ascii=False)

    def read(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)
            self.show()

if __name__ == "__main__":

    # Quilt Metadata
        # version — Quilt format version.
        # views — Number of rendered views.
        # rows — Number of quilt rows.
        # cols — Number of quilt columns.
        # view_width — Width of a single view.
        # view_height — Height of a single view.
        # spread — Camera spacing multiplier. Controls perceived depth strength.
        # focus_plane — Zero parallax plane. Controls whether content appears behind, at, or in front of the display.
        # fov — Camera field of view.
    
    data = {
        "version": 1,
        "views": 16,
        "rows": 4,
        "cols": 4,
        "view_width": 512,
        "view_height": 512,
        "camera": {
            "spread": 1.0,
            "focus_plane": 0.0,
            "fov": 90.0
        } 
    }

    Quilt = Metadata(json.dumps(data))
    Quilt.write('quilt_metadata.json')

    # Display Profile
        # width — Display width in pixels.
        # height — Display height in pixels.
        # ppi — Pixels per inch.
        # lpi — Lenticules per inch.
        # pitch_mm — Lens pitch in millimeters.
        # angle_deg — Lens slant angle.
        # subpixel_mode — Enable RGB subpixel rendering. 
    
    data = {
        "width": 1024,
        "height": 600,
        "ppi": 170,
        "lpi": 50,
        "pitch_mm": 0.508,
        "angle_deg": 0.508,
        "subpixel_mode": True
    }
        
    Profile = Metadata(json.dumps(data))
    Profile.write('profile.json')

    Profile.read('profile.json')