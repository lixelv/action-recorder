import cv2
import numpy as np
import mss
import pyautogui
import time
import signal
import sys

def record(filename, fps, monitor, cursor_size=5):

    # Get screen dimensions and monitor position
    with mss.mss() as sct:
        monitor = sct.monitors[monitor]
        monitor_left = monitor['left']
        monitor_top = monitor['top']
        screen_width = monitor["width"]
        screen_height = monitor["height"]

        # Print monitor position and size for debugging
        print(f"Monitor position: left={monitor_left}, top={monitor_top}")
        print(f"Screen size: {screen_width}x{screen_height}")

    # Set up video codec and create video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Use XVID codec
    out = cv2.VideoWriter(filename, fourcc, fps, (screen_width, screen_height))

    def signal_handler(sig, frame):
        """Signal handler for proper termination."""
        print("\nEnding recording...")
        out.release()
        cv2.destroyAllWindows()
        sys.exit(0)

    # Assign signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting screen recording. Press Ctrl+C to stop.")

    # Main recording loop
    with mss.mss() as sct:
        try:
            while True:
                start_time = time.time()

                # Capture screen
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Get cursor position and adjust for monitor offset
                cursor_x, cursor_y = pyautogui.position()
                cursor_x -= monitor_left
                cursor_y -= monitor_top

                # Draw cursor on frame
                cv2.circle(frame, (cursor_x, cursor_y), cursor_size, (0, 0, 255), -1)

                # Write frame to video file
                out.write(frame)

                # Calculate frame processing time and adjust delay
                elapsed_time = time.time() - start_time
                delay = max(1.0 / fps - elapsed_time, 0)
                time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Release resources
            out.release()
            cv2.destroyAllWindows()
            print(f"Screen recording saved to file '{filename}'")

if __name__ == "__main__":
    record("output.avi", 10)
