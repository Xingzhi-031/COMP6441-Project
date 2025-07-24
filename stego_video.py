import cv2  # type: ignore
import numpy as np
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _message_to_bits(message: bytes) -> str:
    # Converts byte data to a string of bits
    return ''.join(f'{byte:08b}' for byte in message)


def _bits_to_bytes(bits: str) -> bytes:
    # Turns bit string back into byte sequence
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


def embed_video_message(input_video: str, message: bytes, output_video: str, key: bytes) -> None:
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open input video: {input_video}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    capacity = total_frames * width * height * 3

    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # AES encryption using CBC; prepend length and IV
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    payload = len(ciphertext).to_bytes(4, 'big') + iv + ciphertext
    bits = _message_to_bits(payload)

    if len(bits) > capacity:
        raise ValueError(f"Message too large to embed. Capacity: {capacity // 8} bytes, Needed: {len(bits) // 8} bytes.")

    bit_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        flat = frame.flatten()
        for i in range(len(flat)):
            if bit_idx >= len(bits):
                break
            flat[i] = (flat[i] & 0xFE) | int(bits[bit_idx])
            bit_idx += 1

        modified = flat.reshape(frame.shape)
        out.write(modified)

    cap.release()
    out.release()
    print(f"[✔] Embedded message saved to {output_video}")


def extract_video_message(stego_video: str, key: bytes) -> bytes:
    cap = cv2.VideoCapture(stego_video)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open stego video: {stego_video}")

    print(f"[INFO] Extracting from: {stego_video}")

    # Read enough bits to reconstruct the encrypted payload header
    header_bits = ''
    header_bytes_required = 4 + 16  # Length + IV
    header_bits_needed = header_bytes_required * 8

    while cap.isOpened() and len(header_bits) < header_bits_needed:
        ret, frame = cap.read()
        if not ret:
            break
        flat = frame.flatten()
        header_bits += ''.join(str(pixel & 1) for pixel in flat)

    if len(header_bits) < header_bits_needed:
        raise ValueError("Video too short or header damaged.")

    header = _bits_to_bytes(header_bits)
    cipher_len = int.from_bytes(header[:4], 'big')
    iv = header[4:20]
    full_payload_len = 4 + 16 + cipher_len
    total_bits = full_payload_len * 8

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    bits = ''
    while cap.isOpened() and len(bits) < total_bits:
        ret, frame = cap.read()
        if not ret:
            break
        flat = frame.flatten()
        bits += ''.join(str(pixel & 1) for pixel in flat)

    cap.release()

    if len(bits) < total_bits:
        raise ValueError("Not enough data to recover payload.")

    data = _bits_to_bytes(bits[:total_bits])

    try:
        iv = data[4:20]
        ciphertext = data[20:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        print("[✔] Message extracted and decrypted.")
        return plaintext
    except Exception:
        raise ValueError("Decryption failed. Possibly wrong key or corrupted content.")


def get_output_path(input_path: str) -> str:
    # Builds output filename for stego video
    base = os.path.basename(input_path)
    name, _ = os.path.splitext(base)
    return os.path.join("static", f"StegoOutput{name}.mp4")
