from deep_sort_realtime.deepsort_tracker import DeepSort
import config

class ObjectTracker:
    def __init__(self):
        # Initialize DeepSORT
        self.tracker = DeepSort(
            max_age=config.MAX_AGE,
            n_init=config.N_INIT,
            nms_max_overlap=1.0,
            max_cosine_distance=0.2, # Re-identification tolerance
            nn_budget=None,
            override_track_class=None,
            embedder="mobilenet",
            half=True,
            bgr=True,
            embedder_gpu=True
        )
        
    def update(self, detections, frame):
        """
        Updates the tracker with new detections.
        
        Args:
            detections: List of detections from the detector: ([left, top, w, h], confidence, detection_class)
            frame: the current video frame (numpy array) used by DeepSORT for appearance embedding.
            
        Returns:
            tracks: List of updated tracks.
        """
        # DeepSort update expects detections to be passed in
        # It handles matching, occlusion, identity maintenance
        tracks = self.tracker.update_tracks(detections, frame=frame)
        return tracks
