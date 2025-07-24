# StegoChat 

## Project Summary

StegoChat is a local information encryption and steganography tool that encrypts plaintext into ciphertext and hides the ciphertext in common media files, such as PNG images, MP4 videos, and WAV audio. It is suitable for conveying sensitive or secret information in inconspicuous scenarios, such as sending a cartoon picture on WhatsApp or email, making the information not only encrypted but also "invisible". Even if intercepted by hackers, it's difficult for them to detect or extract the hidden content.

It uses AES-256 encryption and the Least Significant Bit (LSB) technology to embed data into the carrier file. The system can be operated through either a simple web interface or the command line. It's designed for situations where confidentiality isn't just about encryption, where making the message itself invisible matters.

## Structure

- app.py                 # Runs the local web interface (Flask)
- server.py              # Handles backend routes and session state  
- crypto.py              # Implements AES-256 encryption and decryption 
- stego_image.py         # LSB embedding for PNG images  
- stego_video.py         # Frame-wise LSB embedding for MP4 videos  
- stego_audio.py         # Sample-level embedding script for WAV audio  
- client.py              # Utility client script  
- test_video_stego.py    # Test script for video extraction
- CalculateImagePSNR.py  # Image quality evaluation (PSNR)  
- check_video.py         # Video integrity check utility  
- templates/             # HTML scripts for Flask frontend 
- static/                # CSS input media, and embedded output media
- video_files/           # Sample MP4 test files  
- *.png / *.mp4          # Media samples for testing  
- README.md              # This file  

## Operation Instructions

### Open Web Interface

```bash
python app.py
```

Then visit: http://127.0.0.1:5000

## Command Line
### Image

```bash
python stego_image.py embed Chicken.png "secret message" Output.png
python stego_image.py extract Output.png
```

### Video

```bash
python stego_video.py embed Flower.mp4 "hidden in video" StegoFlower.mp4
python stego_video.py extract StegoFlower.mp4
```

### Audio

```bash
python stego_audio.py embed audio.wav "hidden in audio" StegoAudio.wav
python stego_audio.py extract StegoAudio.wav
```

## Dependencies
### To install dependencies:

```bash
pip install -r requirements.txt
```

### Required libraries:
1. Flask
2. OpenCV
3. NumPy
4. Cryptography
5. Pillow

## Features
- AES-256 encryption using CBC mode with padding
- LSB steganography for PNG, MP4, and WAV
- Support for both CLI and Flask web interface
- Extraction error handling and capacity checking
- Output quality validation (e.g. PSNR) to ensure minimal distortion after embedding

## Sample Output
Stego output sample: 'static/StegoOutputGarfield.png'
Test files: 
- Image: 'Chicken.png', 'IceCream.mp4', 'MyCat.png'
- Video: 'Chongqing.mp4', 'Flower.mp4', 'Rainbow.mp4'

## Author
Xingzhi Li
z5527197
COMP6441 Project
Week1-8, Term 2, 2025