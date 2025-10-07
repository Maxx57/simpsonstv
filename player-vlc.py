import os
import random
import time
import re
from subprocess import Popen

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')

videos = []


def extract_season_episode(filename):
    """Extract season and episode numbers from filename.
    Returns (season, episode) tuple or (999999, 999999) if not found."""
    # Match patterns like S01E01, S1E1, s01e01, etc.
    match = re.search(r'[Ss](\d+)[Ee](\d+)', filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return (season, episode)
    # Return high numbers if no match found (so they appear at the end)
    return (999999, 999999)


def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))
    
    # Sort videos by season and episode number
    videos.sort(key=lambda x: extract_season_episode(os.path.basename(x)))


def playVideos():
    global videos
    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return
    
    # Don't shuffle - play in order
    # random.shuffle(videos)
    
    # VLC command with automatic crop detection and stretch
    # Let VLC auto-detect the best video output, with verbose logging
    vlc_command = [
        'cvlc',  # Console VLC
        '--fullscreen',
        '--no-osd',
        '--loop',
        '--no-video-title-show',
        '--aspect-ratio=16:9',  # Force aspect ratio to match your screen
        '--crop=16:9',  # Crop to 16:9 (removes black bars)
        '--no-audio',  # Disable audio (PulseAudio not available in service)
        '--no-snapshot-preview',
        '--verbose=2',  # Add verbose output to see what's happening
        '--extraintf=rc',  # Enable RC interface for remote control
        '--rc-unix=/tmp/vlcsocket',  # Unix socket for touch control
    ] + videos
    
    playProcess = Popen(vlc_command)
    playProcess.wait()


while True:
    playVideos() 