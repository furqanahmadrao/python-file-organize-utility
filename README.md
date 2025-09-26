# 🗂️ File Organizer v1.0

**Automatically organize your messy folders by file type!**

A simple yet powerful Python tool that transforms chaos into order by sorting files into categorized folders based on their extensions. Perfect for cleaning up Downloads folders, Desktop clutter, or any messy directory.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## ✨ Features

- 🎯 **Smart Organization**: Automatically sorts files into Images, Documents, Videos, Audio, Archives, Code, and Others
- 📁 **Auto-Folder Creation**: Creates category folders if they don't exist
- ⚙️ **Fully Customizable**: Easy-to-use configuration tool for custom rules
- 📋 **Detailed Logging**: Track every file movement with timestamps
- 🔍 **Preview Mode**: See what would be organized before making changes
- 🛡️ **Safe Operation**: Handles file conflicts and errors gracefully
- 📊 **Log Analysis**: Built-in log viewer with statistics and search
- 🐍 **No Dependencies**: Uses only Python standard library

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/file-organizer.git
cd file-organizer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate
```

### 2. Basic Usage

```bash
# Preview what would be organized (safe mode)
python organizer_main.py --preview

# Actually organize files
python organizer_main.py

# Organize a specific folder
python organizer_main.py --path "/path/to/your/messy/folder"
```

### 3. Configuration & Testing

```bash
# Configure your organization rules
python config_setup.py

# Create test files and try it out
python test_script.py

# Check what happened
python log_viewer.py
```

## 📋 Default File Categories

| Category      | Extensions                                                                        |
| ------------- | --------------------------------------------------------------------------------- |
| **Images**    | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.ico`                  |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx` |
| **Videos**    | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`                   |
| **Audio**     | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`                           |
| **Archives**  | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`                               |
| **Code**      | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.php`, `.rb`               |
| **Others**    | Any unknown file types                                                            |

## 🔧 Tools Overview

### `organizer_main.py` - Main Organizer

The core tool that does the file organization.

**Usage:**

```bash
python organizer_main.py [options]

Options:
  --path PATH      Target directory to organize (overrides config)
  --preview        Preview mode - show what would be organized
  --config CONFIG  Path to config file (default: config.json)
```

**Examples:**

```bash
# Basic organization of default directory
python organizer_main.py

# Preview Downloads folder
python organizer_main.py --path "C:/Users/YourName/Downloads" --preview

# Use custom config
python organizer_main.py --config "my_rules.json"
```

### `config_setup.py` - Configuration Manager

Interactive tool to create and modify organization rules.

**Usage:**

```bash
python config_setup.py
```

**Features:**

- 📋 View current configuration
- 🎯 Change target directory
- ➕ Add new categories
- ✏️ Modify existing categories
- 🗑️ Delete categories
- 💾 Save configuration

### `log_viewer.py` - Log Analysis Tool

View and analyze organization history.

**Usage:**

```bash
# Interactive mode
python log_viewer.py

