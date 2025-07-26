# StegoChat

## Project Summary

StegoChat is a local information encryption and steganography tool that encrypts plaintext into ciphertext and hides the ciphertext in common media files, such as PNG images, MP4 videos, and WAV audio. It is suitable for conveying sensitive or secret information in inconspicuous scenarios, such as sending a cartoon picture on WhatsApp or email, making the information not only encrypted but also "invisible". Even if intercepted by hackers, it's difficult for them to detect or extract the hidden content.

It uses AES-256 encryption and the Least Significant Bit (LSB) technology to embed data into the carrier file. The system can be operated through either a simple web interface or the command line. It's designed for situations where confidentiality isn't just about encryption, where making the message itself invisible matters.

## Structure

- `app.py` — Launches the local web interface (Flask)
- `server.py` — Handles backend routes and session state
- `crypto.py` — AES-256 encryption and decryption
- `stego_image.py` — LSB embedding/extraction for PNG images
- `stego_video.py` — Frame-wise LSB embedding for MP4 videos
- `stego_audio.py` — Sample-level LSB embedding for WAV audio
- `client.py` — Command-line utility client
- `test_video_stego.py` — Script for testing video embedding/extraction
- `CalculateImagePSNR.py` — Evaluates image quality using PSNR
- `check_video.py` — Checks video integrity post-embedding
- `templates/` — HTML templates for the Flask frontend
- `static/` — Static files including CSS, embedded images/videos
- `IMAGES/` — Sample PNG images used as cover files
- `VIDEOS/` — Sample MP4 videos used as cover files
- `README.md` — This documentation

## Operation Instructions

### Open Web Interface

```bash
python app.py
```

Then open a browser and visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Command Line Example
### Image Steganography

```bash
python stego_image.py embed Chicken.png "secret message" Output.png
python stego_image.py extract Output.png
```

### Video Steganography

```bash
python stego_video.py embed Flower.mp4 "hidden in video" StegoFlower.mp4
python stego_video.py extract StegoFlower.mp4
```

### Audio Steganography

```bash
python stego_audio.py embed audio.wav "hidden in audio" StegoAudio.wav
python stego_audio.py extract StegoAudio.wav
```

## Dependencies
### Installation:

```bash
pip install -r requirements.txt
```

### Required libraries:
- `Flask`
- `OpenCV`
- `NumPy`
- `Cryptography`
- `Pillow`

## Features
- AES-256 encryption using CBC mode with padding
- LSB steganography for PNG, MP4, and WAV
- Support for both CLI and Flask web interface
- Extraction error handling and capacity checking
- Output quality validation (e.g. PSNR) to ensure minimal distortion after embedding

## Sample Output

Stego output examples are saved to `static/`:

- Image output: `StegoOutputChicken.png`, `StegoOutputGarfield.png`
- Video output: `StegoOutputChongqing.mp4`, etc.

Input sample files:

- **Images**: `Chicken.png`, `IceCream.png`, `MyCat.png`
- **Videos**: `Chongqing.mp4`, `Flower.mp4`, `Rainbow.mp4`

## Author
Xingzhi Li
z5527197
COMP6441 Project
Week1-8, Term 2, 2025
GitHub Repo: [https://github.com/Xingzhi-031/COMP6441-Project](https://github.com/Xingzhi-031/COMP6441-Project)
