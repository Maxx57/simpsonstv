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
    
    # MPV command with socket interface for touch controls
    mpv_command = [
        'mpv',
        '--input-ipc-server=/tmp/mpvsocket',  # Enable socket for touch.py
        '--fullscreen',
        '--osd-duration=5000',
        '--osd-font-size=80',
        '--osd-playing-msg=${filename/no-ext}',
        '--osd-on-seek=msg-bar',
        '--loop-playlist=inf',  # Loop the entire playlist
        '--no-terminal',  # Don't clutter terminal output
        '--ao=alsa',  # Use ALSA audio output to avoid PipeWire issues
    ] + videos
    
    playProcess = Popen(mpv_command)
    playProcess.wait()


while True:
    playVideos() 