from stego_video import extract_video_message

key = b'MySecretKey123456'
video_path = 'static/StegoOutputflower.mp4'

message = extract_video_message(video_path, key)
print("Extracted:", message.decode())
