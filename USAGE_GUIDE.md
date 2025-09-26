# File Organizer v2.0 - Installation & Usage Guide

## 🚀 **Installation**

### Method 1: Development Installation (Recommended)

```bash
# Clone or download the repository
cd file_oragnizer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install in development mode
pip install -e .

# Or install with all optional features
pip install -e .[all]
```

### Method 2: Direct Installation

```bash
# Install the package directly
pip install -e .

# Install with specific features
pip install -e .[watch]    # Directory watching
pip install -e .[dev]      # Development tools
pip install -e .[all]      # All features
```

### Method 3: Manual Installation

```bash
# Install dependencies (if any)
pip install -r requirements.txt

# Run directly
python file_organizer_cli.py
```

## 📋 **Command Reference**

### 🎯 **Quick Start Commands**

```bash
# Interactive mode (recommended for beginners)
file-organizer

# Preview organization (safe - no changes made)
file-organizer organize --preview --path ~/Downloads

# Organize with default settings
file-organizer organize --path ~/Downloads

# Organize using specific profile
file-organizer organize --path ~/Downloads --profile photographer
```

### 🗂️ **File Organization Commands**

```bash
# Basic organization
file-organizer organize --path /path/to/directory

# Preview mode (dry run)
file-organizer organize --preview --path /path/to/directory

# Use specific profile
file-organizer organize --profile developer --path ~/Projects

# Enable duplicate detection
file-organizer organize --duplicates --path ~/Downloads

# Multi-threaded organization (faster for many files)
file-organizer organize --threads 8 --path /large/directory

# Batch mode (no prompts)
file-organizer organize --batch --path /path/to/organize

# Create undo information
file-organizer organize --undo-info --path ~/Documents
```

### 👤 **Profile Management**

```bash
# List all profiles
file-organizer profiles --list

# Show profile details
file-organizer profiles --show photographer

# Set active profile
file-organizer profiles --set developer

# Copy existing profile
file-organizer profiles --copy photographer my_photo_profile

# Delete profile
file-organizer profiles --delete old_profile
```

### ⚙️ **Configuration Management**

```bash
# Interactive configuration
file-organizer config --interactive

# Create new profile
file-organizer config --create photographer
file-organizer config --create developer
file-organizer config --create student
file-organizer config --create business

# Edit existing profile
file-organizer config --edit my_profile

# Validate profile
file-organizer config --validate photographer

# Export profile to file
file-organizer config --export photographer my_photographer_config.json

# Import profile from file
file-organizer config --import my_photographer_config.json
```

### 📊 **Logs and Statistics**

```bash
# Show recent sessions
file-organizer logs --recent 10

# Show specific session
file-organizer logs --session 2024-01-15_14-30-25

# Show only errors
file-organizer logs --errors

# Search logs
file-organizer logs --search "error"

# Export session to CSV
file-organizer logs --export session_id output.csv

# Clean up old logs
file-organizer logs --cleanup 30
```

### 📈 **Statistics Commands**

```bash
# Show 30-day statistics
file-organizer stats

# Show specific period
file-organizer stats --days 7

# Detailed statistics
file-organizer stats --detailed --days 90
```

### ↩️ **Undo Operations**

```bash
# Undo last operation
file-organizer undo

# Undo from specific file
file-organizer undo --file path/to/undo_info.json
```

### 👀 **Directory Watching**

```bash
# Watch directory for changes
file-organizer watch ~/Downloads

# Watch with specific profile
file-organizer watch ~/Downloads --profile photographer

# Custom check interval
file-organizer watch ~/Downloads --interval 10
```

### 🧹 **Cleanup Commands**

```bash
# Clean old logs
file-organizer clean --logs 30

# Clean all temporary data
file-organizer clean --all

# Clean cache files
file-organizer clean --cache
```

## 🎯 **Common Use Cases**

### 📸 **For Photographers**

```bash
# Create photographer profile
file-organizer config --create photographer

# Organize photos with duplicate detection
file-organizer organize --profile photographer --duplicates --path ~/Pictures/RAW

# Watch Downloads for new photos
file-organizer watch ~/Downloads --profile photographer
```

