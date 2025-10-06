I made some changes to Brandon Withrow's [Waveshare-version TV build](https://withrow.io/simpsons-tv-build-guide-waveshare).

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
'/home/admin/simpsonstv/videos'
```

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
