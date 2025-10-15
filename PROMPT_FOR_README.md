## 📁 Project Source Code

### File: `main.py`

```python
# main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import tempfile
import atexit
from logic import hide_data, extract_data
from utils import preview_handler
from ui.widgets import FileInputFrame

# --- Temp file management ---
temp_dir = tempfile.mkdtemp()
def cleanup_temp_dir():
    import shutil
    shutil.rmtree(temp_dir)
atexit.register(cleanup_temp_dir)

# --- THEME & STYLE DEFINITIONS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") # Using the 'blue' theme as a base

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔊 Professional Audio Steganography Suite")
        self.geometry("1100x850")
        self.minsize(900, 700)

        # --- Style & Font Definitions ---
        self.title_font = ctk.CTkFont(family="Arial", size=26, weight="bold")
        self.label_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.button_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.log_font = ctk.CTkFont(family="Consolas", size=12)

        # Class variables for extracted data
        self.extracted_data = None
        self.extracted_filename = None

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Audio Steganography Suite", font=self.title_font).grid(row=0, column=0, padx=20, pady=20)

        self.main_frame = ctk.CTkFrame(self, fg_color="#1D1D1D", corner_radius=10) # A slightly different bg color
        self.main_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1); self.main_frame.grid_rowconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self.main_frame, corner_radius=8)
        self.tab_view.pack(padx=15, pady=15, fill="both", expand=True)
        self.tab_view.add("🔐 Hide Data"); self.tab_view.add("🔓 Extract Data")
        
        self._create_hide_tab()
        self._create_extract_tab()
        
        # --- Bottom Bar ---
        self.log_console = ctk.CTkTextbox(self, height=90, state="disabled", font=self.log_font, corner_radius=8)
        self.log_console.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(self, mode='determinate', height=8, corner_radius=8)
        self.progress_bar.set(0); self.progress_bar.grid(row=3, column=0, padx=20, pady=(0,15), sticky="ew")

    def _log(self, message):
        self.log_console.configure(state="normal")
        self.log_console.insert("end", f"> {message}\n"); self.log_console.see("end")
        self.log_console.configure(state="disabled")

    def _update_progress(self, message, value):
        self._log(message); self.progress_bar.set(value); self.update_idletasks()
    
    # ======================== HIDE TAB ========================
    def _create_hide_tab(self):
        tab = self.tab_view.tab("🔐 Hide Data")
        tab.grid_columnconfigure(0, weight=1); tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        input_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="Inputs & Options", label_font=self.label_font)
        input_scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.cover_audio_frame = FileInputFrame(input_scroll_frame, "1. Cover Audio (.wav)", [("WAV files", "*.wav")], self._log)
        self.cover_audio_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(input_scroll_frame, text="2. Secret Data", font=self.label_font).pack(pady=(10,0), padx=20, anchor="w")
        self.input_mode_selector = ctk.CTkSegmentedButton(input_scroll_frame, values=["File", "Text"], command=self._switch_input_mode, font=self.button_font)
        self.input_mode_selector.pack(pady=5, padx=10, fill="x"); self.input_mode_selector.set("File")

        self.input_container = ctk.CTkFrame(input_scroll_frame, fg_color="transparent")
        self.input_container.pack(fill="x", expand=True, padx=0, pady=0)

        self.secret_file_frame = FileInputFrame(self.input_container, "", [("All files", "*.*")], self._log)
        self.secret_file_frame.pack(fill="x", expand=True)
        
        self.secret_text_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.secret_text_box = ctk.CTkTextbox(self.secret_text_frame, height=280, corner_radius=8)
        self.secret_text_box.pack(pady=5, padx=10, fill="both", expand=True)
        
        options_frame = ctk.CTkFrame(input_scroll_frame)
        options_frame.pack(pady=20, padx=10, fill="x")
        ctk.CTkLabel(options_frame, text="3. Options & Action", font=self.label_font).pack(pady=5, padx=10, anchor="w")
        self.password_entry_hide = ctk.CTkEntry(options_frame, placeholder_text="Password (optional)", show="*", corner_radius=8)
        self.password_entry_hide.pack(pady=5, padx=10, fill="x")
        self.compress_check = ctk.CTkCheckBox(options_frame, text="Compress data"); self.compress_check.select()
        self.compress_check.pack(pady=5, padx=10, anchor="w")
        self.hide_button = ctk.CTkButton(options_frame, text="Start Hiding", height=45, command=self._start_hiding_thread, font=self.button_font, corner_radius=8)
        self.hide_button.pack(pady=20, padx=10, fill="x")

        self.hide_preview_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="Secret Data Preview", label_font=self.label_font)
        self.hide_preview_scroll_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.hide_preview_scroll_frame, text="Preview of secret data will appear here", text_color="gray").pack(expand=True)
        self.secret_text_box.bind("<KeyRelease>", self._update_hide_preview_from_text)
        self._switch_input_mode("File") # Set initial state

    def _switch_input_mode(self, value):
        self.secret_file_frame.pack_forget(); self.secret_text_frame.pack_forget()
        if value == "File":
            self.secret_file_frame.pack(fill="x", expand=True)
            path = self.secret_file_frame.get()
            if path: self.secret_file_frame.update_preview(path)
        else:
            self.secret_text_frame.pack(fill="x", expand=True)
            self._update_hide_preview_from_text()

    def _update_hide_preview_from_text(self, event=None):
        text = self.secret_text_box.get("1.0", "end-1c")
        preview_handler.create_text_preview(self.hide_preview_scroll_frame, text)

    # ======================== EXTRACT TAB ========================
    def _create_extract_tab(self):
        tab = self.tab_view.tab("🔓 Extract Data")
        tab.grid_columnconfigure(0, weight=1); tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        input_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="Inputs & Options", label_font=self.label_font)
        input_scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.stego_audio_frame = FileInputFrame(input_scroll_frame, "1. Stego Audio (.wav)", [("WAV files", "*.wav")], self._log)
        self.stego_audio_frame.pack(padx=10, pady=10, fill="x")
        
        options_frame = ctk.CTkFrame(input_scroll_frame)
        options_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(options_frame, text="2. Options & Action", font=self.label_font).pack(pady=5, padx=10, anchor="w")
        self.password_entry_extract = ctk.CTkEntry(options_frame, placeholder_text="Password (if required)", show="*", corner_radius=8)
        self.password_entry_extract.pack(pady=5, padx=10, fill="x")
        self.extract_button = ctk.CTkButton(options_frame, text="🔍 Extract & Preview", height=45, command=self._start_extracting_thread, font=self.button_font, corner_radius=8)
        self.extract_button.pack(pady=20, padx=10, fill="x")
        
        self.extract_preview_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="Extracted Data Preview", label_font=self.label_font)
        self.extract_preview_scroll_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.extract_preview_scroll_frame, text="Extracted data will be shown here", text_color="gray").pack(expand=True)
        
        self.save_button = ctk.CTkButton(tab, text="💾 Save to Disk", state="disabled", height=45, command=self._save_extracted_file, font=self.button_font, corner_radius=8)
        self.save_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def _start_hiding_thread(self):
        cover = self.cover_audio_frame.get()
        if not cover: messagebox.showerror("Error", "Please select a cover audio file."); return
        mode = self.input_mode_selector.get()
        if mode == "File":
            secret_path = self.secret_file_frame.get()
            if not secret_path: messagebox.showerror("Error", "Please select a secret file."); return
            with open(secret_path, 'rb') as f: secret_data = f.read()
            secret_filename = os.path.basename(secret_path)
        else: # Text
            secret_data = self.secret_text_box.get("1.0", "end-1c").encode('utf-8')
            if not secret_data: messagebox.showerror("Error", "Please enter text to hide."); return
            secret_filename = "message.txt"
        password = self.password_entry_hide.get(); compress = self.compress_check.get()
        output = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if not output: return
        threading.Thread(target=self._run_hide, args=(cover, secret_data, secret_filename, output, password, compress), daemon=True).start()

    def _run_hide(self, cover, secret_data, filename, output, password, compress):
        try:
            self.hide_button.configure(state="disabled")
            hide_data(cover, secret_data, filename, output, password, compress, self._update_progress)
            messagebox.showinfo("Success", f"Data hidden successfully in\n{output}")
        except Exception as e: self._log(f"ERROR: {e}"); messagebox.showerror("Error", str(e))
        finally: self.hide_button.configure(state="normal")
            
    def _start_extracting_thread(self):
        stego = self.stego_audio_frame.get()
        if not stego: messagebox.showerror("Error", "Please select a stego file."); return
        password = self.password_entry_extract.get()
        self.save_button.configure(state="disabled"); self.extracted_data = None
        threading.Thread(target=self._run_extract, args=(stego, password), daemon=True).start()

    def _run_extract(self, stego, password):
        try:
            self.extract_button.configure(state="disabled")
            self.extracted_data, self.extracted_filename = extract_data(stego, password, self._update_progress)
            self._update_extract_preview()
            messagebox.showinfo("Success", "Data extracted! Preview is now available.")
        except Exception as e: self._log(f"ERROR: {e}"); messagebox.showerror("Error", str(e))
        finally: self.extract_button.configure(state="normal")

    def _update_extract_preview(self):
        for widget in self.extract_preview_scroll_frame.winfo_children(): widget.destroy()
        if not self.extracted_data: return
        
        ext = os.path.splitext(self.extracted_filename)[1].lower()
        if ext in ['.wav', '.mp3']:
            temp_path = os.path.join(temp_dir, self.extracted_filename)
            with open(temp_path, 'wb') as temp_file:
                temp_file.write(self.extracted_data)
            preview_handler.create_waveform_preview(self.extract_preview_scroll_frame, temp_path, self._log)
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            preview_handler.create_image_preview(self.extract_preview_scroll_frame, self.extracted_data)
        elif ext in ['.txt', '.py', '.md', '.json']:
            preview_handler.create_text_preview(self.extract_preview_scroll_frame, self.extracted_data, from_bytes=True)
        else:
            preview_handler.create_info_preview(self.extract_preview_scroll_frame, filename=self.extracted_filename, data=self.extracted_data)
        
        self.save_button.configure(state="normal")

    def _save_extracted_file(self):
        if not self.extracted_data: messagebox.showwarning("Warning", "No data to save."); return
        path = filedialog.asksaveasfilename(initialfile=self.extracted_filename)
        if path:
            try:
                with open(path, 'wb') as f: f.write(self.extracted_data)
                self._log(f"File saved to {path}"); messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e: messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

### File: `logic.py`

```python
# logic.py
import wave
import zlib
from security import encrypt_data, decrypt_data

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
            
        progress_callback("Hiding data in audio (LSB)...", 0.6)
        bits_to_hide = ''.join(format(byte, '08b') for byte in data_to_hide)
        
        for i, bit in enumerate(bits_to_hide):
            cover_frames[i] = (cover_frames[i] & 0b11111110) | int(bit)
            if i % 20000 == 0:
                progress_callback(f"Hiding bits... {i}/{len(bits_to_hide)}", 0.6 + 0.3 * (i / len(bits_to_hide)))
            
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
        max_possible_bits = len(stego_frames) - (header_size_bytes * 8)
        
        extracted_bits_generator = (str(stego_frames[i] & 1) for i in range(header_size_bytes * 8, header_size_bytes * 8 + max_possible_bits))
        
        progress_callback("Reconstructing data...", 0.7)
        extracted_bytes = bytearray()
        
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
        
        secret_data = secret_data[:original_size]
        
        progress_callback("Extraction complete. Ready for preview.", 1.0)
        return secret_data, filename
    except Exception as e:
        raise e
