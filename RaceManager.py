import random
import Track
from Direction import Direction
from Stopwatch import Stopwatch
import copy

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
        self.number_of_laps = 5
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
        self.track.screen.tracer(0)

        [racer.start_timer() for racer in self.racers]

        stopwatch = Stopwatch()
        stopwatch.start()

        while not self.is_race_over():
            for racer in self.racers:
                if racer.completed_race:
                    continue

                if (self.track.racer_in_turn_zone(racer) and should_turn()) or (self.track.racer_must_turn(racer, MAX_DISTANCE)):
                    racer.turn()
                else:
                    old_xcor = racer.turtle.xcor()
                    racer.move_forward(get_random_distance())

                    if Track.racer_crossed_finish(racer.direction, old_xcor, racer.turtle.xcor()):
                        racer.completed_lap()
                        if racer.current_lap == self.number_of_laps:
                            racer.stop_timer()
                            racer.completed_race = True
            self.track.write_leaderboard(self.live_leaderboard(), self.number_of_laps)
            self.track.screen.update()

        stopwatch.stop()

        for racer in self.racers:
            self.track.write_results(self.racers, stopwatch.elapsed_time(), self.find_fastest_lap())
            self.track.screen.update()
            print(racer)

    def is_race_over(self):
        for racer in self.racers:
            if racer.current_lap != self.number_of_laps:
                return False
        return True

    def find_fastest_lap(self):
        fastest_racer = self.racers[0]
        for racer in self.racers:
            if racer.best_lap < fastest_racer.best_lap:
                fastest_racer = racer
        return fastest_racer

    def live_leaderboard(self):
        leaderboard = []
        racer_dict = {}
        racers = self.racers.copy()

        # First, add all racers who have finished based on their total time
        # Second, separate all racers based on their current lap
        # Third, compare the position of each racer based on these criteria and place ahead if true:
        #   - If direction is right AND xcor is less than 0 AND x cor is less than
        #   - If direction is right AND xcor is greather than 0 AND x cor is greather than
        #   - If direction is up AND y cor is greater than
        #   - If direction is left AND x cor is less than
        #   - If direction is down AND y cor is less than
        for racer in sorted(racers, key=lambda racer: racer.stopwatch.elapsed_time()):
            if racer.completed_race:
                leaderboard.append(racer)
                racers.remove(racer)
            else:
                racer_dict.setdefault(racer.current_lap, []).append(racer)

        for lap in sorted(racer_dict.keys(), reverse=True):
            up_direction_racers = [racer for racer in racer_dict[lap] if racer.direction == Direction.UP]
            down_direction_racers = [racer for racer in racer_dict[lap] if racer.direction == Direction.DOWN]
            left_direction_racers = [racer for racer in racer_dict[lap] if racer.direction == Direction.LEFT]
            right_direction_racers = [racer for racer in racer_dict[lap] if racer.direction == Direction.RIGHT]

            end_of_lap_right_direction_racers = [racer for racer in right_direction_racers if racer.turtle.xcor() < 0]
            start_of_lap_right_direction_racers = [racer for racer in right_direction_racers if racer.turtle.xcor() > 0]

            sorted_right_end_of_lap_racers = sorted(end_of_lap_right_direction_racers, key=lambda racer: racer.turtle.xcor(), reverse=True)
            for right_racer in sorted_right_end_of_lap_racers:
                leaderboard.append(right_racer)

            sorted_down_racers = sorted(down_direction_racers, key=lambda racer: racer.turtle.ycor())
            for down_racer in sorted_down_racers:
                leaderboard.append(down_racer)

            sorted_left_racers = sorted(left_direction_racers, key=lambda racer: racer.turtle.xcor())
            for left_racer in sorted_left_racers:
                leaderboard.append(left_racer)

            sorted_up_racers = sorted(up_direction_racers, key=lambda racer: racer.turtle.ycor(), reverse=True)
            for up_racer in sorted_up_racers:
                leaderboard.append(up_racer)

            sorted_right_start_of_lap_racers = sorted(start_of_lap_right_direction_racers, key=lambda racer: racer.turtle.xcor(), reverse=True)
            for right_racer in sorted_right_start_of_lap_racers:
                leaderboard.append(right_racer)

        return leaderboard