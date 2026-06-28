from tracker.head_tracker import HeadTracker
import pprint as pp

tracker = HeadTracker()

while True:

    face = tracker.update()

    if face:

        pp.pprint(face)