from typing import List

# General Settings
MODEL_NAME = "yolov8n.pt"  # Use 'yolov8s.pt' or others for better accuracy

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5
# COCO class IDs. Person is 0. Add more if needed (e.g., car is 2)
CLASSES_TO_DETECT: List[int] = [0] 

# Tracker Settings
MAX_AGE = 30           # Maximum number of frames to keep a track alive without a new detection
N_INIT = 3             # Number of consecutive detections before a track is confirmed

# Display / Output Video Settings
DISPLAY_FPS = True
DRAW_TRAJECTORY = True
TRAJECTORY_LENGTH = 30 # Number of past positions to store for drawing
SHOW_OBJECT_COUNT = True
