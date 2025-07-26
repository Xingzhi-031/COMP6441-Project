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

## PSNR Principle and Design Purpose

**PSNR (Peak Signal-to-Noise Ratio)** is a widely used metric for evaluating the visual quality of images and videos after they have been processed or compressed. It compares the similarity between the original and modified versions by computing the mean squared error (MSE) and converting it to a logarithmic decibel (dB) scale. A higher PSNR value generally indicates better quality — typically, values above 40 dB are considered visually indistinguishable from the original.

In **StegoChat**, PSNR is used to assess the degree to which the embedding process (via LSB steganography) alters the carrier image. This serves two purposes:

- **Integrity Monitoring**: To ensure that embedding the encrypted payload does not significantly distort the visual content.
- **Stealth Verification**: To confirm that the changes introduced are subtle enough to avoid raising suspicion during casual inspection.

The tool `CalculateImagePSNR.py` allows users to measure PSNR between the original and the stego image, helping validate the "invisibility" of the hidden message.


## Sample Output

Stego output examples are saved to `static/`:

- Image output: `StegoOutputChicken.png`, `StegoOutputGarfield.png`
- Video output: `StegoOutputChongqing.mp4`, etc.

Input sample files:

- **Images**: `Chicken.png`, `IceCream.png`, `MyCat.png`
- **Videos**: `Chongqing.mp4`, `Flower.mp4`, `Rainbow.mp4`

## Screen Recording Introduction

To help users better understand the logic, operation, and design of StegoChat, a folder of annotated screen recordings is provided: [ScreenRecordingIntroduction/](https://github.com/Xingzhi-031/COMP6441-Project/tree/main/ScreenRecordingIntroduction).

These include:
- **Environment+Library Introduction.mov** – Setup and dependencies
- **Scripts Introduction.mov** – Walkthrough of key Python scripts
- **Logic_Sender.mov** – Demonstrates the encryption and embedding logic
- **Logic_Receiver.mov** – Explains the extraction and decryption flow
- **Theme+PSNR Analysis.mov** – UI light/dark themes and PSNR explanation
- **image_test_recording.mov** – Recording of image embedding via web interface
- **video_test_demo.mov** – Recording of video embedding via web interface

A higher-resolution, full version of the demonstration video is also available on YouTube: [https://youtu.be/hVhF0LCP3ww](https://youtu.be/hVhF0LCP3ww)

##  Generative AI Use and Attribution

Some portions of this README document (e.g., structure refinement, grammar correction) were improved using ChatGPT (OpenAI, 2025).
The original content, ideas, and technical implementation are fully authored by Xingzhi Li.
Generative AI was not used to generate ideas, code, analysis, or any part of the conceptual design.
All AI assistance was used only after a first full human draft was completed, in line with UNSW's Generative AI guidance.

## Author
Xingzhi Li
z5527197
COMP6441 Project
Week1-8, Term 2, 2025
GitHub Repo: [https://github.com/Xingzhi-031/COMP6441-Project](https://github.com/Xingzhi-031/COMP6441-Project)
