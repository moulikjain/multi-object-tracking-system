import cv2
import numpy as np
from collections import defaultdict
import config

class Visualizer:
    def __init__(self):
        # Store trajectories: track_id -> list of center points (x, y)
        self.trajectories = defaultdict(list)
        # Store all unique object IDs seen
        self.unique_objects = set()

    def draw(self, frame, tracks, fps=None):
        """
        Draws bounding boxes, IDs, trajectories, and statistics on the frame.
        
        Args:
            frame: current image frame (numpy array).
            tracks: list of track objects returned by deep_sort_realtime.
            fps: current frames per second (optional).
            
        Returns:
            frame: the annotated frame.
        """
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            self.unique_objects.add(track_id)
            
            # get_ltrb returns Left, Top, Right, Bottom
            ltrb = track.to_ltrb()
            class_id = track.get_det_class()
            
            x1, y1, x2, y2 = map(int, ltrb)
            
            # Draw bounding box
            color = self._get_color(int(track_id))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw ID label
            label = f"ID: {track_id}"
            cv2.putText(frame, label, (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Trajectory drawing
            if config.DRAW_TRAJECTORY:
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                self.trajectories[track_id].append((center_x, center_y))
                
                # Keep only recent points
                if len(self.trajectories[track_id]) > config.TRAJECTORY_LENGTH:
                    self.trajectories[track_id].pop(0)
                
                # Draw trajectory lines
                points = self.trajectories[track_id]
                for i in range(1, len(points)):
                    thickness = int(np.sqrt(64 / float(i + 1)) * 2)
                    cv2.line(frame, points[i - 1], points[i], color, thickness)
                    
        # Draw Statistics (Object Count and FPS)
        if config.SHOW_OBJECT_COUNT:
            count_label = f"Unique Objects Count: {len(self.unique_objects)}"
            cv2.putText(frame, count_label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
        if config.DISPLAY_FPS and fps is not None:
            fps_label = f"FPS: {fps:.1f}"
            cv2.putText(frame, fps_label, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        return frame

    def _get_color(self, idx):
        """Generates a consistent color for a given track id."""
        np.random.seed(int(idx))
        color = np.random.randint(0, 255, size=3).tolist()
        return tuple(color)

def setup_video_writer(cap, output_path):
    """
    Sets up the VideoWriter.
    
    Args:
        cap: cv2.VideoCapture object.
        output_path: path to save the output video.
        
    Returns:
        out: cv2.VideoWriter object.
    """
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Use mp4v codec for .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    return out
