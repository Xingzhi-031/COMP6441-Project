import cv2  # type: ignore
import sys

# Print basic info and steganographic capacity of a video file
def check_video_properties(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {video_path}")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0
    embedding_capacity_bytes = (frame_count * width * height * 3) // 8  # LSB per channel

    print("Video Properties:")
    print(f"  Resolution: {width} x {height}")
    print(f"  FPS: {fps}")
    print(f"  Total Frames: {frame_count}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Approximate Embedding Capacity: {embedding_capacity_bytes:,} bytes")

    # Warnings for potentially unsuitable files
    if width < 320 or height < 240:
        print("Warning: Resolution is very low (< 320x240)")

    if duration < 2:
        print("Warning: Duration is short (< 2 seconds)")

    if fps < 24:
        print("Warning: Frame rate is low (< 24), may affect playback quality")

    cap.release()

# CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_video.py <video_path>")
    else:
        check_video_properties(sys.argv[1])
