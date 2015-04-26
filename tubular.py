from fabulous import image as fi, color, utils

import pafy

import cv2
import Image
from StringIO import StringIO

import os

import requests
import re
import textwrap

import argparse

class Player():
    MAX_BUF_SIZE = 100
    MAX_WIDTH = 120

    def __init__(self, query=None):
        self.videos = []
        self.results = None
        if query is not None:
            self.search(query)

    def quick_play(self, index=0):
        """Downloads and plays the song at a given index.
        By default will play the top result.
        """
        self.play(self.download(self.results[index]))

    def download(self, url=None):
        """Download the video specified by the URL to the current path."""
        if url is None:
            if self.results is None:
                raise ValueError("Please specify a valid url.")
            else:
                url = self.results[0]
        try:
            meta = pafy.new(url)
        except Exception:
            raise IOError("Video not available for download.")

        vid = meta.getbest()
        path = vid.download()
        self.videos.append(path)
        return path

    def play(self, path=None):
        """Play a video specified by path to the terminal."""
        if path is None:
            path = self.download()

        # Clear the users out buffer before playing the video
        os.system('cls' if os.name == 'nt' else 'clear')

        # Better colors for display
        utils.term.bgcolor = 'white'
        count = 0

        vid = cv2.VideoCapture(path)

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
            if count % self.MAX_BUF_SIZE == 0:
                os.system('cls' if os.name == 'nt' else 'clear')

    def __iter__(self):
        for i in range(len(self.results)):
            yield self.get_result(self, index=i)

    def get_result(self, results=None, index=0):
        """Returns a terminal representation of a YouTube Video result."""
        if results is None:
            results = self.results
        try:
            vid = pafy.new(results[index])
        except Exception:
            return str(index + 1) + ")  This video is not available.\n"

        string = ""
        string += str(index + 1) + ")  "
        string += str(color.bold(color.underline(vid.title))) + "\n"

        more_info = "Time: {} | Rating: {:.2f} | Views: {:,}\n"
        string += more_info.format(vid.duration, vid.rating, vid.viewcount)

        utils.term.bgcolor = 'white'

        thumbnail = requests.get(vid.thumb)
        image = fi.Image(StringIO(thumbnail.content))

        width = min(utils.term.width, self.MAX_WIDTH)
        image.resize(width)
        string += textwrap.fill(vid.description[:500] + "...", width) + "\n"
        string += str(image)
        string += "/"*width + "\n"
        return string

    def search(self, query):
        """Specify a query and return the top matches as URLs."""
        URL = "https://www.youtube.com/results"
        r = requests.get(URL, params={'search_query': query})
        results = re.findall(r'href=\"\/watch\?v=(.{11})', r.content)
        self.results = results[::2]
        return self.results

    def __del__(self):
        try:
            for path in self.videos:
                os.remove(path)
        except OSError:
            pass

if __name__ == '__main__':
    desc = 'A YouTube video player that runs soley on a terminal.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('query', metavar='query', type=str,
                        help='A search query for YouTube videos')
    args = parser.parse_args()

    player = Player(args.query)
    for i in range(3):
        print player.get_result(index=i)

    check = True
    while check:
        selected = raw_input("Select a video (1-3): ")
        try:
            selected = int(selected)
        except ValueError:
            pass
        if selected > 0 and selected < 4:
            check = False

    player.quick_play(selected)