```

### File: `security.py`

```python
# security.py
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data: bytes, password: str) -> bytes:
    """Encrypts data with a password."""
    if not password:
        return data
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return salt + encrypted_data

def decrypt_data(encrypted_data_with_salt: bytes, password: str) -> bytes:
    """Decrypts data with a password."""
    if not password:
        return encrypted_data_with_salt
    try:
        salt = encrypted_data_with_salt[:16]
        encrypted_data = encrypted_data_with_salt[16:]
        key = derive_key(password, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data)
    except Exception as e:
        raise ValueError(f"Decryption failed. Incorrect password or corrupted data. Details: {e}")
```

### File: `ui/widgets.py`

```python
# ui/widgets.py
import customtkinter as ctk
from tkinter import filedialog
import os
from utils import preview_handler

class FileInputFrame(ctk.CTkFrame):
    def __init__(self, master, label_text, file_types=None, progress_callback=None):
        super().__init__(master, fg_color="transparent")
        
        self.file_types = file_types
        self.progress_callback = progress_callback
        
        ctk.CTkLabel(self, text=label_text, font=("Arial", 14, "bold")).pack(pady=(5,0), padx=10, anchor="w")
        self.entry = ctk.CTkEntry(self, placeholder_text="No file selected...")
        self.entry.pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self, text="📁 Browse...", command=self.browse_file).pack(pady=(0,10), padx=10, anchor="w")

        self.preview_frame = ctk.CTkFrame(self, height=200)
        self.preview_frame.pack(pady=5, padx=10, fill="both", expand=True)
        ctk.CTkLabel(self.preview_frame, text="Preview will be shown here", text_color="gray").pack(expand=True)
    
    def get(self):
        return self.entry.get()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=self.file_types if self.file_types else [])
        if path:
            self.entry.delete(0, 'end')
            self.entry.insert(0, path)
            self.update_preview(path)
    
    def update_preview(self, path):
        if not path or not os.path.exists(path): return

        ext = path.split('.')[-1].lower()
        if ext in ['wav', 'mp3']:
            preview_handler.create_waveform_preview(self.preview_frame, path, self.progress_callback)
        elif ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
            preview_handler.create_image_preview(self.preview_frame, path)
        elif ext in ['txt', 'py', 'md', 'json']:
            preview_handler.create_text_preview(self.preview_frame, path, from_file=True)
        else:
            preview_handler.create_info_preview(self.preview_frame, file_path=path)
