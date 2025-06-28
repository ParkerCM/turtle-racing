import random
import Track
from Stopwatch import Stopwatch

TURTLE_WIDTH = 40
MIN_DISTANCE = 1
MAX_DISTANCE = 5

def get_random_distance():
    return random.randint(MIN_DISTANCE, MAX_DISTANCE)

def should_turn():
    return random.randint(1, 50) == 1

class RaceManager:

    def __init__(self, track):
        self.racers = []
        self.completed_racers = []
        self.number_of_laps = 2
        self.track = track

    def add_racer(self, racer):
        self.racers.append(racer)

    def add_racers_to_track(self):
        x_offset = len(self.racers) - 1
        y_offset = 1

        for racer in self.racers:
            racer.turtle.goto(x_offset * -(TURTLE_WIDTH / 2), (self.track.height * -0.2) - ((TURTLE_WIDTH / 2) * y_offset))

            if x_offset != len(self.racers) - 1:
                self.racers[x_offset].current_lap = -1

            y_offset += 1
            x_offset -= 1

    def start_race(self):
        self.add_racers_to_track()
        self.track.write_message("Race started!")
        self.track.screen.tracer(0)

        [racer.start_timer() for racer in self.racers]

        stopwatch = Stopwatch()
        stopwatch.start()

        while len(self.racers) > 0:
            for racer in self.racers:
                if (self.track.racer_in_turn_zone(racer) and should_turn()) or (self.track.racer_must_turn(racer, MAX_DISTANCE)):
                    racer.turn()
                else:
                    old_xcor = racer.turtle.xcor()
                    racer.move_forward(get_random_distance())

                    if Track.racer_crossed_finish(racer.direction, old_xcor, racer.turtle.xcor()):
                        racer.completed_lap()
                        if racer.current_lap == self.number_of_laps:
                            racer.stop_timer()
                            self.completed_racers.append(racer)
                            self.racers.remove(racer)
            self.track.screen.update()

        stopwatch.stop()

        for racer in self.completed_racers:
            self.track.write_results(self.completed_racers, stopwatch.elapsed_time(), self.find_fastest_lap())
            self.track.screen.update()
            print(racer)

    def find_fastest_lap(self):
        fastest_racer = self.completed_racers[0]
        for racer in self.completed_racers:
            if racer.best_lap < fastest_racer.best_lap:
                fastest_racer = racer
        return fastest_racer
