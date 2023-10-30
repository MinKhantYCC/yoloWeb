from ultralytics import YOLO
import cv2
import cvzone
import math
from streamlit_webrtc import webrtc_streamer,RTCConfiguration
import av

class VideoProcess:
    def recv(self, frame):
        frm = frame.to_ndarray(format='bgr24')
        return av.VideoFrame.from_ndarray(frm, format='bgr24')

webrtc_streamer(key='Video', video_processor_factory=VideoProcess,
                rtc_configuration=RTCConfiguration(
                    {"iceServers": [{'urls':["stun:stun.l.google.com:19302"]}]}
                ))