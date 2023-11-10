from ultralytics import YOLO
import cv2
import cvzone
import math
from streamlit_webrtc import webrtc_streamer,RTCConfiguration, WebRtcMode
import av
from twilio_tokens import get_ice_servers

model = YOLO('yolov8n.pt')

# cap = cv2.VideoCapture(0)
# cap.set(3,640) # width
# cap.set(4,360) # height

class VideoProcess():
    def recv(self, frame):
        frm = frame.to_ndarray(format='bgr24')
        results = model(frm, stream=True, verbose=False)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # opencv
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0,200,0), 3)

                # cvzone
                w, h = x2-x1, y2-y1
                cvzone.cornerRect(frm, (x1, y1, w, h))

                conf = math.ceil(box.conf[0])
                # Class Name
                cls = int(box.cls[0])

                cvzone.putTextRect(frm, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
        return av.VideoFrame.from_ndarray(frm, format='bgr24')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": get_ice_servers()},
    video_frame_callback=VideoProcess,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# webrtc_streamer(key='Video', video_processor_factory=VideoProcess,
#                 rtc_configuration=RTCConfiguration(
#                     {"username": "ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e",
#                     "ice_servers": [{'url': 'stun:global.stun.twilio.com:3478', 
#                                      'urls': 'stun:global.stun.twilio.com:3478'}, 
#                                      {'url': 'turn:global.turn.twilio.com:3478?transport=udp', 
#                                       'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
#                                       'urls': 'turn:global.turn.twilio.com:3478?transport=udp', 
#                                       'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}, 
#                                     {'url': 'turn:global.turn.twilio.com:3478?transport=tcp', 
#                                      'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
#                                      'urls': 'turn:global.turn.twilio.com:3478?transport=tcp', 
#                                      'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}, 
#                                     {'url': 'turn:global.turn.twilio.com:443?transport=tcp', 
#                                      'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
#                                      'urls': 'turn:global.turn.twilio.com:443?transport=tcp', 
#                                      'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}],
#                     "date_updated": "2023-11-10 17:47:31+00:00",
#                     "account_sid": "AC049053b997790d028fc79f82a0f5561c",
#                     "ttl": "86400",
#                     "date_created": "2023-11-10 17:47:31+00:00",
#                     "password": "MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig="
#                     }))