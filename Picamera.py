from picamera2 import Picamera2
from libcamera import Transform
from threading import Thread
from datetime import datetime
import numpy as np
import cv2

class Picam2MultiThread:
    def __init__(self, main_size=(640, 480), lores_size=(160, 120),
                 framerate=25.0, verbose=False, rec_vid=0,
                 vid_downsample_factor=3, vid_keepframe_itv=1,
                 vid_framerate=25.0):
        frame_dur = int(1000000.0 / framerate)
        self.cam = Picamera2()
        self.video_config = self.cam.create_video_configuration(main={"size": main_size, "format": "RGB888"},
                                                                 lores={"size": lores_size, "format": "YUV420"},
                                                                 transform=Transform(hflip=True, vflip=True))
        self.cam.configure(self.video_config)
        self.cam.set_controls({"FrameDurationLimits": (frame_dur, frame_dur)})
        self.frame = np.zeros((main_size[0], main_size[1], 3), np.uint8)
        self.stopped = False
        self.total_frame = 0
        self.fps = 0.0
        self.verbose = verbose
        self.rec_vid = rec_vid
        self.vid_downsample_factor = vid_downsample_factor
        self.vid_keepframe_itv = vid_keepframe_itv
        self.vid_framerate = vid_framerate

    def start(self):
        print("camera streaming starting!")
        Thread(target=self.stream).start()
        return self

    def stream(self):
        if self.rec_vid == 1:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            vid_fn = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.avi'
            vidwriter = cv2.VideoWriter(vid_fn, fourcc, self.vid_framerate, (self.frame.shape[1], self.frame.shape[0]))

        self.cam.start()

        while not self.stopped:
            (frame, _), metadata = self.cam.capture_arrays(["main", "lores"])
            last_timestamp = self.frame_timestamp
            self.frame, self.frame_timestamp = frame, metadata["SensorTimestamp"]

            if self.total_frame == 0:
                self.first_frame_timestamp = self.frame_timestamp
            else:
                self.fps = float(1e9 / (self.frame_timestamp - last_timestamp))

            self.total_frame += 1
            self.metadata = metadata

            if self.verbose:
                print(self.total_frame, self.frame_timestamp, self.fps)

            if self.rec_vid == 1 and (self.total_frame - 1) % self.vid_keepframe_itv == 0:
                vidwriter.write(frame)

        if self.rec_vid == 1:
            vidwriter.release()
            print('video saved to', vid_fn)

        self.cam.stop()
        print("camera streaming stopped")

    def stop(self):
        self.stopped = True
