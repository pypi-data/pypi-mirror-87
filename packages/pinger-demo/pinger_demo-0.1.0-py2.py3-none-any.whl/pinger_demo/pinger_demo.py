#!/usr/bin/env python3
import subprocess, platform, time, threading
from pystray import Icon
from PIL import Image, ImageDraw

ADDR_LIST = ['192.168.255.1', '192.168.255.129']
GREEN = (0, 153, 0)
RED = (204, 0, 0)


def ping(host):
    """
    Returns True if host responds to a ping request
    """
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True
    return subprocess.call(args, shell=need_sh) == 0


def create_image(text=None, color=RED):
    text = text.split('.')[-1]
    # Generate an image and draw a pattern
    image = Image.new('RGB', (25, 25), color)
    dc = ImageDraw.Draw(image)
    dc.text((0, 5), '.' + text, fill='white')
    return image


def callback(icon):
    while True:
        color = GREEN if ping(icon.title) else RED
        icon.icon = create_image(icon.title, color)
        icon.visible = True

def run_icon(addr):
    ico = Icon(addr)
    ico.title = addr
    ico.run(setup=callback)


def main():
    for addr in ADDR_LIST:
        threading.Thread(target=run_icon, args=(addr,)).start()

if __name__ == "__main__":
    main()
