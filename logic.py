# logic.py
import wave
import zlib
from security import encrypt_data, decrypt_data

# ... create_header and parse_header remain the same as the previous final version ...
def create_header(secret_filename, original_size, flags):
    filename_bytes = secret_filename.encode('utf-8')
    header = flags.to_bytes(1, 'big')
    header += filename_bytes.ljust(255, b'\0')
    header += original_size.to_bytes(4, 'big')
    return header

def parse_header(stego_frames):
    header_bytes_to_read = (1 + 255 + 4)
    if len(stego_frames) < header_bytes_to_read * 8:
        raise ValueError("Stego file is too small to contain a valid header.")
    header_bits = ''.join(str(frame & 1) for frame in stego_frames[:header_bytes_to_read * 8])
    header_bytes = bytearray(int(header_bits[i:i+8], 2) for i in range(0, len(header_bits), 8))
    flags = header_bytes[0]
    is_compressed = (flags & 1) == 1
    is_encrypted = (flags & 2) == 2
    filename = header_bytes[1:256].rstrip(b'\0').decode('utf-8')
    original_size = int.from_bytes(header_bytes[256:260], 'big')
    return filename, original_size, is_compressed, is_encrypted

def hide_data(cover_path, secret_data, secret_filename, output_path, password, compress, progress_callback):
    """Hides data (bytes) into a cover audio file."""
    try:
        progress_callback("Processing secret data...", 0.1)
        original_size = len(secret_data)
        flags = 0
        
        if compress:
            progress_callback("Compressing data...", 0.2)
            secret_data = zlib.compress(secret_data, level=9)
            flags |= 1
            
        if password:
            progress_callback("Encrypting data...", 0.3)
            secret_data = encrypt_data(secret_data, password)
            flags |= 2
        
        progress_callback("Creating header...", 0.4)
        header = create_header(secret_filename, original_size, flags)
        data_to_hide = header + secret_data
        
        progress_callback("Reading cover audio...", 0.5)
        with wave.open(cover_path, 'rb') as cover_audio:
            params = cover_audio.getparams()
            cover_frames = bytearray(cover_audio.readframes(cover_audio.getnframes()))
        
        if len(data_to_hide) * 8 > len(cover_frames):
            raise ValueError("Cover audio is too small to hide this data.")
            # #################################################
            # #################################################
            # #################################################
        progress_callback("Hiding data in audio (LSB)...", 0.6)
        bits_to_hide = ''.join(format(byte, '08b') for byte in data_to_hide)
        
        for i, bit in enumerate(bits_to_hide):
            cover_frames[i] = (cover_frames[i] & 0b11111110) | int(bit)
            if i % 20000 == 0:
                progress_callback(f"Hiding bits... {i}/{len(bits_to_hide)}", 0.6 + 0.3 * (i / len(bits_to_hide)))
            # #################################################
            # #################################################
            # #################################################
        progress_callback("Writing output file...", 0.9)
        with wave.open(output_path, 'wb') as stego_audio:
            stego_audio.setparams(params)
            stego_audio.writeframes(bytes(cover_frames))
        
        progress_callback("Done! Data hidden successfully.", 1.0)
    except Exception as e:
        raise e

def extract_data(stego_path, password, progress_callback):
    """Extracts data and returns it as bytes along with the original filename."""
    try:
        progress_callback("Reading stego audio file...", 0.1)
        with wave.open(stego_path, 'rb') as stego_audio:
            stego_frames = bytearray(stego_audio.readframes(stego_audio.getnframes()))

        progress_callback("Parsing header...", 0.25)
        filename, original_size, is_compressed, is_encrypted = parse_header(stego_frames)
        
        if is_encrypted and not password:
            raise ValueError("Password required to decrypt the data.")
        
        header_size_bytes = 1 + 255 + 4
        
        progress_callback("Extracting data bits...", 0.4)
        # This is a complex part. We estimate how much to read.
        # A more robust solution might store the final data size in the header.
        # For now, we extract a large chunk and let the decrypt/decompress logic handle it.
        # This simplification can fail if the data is highly uncompressible.
        max_possible_bits = len(stego_frames) - (header_size_bytes * 8)
        
        extracted_bits_generator = (str(stego_frames[i] & 1) for i in range(header_size_bytes * 8, header_size_bytes * 8 + max_possible_bits))
        
        progress_callback("Reconstructing data...", 0.7)
        extracted_bytes = bytearray()
        
        # Read bits in chunks to build bytes
        # This is more memory efficient than joining a massive string
        bit_buffer = ""
        for bit in extracted_bits_generator:
            bit_buffer += bit
            if len(bit_buffer) == 8:
                extracted_bytes.append(int(bit_buffer, 2))
                bit_buffer = ""

        secret_data = bytes(extracted_bytes)
        if is_encrypted:
            progress_callback("Decrypting data...", 0.8)
            secret_data = decrypt_data(secret_data, password)

        if is_compressed:
            progress_callback("Decompressing data...", 0.9)
            secret_data = zlib.decompress(secret_data)
        
        # VERY IMPORTANT: Truncate to the original size stored in the header
        secret_data = secret_data[:original_size]
        
        progress_callback("Extraction complete. Ready for preview.", 1.0)
        return secret_data, filename
    except Exception as e:
        raise e