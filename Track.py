import turtle
from Direction import Direction

def draw_track(t, width, height):
    t.penup()
    t.goto(width, height)
    t.down()

    for _ in range(2):
        t.forward(width * -2)
        t.left(90)
        t.forward(height * -2)
        t.left(90)

def draw_start_finish(t, height):
    t.penup()
    t.goto(0, height * -0.2)
    t.pendown()
    t.goto(0, (height * -0.2) * 2)


def racer_crossed_finish(direction, old_xcor, new_xcor):
    return direction == Direction.RIGHT and old_xcor < 0 <= new_xcor

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
        draw_track(t, self.width * -self.OUTER_SCALE, self.height * -self.OUTER_SCALE)
        draw_track(t, self.width * -self.INNER_SCALE, self.height * -self.INNER_SCALE)

        # draw the start / finish line
        draw_start_finish(t, self.height)

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

    def write_message(self, message, x=0, y=0):
        self.writer.goto(x, y)
        self.writer.write(message, align="center", font=("Arial", 24, "normal"))

    def write_results(self, racers, total_time, fastest_racer):
        self.writer.clear()
        y = self.height * self.INNER_SCALE - 50

        self.write_message("Results", 0, y)
        y -= 25

        self.write_message(f"Total time: {total_time:.2f}", 0, y)
        y -= 30

        self.write_message("---------------------------", 0, y)
        y -= 30

        for idx, racer in enumerate(racers):
            self.write_message(f"{idx + 1}. {racer.color} ({racer.stopwatch.elapsed_time():.2f}) {'[fastest lap]' if fastest_racer == racer else ''}", 0 , y)
            y -= 25