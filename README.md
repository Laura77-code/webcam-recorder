# CamRec - Webcam Video Recorder

A simple and easy-to-use video recorder application built with Python and OpenCV. Record your webcam stream in real-time with a preview mode and recording mode.

---



## Quick Start

### Install Requirements
```bash
pip install opencv-python
```

### Run the Program
```bash
python hw1.py
```

---

## Features

### Required Features
✅ **Live Camera Display** - See your webcam feed in real-time using `cv.VideoCapture`  
✅ **Video Recording** - Save your webcam as MP4 video files using `cv.VideoWriter`  
✅ **Preview & Record Modes** - Switch between viewing and recording  
✅ **Recording Indicator** - Red circle appears when recording  
✅ **Simple Controls** - Space to toggle mode, ESC to exit  

### Additional Features
✨ **Horizontal Flip** - Press `F` to mirror the video  
✨ **Auto-Named Files** - Videos saved as `recorded_YYYYMMDD_HHMMSS.mp4`  
✨ **Custom Settings** - Adjustable FPS and codec options  

---

## How to Use

| Key | Function |
|-----|----------|
| **SPACE** | Switch between Preview and Record modes |
| **F** | Flip video horizontally |
| **ESC** | Exit the program |

**Simple workflow:**
1. Start the program → camera appears
2. Press SPACE → red circle shows recording started
3. Press SPACE → video is saved
4. Press ESC → exit

---

## Demo

### Screenshot
<p align="center">
  <img src="vid%20recorder%20img.png" alt="Video Recorder Application" width="400">
</p>

### Sample Video
Click to view or download:
**[📹 Watch Sample Video](recorded_20260314_215839.mp4)** (MP4, 2.89 MB)

---

## Technical Details

| Setting | Value |
|---------|-------|
| **Codec** | MP4v |
| **FPS** | 20 frames per second |
| **Format** | MP4 |
| **Resolution** | Native camera resolution |

---

## File Structure

```
CamRec/
├── hw1.py                    # Main program
├── README.md                 # This file
└── recorded_*.mp4            # Your saved videos
```

---

## License


Laura Morales
Open source for educational purposes.
