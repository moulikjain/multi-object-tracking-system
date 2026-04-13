from ultralytics import YOLO
import config

class ObjectDetector:
    def __init__(self):
        # Initialize the YOLOv8 model
        self.model = YOLO(config.MODEL_NAME)
        self.confidence_threshold = config.CONFIDENCE_THRESHOLD
        self.classes_to_detect = config.CLASSES_TO_DETECT

    def detect(self, frame):
        """
        Runs object detection on a single frame.
        
        Args:
            frame: numpy array representing the image frame.
            
        Returns:
            detections: List of tuples representing the detections in deep_sort format:
                        ([left, top, w, h], confidence, detection_class)
        """
        # Perform inference
        # YOLOv8 returns a list of Results objects (one per image if batch is 1)
        results = self.model(frame, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                
                # Filter by class and confidence
                if conf < self.confidence_threshold:
                    continue
                if self.classes_to_detect and class_id not in self.classes_to_detect:
                    continue
                
                # YOLO returns xyxy (top-left x, top-left y, bottom-right x, bottom-right y)
                # deep_sort_realtime expects ([left, top, w, h], confidence, detection_class)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                w = x2 - x1
                h = y2 - y1
                
                detections.append(([x1, y1, w, h], conf, class_id))
                
        return detections
