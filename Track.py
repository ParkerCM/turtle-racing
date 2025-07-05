import turtle
from Direction import Direction

class Track:

    OUTER_SCALE = 0.4
    INNER_SCALE = 0.2
    TURN_ZONE_SCALE = 0.4
    TURN_LIMIT_SCALE = 0.8

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = turtle.Screen()

        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()

    def setup_track(self):
        # setup the screen size
        self.screen.setup(self.width, self.height)

        # create invisible turtle which moves fast to draw the track
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.pensize(5)

        # draw outer and inner track lines
        self._draw_track(t, self.width * -self.OUTER_SCALE, self.height * -self.OUTER_SCALE)
        self._draw_track(t, self.width * -self.INNER_SCALE, self.height * -self.INNER_SCALE)

        # draw the start / finish line
        self._draw_start_finish(t, self.height)

    def racer_in_turn_zone(self, racer):
        x, y = racer.turtle.xcor(), racer.turtle.ycor()
        dir = racer.direction

        zone_x_min = self.half_width * self.TURN_ZONE_SCALE
        zone_x_max = self.half_width * self.TURN_LIMIT_SCALE
        zone_y_min = self.half_height * self.TURN_ZONE_SCALE
        zone_y_max = self.half_height * self.TURN_LIMIT_SCALE

        return (
            (dir == Direction.RIGHT and zone_x_min < x < zone_x_max and y < 0) or
            (dir == Direction.UP and zone_y_min < y < zone_y_max and x > 0) or
            (dir == Direction.LEFT and -zone_x_max < x < -zone_x_min and y > 0) or
            (dir == Direction.DOWN and -zone_y_max < y < -zone_y_min and x < 0)
        )

    def racer_must_turn(self, racer, max_distance):
        x, y = racer.turtle.xcor(), racer.turtle.ycor()
        dir = racer.direction

        limit_x = self.half_width * self.TURN_LIMIT_SCALE
        limit_y = self.half_height * self.TURN_LIMIT_SCALE

        return (
            (dir == Direction.RIGHT and x + max_distance > limit_x) or
            (dir == Direction.UP and y + max_distance > limit_y) or
            (dir == Direction.LEFT and x - max_distance < -limit_x) or
            (dir == Direction.DOWN and y - max_distance < -limit_y)
        )

    @staticmethod
    def _draw_track(t, width, height):
        t.penup()
        t.goto(width, height)
        t.down()

        for _ in range(2):
            t.forward(width * -2)
            t.left(90)
            t.forward(height * -2)
            t.left(90)

    @staticmethod
    def _draw_start_finish(t, height):
        t.penup()
        t.goto(0, height * -0.2)
        t.pendown()
        t.goto(0, (height * -0.2) * 2)

    @staticmethod
    def racer_crossed_finish(direction, old_xcor, new_xcor):
        return direction == Direction.RIGHT and old_xcor < 0 <= new_xcor

    def _write_message(self, message, x=0, y=0):
        self.writer.goto(x, y)
        self.writer.write(message, align="center", font=("Arial", 24, "normal"))

    def write_results(self, racers, total_time, fastest_racer):
        sorted_racers = sorted(racers, key=lambda racer: racer.stopwatch.elapsed_time())

        self.writer.clear()
        y = self.height * self.INNER_SCALE - 50

        self._write_message("results", 0, y)
        y -= 25

        self._write_message(f"total time: {self._format_time(total_time)}", 0, y)
        y -= 30

        self._write_message("---------------------------", 0, y)
        y -= 30

        for idx, racer in enumerate(sorted_racers):
            self._write_message(f"{idx + 1}. {racer.name} ({self._format_time(racer.stopwatch.elapsed_time())}) {'[fastest lap]' if fastest_racer == racer else ''}", 0, y)
            y -= 25

        self._keep_screen_open()

    def write_leaderboard(self, leaderboard, number_of_laps):
        self.writer.clear()
        y = self.height * self.INNER_SCALE - 50

        self._write_message("leaderboard", 0, y)
        y -= 25

        self._write_message(f"{number_of_laps} lap race", 0, y)
        y -= 25

        self._write_message("---------------------------", 0, y)
        y -= 30

        for idx, racer in enumerate(leaderboard):
            self._write_message(f"{idx + 1}. {racer.name} (lap {self._get_lap_for_leaderboard(racer.current_lap, number_of_laps)}/{number_of_laps}) {f'[finished]' if racer.completed_race else ''}", 0, y)
            y -= 25

    @staticmethod
    def _get_lap_for_leaderboard(current_lap, number_of_laps):
        if current_lap == -1:
            return 1
        elif current_lap == number_of_laps:
            return current_lap
        else:
            return current_lap + 1

    def _keep_screen_open(self):
        self.screen.listen()
        self.screen.onkey(self._close_screen, "Return")
        self.screen.mainloop()

    def _close_screen(self):
        self.screen.bye()

    @staticmethod
    def _format_time(seconds: float) -> str:
        minutes, secs = divmod(seconds, 60)
        return f"{int(minutes)}:{secs:05.2f}"