```

### File: `utils/audio_player.py`

```python
# utils/audio_player.py
import simpleaudio as sa
import threading
import numpy as np
import os
import io

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

current_playback = None

def play_audio(audio_path, progress_callback):
    global current_playback
    stop_audio()
    
    try:
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub is required to play audio.")

        ext = os.path.splitext(audio_path)[1].lower()
        if ext == '.wav':
            audio = AudioSegment.from_wav(audio_path)
        elif ext == '.mp3':
            audio = AudioSegment.from_mp3(audio_path)
        else:
            audio = AudioSegment.from_file(audio_path)

        data = audio.raw_data
        samplerate = audio.frame_rate
        num_channels = audio.channels
        bytes_per_sample = audio.sample_width

        def player_thread():
            global current_playback
            progress_callback(f"▶️ Playing {os.path.basename(audio_path)}...")
            current_playback = sa.play_buffer(data, num_channels, bytes_per_sample, samplerate)
            current_playback.wait_done()
            progress_callback("⏹️ Playback finished.")
            current_playback = None

        threading.Thread(target=player_thread, daemon=True).start()

    except Exception as e:
        progress_callback(f"Error playing audio: {e}")

def stop_audio():
    global current_playback
    if current_playback and current_playback.is_playing():
        sa.stop_all()
        current_playback = None
        return True
    return False
