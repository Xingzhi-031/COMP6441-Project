from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Generate 256-bit AES key
def generate_key():
    return os.urandom(32)

# Encrypt plaintext to ciphertext by AES-CBC
def encrypt_aes(plaintext: bytes, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return iv + ciphertext

# Decrypt ciphertext: iv + actual ciphertext
def decrypt_aes(combined: bytes, key: bytes) -> bytes:
    iv = combined[:16]
    ciphertext = combined[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

# Convert hex string (64 characters) into 32-byte key
def hex_to_key(hex_str: str) -> bytes:
    if len(hex_str) != 64:
        raise ValueError("AES key must be 64 hexadecimal characters (32 bytes)")
    return bytes.fromhex(hex_str)

if __name__ == '__main__':
    msg = b"StegoChat is secure!"
    key = generate_key()

    encrypted = encrypt_aes(msg, key)
    print("Encrypted (hex):", encrypted.hex())

    decrypted = decrypt_aes(encrypted, key)
    print("Decrypted:", decrypted.decode())
