from Track import Track
from Racer import Racer
from RaceManager import RaceManager

WIDTH = 1500
HEIGHT = 1200

track = Track(WIDTH, HEIGHT)
rm = RaceManager(track)

track.setup_track()

rm.add_racer(Racer("One", "red"))
rm.add_racer(Racer("One", "green"))
rm.add_racer(Racer("One", "orange"))
rm.add_racer(Racer("One", "blue"))
rm.add_racer(Racer("One", "teal"))
rm.add_racer(Racer("One", "brown"))
rm.add_racer(Racer("One", "black"))
rm.add_racer(Racer("One", "gray"))
rm.add_racer(Racer("One", "purple"))
rm.add_racer(Racer("One", "pink"))
rm.add_racer(Racer("One", "magenta"))

rm.start_race()

input()