import os
from pathlib import Path
import subprocess
import json

def get_video_duration(video_path):
    """
    Get video duration using ffprobe (part of ffmpeg)
    Returns duration in seconds, or None if failed
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            return duration
        else:
            return None
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return None

def format_duration(seconds):
    """Convert seconds to HH:MM:SS format"""
    if seconds is None:
        return "N/A"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def scan_videos(root_path, extensions=None):
    """
    Scan directory for video files and get their durations
    
    Args:
        root_path: Path to start scanning from
        extensions: List of video extensions to look for (e.g., ['.mp4', '.avi'])
    """
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    
    # Convert to lowercase for comparison
    extensions = [ext.lower() for ext in extensions]
    
    root = Path(root_path)
    
    if not root.exists():
        print(f"Error: Path '{root_path}' does not exist!")
        return
    
    print(f"Scanning directory: {root_path}")
    print("-" * 80)
    
    total_duration = 0
    video_count = 0
    
    # Walk through all directories and subdirectories
    for video_file in root.rglob('*'):
        if video_file.is_file() and video_file.suffix.lower() in extensions:
            duration = get_video_duration(video_file)
            
            if duration is not None:
                total_duration += duration
                video_count += 1
                
                # Print relative path for cleaner output
                rel_path = video_file.relative_to(root)
                print(f"{rel_path}")
                print(f"  Duration: {format_duration(duration)} ({duration:.2f} seconds)")
                print()
    
    print("-" * 80)
    print(f"\nSummary:")
    print(f"Total videos found: {video_count}")
    print(f"Total duration: {format_duration(total_duration)} ({total_duration:.2f} seconds)")
    print(f"Average duration: {format_duration(total_duration / video_count if video_count > 0 else 0)}")

if __name__ == "__main__":
    # Replace this with your hard disk path
    # folder_path = r"C:\Your\Video\Folder"  # Windows example
    folder_path = "/home/sreyas/Desktop"  # Linux/Mac example
    
    scan_videos(folder_path)