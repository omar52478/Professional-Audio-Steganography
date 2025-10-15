# 🔊 Professional Audio Steganography Tool (ProStego)# 🔊 Professional Audio Steganography Tool (ProStego)# 🔊 Professional Audio Steganography Tool (ProStego)



![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

![License](https://img.shields.io/badge/license-MIT-green)

![Status](https://img.shields.io/badge/status-Active%20Development-brightgreen)![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)



---![License](https://img.shields.io/badge/license-MIT-green)![License](https://img.shields.io/badge/license-MIT-green)



## 📸 Screenshot![Status](https://img.shields.io/badge/status-Active%20Development-brightgreen)![Status](https://img.shields.io/badge/status-Active%20Development-brightgreen)



![ProStego GUI](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=flat-square)



*A modern desktop application with intuitive interface for hiding and extracting data from audio files.*------



---



## ✨ Features## 📸 Screenshot## 📸 Screenshot



- 🎵 **Audio Steganography**: Hide files and text inside WAV audio files using LSB (Least Significant Bit) technique

- 🔐 **Secure Encryption**: AES-256 encryption with PBKDF2 key derivation and password protection

- 📦 **Data Compression**: Automatic compression using zlib to maximize storage capacity![ProStego GUI](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=flat-square)![ProStego GUI](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=flat-square)

- 🎨 **Modern GUI**: Beautiful, user-friendly interface built with CustomTkinter

- 👁️ **Real-time Preview**: View audio waveforms, images, and text before hiding/extracting

- 🎶 **Audio Player**: Built-in player to preview audio files with play/stop controls

- 📄 **Multi-format Support**: Hide any file type (PDF, images, text, documents, etc.)*A modern desktop application with intuitive interface for hiding and extracting data from audio files.**A modern desktop application with intuitive interface for hiding and extracting data from audio files.*

- ⚙️ **Progress Tracking**: Real-time progress bar and logging console

- 🌙 **Dark Theme**: Modern dark mode interface for comfortable viewing

- ✅ **Data Validation**: Ensures data integrity and safety

------

---



## 🔧 How It Works

## ✨ Features## ✨ Features

### LSB (Least Significant Bit) Steganography



The application uses LSB steganography to hide data imperceptibly within audio files:

- 🎵 **Audio Steganography**: Hide files and text inside WAV audio files using LSB (Least Significant Bit) technique- 🎵 **Audio Steganography**: Hide files and text inside WAV audio files using LSB (Least Significant Bit) technique

```

Original byte:  10110101- 🔐 **Secure Encryption**: AES-256 encryption with PBKDF2 key derivation and password protection- 🔐 **Secure Encryption**: AES-256 encryption with PBKDF2 key derivation and password protection

After hiding:   10110100  (LSB changed from 1 to 0)

Audio quality:  Imperceptible to human ear ✓- 📦 **Data Compression**: Automatic compression using zlib to maximize storage capacity- 📦 **Data Compression**: Automatic compression using zlib to maximize storage capacity

```

- 🎨 **Modern GUI**: Beautiful, user-friendly interface built with CustomTkinter- 🎨 **Modern GUI**: Beautiful, user-friendly interface built with CustomTkinter

Each audio sample's least significant bit is modified to store data bits. This creates minimal audio degradation while allowing large data storage.

- 👁️ **Real-time Preview**: View audio waveforms, images, and text before hiding/extracting- 👁️ **Real-time Preview**: View audio waveforms, images, and text before hiding/extracting

### Data Flow

- 🎶 **Audio Player**: Built-in player to preview audio files with play/stop controls- 🎶 **Audio Player**: Built-in player to preview audio files with play/stop controls

**Hiding Process:**

```- 📄 **Multi-format Support**: Hide any file type (PDF, images, text, documents, etc.)- 📄 **Multi-format Support**: Hide any file type (PDF, images, text, documents, etc.)

Secret Data → Compress → Encrypt → Add Header → Insert into Audio (LSB) → Output File

```- ⚙️ **Progress Tracking**: Real-time progress bar and logging console- ⚙️ **Progress Tracking**: Real-time progress bar and logging console



**Extraction Process:**- 🌙 **Dark Theme**: Modern dark mode interface for comfortable viewing- 🌙 **Dark Theme**: Modern dark mode interface for comfortable viewing

```

Stego Audio → Extract LSB Bits → Remove Header → Decrypt → Decompress → Recover Data- ✅ **Data Validation**: Ensures data integrity and safety- ✅ **Data Validation**: Ensures data integrity and safety

```



### Custom Metadata Header

------

The header structure stores essential information:



| Field | Size (bytes) | Purpose | Example |

|-------|--------------|---------|---------|## 🔧 How It Works## 🔧 How It Works

| Flags | 1 | Compression & Encryption status | `0x03` (both enabled) |

| Filename | 255 | Original filename | `document.pdf` |

| Original Size | 4 | Uncompressed data size | `1048576` |

### LSB (Least Significant Bit) Steganography### LSB (Least Significant Bit) Steganography

### Encryption Pipeline



```

Password InputThe application uses LSB steganography to hide data imperceptibly within audio files:The application uses LSB steganography to hide data imperceptibly within audio files:

    ↓

PBKDF2 Key Derivation (100,000 iterations)

    ↓

Strong 256-bit Key Generated``````

    ↓

Fernet AES Encryption AppliedOriginal byte:  10110101Original byte:  10110101

    ↓

Encrypted Data with SaltAfter hiding:   10110100  (LSB changed from 1 to 0)After hiding:   10110100  (LSB changed from 1 to 0)

```

Audio quality:  Imperceptible to human ear ✓Audio quality:  Imperceptible to human ear ✓

---

``````

## 🛠️ Technologies & Libraries



| Technology | Version | Purpose |

|-----------|---------|---------|Each audio sample's least significant bit is modified to store data bits. This creates minimal audio degradation while allowing large data storage.Each audio sample's least significant bit is modified to store data bits. This creates minimal audio degradation while allowing large data storage.

| **Python** | 3.8+ | Core programming language |

| **CustomTkinter** | 5.2.2 | Modern GUI framework |

| **cryptography** | 46.0.2 | AES/Fernet encryption |

| **pydub** | 0.25.1 | Audio file handling |### Data Flow### Data Flow

| **matplotlib** | 3.10.7 | Waveform visualization |

| **simpleaudio** | 1.0.4 | Audio playback |

| **Pillow** | 12.0.0 | Image processing |

**Hiding Process:****Hiding Process:**

---

``````

## 📦 Installation

Secret Data → Compress → Encrypt → Add Header → Insert into Audio (LSB) → Output FileSecret Data → Compress → Encrypt → Add Header → Insert into Audio (LSB) → Output File

### System Requirements

``````

- **Python**: 3.8 or higher

- **OS**: Windows, macOS, or Linux

- **RAM**: Minimum 2GB (4GB recommended)

- **Storage**: 500MB free space for dependencies**Extraction Process:****Extraction Process:**



### Step-by-Step Setup``````



#### 1. Clone the RepositoryStego Audio → Extract LSB Bits → Remove Header → Decrypt → Decompress → Recover DataStego Audio → Extract LSB Bits → Remove Header → Decrypt → Decompress → Recover Data



```bash``````

git clone https://github.com/omar52478/Professional-Audio-Steganography.git

cd Professional-Audio-Steganography

```

### Custom Metadata Header### Custom Metadata Header

#### 2. Create Virtual Environment



**Windows (PowerShell):**

```powershellThe header structure stores essential information:The header structure stores essential information:

python -m venv venv

.\venv\Scripts\Activate.ps1

```

| Field | Size (bytes) | Purpose | Example || Field | Size (bytes) | Purpose | Example |

**Linux/macOS:**

```bash|-------|--------------|---------|---------||-------|--------------|---------|---------|

python3 -m venv venv

source venv/bin/activate| Flags | 1 | Compression & Encryption status | `0x03` (both enabled) || Flags | 1 | Compression & Encryption status | `0x03` (both enabled) |

```

| Filename | 255 | Original filename | `document.pdf` || Filename | 255 | Original filename | `document.pdf` |

#### 3. Install Dependencies

| Original Size | 4 | Uncompressed data size | `1048576` || Original Size | 4 | Uncompressed data size | `1048576` |

```bash

pip install -r requirements.txt

```

### Encryption Pipeline### Encryption Pipeline

#### 4. Run the Application



```bash

python main.py``````

```

Password InputPassword Input

---

    ↓    ↓

## 🚀 Usage Guide

PBKDF2 Key Derivation (100,000 iterations)PBKDF2 Key Derivation (100,000 iterations)

### Hiding Data

    ↓    ↓

1. **Select Cover Audio**: Click "Browse" to choose a WAV audio file

2. **Choose Secret Data**: Strong 256-bit Key GeneratedStrong 256-bit Key Generated

   - Select "File" to hide any file type

   - Or select "Text" to hide plain text    ↓    ↓

3. **Configure Options**:

   - Set optional password for encryptionFernet AES Encryption AppliedFernet AES Encryption Applied

   - Check "Compress data" for better capacity (recommended)

4. **Hide Data**: Click "Start Hiding" and choose output location    ↓    ↓

5. **Success**: Your stego audio file is ready to share!

Encrypted Data with SaltEncrypted Data with Salt

### Extracting Data

``````

1. **Select Stego Audio**: Choose the audio file containing hidden data

2. **Enter Password**: If encryption was used, enter the password

3. **Extract & Preview**: Click to extract and preview the data

4. **Save Data**: Click "Save to Disk" to save the recovered file------



---



## 📁 Project Structure## 🛠️ Technologies & Libraries## 🛠️ Technologies & Libraries



```

ProStegoApp/

├── main.py                 # Main GUI application entry point| Technology | Version | Purpose || Technology | Version | Purpose |

├── logic.py               # LSB hiding and extraction core logic

├── security.py            # Encryption/decryption functions|-----------|---------|---------||-----------|---------|---------|

├── requirements.txt       # Python dependencies

├── README.md             # This file| **Python** | 3.8+ | Core programming language || **Python** | 3.8+ | Core programming language |

│

├── ui/| **CustomTkinter** | 5.2.2 | Modern GUI framework || **CustomTkinter** | 5.2.2 | Modern GUI framework |

│   ├── __init__.py

│   └── widgets.py        # Custom GUI components (FileInputFrame)| **cryptography** | 46.0.2 | AES/Fernet encryption || **cryptography** | 46.0.2 | AES/Fernet encryption |

│

└── utils/| **pydub** | 0.25.1 | Audio file handling || **pydub** | 0.25.1 | Audio file handling |

    ├── __init__.py

    ├── audio_player.py   # Audio playback functionality| **matplotlib** | 3.10.7 | Waveform visualization || **matplotlib** | 3.10.7 | Waveform visualization |

    └── preview_handler.py # File preview generators (waveform, images, text)

```| **simpleaudio** | 1.0.4 | Audio playback || **simpleaudio** | 1.0.4 | Audio playback |



---| **Pillow** | 12.0.0 | Image processing || **Pillow** | 12.0.0 | Image processing |



## ⚙️ Advanced Features



### Capacity Calculation------



Maximum data capacity depends on audio file size:



- **Capacity Formula**: `Audio file size (bytes) ÷ 8`## 📦 Installation## 📦 Installation

- **Example**: 10MB WAV file can hide ~1.25MB of data (with compression)



### Security Best Practices

### System Requirements### System Requirements

**✅ Do:**

- Use strong passwords (12+ characters with mixed case, numbers, symbols)

- Store stego files safely

- Verify file integrity before extraction- **Python**: 3.8 or higher- **Python**: 3.8 or higher

- Keep backup copies of original audio

- **OS**: Windows, macOS, or Linux- **OS**: Windows, macOS, or Linux

**❌ Don't:**

- Use weak passwords- **RAM**: Minimum 2GB (4GB recommended)- **RAM**: Minimum 2GB (4GB recommended)

- Share stego files without protection

- Delete original audio files immediately- **Storage**: 500MB free space for dependencies- **Storage**: 500MB free space for dependencies

- Ignore error messages



### Supported File Types

### Step-by-Step Setup### Step-by-Step Setup

**For Hiding:**

- Documents: PDF, DOCX, TXT, etc.

- Images: PNG, JPG, GIF, BMP

- Audio: MP3 files (as text data)#### 1. Clone the Repository#### 1. Clone the Repository

- Any binary file type



**Cover Audio:**

- WAV files (primary support)```bash```bash

- Higher quality audio = more data capacity

git clone https://github.com/omar52478/Professional-Audio-Steganography.gitgit clone https://github.com/omar52478/Professional-Audio-Steganography.git

---

cd Professional-Audio-Steganographycd Professional-Audio-Steganography

## 🐛 Troubleshooting

``````

### Issue: "Cover audio is too small to hide this data"



**Solution:** Use a larger audio file or enable compression

#### 2. Create Virtual Environment#### 2. Create Virtual Environment

### Issue: "pydub is not installed"



**Solution:** Run `pip install pydub` and ensure FFmpeg is installed

**Windows (PowerShell):****Windows (PowerShell):**

### Issue: "Decryption failed - Incorrect password"

```powershell```powershell

**Solution:** Verify the password is correct and case-sensitive

python -m venv venvpython -m venv venv

### Issue: Audio playback not working

.\venv\Scripts\Activate.ps1.\venv\Scripts\Activate.ps1

**Solution:** Install FFmpeg on your system:

- **Windows**: `choco install ffmpeg```````

- **macOS**: `brew install ffmpeg`

- **Linux**: `sudo apt-get install ffmpeg`



---**Linux/macOS:****Linux/macOS:**



## 🤝 Contributing```bash```bash



Contributions are welcome! To contribute:python3 -m venv venvpython3 -m venv venv



1. Fork the repositorysource venv/bin/activatesource venv/bin/activate

2. Create a feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add amazing feature'`)``````

4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request



### Code Style#### 3. Install Dependencies#### 3. Install Dependencies



- Follow PEP 8 conventions

- Use meaningful variable names

- Add comments for complex logic```bash```bash

- Test thoroughly before submitting

pip install -r requirements.txtpip install -r requirements.txt

---

``````

## 📄 License



This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

#### 4. Run the Application#### 4. Run the Application

**You are free to:**

- ✅ Use commercially

- ✅ Modify and distribute

- ✅ Use privately```bash```bash

- ⚠️ Include license and copyright notice

python main.pypython main.py

---

``````

## 👨‍💻 Author



**Omar Ahmed** (@omar52478)

- GitHub: [omar52478](https://github.com/omar52478)------

- Project: [Professional Audio Steganography](https://github.com/omar52478/Professional-Audio-Steganography)



---

## 🚀 Usage Guide## 🚀 Usage Guide

## 📞 Support



If you encounter issues or have questions:

### Hiding Data### Hiding Data

1. Check the **Troubleshooting** section

2. Review existing [Issues](https://github.com/omar52478/Professional-Audio-Steganography/issues)

3. Create a new issue with detailed information

1. **Select Cover Audio**: Click "Browse" to choose a WAV audio file1. **Select Cover Audio**: Click "Browse" to choose a WAV audio file

---

2. **Choose Secret Data**: 2. **Choose Secret Data**: 

## 🌟 Acknowledgments

   - Select "File" to hide any file type   - Select "File" to hide any file type

- **CustomTkinter**: Modern GUI framework

- **pydub**: Audio file processing   - Or select "Text" to hide plain text   - Or select "Text" to hide plain text

- **cryptography**: Secure encryption library

- Community feedback and contributions3. **Configure Options**:3. **Configure Options**:



---   - Set optional password for encryption   - Set optional password for encryption



## 📚 Learn More   - Check "Compress data" for better capacity (recommended)   - Check "Compress data" for better capacity (recommended)



- [Steganography on Wikipedia](https://en.wikipedia.org/wiki/Steganography)4. **Hide Data**: Click "Start Hiding" and choose output location4. **Hide Data**: Click "Start Hiding" and choose output location

- [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)

- [Python Documentation](https://docs.python.org/3/)5. **Success**: Your stego audio file is ready to share!5. **Success**: Your stego audio file is ready to share!



---



**Made with ❤️ for secure data hiding and audio steganography enthusiasts**### Extracting Data### Extracting Data




1. **Select Stego Audio**: Choose the audio file containing hidden data1. **Select Stego Audio**: Choose the audio file containing hidden data

2. **Enter Password**: If encryption was used, enter the password2. **Enter Password**: If encryption was used, enter the password

3. **Extract & Preview**: Click to extract and preview the data3. **Extract & Preview**: Click to extract and preview the data

4. **Save Data**: Click "Save to Disk" to save the recovered file4. **Save Data**: Click "Save to Disk" to save the recovered file



------



## 📁 Project Structure## 📁 Project Structure



``````

ProStegoApp/ProStegoApp/

├── main.py                 # Main GUI application entry point├── main.py                 # Main GUI application entry point

├── logic.py               # LSB hiding and extraction core logic├── logic.py               # LSB hiding and extraction core logic

├── security.py            # Encryption/decryption functions├── security.py            # Encryption/decryption functions

├── requirements.txt       # Python dependencies├── requirements.txt       # Python dependencies

├── README.md             # This file├── README.md             # This file

││

├── ui/├── ui/

│   ├── __init__.py│   ├── __init__.py

│   └── widgets.py        # Custom GUI components (FileInputFrame)│   └── widgets.py        # Custom GUI components (FileInputFrame)

││

└── utils/└── utils/

    ├── __init__.py    ├── __init__.py

    ├── audio_player.py   # Audio playback functionality    ├── audio_player.py   # Audio playback functionality

    └── preview_handler.py # File preview generators (waveform, images, text)    └── preview_handler.py # File preview generators (waveform, images, text)

``````



------



## ⚙️ Advanced Features## ⚙️ Advanced Features



### Capacity Calculation### Capacity Calculation



Maximum data capacity depends on audio file size:Maximum data capacity depends on audio file size:

- **Capacity** = Audio file size in bytes ÷ 8 (before compression)- **Capacity** = Audio file size in bytes ÷ 8 (before compression)

- **Example**: 10MB WAV file can hide ~1.25MB of data (with compression)- **Example**: 10MB WAV file can hide ~1.25MB of data (with compression)



### Security Best Practices### Security Best Practices



✅ **Do:**✅ **Do:**

- Use strong passwords (12+ characters with mixed case, numbers, symbols)- Use strong passwords (12+ characters with mixed case, numbers, symbols)

- Store stego files safely- Store stego files safely

- Verify file integrity before extraction- Verify file integrity before extraction

- Keep backup copies of original audio- Keep backup copies of original audio



❌ **Don't:**❌ **Don't:**

- Use weak passwords- Use weak passwords

- Share stego files without protection- Share stego files without protection

- Delete original audio files immediately- Delete original audio files immediately

- Ignore error messages- Ignore error messages



### Supported File Types### Supported File Types



**For Hiding:****For Hiding:**

- Documents: PDF, DOCX, TXT, etc.- Documents: PDF, DOCX, TXT, etc.

- Images: PNG, JPG, GIF, BMP- Images: PNG, JPG, GIF, BMP

- Audio: MP3 files (as text data)- Audio: MP3 files (as text data)

- Any binary file type- Any binary file type



**Cover Audio:****Cover Audio:**

- WAV files (primary support)- WAV files (primary support)

- Higher quality audio = more data capacity- Higher quality audio = more data capacity



------



## 🐛 Troubleshooting## 🐛 Troubleshooting



### Issue: "Cover audio is too small to hide this data"### Issue: "Cover audio is too small to hide this data"

**Solution:** Use a larger audio file or enable compression**Solution:** Use a larger audio file or enable compression



### Issue: "pydub is not installed"### Issue: "pydub is not installed"

**Solution:** Run `pip install pydub` and ensure FFmpeg is installed**Solution:** Run `pip install pydub` and ensure FFmpeg is installed



### Issue: "Decryption failed - Incorrect password"### Issue: "Decryption failed - Incorrect password"

**Solution:** Verify the password is correct and case-sensitive**Solution:** Verify the password is correct and case-sensitive



### Issue: Audio playback not working### Issue: Audio playback not working

**Solution:** Install FFmpeg on your system:**Solution:** Install FFmpeg on your system:

- **Windows**: `choco install ffmpeg`- **Windows**: `choco install ffmpeg`

- **macOS**: `brew install ffmpeg`- **macOS**: `brew install ffmpeg`

- **Linux**: `sudo apt-get install ffmpeg`- **Linux**: `sudo apt-get install ffmpeg`



------



## 🤝 Contributing## 🤝 Contributing



Contributions are welcome! To contribute:Contributions are welcome! To contribute:



1. Fork the repository1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)2. Create a feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add amazing feature'`)3. Commit your changes (`git commit -m 'Add amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request5. Open a Pull Request



### Code Style### Code Style



- Follow PEP 8 conventions- Follow PEP 8 conventions

- Use meaningful variable names- Use meaningful variable names

- Add comments for complex logic- Add comments for complex logic

- Test thoroughly before submitting- Test thoroughly before submitting



------



## 📄 License## 📄 License



This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.



**You are free to:****You are free to:**

- ✅ Use commercially- ✅ Use commercially

- ✅ Modify and distribute- ✅ Modify and distribute

- ✅ Use privately- ✅ Use privately

- ⚠️ Include license and copyright notice- ⚠️ Include license and copyright notice



------



## 👨‍💻 Author## 👨‍💻 Author



**Omar Ahmed** (@omar52478)**Omar Ahmed** (@omar52478)

- GitHub: [omar52478](https://github.com/omar52478)- GitHub: [omar52478](https://github.com/omar52478)

- Project: [Professional Audio Steganography](https://github.com/omar52478/Professional-Audio-Steganography)- Project: [Professional Audio Steganography](https://github.com/omar52478/Professional-Audio-Steganography)



------



## 📞 Support## 📞 Support



If you encounter issues or have questions:If you encounter issues or have questions:



1. Check the **Troubleshooting** section1. Check the **Troubleshooting** section

2. Review existing [Issues](https://github.com/omar52478/Professional-Audio-Steganography/issues)2. Review existing [Issues](https://github.com/omar52478/Professional-Audio-Steganography/issues)

3. Create a new issue with detailed information3. Create a new issue with detailed information



------



## 🌟 Acknowledgments## 🌟 Acknowledgments



- **CustomTkinter**: Modern GUI framework- **CustomTkinter**: Modern GUI framework

- **pydub**: Audio file processing- **pydub**: Audio file processing

- **cryptography**: Secure encryption library- **cryptography**: Secure encryption library

- Community feedback and contributions- Community feedback and contributions



------



## 📚 Learn More## 📚 Learn More



- [Steganography on Wikipedia](https://en.wikipedia.org/wiki/Steganography)- [Steganography on Wikipedia](https://en.wikipedia.org/wiki/Steganography)

- [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)- [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)

- [Python Documentation](https://docs.python.org/3/)- [Python Documentation](https://docs.python.org/3/)



------
