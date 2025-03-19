#!/usr/bin/env python3
import subprocess
import time
import os
from datetime import datetime

def save_all_acrobat_documents():
    """Save all modified documents in Adobe Acrobat across all tabs"""
    # First check if Acrobat is running
    check_script = '''
    tell application "System Events"
        set acrobatRunning to exists (processes where name is "AdobeAcrobat")
    end tell
    '''
    result = subprocess.run(["osascript", "-e", check_script], capture_output=True, text=True)
    is_running = result.stdout.strip() == "true"

    if not is_running:
        print(f"{datetime.now().strftime('%H:%M:%S')} - AdobeAcrobat is not running")
        return False

    print(f"{datetime.now().strftime('%H:%M:%S')} - AdobeAcrobat is running, checking all documents...")

    # Try to save all documents using the application's commands
    save_all_script = '''
    tell application "Adobe Acrobat"
        set docCount to count of documents
        set savedCount to 0
        set modifiedCount to 0

        if docCount is 0 then
            return "no documents"
        end if

        repeat with i from 1 to docCount
            set currentDoc to document i
            try
                if modified of currentDoc then
                    set modifiedCount to modifiedCount + 1
                    save currentDoc
                    set savedCount to savedCount + 1
                end if
            on error errMsg
                -- Just continue to next document
            end try
        end repeat

        return "checked:" & docCount & ",modified:" & modifiedCount & ",saved:" & savedCount
    end tell
    '''

    try:
        result = subprocess.run(["osascript", "-e", save_all_script], capture_output=True, text=True, timeout=10)
        save_result = result.stdout.strip()

        if save_result == "no documents":
            print(f"{datetime.now().strftime('%H:%M:%S')} - No documents open in Adobe Acrobat")
            return True
        elif save_result.startswith("checked:"):
            print(f"{datetime.now().strftime('%H:%M:%S')} - {save_result}")
            if "error:" in save_result:
                return fallback_save_all_documents()
            return True
        else:
            print(f"Unexpected result: {save_result}")
            return fallback_save_all_documents()
    except subprocess.TimeoutExpired:
        print("Direct save all method timed out, trying fallback...")
        return fallback_save_all_documents()

def fallback_save_all_documents():
    """Fallback method that uses Command+Option+S (Save All) if the direct save method fails"""
    # Get currently active application
    get_frontmost_script = '''
    tell application "System Events"
        set frontApp to name of first process where it is frontmost
    end tell
    '''
    result = subprocess.run(["osascript", "-e", get_frontmost_script], capture_output=True, text=True)
    front_app = result.stdout.strip()

    # Use Command+Option+S to Save All (if supported by your version of Adobe Acrobat)
    # If not supported, we'll send Command+S instead
    save_all_script = '''
    tell application "System Events"
        tell process "AdobeAcrobat"
            set frontmost to true
            delay 0.3

            -- Try Command+Option+S (Save All in some versions)
            try
                keystroke "s" using {command down, option down}
                delay 0.5
            on error
                -- If that fails, just do regular Command+S
                keystroke "s" using command down
                delay 0.5
            end try
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", save_all_script])

    # Restore focus to original app
    restore_focus_script = f'''
    tell application "System Events"
        tell process "{front_app}"
            set frontmost to true
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", restore_focus_script])

    print(f"{datetime.now().strftime('%H:%M:%S')} - Save All command sent to AdobeAcrobat (with focus)")
    return True

def main():
    save_interval = 60  # Save every 1 minute

    print(f"Adobe Acrobat AutoSave started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Saving all modified documents every {save_interval} seconds")
    print(f"Press Ctrl+C to stop")

    try:
        # Save immediately when starting
        save_all_acrobat_documents()

        # Then continue saving at regular intervals
        while True:
            time.sleep(save_interval)
            save_all_acrobat_documents()
    except KeyboardInterrupt:
        print(f"\nAutoSave script stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()