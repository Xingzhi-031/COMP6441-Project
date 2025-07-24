import wave
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _msg_to_bitstream(raw_msg):
    return ''.join(f'{b:08b}' for b in raw_msg)


def _bitstream_to_bytes(bitstring):
    # Grab 8 bits at a time and rebuild the original bytes
    return bytes(int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8))


def embed_audio_message(source_wav, msg, target_wav, key_material):
    wf = wave.open(source_wav, 'rb')
    num_frames = wf.getnframes()
    pcm_data = bytearray(wf.readframes(num_frames))
    audio_fmt = wf.getparams()
    wf.close()

    # Encrypt with AES-CBC using random IV
    iv = get_random_bytes(16)
    aes = AES.new(key_material, AES.MODE_CBC, iv)
    cipherblob = aes.encrypt(pad(msg, AES.block_size))
    total_payload = iv + cipherblob

    bits = _msg_to_bitstream(total_payload)

    if len(bits) > len(pcm_data):
        print(f"[!] Not enough room in audio: need {len(bits)} bits, have {len(pcm_data)} bytes")
        raise ValueError("Insufficient audio space")

    changes = 0
    for i in range(len(bits)):
        old = pcm_data[i]
        pcm_data[i] = (pcm_data[i] & 0b11111110) | int(bits[i])
        if pcm_data[i] != old:
            changes += 1

    print(f"[i] Modified {changes} bytes for embedding")

    with wave.open(target_wav, 'wb') as out_wav:
        out_wav.setparams(audio_fmt)
        out_wav.writeframes(pcm_data)


def extract_audio_message(stego_wav_path, secret_key):
    wf = wave.open(stego_wav_path, 'rb')
    raw = bytearray(wf.readframes(wf.getnframes()))
    wf.close()

    # Extract LSBs — assuming max 2KB payload
    lsb_bits = ''
    chunk_limit = 16000  # approx 2KB

    for i in range(min(chunk_limit, len(raw))):
        lsb_bits += str(raw[i] & 1)

    # Attempt decrypt
    try:
        byte_data = _bitstream_to_bytes(lsb_bits)
        iv = byte_data[:16]
        ciphertext = byte_data[16:]

        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)

        # Might raise if padding is invalid
        cleartext = unpad(decrypted, AES.block_size)
        return cleartext

    except Exception as err:
        print("[x] Decryption failed:", err)
        raise ValueError("Could not extract message. Possibly wrong key or corrupted audio.")
