import os

TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))

FACE_MODEL_PATH = os.path.join(TRACKER_DIR, "face_landmarker.task")
POSE_MODEL_PATH = os.path.join(TRACKER_DIR, "pose_landmarker.task")

FACE_INTERVAL = 0.05 
POSE_INTERVAL = 0.5

EAR_THRESHOLD = 0.22              
BLINK_FRAME_CONSECUTIVE = 2       
SHOULDER_DIST_LIMIT_RATIO = 1.20  
NECK_DIST_LIMIT_RATIO = 0.94
LEFT_EYE = {
    "v1": (160, 144),  
    "v2": (158, 153),  
    "h":  (33, 133)    
}

RIGHT_EYE = {
    "v1": (387, 373),
    "v2": (385, 380),
    "h":  (362, 263)
}

LEFT_EAR_IDX = 7
RIGHT_EAR_IDX = 8

LEFT_SHOULDER_IDX = 11
RIGHT_SHOULDER_IDX = 12
