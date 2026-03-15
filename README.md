# CamRec Vision Playground

A lightweight webcam video recorder and computer vision playground built with Python and OpenCV. It supports live preview, recording, visual effects, brightness/contrast control, codec switching, and real-time experimentation with webcam frames.

---

## Overview

This project started as a webcam recorder assignment and was extended into a small **computer vision sandbox** for learning image processing in real time.

With this app, you can:
- preview your webcam feed live
- record processed video
- switch between multiple visual effects
- adjust brightness and contrast interactively
- change FPS and codec before recording
- experiment with frame-based computer vision ideas

---

## Features

### Core Features
- **Real-time Camera Display** using OpenCV's `cv.VideoCapture`
- **Preview / Record Mode Toggle** with keyboard input
- **Video Recording** with timestamped output filenames
- **Recording Indicator** (`REC` + red circle) while recording
- **FPS Adjustment** before recording starts
- **Codec Switching** between available codecs, with matching output file extension
- **Horizontal Flip** for mirror-like preview
- **On-screen Status Overlay** for mode, flip, FPS, codec, effect, brightness, and contrast

### Computer Vision Playground Features
- **Normal mode**
- **Negative effect**
- **Grayscale effect**
- **Canny edge detection**
- **Blur effect**
- **Frame difference** (current frame vs previous frame)
- **Background subtraction**
- **Cartoon effect**
- **Pixelation effect**
- **RGB glitch effect**
- **Interactive brightness control**
- **Interactive contrast control**

---

## Requirements

- Python 3.10+
- OpenCV
- NumPy

Install dependencies with:

```bash
py -m pip install opencv-python numpy
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Laura77-code/webcam-recorder.git
cd webcam-recorder
```

---

## Run the Project

On Windows:

```bash
py main.py
```

If `python main.py` does not work correctly on your machine, use `py main.py`.

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start / stop recording |
| `ESC` | Exit application |
| `F` | Toggle horizontal flip |
| `C` | Change codec |
| `+` / `=` | Increase FPS |
| `-` | Decrease FPS |
| `I` | Increase brightness |
| `K` | Decrease brightness |
| `O` | Increase contrast |
| `L` | Decrease contrast |
| `1` | Normal |
| `2` | Negative |
| `3` | Grayscale |
| `4` | Canny edges |
| `5` | Blur |
| `6` | Frame difference |
| `7` | Background subtraction |
| `8` | Cartoon |
| `9` | Pixelate |
| `0` | RGB glitch |

---

## How It Works

1. Run the program.
2. The webcam feed opens in preview mode.
3. Select an effect using the number keys.
4. Adjust brightness and contrast if needed.
5. Press `SPACE` to start recording.
6. Press `SPACE` again to stop and save the video.
7. Press `ESC` to exit.

---

## Output

Recorded videos are saved automatically with timestamped filenames.

Example:

```text
recordings/recorded_20260315_153210.avi
```
---

## Technical Notes

- Webcam frames are captured with `cv.VideoCapture(0)`
- Recorded files are written using `cv.VideoWriter`
- Effects are applied frame by frame in real time
- Some effects operate on grayscale internally and are converted back to BGR for display/recording
- Background subtraction uses OpenCV's built-in subtractor
- Frame difference compares the current frame with the previous one
- The output file extension is matched to the selected codec for better compatibility

---

## Learning Goals

This project is useful for practicing:
- webcam input/output with OpenCV
- image representation in NumPy
- geometric transformations such as flip
- photometric changes such as brightness and contrast
- edge detection
- temporal frame processing
- simple computer vision experimentation in real time

---

## Troubleshooting

### Camera does not open
- Make sure no other application is using the webcam
- Try changing the camera index in the code:

```python
cap = cv.VideoCapture(1)
```

- On some Windows systems this may help:

```python
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
```
- 

### `python main.py` does not run correctly
Use:

```bash
py main.py
```

### Output video is not created
- Check that the selected codec is supported on your machine
- Make sure the app has permission to write files
- The app automatically matches the file extension to the selected codec
- Try a different codec such as `mp4v`, `XVID`, or `MJPG`

---

## Suggested Project Structure

```text
webcam-recorder/
├── main.py
├── README.md
├── recordings/
    └── recorded_<timestamp>.avi

```

## Author

Laura Morales - 24101204  
Computer Vision course project.
