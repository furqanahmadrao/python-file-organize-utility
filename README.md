# 🗂️ FileNest

**Simple, powerful file organization made easy!**

FileNest is a production-ready file organizer that automatically sorts your files into categories. Perfect for anyone who wants their Downloads folder organized without complexity.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-minimal-brightgreen)

## ✨ Features

- 🗂️ **Automatic Organization**: Sorts files by type (Images, Documents, Videos, etc.)
- ⚙️ **Simple Configuration**: Easy setup with `config-setup` command
- 👀 **Real-time Watching**: Monitor folders for new files with `--watch`
- 🔍 **Preview Mode**: See what will happen with `--dry-run`
- 📝 **Clean Logging**: Human-readable logs with timestamps
- 🔄 **Duplicate Handling**: Smart handling of existing files
- 🖥️ **Cross-platform**: Works on Windows, macOS, and Linux
- 📦 **Multiple Install Options**: Pip package or standalone executable

## 🚀 Quick Start

### Option 1: Install with pip (Recommended)

```bash
pip install filenest[all]
```

### Option 2: Use standalone executable

Download `filenest.exe` (Windows) or `filenest` (Linux/macOS) - no Python required!

### Option 3: Install from source

```bash
git clone https://github.com/furqanahmadrao/python-file-organize-utility.git
cd python-file-organize-utility
python install.py
```

## 📋 Usage

### 1. Set up configuration
```bash
config-setup
```

### 2. Organize your Downloads folder
```bash
organize
```

### 3. Preview before organizing
```bash
organize --dry-run
```

### 4. Watch for new files automatically
```bash
organize --watch
```

### 5. Organize a specific folder
```bash
organize --path "/path/to/folder"
```

### 6. View logs
```bash
log-viewer
log-viewer --recent 10
log-viewer --today
```

## 🏗️ Default File Categories

- **Images**: `.jpg`, `.png`, `.gif`, `.svg`, etc.
- **Documents**: `.pdf`, `.docx`, `.txt`, `.xlsx`, etc.
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, etc.
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, etc.
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, etc.
- **Software**: `.exe`, `.msi`, `.dmg`, `.deb`, etc.
- **Code**: `.py`, `.js`, `.html`, `.css`, etc.
- **Others**: Any file that doesn't match above categories

## ⚙️ Configuration

FileNest uses a simple `config.json` file:

```json
{
  "target_path": "/home/user/Downloads",
  "categories": {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"]
  },
  "others_folder": "Others",
  "duplicate_strategy": "rename"
}
```

### Duplicate Strategies
- **rename**: Add (1), (2), etc. to filename
- **skip**: Don't move files that already exist
- **overwrite**: Replace existing files

## 🔧 Command Line Options

```bash
organize                    # Organize Downloads folder
organize --path PATH        # Organize specific folder
organize --dry-run          # Preview without moving files
organize --watch            # Watch for new files
organize --once             # Run once and exit (default)
organize --show-log         # Show log entries after organizing
organize --version          # Show version information

config-setup                # Interactive configuration setup
config-setup --show         # Show current configuration
config-setup --import FILE  # Import configuration from file

log-viewer                  # View recent logs
log-viewer --recent N       # Show N recent entries
log-viewer --today          # Show today's entries
log-viewer --search QUERY   # Search logs
log-viewer --stats          # Show statistics
```

## 📊 Log Format

FileNest creates clean, readable logs:

```
2025-09-26T10:45:03Z | Moved | vacation.jpg | /Downloads | /Downloads/Images
2025-09-26T10:45:04Z | Created | Images
2025-09-26T10:45:05Z | Skipped | document.pdf | File already exists
```

## 🔨 Development & Building

### Build all distributions
```bash
python build_script.py
```

### Build specific format
```bash
python build_script.py wheel    # Pip installable
python build_script.py exe      # Standalone executable
python build_script.py release  # Complete package
```

## 📁 Project Structure

```
filenest/
├── organizer.py           # Main file organization engine
├── config_setup.py        # Interactive configuration
├── log_viewer.py          # Log viewing utility
├── setup.py              # Package configuration
├── build_script.py       # Build automation
├── install.py            # Quick installer
├── filenest.spec         # PyInstaller configuration
├── config.json           # User configuration
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/furqanahmadrao/python-file-organize-utility/issues)
- **Documentation**: This README
- **Logs**: Use `log-viewer` to check operation logs

---

**Happy organizing! 🗂️✨**