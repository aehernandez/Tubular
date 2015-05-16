***Tubular, a YouTube to Terminal Video Player

Dependencies:
====
Make sure opencv is installed
    apt-get install libopencv-dev python-opencv
Make sure other dependencies are installed
    pip install -r requirements.txt

In the root project directory run 'python tubular.py [query]'
Where [query] is a string representing a YouTube video search query.
For example 'python tubular.py "upenn grasp"' could be run.
The top three results will be shown. Type 1, 2, or 3 to select the video you
want to play and then hit enter. Enjoy the video!
