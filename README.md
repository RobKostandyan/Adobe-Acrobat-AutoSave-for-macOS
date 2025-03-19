# Adobe-Acrobat-AutoSave-for-macOS

This is a Python script that automatically saves your Adobe Acrobat documents at regular intervals. The native Acrobat's autosave, when it saves to a temporary file, was not enough for me, because my pdf's are stored in iCloud, and I have access to them from different devices, so I wanted it to be just automatically saved to the main doc, the same way when you press Command + S. 

## 🌟 Features

- **Silent Auto-Saving**: Automatically saves all open modified documents in Adobe Acrobat
- **Background Operation**: Works without disrupting your workflow - no focus switching when possible
- **Multi-Document Support**: Detects and saves all open tabs in Adobe Acrobat
- **Smart Saving**: Only saves documents that have actual modifications
- **iCloud Sync Friendly**: Ensures your changes appear on all your devices
- **macOS Native**: Designed specifically for macOS with AppleScript integration

## 📋 Requirements

- macOS 
- Python 3.6 or higher
- Adobe Acrobat DC / Adobe Acrobat Reader DC

## 🚀 Installation

### Option 1: Quick Setup

1. Download `adobe_autosave.py` from this repository
2. Place it in a permanent location (e.g., `~/Documents/Python projects/`)

### Option 2: Clone the Repository

```bash
git clone https://github.com/RobKostandyan/Adobe-Acrobat-AutoSave-for-macOS.git
cd Adobe-Acrobat-AutoSave-for-macOS
```

## 💻 Usage

### Method 1: Run Directly in Terminal

Run the script manually whenever you need it:

```bash
cd ~/path/to/script/directory
python3 adobe_autosave.py
```

The script will start saving your documents every minute. To stop the script, press `Ctrl+C`.

### Method 2: Run in Background from Terminal

To run the script in the background (allowing you to close the Terminal):

```bash
cd ~/path/to/script/directory
nohup python3 adobe_autosave.py > /dev/null 2>&1 &
```

To stop the background script later:
```bash
ps aux | grep adobe_autosave
kill [PID]  # Replace [PID] with the process ID number shown
```

### Method 3: Automator App (Recommended Setup)

Create an Automator app to easily start the script:

1. Open **Automator** (from Applications folder)
2. Choose **Application** as the document type
3. Search for and add **Run Shell Script** action
4. Set Shell to `/bin/zsh` (or `/bin/bash`)
5. Paste this script:
   ```bash
   cd "~/path/to/script/directory"
   /usr/bin/python3 adobe_autosave.py >> ~/Documents/autosave.txt 2>&1 &
   ```

6. Replace the path with your actual script location
7. Save as an application (e.g., "Adobe AutoSave.app") to Applications
To run: Double-click the Automator app

To automatically start at login:
1. Go to **System Preferences → Users & Groups → Login Items**
2. Click **+** and add your Automator application

## ⚙️ How It Works

This script leverages AppleScript to interact with Adobe Acrobat:

1. Every 60 seconds, it checks if Adobe Acrobat is running
2. If running, it identifies all open documents
3. For each document, it checks if there are unsaved modifications
4. It uses Adobe Acrobat's native save functionality to save modified documents
5. If direct saving fails, it falls back to simulating Command+S keystrokes
6. The script carefully preserves your focus on whatever application you're using
The script is designed to be as non-intrusive as possible, only interacting with Adobe Acrobat when necessary and only saving documents that have actually been modified.

## 🔍 Troubleshooting

### Script says "Adobe Acrobat is not running" even though it is

The process name might be different on your system. Check the exact process name:

```bash
ps aux | grep -i acrobat
```

Then update the script, changing "AdobeAcrobat" to match your process name.

### Background script not working

If running as a background process isn't working, try the Automator method which tends to be more reliable for long-term background execution.

## 🙏 Acknowledgements

This script was developed to solve the real-world problem of Adobe Acrobat's lack of true auto-save functionality, especially regarding iCloud sync between macOS and iOS devices.
