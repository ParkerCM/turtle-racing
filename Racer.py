import turtle
from Direction import Direction
from Stopwatch import Stopwatch

class Racer:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.current_lap = 0
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color(self.color)
        self.turtle.penup()
        self.completed_race = False
        self.direction = Direction.RIGHT
        self.stopwatch = Stopwatch()
        self.best_lap = 0
        self.total_time = 0

    def __str__(self):
        return f"Name: {self.name}; {self.color}; {self.current_lap}"

    def move_forward(self, distance):
        self.turtle.forward(distance)

    def turn(self):
        match self.direction:
            case Direction.RIGHT:
                self.direction = Direction.UP
            case Direction.UP:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.RIGHT
        self.turtle.left(90)

    def completed_lap(self):
        self.current_lap += 1

        # started behind the finish line and we're crossing it for the first time.
        # this is not a valid lap around the track
        if self.current_lap != 0:
            lap_time = self.stopwatch.lap_time()
            if lap_time < self.best_lap or self.best_lap == 0:
                self.best_lap = lap_time
            print(f"Lap time: {lap_time}")

    def start_timer(self):
        self.stopwatch.start()

    def stop_timer(self):
        self.stopwatch.stop()
        self.total_time = self.stopwatch.elapsed_time()
        print(f"Best lap: {self.best_lap}")
        print(f"Total time: {self.total_time}")