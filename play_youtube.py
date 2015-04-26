from fabulous import image as fi, utils
import fabulous.color as color
import pafy
import cv2
import Image
from StringIO import StringIO
import sys
import os
import requests
import re
import textwrap

MAX_BUF_SIZE = 100
MAX_WIDTH = 120

def download(url):
    meta = pafy.new(url)
    vid = meta.getbest()
    return vid.download()

def play(path):
    # Better colors for display
    utils.term.bgcolor = 'white'
    count = 0

    vid = cv2.VideoCapture(path)

    # Initialize the display

    while(vid.isOpened()):
        # Read the frame
        ret, frame = vid.read()
        count += 1

        # Convert to work with PIL and fabulous
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        display = fi.Image("demo.png")
        display.img = image.convert("RGBA")
        display.resize()
        print str(display)[:-1]

        # Clear the stdout buffer after MAX_FRAME number frames
        if count % MAX_BUF_SIZE == 0:
            os.system('cls' if os.name == 'nt' else 'clear')


def print_result(results, index):
    vid = pafy.new(results[index])
    print str(index + 1) + ")", color.bold(color.underline(vid.title))
    print "Time: {} | Rating: {:.2f} | Views: {:,}".format(vid.duration,
                                                     vid.rating,
                                                     vid.viewcount)
    utils.term.bgcolor = 'white'

    thumbnail = requests.get(vid.thumb)
    image = fi.Image(StringIO(thumbnail.content))

    width = min(utils.term.width, MAX_WIDTH)
    image.resize(width)
    print textwrap.fill(vid.description[:500] + "...", width)
    print str(image)[:-1] # Remove pesky new line character
    print "/"*width

def get_results(search):
    URL = "https://www.youtube.com/results"
    r = requests.get(URL, params={'search_query': search})
    results = re.findall(r'href=\"\/watch\?v=(.{11})', r.content)
    return results[::2]

if __name__ == '__main__':
    results = get_results(sys.argv[1])
    for i in range(3):
        print_result(results, i)

    check = True
    while check:
        selected = raw_input("Select a video (1-3): ")
        try:
            selected = int(selected)
        except ValueError:
            pass
        if selected > 0 and selected < 4:
            check = False

    path = download(results[selected-1])
    os.system('cls' if os.name == 'nt' else 'clear')
    play(path)