# Command-line options
python log_viewer.py --summary              # Show summary
python log_viewer.py --recent 3             # Show 3 recent sessions
python log_viewer.py --errors               # Show errors only
python log_viewer.py --search "filename"    # Search logs
python log_viewer.py --stats                # Show statistics
```

### `test_script.py` - Test Suite

Create sample files and test the organization functionality.

**Usage:**

```bash
python test_script.py
```

## ⚙️ Configuration

The `config.json` file stores all your organization rules:

```json
{
  "target_directory": "./Downloads",
  "rules": {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Code": [".py", ".js", ".html", ".css"],
    "Others": []
  }
}
```

### Adding Custom Categories

**Via Configuration Tool:**

```bash
python config_setup.py
# Follow the interactive prompts
```

**Manual Editing:**

```json
{
  "rules": {
    "Scripts": [".py", ".sh", ".bat", ".ps1"],
    "eBooks": [".epub", ".mobi", ".pdf"],
    "3D Models": [".obj", ".stl", ".fbx"],
    "Others": []
  }
}
```

## 📊 Logging System

Every file operation is logged with detailed information:

```
2024-01-15 14:30:25 | MOVED: vacation_photo.jpg → Images/vacation_photo.jpg
2024-01-15 14:30:25 | MOVED: report.pdf → Documents/report.pdf
2024-01-15 14:30:26 | ERROR moving locked_file.docx: Permission denied
```

**Log Features:**

- ✅ Successful moves with timestamps
- ❌ Error tracking with details
- 📊 Session summaries
- 🔍 Searchable history

## 🛡️ Safety Features

- **Preview Mode**: See what would happen before making changes
- **File Conflict Handling**: Automatically renames conflicting files (e.g., `file_1.txt`)
- **Error Recovery**: Continues processing even if some files fail
- **Detailed Logging**: Complete audit trail of all operations
- **Permission Checks**: Handles permission errors gracefully

## 📁 Project Structure

```
file-organizer/
├── organizer_main.py      # Main file organization engine
├── config_setup.py        # Interactive configuration tool
├── log_viewer.py          # Log analysis and viewing tool
├── test_script.py         # Test suite with sample files
├── activate_env.py        # Virtual environment helper
├── requirements.txt       # Dependencies (empty - uses stdlib only)
├── .gitignore            # Git ignore rules
├── VENV_SETUP.md         # Virtual environment documentation
└── README.md             # This documentation
```

## 🔧 Advanced Usage

### Batch Processing Multiple Folders

```bash
# PowerShell example
@("Downloads", "Desktop", "Documents\Temp") | ForEach-Object {
    python organizer_main.py --path $_ --preview
}
```

### Custom Configurations for Different Use Cases

```bash
# Work files configuration
python organizer_main.py --config "work_config.json" --path "WorkFolder"

# Personal files configuration
python organizer_main.py --config "personal_config.json" --path "PersonalFolder"
```

### Automated Scheduling

**Windows (Task Scheduler):**

```
Program: python
Arguments: C:\path\to\organizer_main.py --path "C:\Users\YourName\Downloads"
```

**Linux/Mac (Crontab):**

```bash
# Run every day at 6 PM
0 18 * * * cd /path/to/file-organizer && python organizer_main.py
```

## 🐛 Troubleshooting

### Common Issues

**Permission Denied Errors:**

- Run as administrator/sudo if organizing system folders
- Check file permissions before organizing

**Config File Not Found:**

- Run `python config_setup.py` to create initial configuration
- Ensure `config.json` exists in the same directory

**No Files Being Moved:**

- Check if files are actually in the target directory
- Verify extensions match your configuration rules
- Use `--preview` mode to debug

**Log File Issues:**

- Ensure write permissions in the project directory
- Log file `log.txt` is created automatically

### Getting Help

1. Check the log file for detailed error messages
2. Use preview mode to test configuration
3. Verify file permissions and paths
4. Check that Python 3.6+ is installed

## 🚀 Installation

### Requirements

- Python 3.6 or higher
- No external dependencies required!

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Run the organizer
python organizer_main.py --preview
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue with detailed error information
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Fork, develop, and submit pull requests
4. **Documentation**: Help improve this README and code comments

### Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/file-organizer.git
cd file-organizer
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python test_script.py  # Create test environment
```

## 🙏 Acknowledgments

- Built with Python standard library - no external dependencies!
- Inspired by the need to organize messy Downloads folders everywhere
- Thanks to everyone who tested and provided feedback

## 📈 Future Roadmap

### Phase 2 Features

- 📅 GUI application (Tkinter/PyQt)
- 🔄 Duplicate file detection and handling
- 📤 Export logs to CSV/JSON formats
- 🎨 Enhanced CLI interface with colors

### Phase 3 Features

- 👀 Real-time folder monitoring
- 📦 Standalone executable (.exe/.app)
- ☁️ Cloud folder integration
- 🤖 AI-powered file categorization

---

**Happy Organizing! 🗂️✨**

_If you find this tool useful, please give it a ⭐ on GitHub!_