```

### File: `utils/preview_handler.py`

```python
# utils/preview_handler.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import io
import numpy as np
from . import audio_player

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

plt.style.use('dark_background')

def create_waveform_preview(frame, audio_path, progress_callback):
    """Generates and embeds a waveform plot for audio files using a thread-safe method."""
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is not installed.")

        ext = os.path.splitext(audio_path)[1].lower()
        if ext == '.wav':
            audio = AudioSegment.from_wav(audio_path)
        elif ext == '.mp3':
            audio = AudioSegment.from_mp3(audio_path)
        else:
            raise NotImplementedError(f"Preview for {ext} is not supported.")
        
        audio = audio.set_channels(1)
        data = np.array(audio.get_array_of_samples())

        fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
        fig.patch.set_facecolor('#2B2B2B')
        ax.set_facecolor('#242424')
        ax.plot(data, color='#1F6AA5', linewidth=0.5)
        ax.set_title("Audio Waveform", color='white', fontsize=10)
        ax.tick_params(axis='x', colors='gray'); ax.tick_params(axis='y', colors='gray')
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        image_label = ctk.CTkLabel(frame, image=ctk_img, text="")
        image_label.pack(fill="both", expand=True, padx=5, pady=5)

        control_frame = ctk.CTkFrame(frame, fg_color="transparent")
        control_frame.pack(pady=5)
        play_button = ctk.CTkButton(control_frame, text="Play ▶", command=lambda: audio_player.play_audio(audio_path, progress_callback))
        play_button.pack(side="left", padx=5)
        stop_button = ctk.CTkButton(control_frame, text="Stop ■", command=lambda: progress_callback("⏹️ Playback stopped.") if audio_player.stop_audio() else None)
        stop_button.pack(side="left", padx=5)

    except Exception as e:
        ctk.CTkLabel(frame, text=f"⚠️\nCould not plot waveform:\n{e}", text_color="gray").pack(expand=True)

