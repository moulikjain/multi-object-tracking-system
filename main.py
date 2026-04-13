import argparse
import cv2
import time
import sys

from detector import ObjectDetector
from tracker import ObjectTracker
from utils import Visualizer, setup_video_writer

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-Object Detection and Tracking")
    parser.add_argument("--input", type=str, required=True, help="Path to input video file")
    parser.add_argument("--output", type=str, required=True, help="Path to output video file")
    return parser.parse_args()

def main():
    args = parse_args()

    # Initialize components
    print("Initializing YOLOv8 Detector...")
    detector = ObjectDetector()
    
    print("Initializing DeepSORT Tracker...")
    tracker = ObjectTracker()
    
    visualizer = Visualizer()
    
    # Open input video
    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        print(f"Error: Could not open video file {args.input}")
        sys.exit(1)
        
    # Setup output video
    out = setup_video_writer(cap, args.output)
    
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {total_frames} frames...")
    
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. Detection
        detections = detector.detect(frame)
        
        # 2. Tracking
        tracks = tracker.update(detections, frame)
        
        # Calculate FPS
        end_time = time.time()
        fps = 1.0 / (end_time - start_time) if (end_time - start_time) > 0 else 0
        
        # 3. Visualization
        annotated_frame = visualizer.draw(frame, tracks, fps)
        
        # 4. Write frame
        out.write(annotated_frame)
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames")
            
    # Cleanup
    cap.release()
    out.release()
    print("Processing complete!")
    print(f"Output saved to {args.output}")

if __name__ == "__main__":
    main()
