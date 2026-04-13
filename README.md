# Object Tracking System

A robust Python application for real-time multi-object detection and tracking in sports and event footage.

**Original Video Source:** [YouTube Shorts Link](https://youtube.com/shorts/x45N8Ar-0hA?si=7l4acmhKxLoqK_Ys)  
**Complete Tutorial:** [Google Drive Tutorial](https://drive.google.com/file/d/1CB_3u4wQsOYJBpPueCXfPyWhw4sTK_FV/view?usp=drivesdk)

## Output Showcase
Below are examples of the tracker natively maintaining unique IDs across frames and displaying telemetry data.

<div align="center">
  <img src="screenshot1.jpg" width="30%" alt="Tracking Screenshot 1">
  <img src="screenshot2.jpg" width="30%" alt="Tracking Screenshot 2">
  <img src="screenshot3.jpg" width="30%" alt="Tracking Screenshot 3">
</div>

## Architecture Highlights
- **Detection**: YOLOv8 via the `ultralytics` framework.
- **Tracking**: DeepSORT implementation for persistent ID assignment and tracking across frames.
- **Interface**: Built-in Tkinter application for local GUI operations.

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   cd object_tracking_project
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode
To run the tracker using the graphical interface:
```bash
python gui.py
```

### CLI Mode
For automated processing or server deployment:
```bash
python main.py --input data/sample.mp4 --output results/output.mp4
```

## Configuration
Modify `config.py` to adjust:
- Model precision (`yolov8n.pt`, `yolov8s.pt`, etc.)
- Tracking thresholds (confidence filters)
- Visualization settings (trajectory length, colors, ID display)

## Limitations
- High-density occlusions might trigger ID re-assignments depending on the configured tracking age threshold.
- The standard implementation relies on CPU execution. For higher performance, GPU acceleration natively over PyTorch and CUDA is recommended.
