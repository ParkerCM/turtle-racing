from Track import Track
from Racer import Racer
from RaceManager import RaceManager

WIDTH = 1500
HEIGHT = 1200
NUMBER_OF_LAPS = 5

track = Track(WIDTH, HEIGHT)
rm = RaceManager(NUMBER_OF_LAPS, track)

track.setup_track()

rm.add_racer(Racer("shellfire 🔥", "red"))
rm.add_racer(Racer("guac rocket 🥑", "green"))
rm.add_racer(Racer("slowrange 🍊", "orange"))
rm.add_racer(Racer("blurricane 🌪️", "blue"))
rm.add_racer(Racer("turboost 🐬", "teal"))
rm.add_racer(Racer("dirt napper 🪵", "brown"))
rm.add_racer(Racer("shadow snap 🐢", "black"))
rm.add_racer(Racer("gravy train 🚂", "gray"))
rm.add_racer(Racer("blurple ⚡", "purple"))
rm.add_racer(Racer("peony power 🌸", "pink"))
rm.add_racer(Racer("zoomenta 🌀", "magenta"))

rm.start_race()
