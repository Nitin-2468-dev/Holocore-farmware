import cv2
from .OpenSeeFace.tracker import Tracker
from dataclasses import dataclass

@dataclass
class HeadPose:
    x: float
    y: float
    z: float
    yaw: float
    pitch: float
    roll: float

class HeadTracker:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        ok, frame = self.cap.read()

        if not ok:
            raise RuntimeError("Cannot open camera")

        h, w = frame.shape[:2]

        self.tracker = Tracker(
            w,
            h,
            max_faces=1,
            model_type=3
        )

    def update(self):

        ok, frame = self.cap.read()

        if not ok:
            return None

        faces = self.tracker.predict(frame)

        if len(faces) == 0:
            return None

        face = faces[0]

        translation = face.translation
        rotation = face.euler

        return HeadPose(
            x=translation[0],
            y=translation[1],
            z=translation[2],
            yaw=rotation[1],
            pitch=rotation[0],
            roll=rotation[2],
        )