### 💻 **For Developers**

```bash
# Create developer profile
file-organizer config --create developer

# Organize project files
file-organizer organize --profile developer --path ~/Downloads

# Preview before organizing source code
file-organizer organize --preview --profile developer --path ~/Projects/messy-folder
```

### 🎓 **For Students**

```bash
# Create student profile
file-organizer config --create student

# Organize semester downloads
file-organizer organize --profile student --path ~/Downloads

# Create undo info for important docs
file-organizer organize --profile student --undo-info --path ~/Documents/School
```

### 🏢 **For Business Use**

```bash
# Create business profile
file-organizer config --create business

# Batch organize without prompts
file-organizer organize --profile business --batch --path ~/Documents/Projects

# Multi-threaded for large document sets
file-organizer organize --profile business --threads 6 --path /shared/documents
```

## 🛡️ **Safety Features**

### Preview Mode

Always use `--preview` first to see what will happen:

```bash
file-organizer organize --preview --path ~/Downloads
```

### Undo Functionality

Enable undo for important operations:

```bash
file-organizer organize --undo-info --path ~/Documents
# Later if needed:
file-organizer undo
```

### Batch vs Interactive

- Use `--batch` for automated scripts
- Default interactive mode asks for confirmation

## 📋 **Profile Types**

### 🔧 **Default Profile**

- General purpose organization
- Organizes by file type (Documents, Images, Audio, Video, etc.)
- Good starting point for most users

### 📸 **Photographer Profile**

- Optimized for photo and video files
- Separates RAW files from processed images
- Creates date-based folders
- Handles various camera formats

### 💻 **Developer Profile**

- Optimized for code and development files
- Separates by programming language
- Organizes documentation and config files
- Handles various development formats

### 🎓 **Student Profile**

- Optimized for academic work
- Organizes by document type and subject
- Handles presentations, assignments, research
- Creates semester-based organization

### 🏢 **Business Profile**

- Optimized for business documents
- Separates financial, legal, marketing materials
- Handles spreadsheets, presentations, reports
- Creates project-based organization

## 🔧 **Troubleshooting**

### Common Issues

**"No profiles available"**

```bash
# Create default profile
file-organizer config --create default
```

**"Directory does not exist"**

```bash
# Check path spelling, use absolute paths
file-organizer organize --path "/full/path/to/directory"
```

**"Permission denied"**

```bash
# Run with appropriate permissions, check folder ownership
# On Windows, try running as administrator if needed
```

**"No files organized"**

```bash
# Check if files match profile rules
file-organizer organize --preview --path /your/path
# Verify profile settings
file-organizer profiles --show your_profile
```

### Getting Help

```bash
# Show help
file-organizer --help

# Show command-specific help
file-organizer organize --help
file-organizer config --help

# Check recent logs for errors
file-organizer logs --recent 5 --errors
```

### Validation

```bash
# Validate your configuration
file-organizer config --validate your_profile

# Check statistics for issues
file-organizer stats --detailed
```

## 🎨 **Advanced Features**

### Custom Profiles

1. Create base profile: `file-organizer config --create default`
2. Export it: `file-organizer config --export default my_custom.json`
3. Edit the JSON file manually
4. Import it: `file-organizer config --import my_custom.json`

### Automation

Create shell scripts for routine tasks:

```bash
#!/bin/bash
# daily_organize.sh
file-organizer organize --batch --profile photographer --path ~/Downloads
file-organizer organize --batch --profile default --path ~/Documents/Unsorted
```

### Integration

Use with cron (Linux/Mac) or Task Scheduler (Windows) for automated organization:

```bash
# Run daily at 2 AM
0 2 * * * /path/to/file-organizer organize --batch --path ~/Downloads
```

## 📞 **Support**

- **Documentation**: Check this guide and `--help` commands
- **Logs**: Use `file-organizer logs --errors` to check for issues
- **GitHub**: [Report issues](https://github.com/furqanahmadrao/python-file-organize-utility/issues)
- **Testing**: Run `python enhanced_test_suite.py` to verify installation

---

**Remember**: Always use `--preview` mode first to see what the organizer will do before making changes to your files!
