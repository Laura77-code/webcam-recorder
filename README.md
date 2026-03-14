# CamRec - WebCam Video Recorder

A lightweight, easy-to-use video recorder application built with Python and OpenCV. Capture your webcam stream in real-time with preview and recording modes.

---

## Demo

### Screenshot
<p align="center">
  <img src="vid%20recorder%20img.png" alt="Video Recorder Application" width="400">
</p>

### Application in Action
![Application Demo](demoVid.mp4)

### Sample Output Recording
![Sample Recording](recorded_20260314_235119.mp4)

---

## Features

### Core Features (Required)
- **Real-time Camera Display**: View live webcam stream using OpenCV's `cv.VideoCapture`
- **Mode Toggle**: Switch between Preview and Record modes
- **Video Recording**: Save webcam stream as MP4 video files with automatic timestamped filenames
- **Recording Indicator**: Visual red circle indicator displayed during recording
- **Customizable Settings**: Adjust FPS and select different video codecs (MP4V, XVID, MJPG) on the fly
- **Keyboard Controls**: 
  - `SPACE` - Toggle between Preview and Record modes
  - `F` - Toggle horizontal flip
  - `+` / `-` - Increase or decrease FPS (while in Preview)
  - `C` - Cycle through available video codecs (while in Preview)
  - `ESC` - Exit application

### Additional Features
- **Horizontal Flip**: Press `F` to flip the video horizontally (useful for mirror-like preview)
- **Automatic Naming**: Video files are automatically named with timestamps (format: `recorded_YYYYMMDD_HHMMSS.mp4`)
- **Codec Configuration**: Uses MP4v codec for broad compatibility
- **Status Display**: On-screen display shows current mode and flip status

## Requirements

- Python 3.6+
- OpenCV (cv2)

## Installation

### 1. Install OpenCV

```bash
pip install opencv-python
```

### 2. Clone or Download This Repository

```bash
git clone https://github.com/Laura77-code/webcam-recorder.git
cd webcam-recorder
```

## Usage

Run the application:

```bash
python hw1.py
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `SPACE` | Toggle between Preview and Record modes |
| `F` | Toggle horizontal flip on/off |
| `+` / `=` | Increase recording FPS (Max 60) |
| `-` / `_` | Decrease recording FPS (Min 1) |
| `C` | Cycle through video codecs (MP4V, XVID, MJPG) |
| `ESC` | Exit the application |

### How It Works

1. **Start the program** - Camera feed displays in a window
2. **Preview Mode** - Default mode where you see the live camera feed
3. **Record Mode** - Press `SPACE` to start recording (red REC indicator appears)
4. **Stop Recording** - Press `SPACE` again to stop and save the video
5. **Exit** - Press `ESC` to close the application

## Output

Recorded video files are saved in the same directory with timestamped filenames:
- Example: `recorded_20260314_143022.mp4`

## Technical Specifications

- **Video Codecs**: Supports MP4v, XVID, and MJPG
- **Adjustable FPS**: Range from 1 to 60 FPS (Default: 20.0)
- **Resolution**: Matches your camera's native resolution
- **Format**: MP4 container

## Future Enhancements

Potential improvements for future versions:
- Adjustable FPS and codec selection
- Video effects (grayscale, blur, edge detection)
- Brightness and contrast adjustment
- Screen capture option
- Video format selection (AVI, MOV, etc.)
- Resolution adjustment UI

## Troubleshooting

### Camera Not Opening
- Ensure your webcam is connected and working
- Check if another application is using your camera
- Try a different camera index (modify `cv.VideoCapture(0)` to `cv.VideoCapture(1)`)

### Video File Not Created
- Check that you have write permissions in the application directory
- Ensure sufficient disk space available
- Try restarting the application

### Poor Video Quality
- Ensure adequate lighting for the camera
- Some webcams require a moment to auto-focus
- Adjust FPS in the code if needed (modify `fps` parameter in `create_writer()`)

## Project Structure

```
webcam-recorder/
├── hw1.py          # Main application
├── README.md       # This file
└── recorded_*.mp4  # Generated video files
```

## License

This project is open source and available for educational purposes.

## Author
Laura Morales - 24101204
Created as a Computer Vision course assignment.

