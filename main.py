import cv2 as cv
from datetime import datetime


def create_writer(frame_width, frame_height, fps=20.0, codec="mp4v"):
    """
    Create a VideoWriter with a timestamped filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_{timestamp}.mp4"

    # Define the codec using FourCC
    fourcc = cv.VideoWriter_fourcc(*codec)
    writer = cv.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

    return writer, filename


def draw_recording_indicator(frame):
    """
    Draw a red circle and REC text on the frame.
    """
    cv.circle(frame, (30, 30), 12, (0, 0, 255), -1)
    cv.putText(
        frame,
        "REC",
        (55, 38),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
        cv.LINE_AA
    )


def draw_status_text(frame, mode, flip_enabled, fps, codec):
    """
    Draw mode and extra feature status on the frame.
    """
    # Current Mode
    cv.putText(
        frame,
        f"Mode: {mode}",
        (10, frame.shape[0] - 100),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv.LINE_AA
    )

    # Flip Status
    cv.putText(
        frame,
        f"Flip: {'ON' if flip_enabled else 'OFF'}",
        (10, frame.shape[0] - 70),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv.LINE_AA
    )

    # FPS Setting
    cv.putText(
        frame,
        f"FPS: {fps}",
        (10, frame.shape[0] - 40),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv.LINE_AA
    )

    # Codec Setting
    cv.putText(
        frame,
        f"Codec: {codec}",
        (10, frame.shape[0] - 10),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv.LINE_AA
    )


def main():
    # Open webcam (0 is usually the default webcam)
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Read one frame first to get frame size
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read from camera.")
        cap.release()
        return

    frame_height, frame_width = frame.shape[:2]

    recording = False
    flip_enabled = False
    writer = None
    output_filename = None

    # Settings
    fps = 20.0
    codecs = ["mp4v", "XVID", "MJPG"]
    codec_idx = 0

    print("=== Video Recorder ===")
    print("SPACE: Toggle Preview / Record")
    print("F    : Toggle horizontal flip")
    print("+ / -: Adjust FPS")
    print("C    : Cycle Codec")
    print("ESC  : Exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        # Extra feature: flip horizontally
        if flip_enabled:
            frame = cv.flip(frame, 1)

        display_frame = frame.copy()

        # Draw mode info
        mode_text = "Record" if recording else "Preview"
        draw_status_text(display_frame, mode_text, flip_enabled, fps, codecs[codec_idx])

        # If recording, draw indicator and write frame
        if recording:
            draw_recording_indicator(display_frame)
            writer.write(frame)

        cv.imshow("Video Recorder", display_frame)

        key = cv.waitKey(1) & 0xFF

        # ESC -> exit
        if key == 27:
            break

        # SPACE -> toggle Preview / Record
        elif key == 32:
            recording = not recording

            if recording:
                writer, output_filename = create_writer(
                    frame_width, frame_height, fps=fps, codec=codecs[codec_idx]
                )
                print(f"Recording started: {output_filename} (FPS: {fps}, Codec: {codecs[codec_idx]})")
            else:
                if writer is not None:
                    writer.release()
                    writer = None
                    print(f"Recording stopped. Saved as: {output_filename}")

        # F -> extra feature: horizontal flip
        elif key == ord('f') or key == ord('F'):
            flip_enabled = not flip_enabled
            print(f"Flip {'enabled' if flip_enabled else 'disabled'}.")

        # + / = -> increase FPS (max 60)
        elif key == ord('+') or key == ord('='):
            if not recording:
                fps = min(60.0, fps + 1.0)
                print(f"FPS increased to: {fps}")

        # - / _ -> decrease FPS (min 1)
        elif key == ord('-') or key == ord('_'):
            if not recording:
                fps = max(1.0, fps - 1.0)
                print(f"FPS decreased to: {fps}")

        # C -> cycle through codecs
        elif key == ord('c') or key == ord('C'):
            if not recording:
                codec_idx = (codec_idx + 1) % len(codecs)
                print(f"Codec changed to: {codecs[codec_idx]}")

    # Cleanup
    if writer is not None:
        writer.release()

    cap.release()
    cv.destroyAllWindows()
    print("Program closed.")


if __name__ == "__main__":
    main()