def create_image_preview(frame, file_path_or_data):
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        img = Image.open(io.BytesIO(file_path_or_data) if isinstance(file_path_or_data, bytes) else file_path_or_data)
        img.thumbnail((350, 250))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        label = ctk.CTkLabel(frame, image=ctk_img, text="")
        label.pack(expand=True, padx=5, pady=5)
    except Exception as e:
        ctk.CTkLabel(frame, text=f"🖼️\nInvalid Image:\n{e}", text_color="gray").pack(expand=True)

def create_text_preview(frame, text_content, from_file=False, from_bytes=False):
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        textbox = ctk.CTkTextbox(frame, state="normal", fg_color="transparent", wrap="word")
        textbox.pack(fill="both", expand=True, padx=5, pady=5)
        textbox.delete("1.0", "end")
        content = ""
        if from_file:
            with open(text_content, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
        elif from_bytes:
            content = text_content.decode('utf-8', errors='ignore')
        else:
            content = text_content
        textbox.insert("1.0", content)
        textbox.configure(state="disabled")
    except Exception as e:
        ctk.CTkLabel(frame, text=f"📝\nError reading text:\n{e}", text_color="gray").pack(expand=True)
        
def create_info_preview(frame, file_path=None, filename=None, data=None):
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        name = os.path.basename(file_path) if file_path else filename
        size_kb = (os.path.getsize(file_path) if file_path else len(data)) / 1024
        info_text = f"ℹ️ File Info\n\nName: {name}\nSize: {size_kb:.2f} KB\n\n(No visual preview available)"
        ctk.CTkLabel(frame, text=info_text, text_color="gray").pack(expand=True)
    except Exception as e:
        ctk.CTkLabel(frame, text=f"ℹ️\nError reading file:\n{e}", text_color="gray").pack(expand=True)
```

### File: `requirements.txt`

```
cffi==2.0.0
contourpy==1.3.3
cryptography==46.0.2
customtkinter==5.2.2
cycler==0.12.1
darkdetect==0.8.0
fonttools==4.60.1
kiwisolver==1.4.9
matplotlib==3.10.7
numpy==2.3.4
packaging==25.0
pillow==12.0.0
pycparser==2.23
pydub==0.25.1
pyparsing==3.2.5
python-dateutil==2.9.0.post0
simpleaudio==1.0.4
six==1.17.0
```

---

## 📋 Instructions for README.md Generation

Based on your complete analysis of the code provided, generate the `README.md` file following these precise instructions:

### 1. Bilingual Requirement
The README **must be fully bilingual**. Generate the complete **Arabic version first**, followed by the complete **English version**. Both versions must contain all the sections listed below.

### 2. Tone and Style
- Professional yet accessible tone
- Explain complex topics like steganography and cryptography in a way that is easy for a student or intermediate developer to understand
- Use friendly language and examples where possible

### 3. Required Sections

**For BOTH Arabic and English versions:**

#### A. Project Title
- A clear, professional title like "Professional Audio Steganography Tool (ProStego)"
- Include a brief subtitle explaining what the project does

#### B. Badges
- Include relevant Markdown badges for:
  - Python version (3.8+)
  - License (MIT)
  - Status (Active Development)
  - You can suggest others if appropriate

#### C. Screenshot
- Include a Markdown placeholder for a future screenshot of the application's GUI
- Format: `![ProStego GUI](link-to-your-screenshot.png)`
- Add a brief caption explaining what the screenshot shows

#### D. Features
- Create a **detailed bulleted list** of all the application's features identified from the code:
  - GUI interface (CustomTkinter)
  - Encryption functionality
  - Compression support
  - File preview capabilities (audio waveforms, images, text files)
  - Audio player integration
  - Multiple file type support
  - Password protection
  - LSB steganography technique
  - Progress tracking
  - Extraction and hiding capabilities
  - Theme customization (Dark mode)
  - Data validation

#### E. Techniques Used (How It Works)
**This is a critical section.** Create subsections for:

1. **LSB (Least Significant Bit) Steganography**
   - Explain the concept clearly for beginners
   - MUST include a simple text-based diagram showing how a bit is hidden in a byte
   - Example: Show a byte like `10110101` and demonstrate how the LSB is modified
   - Explain why this method is effective but imperceptible to audio quality

2. **Custom Metadata Header Structure**
   - Explain the header structure with a **table format** showing:
     - Field name
     - Size (bytes)
     - Purpose
     - Example values
   - Explain why each component is necessary
   - Mention: Flags (compression, encryption), Filename (255 bytes), Original Size (4 bytes)

3. **Secure Encryption Process**
   - Create a pipeline diagram showing: `Password → PBKDF2 (Key Stretching) → Strong Key → Fernet (AES) Encryption`
   - Explain each step:
     - Why password-based encryption is used
     - What PBKDF2 does and why it's important (iterations, salt)
     - Why Fernet is chosen (AES + HMAC for authenticity)
   - Mention the iterations count (100,000)

4. **Complete Workflow Diagram**
   - Show both hiding and extraction processes
   - Can be a simple text-based flowchart

#### F. Libraries & Technologies
- Create a **table or organized list** of:
  - Main technologies (Python, CustomTkinter, Cryptography, etc.)
  - Core libraries with brief descriptions of their role
  - Why each was chosen
  - Example table format:
    | Library | Version | Purpose |
    |---------|---------|---------|
    | CustomTkinter | 5.2.2 | Modern GUI framework |
    | cryptography | 46.0.2 | Encryption (Fernet/AES) |
    | ... | ... | ... |

#### G. Installation & Usage

1. **System Requirements**
   - Python version
   - OS compatibility
   - RAM/disk space recommendations

2. **Step-by-Step Installation**
   - Clone the repository
   - Create a virtual environment (with specific commands for Windows/Linux/Mac)
   - Install dependencies from requirements.txt
   - Run the application

3. **Usage Guide**
   - How to hide data:
     - Select cover audio
     - Choose secret data (file or text)
     - Optional: set password and compression
     - Choose output location
   - How to extract data:
     - Select stego audio file
     - Enter password if used
     - Preview extracted data
     - Save to disk

4. **Command Examples**
   - All commands must be in proper code blocks with syntax highlighting
   - Include examples for both Windows PowerShell and Unix shells

#### H. Project Structure
- Create a tree structure diagram showing all files and directories
- **Explain the purpose of each file and directory**
- Example format:
  ```
  ProStegoApp/
  ├── main.py              # Main GUI application entry point
  ├── logic.py             # Core LSB steganography logic
  ├── security.py          # Encryption/decryption functions
  ├── requirements.txt     # Project dependencies
  ├── ui/
  │   └── widgets.py       # Custom GUI components
  └── utils/
      ├── audio_player.py  # Audio playback functionality
      └── preview_handler.py # File preview generators
  ```

### 4. Additional Recommendations

#### Performance & Security
- Mention how the application handles large files
- Explain capacity limitations (based on audio file size)
- Note security considerations and best practices

#### Troubleshooting
- Common issues and solutions
- Installation problems
- Audio file compatibility
- Password-related issues

#### Contributing
- Brief section on how to contribute
- Code style guidelines
- Testing requirements

#### License & Author
- License type (MIT)
- Author/creator information
- Date of creation

### 5. Formatting Guidelines

- Use **Markdown extensively** for:
  - Headers (## for main sections, ### for subsections, #### for subsubsections)
  - **Bold text** for emphasis
  - `Code blocks` for file names and code snippets
  - Fenced code blocks with language specification (```python, ```bash, etc.)
  - Tables for structured data
  - Ordered and unordered lists
  - Links to relevant resources

- All command-line instructions must be in proper code blocks
- All code examples must have proper syntax highlighting
- Keep line lengths reasonable for readability
- Use emojis tastefully (as done in the main.py file)

### 6. Quality Checklist

Before finalizing, ensure:
- ✅ Both Arabic and English versions are complete and equal in detail
- ✅ All technical concepts are explained clearly for intermediate developers
- ✅ Code examples are accurate and executable
- ✅ Diagrams and tables are properly formatted
- ✅ No spelling or grammar errors
- ✅ All file paths and references are accurate
- ✅ The document is well-organized and easy to navigate
- ✅ Visual elements (emojis, formatting) enhance readability without clutter

---

## 🎯 Now Generate the Complete README.md

Based on all the analysis and instructions provided above, please generate the complete `README.md` file for the ProStegoApp project. 

Ensure it meets all the requirements and follows all formatting guidelines. The final output should be production-ready and can be directly used in the GitHub repository.

**Let's create an exceptional README that clearly explains this sophisticated audio steganography tool!**
