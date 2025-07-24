from PIL import Image
from crypto import decrypt_aes
import cv2  # type: ignore
import numpy as np
from binascii import unhexlify

# Calculate PSNR between two images to check distortion level
def calculate_psnr(original_path, stego_path):
    original_image = cv2.imread(original_path)
    stego_image = cv2.imread(stego_path)

    if original_image is None or stego_image is None:
        raise FileNotFoundError("Could not load one or both images")

    if original_image.shape != stego_image.shape:
        raise ValueError("Image sizes must match for PSNR calculation")

    mse = np.mean((original_image - stego_image) ** 2)
    if mse == 0:
        return float('inf')

    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr

# Try to extract and decrypt a message from a stego image
def extract_message(image_path: str, key: bytes) -> bytes:
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size

    bit_string = ''
    for y in range(height):
        for x in range(width):
            red, green, blue = pixels[x, y]
            bit_string += str(red & 1)
            bit_string += str(green & 1)
            bit_string += str(blue & 1)

    for byte_length in range(32, len(bit_string) // 8, 16):
        try:
            candidate_bytes = bytes(int(bit_string[i:i+8], 2) for i in range(0, byte_length * 8, 8))
            plaintext = decrypt_aes(candidate_bytes, key)
            return plaintext
        except Exception:
            continue

    raise ValueError("Unable to decrypt any valid message from image")

# Simple CLI tool for testing extraction and PSNR
def debug_image_stego():
    print("=== StegoChat Image Debugging ===")
    original_path = input("Enter path to original image (e.g. static/InputGarfield.png): ").strip()
    stego_path = input("Enter path to stego image (e.g. static/StegoOutputGarfield.png): ").strip()
    key_hex = input("Enter AES key in hex (64 characters): ").strip()

    try:
        key = unhexlify(key_hex)
        if len(key) != 32:
            raise ValueError("AES key must be 32 bytes (64 hex characters)")
    except Exception as error:
        print("Invalid AES key:", error)
        return

    try:
        psnr_value = calculate_psnr(original_path, stego_path)
        print(f"PSNR: {psnr_value:.2f} dB")
    except Exception as error:
        print("PSNR calculation failed:", error)
        print("Hint: Check that both images have the same resolution.")

    try:
        message = extract_message(stego_path, key)
        try:
            print("Decrypted message (UTF-8):", message.decode('utf-8'))
        except UnicodeDecodeError:
            print("Decrypted message (raw bytes):", message)
    except Exception as error:
        print("Message extraction or decryption failed:", error)

if __name__ == "__main__":
    debug_image_stego()
