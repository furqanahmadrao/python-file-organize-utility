# File Organizer v1.0 - Virtual Environment Setup

## Virtual Environment Information

- **Python Version**: 3.13.7
- **Environment Name**: venv
- **Location**: `./venv/`

## Quick Start Commands

### Activate Virtual Environment

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment

```bash
deactivate
```

### Install Dependencies (if any are added later)

```bash
pip install -r requirements.txt
```

### Test the Environment

```bash
# Verify Python is using the virtual environment
python -c "import sys; print(sys.executable)"

# Should show: C:\Users\Furqan\Documents\file_oragnizer\venv\Scripts\python.exe
```

## Project Usage (with Virtual Environment)

1. **Activate the virtual environment first**:

   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Run the organizer**:

   ```bash
   python organizer_main.py --preview
   python organizer_main.py
   ```

3. **Configure settings**:

   ```bash
   python config_setup.py
   ```

4. **View logs**:

   ```bash
   python log_viewer.py
   ```

5. **Run tests**:
   ```bash
   python test_script.py
   ```

## Notes

- This project uses only Python standard library, so no external packages are required
- The virtual environment ensures isolation from system Python packages
- Always activate the virtual environment before running the project scripts
