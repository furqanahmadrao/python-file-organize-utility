# 🗂️ File Organizer v1.0

**Automatically organize your messy folders by file type!**

Transform chaos into order with this simple Python tool that sorts files into categorized folders based on their extensions.

## ✨ Features

- 🎯 **Smart Organization**: Automatically sorts files into Images, Documents, Videos, Audio, Archives, Code, and Others
- 📁 **Auto-Folder Creation**: Creates category folders if they don't exist
- ⚙️ **Fully Customizable**: Easy-to-use configuration tool for custom rules
- 📋 **Detailed Logging**: Track every file movement with timestamps
- 🔍 **Preview Mode**: See what would be organized before making changes
- 🛡️ **Safe Operation**: Handles file conflicts and errors gracefully
- 📊 **Log Analysis**: Built-in log viewer with statistics and search

## 🚀 Quick Start

### 1. Download & Setup
```bash
# Clone or download the project
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer

# No additional dependencies needed - uses only Python standard library!
```

### 2. Basic Usage
```bash
# Preview what would be organized (safe mode)
python organizer.py --preview

# Actually organize files
python organizer.py

# Organize a specific folder
python organizer.py --path "/path/to/your/messy/folder"
```

### 3. First Time Setup
```bash
# Configure your organization rules
python config_setup.py

# Check what happened
python log_viewer.py
```

## 📋 Default File Categories

| Category | Extensions |
|----------|------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .webp, .svg, .ico |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2, .xz |
| **Code** | .py, .js, .html, .css, .java, .cpp, .c, .php, .rb |
| **Others** | Any unknown file types |

## 🔧 Tools Overview

### `organizer.py` - Main Organizer
The core tool that does the file organization.

**Usage:**
```bash
python organizer.py [options]

Options:
  --path PATH      Target directory to organize (overrides config)
  --preview        Preview mode - show what would be organized
  --config CONFIG  Path to config file (default: config.json)
```

**Examples:**
```bash
# Basic organization of default directory
python organizer.py

# Preview Downloads folder
python organizer.py --path "C:/Users/YourName/Downloads" --preview

# Use custom config
python organizer.py --config "my_rules.json"
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

**Features:**
- 📊 Session summaries and statistics
- 🕒 Recent activity viewing
- ❌ Error analysis
- 🔍 Log searching
- 📈 Detailed statistics

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
├── organizer.py       # Main file organization engine
├── config_setup.py    # Interactive configuration tool
├── log_viewer.py      # Log analysis and viewing tool
├── config.json        # Organization rules (auto-created)
├── log.txt           # Operation history (auto-created)
└── README.md         # This documentation
```

## 🔧 Advanced Usage

### Batch Processing Multiple Folders
```bash
# Create a batch script to organize multiple folders
for folder in "Downloads" "Desktop" "Documents/Temp"; do
    python organizer.py --path "$folder" --preview
done
```

### Custom Configurations for Different Use Cases
```bash
# Work files configuration
python organizer.py --config "work_config.json" --path "WorkFolder"

# Personal files configuration  
python organizer.py --config "personal_config.json" --path "PersonalFolder"
```

### Automated Scheduling
Add to your system's task scheduler or cron:

**Windows (Task Scheduler):**
```
Program: python
Arguments: C:\path\to\organizer.py --path "C:\Users\YourName\Downloads"
```

**Linux/Mac (Crontab):**
```bash
# Run every day at 6 PM
0 18 * * * cd /path/to/file-organizer && python organizer.py
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

## 🚀 Future Roadmap

### Phase 2 Features
- 📅 Automatic scheduling support
- 🔄 Duplicate file detection and handling
- 📤 Export logs to CSV/JSON formats
- 🎨 Enhanced CLI interface with colors

### Phase 3 Features
- 👀 Real-time folder monitoring
- 🖥️ GUI application (Tkinter/PyQt)
- 📦 Standalone executable (.exe/.app)
- ☁️ Cloud folder integration

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue with detailed error information
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Fork, develop, and submit pull requests
4. **Documentation**: Help improve this README and code comments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python standard library - no external dependencies!
- Inspired by the need to organize messy Downloads folders everywhere
- Thanks to everyone who tested and provided feedback

---

**Happy Organizing! 🗂️✨**