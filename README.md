# Simpsons TV - Raspberry Pi Zero 2W Build

I made some changes to Brandon Withrow's [Waveshare-version TV build](https://withrow.io/simpsons-tv-build-guide-waveshare). That include the changes (https://github.com/jeremywhelchel/simpsonstv) made to use MPV as the video player and added touch controls. The below gif is his and some of his text changes in the readme. I further added a VLC version of the player, as well as updated the encode.py to remove the black bars on the side of the videos if they are there.

I also added a rename files script, in case you have extra information after the season and episode in the file names. Because who doesn't love a good filename that looks like `The.Simpsons.S1E1.REMASTERED.ULTIMATE.DIRECTORS.CUT.EXTENDED.EDITION.FINAL.FINAL2.mp4`? Yeah, we're fixing that.

In the player.py I also updated the play order to respect the seasons and episodes in case there was some weird ordering based on files named something like `The.Simpsons.S1E1.some.extra.info.mp4` and `The.Simpsons.S12E12.some.extra.info.mp4` in file ordering. Mine rename them all to add a zero (0) for single digit season and episode so this `S1E1` becomes `S01E01` and removes all the extra info to the right of the season and episode, etc. Because apparently computers can't count like humans. Who knew? 🤷

---

## Table of Contents

- [Simpsons TV - Raspberry Pi Zero 2W Build](#simpsons-tv---raspberry-pi-zero-2w-build)
  - [Table of Contents](#table-of-contents)
  - [Hardware Used](#hardware-used)
  - [**jeremywhelchel Instructions:**](#jeremywhelchel-instructions)
  - [Touchscreen player control](#touchscreen-player-control)
  - [Videos](#videos)
  - [Video Player Options](#video-player-options)
  - [Hardware changes](#hardware-changes)
  - [MPV Video player](#mpv-video-player)
  - [**MY ADDITIONAL CHANGES:**](#my-additional-changes)
  - [Complete Setup Guide for Raspberry Pi Zero 2W](#complete-setup-guide-for-raspberry-pi-zero-2w)
    - [Step 1: Flash the SD Card with Raspberry Pi OS](#step-1-flash-the-sd-card-with-raspberry-pi-os)
    - [Step 2: Configure the Boot Partition](#step-2-configure-the-boot-partition)
    - [Step 3: First Boot and SSH Connection](#step-3-first-boot-and-ssh-connection)
    - [Step 4: Initial Raspberry Pi Configuration](#step-4-initial-raspberry-pi-configuration)
  - [Quick Reference: Required Software Installation](#quick-reference-required-software-installation)
    - [Step 5: Install Required Software and Python Libraries](#step-5-install-required-software-and-python-libraries)
    - [Step 6: Transfer Project Files](#step-6-transfer-project-files)
      - [Option A: Transfer Files using FileZilla (Slower)](#option-a-transfer-files-using-filezilla-slower)
      - [Option B: Transfer Video Files using USB Drive (Faster)](#option-b-transfer-video-files-using-usb-drive-faster)
    - [Step 7: Install and Configure Systemd Services](#step-7-install-and-configure-systemd-services)
    - [Step 8: Service Management Commands](#step-8-service-management-commands)
    - [Troubleshooting](#troubleshooting)
  - [Additional Notes](#additional-notes)
    - [Video Encoding](#video-encoding)
    - [File Renaming](#file-renaming)

---

## Hardware Used

I'm also using this Raspberry Pi Zero 2W hardware:
(https://www.amazon.com/dp/B0DKKXS4RV?ref=ppx_yo2ov_dt_b_fed_asin_title)

And this waveshare display:
(https://www.amazon.com/dp/B08LZG5G19?ref=ppx_yo2ov_dt_b_fed_asin_title)

And I got these micro usb to type A converters to connect a keyboard to the Pi and manually run the player and touch files using these commands:
`python3 /home/pi/simpsonstv/player.py`

`python3 /home/pi/simpsonstv/touch.py`

(https://www.amazon.com/dp/B0BX9FSCFH?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

![Unidirectional Micro USB Male to US.png](simpson-tv/Unidirectional%20Micro%20USB%20Male%20to%20US.png)

Wherever you see `pi` in the commands, replace that with your username since that's the user you will be using unless you changed it. By default yours will be `pi`, I highly recommend that you change at least the password during the setup process of the flashing of the SSD - I had trouble connecting to the pi using SSH if I used the raspberry OS imager program using the system tools, so I just did the default flash of the ssd card not using the imager system tools (I chose NO) and then did all the setup on the pi using my keyboard connected directly to the pi and a magnifying glass - ;) so I could see what I was typing on that tiny display.

_Pro tip: If you squint really hard at that 2.8" screen while typing, you'll develop either eagle-eye vision or a splitting headache. Possibly both. That's why we're using SSH for most of this. You're welcome._

---

## **jeremywhelchel Instructions:**

![tv demo](tv.gif)

## Touchscreen player control

The Waveshare 2.8" screen has capacitive touch that wasn't used in the original
build. I added a simple `touch.py` job to listen to screen events and send a
handful of commands to the video player. Be sure to add a corresponding systemd
service.

You can:

- Touch left side of screen - seek back 30 seconds
- Touch middle of screen - play / pause
- Touch right side of screen - seek forward 30 seconds
- Swipe from left to right - next video
- Swipe from right to left - previous video

## Videos

The videos are all located at the following directory on the Raspberry Pi

```
'/home/pi/simpsonstv/videos'
```

## Video Player Options

This project includes two video player options:

**Option 1: MPV (Recommended - Default)**

- File: `player.py`
- **Fully compatible with touch controls** via socket interface
- Better performance on Raspberry Pi Zero 2W
- Automatic playlist looping
- On-screen display for current episode
- Touch controls work: play/pause, seek, next/previous episode

**Option 2: VLC (Alternative)**

- File: `player-vlc.py`
- Alternative if you prefer VLC
- Better aspect ratio handling for some video files
- Automatic cropping to 16:9
- **Note:** Touch controls may not work with VLC

**To switch between players:**

Edit the `tvplayer.service` file and change the `ExecStart` line:

For MPV (default):

```
ExecStart=/usr/bin/python3 /home/pi/simpsonstv/player.py
```

For VLC:

```
ExecStart=/usr/bin/python3 /home/pi/simpsonstv/player-vlc.py
```

Then reload and restart the service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tvplayer.service
```

**Recommendation:** Use MPV (`player.py`) for full touch control functionality.

## Hardware changes

Used the newer RPi Zero 2W. This was mostly a drop-in replacement.

I attempted to use a 64-bit version Debian Bookworm, but couldn't properly get
it to work. The screen worked using the newer Waveshare screen overlay setup,
but it took control of the GPIO pins needed for the audio circuit. So I
continued to use the 32-bit Buster OS.

I also glued in the screen upside down, since the bezel was better covered by
the 3d printed housing that way. To invert the screen, set `display_rotate=3` in `/boot/config.txt`

Switched from Micro-USB to USB-C for the power input. Use something like this
[Adafruit USB Type-C breakout board](https://www.adafruit.com/product/4090). Make sure the breakout board has CC resistors that properly indicate 5 volts--otherwise this won't work with C-to-C cables.

## MPV Video player

Because I was originally experimenting 64-bit Bookwork, I couldn't use omxplayer
since it was no longer provided with that distribution. Instead I found MPV to
be a great replacement, and ended up using it for my touch screen scripting as
well.

`sudo apt install mpv`

The player python script is replaced by a much simpler `start.sh` script.

**NOTE: I am not using the start.sh script in my build, though I left it in there. Look at the eremywhelchel version of his code in the tvplayer.service file. His calls the `start.sh` where as mine calls the player.py file.**

---

## **MY ADDITIONAL CHANGES:**

## Complete Setup Guide for Raspberry Pi Zero 2W

This guide walks you through the complete process of setting up a Raspberry Pi Zero 2W with the Waveshare 2.8" DPI LCD for the Simpsons TV project.

### Step 1: Flash the SD Card with Raspberry Pi OS

**1.1 Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/)**

**1.2 Launch Raspberry Pi Imager and select your device**

![SSD Flash Pi Zero 2W Step 1](simpson-tv/SSD%20Flash%20Pi%20Zero%202W%20Step%201.png)

- Click "CHOOSE DEVICE"
- Select "Raspberry Pi Zero 2 W"

**1.3 Select the operating system**

![SSD Flash Pi Zero 2W Step 2](simpson-tv/SSD%20Flash%20Pi%20Zero%202W%20Step%202.png)

- Click "CHOOSE OS"
- Navigate to: **Raspberry Pi OS (other)** → **Raspberry Pi OS (Legacy, 32-bit) Lite**
  - We use the 32-bit Buster-based OS because the 64-bit Bookworm has GPIO conflicts with the Waveshare screen overlay
  - The Lite version is sufficient as we don't need the desktop environment

**1.4 Select your storage device**

![SSD Flash Pi Zero 2W Step 3](simpson-tv/SSD%20Flash%20Pi%20Zero%202W%20Step%203.png)

- Click "CHOOSE STORAGE"
- Select your SD card (typically 16GB or larger recommended)
- Click "NEXT" and then "WRITE" to flash the OS to the SD card

**1.5 Wait for the imaging process to complete**

The Raspberry Pi Imager will download the OS (if needed), write it to the SD card, and verify the write. This may take several minutes.

_Perfect time to grab a coffee, practice your Homer Simpson impression ("D'oh!"), or contemplate why you're building a tiny TV when you already have a perfectly good one on the wall. Don't question it. Just embrace the madness._

### Step 2: Configure the Boot Partition

After the OS is flashed, the SD card will be ejected and remounted. You should see a "boot" partition accessible on your computer.

**2.1 Copy Waveshare LCD drivers**

Navigate to the `boot/overlays` folder on your SD card and copy the Waveshare DPI LCD overlay files from the `simpsons-tv/boot/overlays` folder in this repository:

```
boot/overlays/vc4-kms-dpi-2inch8.dtbo
boot/overlays/waveshare-28dpi-3b.dtbo
boot/overlays/waveshare-28dpi-3b-4b.dtbo
boot/overlays/waveshare-28dpi-4b.dtbo
boot/overlays/waveshare-touch-28dpi.dtbo
```

**2.2 Copy or replace the `config.txt` file**

Copy the `config.txt` file from this repository to the root of the boot partition, replacing the existing one. This file contains the necessary configuration for the Waveshare 2.8" screen, including:

- Display rotation settings (`display_rotate=3` for upside-down screen)
- DPI LCD overlay configuration
- Audio settings

**2.3 Enable SSH**

Create an empty file named `ssh` (no extension) in the root of the boot partition. This enables SSH access on first boot.

On Windows PowerShell:

```powershell
New-Item -Path "E:\ssh" -ItemType File
```

(Replace `E:` with your SD card's drive letter)

**2.4 Configure WiFi**

Copy the `wpa_supplicant.conf` file from this repository to the root of the boot partition. **IMPORTANT:** Before copying, edit the file to add your WiFi credentials:

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_WIFI_SSID"
    psk="YOUR_WIFI_PASSWORD"
}
```

Replace `YOUR_WIFI_SSID` with your network name and `YOUR_WIFI_PASSWORD` with your WiFi password.

**2.5 Safely eject the SD card**

Once all files are copied, safely eject the SD card from your computer and insert it into your Raspberry Pi Zero 2W.

_Look at you, being all responsible and safely ejecting things! Your computer thanks you. The SD card... well, it doesn't care, but good job anyway!_

### Step 3: First Boot and SSH Connection

**3.1 Power on the Raspberry Pi**

Insert the SD card and connect power to your Pi Zero 2W. Wait 1-2 minutes for the first boot to complete.

_This is where you stare at a tiny screen hoping for signs of life. It's like waiting for a text back, except nerdier and with more LEDs blinking._

**3.2 Find the Pi's IP address**

- Check your router's admin panel for connected devices
- Look for a device named `raspberrypi` or similar
- Note the IP address (e.g., `192.168.1.100`)

**3.3 Connect via SSH using mRemoteNG**

![Using mRemoteNG to configure Raspberry Pi](simpson-tv/using%20mRemoteNG%20to%20configure%20Raspberry%20Pi.png)

Download and install [mRemoteNG](https://mremoteng.org/) if you haven't already.

Configure a new SSH connection:

- **Name:** Raspberry Pi Simpson TV
- **Protocol:** SSH version 2
- **Hostname:** [Your Pi's IP address]
- **Username:** `pi` (default for Raspberry Pi OS Legacy)
- **Password:** `raspberry` (default password)
- **Port:** 22

Connect to your Raspberry Pi using this configuration.

### Step 4: Initial Raspberry Pi Configuration

Once connected via SSH, run the Raspberry Pi configuration tool:

```bash
sudo raspi-config
```

**4.1 Change default password (IMPORTANT for security)**

- Navigate to: `1 System Options` → `S3 Password`
- Set a new secure password

**4.2 Configure localization settings**

**Timezone:**

- Navigate to: `5 Localisation Options` → `L2 Timezone`
- Select your geographic area and timezone

**Locale:**

- Navigate to: `5 Localisation Options` → `L1 Locale`
- Select `en_US.UTF-8 UTF-8` (or your preferred locale)

**Keyboard:**

- Navigate to: `5 Localisation Options` → `L3 Keyboard`
- Select `Generic 105-key PC`
- Select `Other` → `English (US)` → `English (US)` → `The default for the keyboard layout` → `No compose key`

**WLAN Country:**

- Navigate to: `5 Localisation Options` → `L4 WLAN Country`
- Select `US` (or your country code)

**4.3 Enable SSH permanently (if not already enabled)**

- Navigate to: `3 Interface Options` → `I2 SSH`
- Select `Yes` to enable SSH server

**4.4 Expand filesystem**

- Navigate to: `6 Advanced Options` → `A1 Expand Filesystem`
- This ensures the OS uses the full SD card capacity

**4.5 Finish and reboot**

- Select `Finish`
- Select `Yes` to reboot

Wait for the Pi to reboot (about 30-60 seconds), then reconnect via SSH.

_Rebooting: a computer's way of saying "have you tried turning it off and on again?" Spoiler alert: it usually works. Unlike your New Year's resolutions._

## Quick Reference: Required Software Installation

After flashing your SD card and completing initial setup with `raspi-config`, you'll need to install the following packages. **This must be done via SSH or directly on the Pi** (SSH is much easier!). The same step by step process is outlined below this, I just added this section for a full list of libraries needed for quick reference:

```bash
# Update system first
sudo apt update && sudo apt upgrade -y

# Install all required packages (one command)
sudo apt install -y mpv vlc ffmpeg python3-pip python3-gpiod python3-evdev
```

**What these packages do:**

- `mpv` - Video player for playback
- `vlc` - Alternative video player option
- `ffmpeg` - Video encoding/conversion tool
- `python3-gpiod` - GPIO control for buttons and backlight
- `python3-evdev` - Touchscreen input handling

See **Step 5** in the complete setup guide below for detailed installation instructions.

_TL;DR for the impatient ones who scrolled down here first: copy that command, run it, and pretend you read everything. We won't tell. 🤫_

---

### Step 5: Install Required Software and Python Libraries

**IMPORTANT:** This step installs all the necessary system packages and Python libraries needed to run the Simpsons TV project. You must complete this step after connecting to your Pi via SSH (using mRemoteNG or another SSH client). While you can also run these commands directly on the Pi with an attached keyboard, using SSH is much easier! **Do not skip this step** - the scripts will not work without these libraries.

**5.1 Update the system**

First, update the package list and upgrade existing packages:

```bash
sudo apt update
sudo apt upgrade -y
```

**5.2 Install required system packages**

Install all required system packages in one command:

```bash
sudo apt install -y mpv vlc ffmpeg python3-pip python3-gpiod python3-evdev
```

**What each package does:**

- **mpv**: Primary video player (used by `player.py`)
- **vlc**: Alternative video player (used by `player-vlc.py`)
- **ffmpeg**: Video encoding tool (used by `encode.py`)
- **python3-pip**: Python package installer
- **python3-gpiod**: GPIO control library (used by `buttons.py` for button and backlight control)
- **python3-evdev**: Event device library (used by `touch.py` for touchscreen input)

**5.3 Verify installations**

You can verify the installations were successful:

```bash
mpv --version
vlc --version
ffmpeg -version
python3 -c "import gpiod; print('gpiod installed')"
python3 -c "import evdev; print('evdev installed')"
```

**Note:** If you plan to use only MPV (recommended), you can skip installing VLC. If you plan to use VLC instead, you'll need to modify the systemd service to use `player-vlc.py` instead of `player.py`. If you use VLC you'll also need to do the work to change the touch.py to use VLC instead of MPV.

_Congratulations! You just installed things! 🎉 I know, I know, hold your applause. But seriously, these boring terminal commands are the foundation of your soon-to-be-awesome tiny TV. Stay strong, warrior._

### Step 6: Transfer Project Files

**Video files:**

- Transfer all your encoded video files from `videos/encoded/` to `/home/pi/simpsonstv/videos/encoded/`

> **Note:** Make sure your videos are properly encoded and renamed before transferring. See the [Video Encoding](#video-encoding) and [File Renaming](#file-renaming) sections if you need to prepare your video files first.

**6.1 Make scripts executable**

In your SSH session, make the shell script executable:

```bash
chmod +x /home/pi/simpsonstv/start.sh
```

_Ah yes, chmod +x. The ancient ritual of making files "executable." It's like knighting a file. "I dub thee... executable!" ⚔️ Your script can now run free and wild._

---

You have two options for transferring your video files to the Raspberry Pi: **FileZilla (slower but simpler)** or **USB Drive (faster)**. Choose the method that works best for you.

#### Option A: Transfer Files using FileZilla (Slower)

**6.2 Install and configure FileZilla**

![Using FileZilla to copy files](simpson-tv/Using%20FileZilla%20to%20copy%20files.png)

Download and install [FileZilla Client](https://filezilla-project.org/).

Configure the connection:

- **Host:** sftp://[Your Pi's IP address]
- **Username:** pi
- **Password:** [Your new password]
- **Port:** 22

Click "Quickconnect"

**6.3 Create the project directory**

In your SSH session, create the directory:

```bash
mkdir -p /home/pi/simpsonstv/videos/encoded
```

**6.4 Transfer files via FileZilla**

Using FileZilla, navigate to the remote directory `/home/pi/simpsonstv/` and transfer the following files from your local repository:

**Root directory files:**

- `buttons.py`
- `player.py`
- `touch.py`
- `start.sh`
- `tv.gif`

**Service files:**

- `tvbuttons.service`
- `tvplayer.service`
- `tvtouch.service`

---

#### Option B: Transfer Video Files using USB Drive (Faster)

If you have a large number of video files, using a USB drive is significantly faster than FileZilla. You'll still need to transfer the Python scripts and service files using FileZilla (Option A, steps 6.1-6.3), but you can use a USB drive for the video files.

**6.5 Prepare the USB drive on your computer**

1. Copy all your encoded video files from `videos/encoded/` to a USB drive
2. Safely eject the USB drive from your computer

> **Note:** Make sure your videos are properly encoded and renamed before copying to the USB drive. See the [Video Encoding](#video-encoding) and [File Renaming](#file-renaming) sections if you need to prepare your video files first.

**6.6 Connect USB drive to Raspberry Pi**

1. Plug the USB drive into the micro USB to Type A adapter (mentioned in the [Hardware Used](#hardware-used) section)
2. Connect the adapter to the Raspberry Pi's micro USB port

**6.7 Mount the USB drive on the Pi**

In your SSH session, run the following commands:

1. Create a mount point for the USB drive:

   ```bash
   sudo mkdir -p /mnt/usb
   ```

2. Find your USB drive (it's usually `sda1`):

   ```bash
   sudo fdisk -l
   ```

   Look for a device like `/dev/sda1` - this is typically your USB drive.

3. Mount the USB drive:

   ```bash
   sudo mount /dev/sda1 /mnt/usb
   ```

4. Verify the files are accessible:
   ```bash
   ls /mnt/usb
   ```

**6.8 Copy video files to the Pi**

Copy all video files from the USB drive to the Pi's videos directory:

```bash
cp /mnt/usb/*.mp4 /home/pi/simpsonstv/videos/encoded/
```

**6.9 Unmount the USB drive**

Once the copy is complete:

```bash
sudo umount /mnt/usb
```

Now you can safely remove the USB drive from the Raspberry Pi.

_USB transfer: because watching FileZilla crawl through 100 video files at 2MB/s is about as fun as watching grass grow. With USB, you'll be done before you can even finish your coffee! ☕ Just plug it in, copy, unplug. Boom. Done. Like a technological ninja. 🥷_

---

**Whichever method you choose, continue to Step 7 below.**

### Step 7: Install and Configure Systemd Services

**7.1 Copy service files to systemd directory**

```bash
sudo cp /home/pi/simpsonstv/tvbuttons.service /etc/systemd/system/
sudo cp /home/pi/simpsonstv/tvplayer.service /etc/systemd/system/
sudo cp /home/pi/simpsonstv/tvtouch.service /etc/systemd/system/
```

**7.2 Reload systemd daemon**

```bash
sudo systemctl daemon-reload
```

**7.3 Enable services to start on boot**

```bash
sudo systemctl enable tvbuttons.service
sudo systemctl enable tvplayer.service
sudo systemctl enable tvtouch.service
```

**7.4 Start the services**

```bash
sudo systemctl start tvbuttons.service
sudo systemctl start tvplayer.service
sudo systemctl start tvtouch.service
```

**7.5 Check service status**

Verify that all services are running correctly:

```bash
sudo systemctl status tvbuttons.service
sudo systemctl status tvplayer.service
sudo systemctl status tvtouch.service
```

Press `q` to exit the status view.

_If all three services show green "active (running)" status, you're basically a Linux sysadmin now. Add it to your resume. If they're red and angry... well, welcome to the troubleshooting section below! 😅_

### Step 8: Service Management Commands

**To stop a service:**

```bash
sudo systemctl stop tvplayer.service
```

**To restart a service:**

```bash
sudo systemctl restart tvplayer.service
```

**To disable a service from starting on boot:**

```bash
sudo systemctl disable tvplayer.service
```

**To view service logs:**

```bash
sudo journalctl -u tvplayer.service -f
```

**To stop all Simpsons TV services:**

```bash
sudo systemctl stop tvbuttons.service tvplayer.service tvtouch.service
```

**To start all Simpsons TV services:**

```bash
sudo systemctl start tvbuttons.service tvplayer.service tvtouch.service
```

**To restart all Simpsons TV services:**

```bash
sudo systemctl restart tvbuttons.service tvplayer.service tvtouch.service
```

_Did something break? Try the classic "turn it off and back on again" approach. They've done studies, you know. 60% of the time, it works every time. Those are pretty good odds if you ask me!_

### Troubleshooting

**Missing Python library errors:**

If you see errors like `ModuleNotFoundError: No module named 'gpiod'` or `ModuleNotFoundError: No module named 'evdev'`:

- Make sure you completed **Step 5** and installed all required packages
- Verify installations:
  ```bash
  python3 -c "import gpiod; print('gpiod OK')"
  python3 -c "import evdev; print('evdev OK')"
  ```
- If still missing, reinstall the specific package:
  ```bash
  sudo apt install -y python3-gpiod python3-evdev
  ```

**Button controls not working:**

- Verify `tvbuttons.service` is running: `sudo systemctl status tvbuttons.service`
- Check for gpiod library errors in logs: `sudo journalctl -u tvbuttons.service -n 50`
- Ensure python3-gpiod is installed (see above)

**Screen not displaying correctly:**

- Verify the `config.txt` file was copied correctly to the boot partition
- Check that the Waveshare overlay file exists in `/boot/overlays/`
- Ensure `display_rotate=3` is set if you installed the screen upside down

**WiFi not connecting:**

- Verify your `wpa_supplicant.conf` has the correct SSID and password
- Check that the country code matches your location
- Ensure the file is in the boot partition before first boot

**Touch screen not responding:**

- Check that `tvtouch.service` is running: `sudo systemctl status tvtouch.service`
- Verify the Python evdev library is installed: `python3 -c "import evdev"`
- Check for permission errors in logs: `sudo journalctl -u tvtouch.service -n 50`
- Ensure user is in the `input` group: `sudo usermod -a -G input pi` (then reboot)

**Videos not playing:**

- Check that MPV is installed: `mpv --version`
- Verify video files exist in `/home/pi/simpsonstv/videos/encoded/`
- Check `tvplayer.service` logs: `sudo journalctl -u tvplayer.service -n 50`
- Ensure video files are in MP4 format

**MPV or VLC not found:**

- Install the missing player:
  ```bash
  sudo apt install -y mpv vlc
  ```
- Verify installation: `mpv --version` or `vlc --version`

**Services not starting:**

- Check for errors: `sudo systemctl status [service-name]`
- View detailed logs: `sudo journalctl -u [service-name] -n 50`
- Verify file permissions and paths in the service files
- Ensure all required libraries are installed (see **Step 5**)

**Python script errors:**

Common errors and solutions:

- `ModuleNotFoundError`: Missing Python library - install required packages from **Step 5**
- `FileNotFoundError: /tmp/mpvsocket`: MPV player not running or not started with socket support
- `Permission denied /dev/input/event0`: User not in input group - run `sudo usermod -a -G input pi` and reboot

---

## Additional Notes

### Video Encoding

If you need to encode new videos to the correct format for the Raspberry Pi, use the `encode.py` script in the `videos/` directory.

**Requirements:**

- `ffmpeg` must be installed (included in **Step 5**)

**How to use:**

1. Place your source video files in the `videos/` directory (supports .mp4, .mkv, .mov, .avi formats)
2. Run the encoding script:
   ```bash
   cd /home/pi/simpsonstv/videos
   python3 encode.py
   ```
3. Encoded videos will be saved to `videos/encoded/` with optimized settings:
   - Resolution: 480p height (appropriate for the 2.8" screen)
   - Cropping: Removes black bars from sides (240px removed)
   - Video codec: H.264 baseline profile (compatible with Raspberry Pi)
   - Audio: AAC stereo at 128kbps

**Note:** Encoding is CPU-intensive and may be slow on the Raspberry Pi. Consider encoding videos on a more powerful computer before transferring them to the Pi.

_Fair warning: Encoding videos on a Pi Zero 2W is like watching paint dry... in slow motion... on a Tuesday. Seriously, do yourself a favor and encode on your main computer first. Your sanity will thank you. This is the perfect time for a bathroom break, a snack, a nap, or perhaps reorganizing your sock drawer. Come back in... well, a while. A long while. Maybe bring a book. 📚_

### File Renaming

Use the `renamefiles.py` script in `videos/encoded/` to standardize video filenames to the format `The.Simpsons.S##E##.mp4` (with zero-padded season and episode numbers).

**How to use:**

1. Navigate to the encoded videos directory:
   ```bash
   cd /home/pi/simpsonstv/videos/encoded
   ```
2. Run the rename script:
   ```bash
   python3 renamefiles.py
   ```

This ensures proper alphabetical sorting and sequential playback of episodes.

_Because `S1E1` coming after `S12E12` in alphabetical order is the kind of chaos we simply cannot tolerate in a civilized society. We're building a tiny TV here, people! Standards matter! The script will clean up those filenames faster than you can say "D'oh!" Now go forth and enjoy your properly sorted Simpsons episodes, you magnificent nerd. You did it! 🎊_

---

**You've made it to the end!** If everything works, you now have a fully functional miniature Simpsons TV. If it doesn't... well, there's always the troubleshooting section above. And coffee. Lots of coffee. ☕

Happy binge-watching on your ridiculously tiny TV! 📺✨
