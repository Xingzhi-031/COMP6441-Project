from PIL import Image
import numpy as np
import os
import cv2  # type: ignore
from crypto import encrypt_aes, decrypt_aes

# Converts bytes to binary string
def bytes_to_bits(data):
    return ''.join(format(b, '08b') for b in data)

# Converts binary string back to bytes
def bits_to_bytes(bitstring):
    result = []
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        if len(byte) == 8:
            result.append(int(byte, 2))
    return bytes(result)

# Resizes image if dimensions are not 512x512
def resize_if_needed(image, size=(512, 512)):
    if image.size != size:
        print(f"Resizing image from {image.size} to {size}")
        return image.resize(size)
    return image

# Saves pixel difference image between original and stego
def show_difference(orig_path, stego_path, out_path="static/diff_output.png"):
    orig = cv2.imread(orig_path)
    mod = cv2.imread(stego_path)
    if orig.shape != mod.shape:
        raise ValueError("Image dimensions must match")

    diff = cv2.absdiff(orig, mod)
    diff *= 20
    diff = np.clip(diff, 0, 255).astype(np.uint8)
    cv2.imwrite(out_path, diff)
    print(f"Saved difference image to {out_path}")

# Computes PSNR value between original and stego
def calculate_psnr(orig_path, stego_path):
    original = cv2.imread(orig_path)
    altered = cv2.imread(stego_path)
    if original.shape != altered.shape:
        raise ValueError("Size mismatch")

    err = np.mean((original - altered) ** 2)
    if err == 0:
        return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(err))

# Encrypts and embeds message into image
def embed_message_into_image(input_image_path, plaintext, output_image_path, aes_key):
    img = Image.open(input_image_path).convert('RGB')
    img = resize_if_needed(img)
    w, h = img.size
    pix = img.load()

    encrypted = encrypt_aes(plaintext, aes_key)
    bitstream = bytes_to_bits(encrypted)
    bit_total = len(bitstream)

    if bit_total > w * h * 3:
        raise ValueError("Message too large")

    idx = 0
    change_counter = 0

    for y in range(h):
        for x in range(w):
            if idx >= bit_total:
                break

            r, g, b = pix[x, y]
            r0, g0, b0 = r, g, b

            if idx < bit_total:
                r = (r & ~1) | int(bitstream[idx])
                idx += 1
            if idx < bit_total:
                g = (g & ~1) | int(bitstream[idx])
                idx += 1
            if idx < bit_total:
                b = (b & ~1) | int(bitstream[idx])
                idx += 1

            if (r, g, b) != (r0, g0, b0):
                change_counter += 1

            pix[x, y] = (r, g, b)

        if idx >= bit_total:
            break

    img.save(output_image_path)
    print(f"Embedded message into {output_image_path}")
    print(f"{change_counter} pixels changed")

    input_base = os.path.basename(input_image_path)
    name, ext = os.path.splitext(input_base)
    if name.startswith("Input"):
        name = name[len("Input"):]
    resized_input_path = os.path.join("static", f"InputResized{name}{ext}")
    img.save(resized_input_path)

    try:
        psnr = calculate_psnr(resized_input_path, output_image_path)
        print(f"PSNR: {psnr:.2f} dB")
        show_difference(resized_input_path, output_image_path)
        return psnr
    except Exception as e:
        print("PSNR calculation failed:", e)
        return None

# Extracts message and decrypts it
def extract_message_from_image(stego_path, aes_key):
    img = Image.open(stego_path).convert('RGB')
    w, h = img.size
    pix = img.load()

    bits = ''
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    for guess_len in range(32, len(bits) // 8, 16):
        try:
            candidate = bits_to_bytes(bits[:guess_len * 8])
            result = decrypt_aes(candidate, aes_key)
            return result
        except Exception:
            continue

    raise ValueError("No valid message found")

# Generates output filename from input
def build_output_filename(input_file_path):
    name, ext = os.path.splitext(os.path.basename(input_file_path))
    if name.startswith("Input"):
        name = name[len("Input"):]
    return os.path.join("static", f"StegoOutput{name}{ext}")

# CLI usage for manual testing
if __name__ == "__main__":
    from crypto import generate_key

    key = generate_key()
    message = b"This is a demo message for steganography."

    images = [f for f in os.listdir('.') if f.lower().endswith('.png') and '_stego' not in f]
    print("Available PNGs:")
    for f in images:
        print("-", f)

    filename = input("Enter image filename: ").strip()
    name_only, ext = os.path.splitext(filename)
    out_file = name_only + "_stego" + ext

    embed_message_into_image(filename, message, out_file, key)
    recovered = extract_message_from_image(out_file, key)
    print("Extracted:", recovered.decode(errors="replace"))
