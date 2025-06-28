import random

from Direction import Direction
from Stopwatch import Stopwatch
from Track import Track

class RaceManager:

    TURTLE_WIDTH = 40
    MIN_DISTANCE = 1
    MAX_DISTANCE = 5

    def __init__(self, track):
        self.racers = []
        self.number_of_laps = 5
        self.track = track

    def add_racer(self, racer):
        self.racers.append(racer)

    def start_race(self):
        self._add_racers_to_track()
        self.track.screen.tracer(0)

        [racer.start_timer() for racer in self.racers]

        stopwatch = Stopwatch()
        stopwatch.start()

        while not self._is_race_over():
            for racer in self.racers:
                if racer.completed_race:
                    continue

                if (self.track.racer_in_turn_zone(racer) and self._should_turn()) or (
                        self.track.racer_must_turn(racer, RaceManager.MAX_DISTANCE)):
                    racer.turn()
                else:
                    old_xcor = racer.turtle.xcor()
                    racer.move_forward(self._get_random_distance())

                    if Track.racer_crossed_finish(racer.direction, old_xcor, racer.turtle.xcor()):
                        racer.completed_lap()
                        if racer.current_lap == self.number_of_laps:
                            racer.stop_timer()
                            racer.completed_race = True
            self.track.write_leaderboard(self._live_leaderboard(), self.number_of_laps)
            self.track.screen.update()

        stopwatch.stop()

        for racer in self.racers:
            self.track.write_results(self.racers, stopwatch.elapsed_time(), self._find_fastest_lap())
            self.track.screen.update()
            print(racer)

    def _add_racers_to_track(self):
        x_offset = len(self.racers) - 1
        y_offset = 1

        for racer in self.racers:
            racer.turtle.goto(x_offset * -(RaceManager.TURTLE_WIDTH / 2),
                              (self.track.height * -0.2) - ((RaceManager.TURTLE_WIDTH / 2) * y_offset))

            if x_offset != len(self.racers) - 1:
                self.racers[x_offset].current_lap = -1

            y_offset += 1
            x_offset -= 1

    def _is_race_over(self):
        for racer in self.racers:
            if racer.current_lap != self.number_of_laps:
                return False
        return True

    def _find_fastest_lap(self):
        fastest_racer = self.racers[0]
        for racer in self.racers:
            if racer.best_lap < fastest_racer.best_lap:
                fastest_racer = racer
        return fastest_racer

    def _live_leaderboard(self):
        leaderboard = []
        racers = self.racers.copy()

        # Separate finished racers and group the rest by current lap
        racer_dict = self._group_unfinished_racers_by_lap(racers, leaderboard)

        for lap in sorted(racer_dict.keys(), reverse=True):
            grouped = self._group_racers_by_direction(racer_dict[lap])

            self._add_sorted_racers(
                leaderboard,
                [r for r in grouped[Direction.RIGHT] if r.turtle.xcor() < 0],
                key=lambda r: r.turtle.xcor(),
                reverse=True
            )

            self._add_sorted_racers(
                leaderboard,
                grouped[Direction.DOWN],
                key=lambda r: r.turtle.ycor()
            )

            self._add_sorted_racers(
                leaderboard,
                grouped[Direction.LEFT],
                key=lambda r: r.turtle.xcor()
            )

            self._add_sorted_racers(
                leaderboard,
                grouped[Direction.UP],
                key=lambda r: r.turtle.ycor(),
                reverse=True
            )

            self._add_sorted_racers(
                leaderboard,
                [r for r in grouped[Direction.RIGHT] if r.turtle.xcor() > 0],
                key=lambda r: r.turtle.xcor(),
                reverse=True
            )

        return leaderboard

    @staticmethod
    def _get_random_distance():
        return random.randint(RaceManager.MIN_DISTANCE, RaceManager.MAX_DISTANCE)

    @staticmethod
    def _should_turn():
        return random.randint(1, 50) == 1

    @staticmethod
    def _get_racers_for_direction(racers, direction):
        return [racer for racer in racers if racer.direction == direction]

    @staticmethod
    def _group_unfinished_racers_by_lap(racers, leaderboard):
        racer_dict = {}
        for racer in sorted(racers, key=lambda r: r.stopwatch.elapsed_time()):
            if racer.completed_race:
                leaderboard.append(racer)
            else:
                racer_dict.setdefault(racer.current_lap, []).append(racer)
        return racer_dict

    @staticmethod
    def _group_racers_by_direction(racers):
        from collections import defaultdict
        grouped = defaultdict(list)
        for racer in racers:
            grouped[racer.direction].append(racer)
        return grouped

    @staticmethod
    def _add_sorted_racers(leaderboard, racers, key, reverse=False):
        for racer in sorted(racers, key=key, reverse=reverse):
            leaderboard.append(racer)
