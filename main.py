import cv2 as cv
import os
from datetime import datetime
import numpy as np


# =========================
# CONFIG
# =========================
OUTPUT_DIR = "recordings"
DEFAULT_FPS = 20
CODECS = ["mp4v", "XVID", "MJPG"]


# =========================
# VIDEO WRITER
# =========================
def create_writer(frame_width, frame_height, fps, codec):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(
        OUTPUT_DIR,
        f"recorded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    )
    fourcc = cv.VideoWriter_fourcc(*codec)
    writer = cv.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
    if not writer.isOpened():
        return None, None
    return writer, filename


# =========================
# OVERLAYS
# =========================
def draw_recording_indicator(frame):
    cv.circle(frame, (30, 30), 10, (0, 0, 255), -1)
    cv.putText(frame, "REC", (50, 36), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


def draw_status_text(frame, is_recording, flip_enabled, fps, codec, effect, brightness, contrast):
    mode_text = "Mode: RECORD" if is_recording else "Mode: PREVIEW"
    flip_text = f"Flip: {'ON' if flip_enabled else 'OFF'}"
    fps_text = f"FPS: {fps}"
    codec_text = f"Codec: {codec}"
    effect_text = f"Effect: {effect}"
    bc_text = f"Brightness: {brightness}  Contrast: {contrast:.2f}"

    cv.putText(frame, mode_text, (10, frame.shape[0] - 110),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv.putText(frame, flip_text, (10, frame.shape[0] - 85),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv.putText(frame, fps_text, (10, frame.shape[0] - 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv.putText(frame, codec_text, (10, frame.shape[0] - 35),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv.putText(frame, effect_text, (10, frame.shape[0] - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

    cv.putText(frame, bc_text, (10, 25),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)


def draw_help(frame):
    help_lines = [
        "SPACE: Record ON/OFF   ESC: Exit   F: Flip   C: Change codec",
        "+/-: FPS   I/K: Brightness   O/L: Contrast",
        "1 Normal  2 Negative  3 Gray  4 Canny  5 Blur",
        "6 Diff  7 BG Sub  8 Cartoon  9 Pixelate  0 RGB Glitch"
    ]

    y = 55
    for line in help_lines:
        cv.putText(frame, line, (10, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        y += 22


# =========================
# EFFECTS
# =========================
def apply_brightness_contrast(frame, brightness=0, contrast=1.0):
    temp = frame.astype(np.float32) * contrast + brightness
    temp = np.clip(temp, 0, 255)
    return temp.astype(np.uint8)


def effect_negative(frame):
    return 255 - frame


def effect_gray(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return cv.cvtColor(gray, cv.COLOR_GRAY2BGR)


def effect_canny(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 100, 200)
    return cv.cvtColor(edges, cv.COLOR_GRAY2BGR)


def effect_blur(frame):
    return cv.GaussianBlur(frame, (15, 15), 0)


def effect_diff(frame, prev_frame):
    if prev_frame is None:
        return frame
    return cv.absdiff(frame, prev_frame)


def effect_bgsub(frame, bg_sub):
    mask = bg_sub.apply(frame)
    return cv.cvtColor(mask, cv.COLOR_GRAY2BGR)


def effect_cartoon(frame):
    color = cv.bilateralFilter(frame, 9, 75, 75)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 7)
    edges = cv.adaptiveThreshold(
        gray, 255,
        cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY,
        9, 7
    )
    edges = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
    return cv.bitwise_and(color, edges)


def effect_pixelate(frame, pixel_size=16):
    h, w = frame.shape[:2]
    small = cv.resize(frame, (max(1, w // pixel_size), max(1, h // pixel_size)), interpolation=cv.INTER_LINEAR)
    return cv.resize(small, (w, h), interpolation=cv.INTER_NEAREST)


def effect_rgb_glitch(frame):
    h, w = frame.shape[:2]
    b, g, r = cv.split(frame)

    shift_r = 10
    shift_g = -10

    M_r = np.float32([[1, 0, shift_r], [0, 1, 0]])
    M_g = np.float32([[1, 0, shift_g], [0, 1, 0]])

    r_shifted = cv.warpAffine(r, M_r, (w, h))
    g_shifted = cv.warpAffine(g, M_g, (w, h))

    return cv.merge([b, g_shifted, r_shifted])


def apply_effect(frame, effect_name, prev_frame=None, bg_sub=None, brightness=0, contrast=1.0):
    base = apply_brightness_contrast(frame, brightness, contrast)

    if effect_name == "normal":
        out = base
    elif effect_name == "negative":
        out = effect_negative(base)
    elif effect_name == "gray":
        out = effect_gray(base)
    elif effect_name == "canny":
        out = effect_canny(base)
    elif effect_name == "blur":
        out = effect_blur(base)
    elif effect_name == "diff":
        out = effect_diff(base, prev_frame)
    elif effect_name == "bgsub":
        out = effect_bgsub(base, bg_sub)
    elif effect_name == "cartoon":
        out = effect_cartoon(base)
    elif effect_name == "pixelate":
        out = effect_pixelate(base)
    elif effect_name == "rgb_glitch":
        out = effect_rgb_glitch(base)
    else:
        out = base

    return out


# =========================
# MAIN
# =========================
def main():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        cap.release()
        return

    frame_height, frame_width = frame.shape[:2]

    is_recording = False
    flip_enabled = False
    fps = DEFAULT_FPS
    codec_index = 0
    codec = CODECS[codec_index]
    writer = None
    filename = None

    effect = "normal"
    brightness = 0
    contrast = 1.0

    prev_frame = None
    bg_sub = cv.createBackgroundSubtractorMOG2(history=300, varThreshold=25, detectShadows=True)

    print("Controls:")
    print("  SPACE  - Start/Stop recording")
    print("  F      - Toggle horizontal flip")
    print("  C      - Change codec")
    print("  + / -  - Increase/Decrease FPS")
    print("  I / K  - Increase/Decrease brightness")
    print("  O / L  - Increase/Decrease contrast")
    print("  1      - Normal")
    print("  2      - Negative")
    print("  3      - Grayscale")
    print("  4      - Canny")
    print("  5      - Blur")
    print("  6      - Difference with previous frame")
    print("  7      - Background subtraction")
    print("  8      - Cartoon")
    print("  9      - Pixelate")
    print("  0      - RGB glitch")
    print("  ESC    - Exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Could not read frame. Exiting.")
            break

        raw_frame = frame.copy()

        if flip_enabled:
            raw_frame = cv.flip(raw_frame, 1)

        processed_frame = apply_effect(
            raw_frame,
            effect_name=effect,
            prev_frame=prev_frame,
            bg_sub=bg_sub,
            brightness=brightness,
            contrast=contrast
        )

        display_frame = processed_frame.copy()

        if is_recording:
            draw_recording_indicator(display_frame)
            if writer is not None:
                writer.write(processed_frame)

        draw_status_text(display_frame, is_recording, flip_enabled, fps, codec, effect, brightness, contrast)
        draw_help(display_frame)

        cv.imshow("CamRec Vision Playground", display_frame)

        prev_frame = raw_frame.copy()

        key = cv.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break

        elif key == 32:  # SPACE
            if not is_recording:
                writer, filename = create_writer(frame_width, frame_height, fps, codec)
                if writer is None:
                    print("Error: Could not create VideoWriter.")
                else:
                    is_recording = True
                    print(f"Recording started: {filename}")
            else:
                is_recording = False
                if writer is not None:
                    writer.release()
                    writer = None
                print("Recording stopped.")

        elif key in (ord('f'), ord('F')):
            flip_enabled = not flip_enabled

        elif key in (ord('c'), ord('C')):
            if not is_recording:
                codec_index = (codec_index + 1) % len(CODECS)
                codec = CODECS[codec_index]
                print(f"Codec changed to: {codec}")
            else:
                print("Cannot change codec while recording.")

        elif key in (ord('+'), ord('=')):
            if not is_recording:
                fps += 1
                print(f"FPS increased to: {fps}")
            else:
                print("Cannot change FPS while recording.")

        elif key == ord('-'):
            if not is_recording and fps > 1:
                fps -= 1
                print(f"FPS decreased to: {fps}")
            else:
                print("Cannot change FPS while recording or FPS already minimum.")

        elif key in (ord('i'), ord('I')):
            brightness = min(brightness + 10, 100)
            print(f"Brightness: {brightness}")

        elif key in (ord('k'), ord('K')):
            brightness = max(brightness - 10, -100)
            print(f"Brightness: {brightness}")

        elif key in (ord('o'), ord('O')):
            contrast = min(contrast + 0.1, 3.0)
            print(f"Contrast: {contrast:.2f}")

        elif key in (ord('l'), ord('L')):
            contrast = max(contrast - 0.1, 0.2)
            print(f"Contrast: {contrast:.2f}")

        elif key == ord('1'):
            effect = "normal"
        elif key == ord('2'):
            effect = "negative"
        elif key == ord('3'):
            effect = "gray"
        elif key == ord('4'):
            effect = "canny"
        elif key == ord('5'):
            effect = "blur"
        elif key == ord('6'):
            effect = "diff"
        elif key == ord('7'):
            effect = "bgsub"
        elif key == ord('8'):
            effect = "cartoon"
        elif key == ord('9'):
            effect = "pixelate"
        elif key == ord('0'):
            effect = "rgb_glitch"

    if writer is not None:
        writer.release()

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()