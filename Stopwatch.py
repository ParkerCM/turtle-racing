from time import time

class Stopwatch:
    def __init__(self):
        self.__start_time = time()
        self.__end_time = time()
        self.__lap_start_time = time()

    def start(self):
        self.__start_time = time()

    def stop(self):
        self.__end_time = time()

    def elapsed_time(self):
        return self.__end_time - self.__start_time

    def lap_time(self):
        lap_time = time() - self.__lap_start_time
        self.__lap_start_time = time()
        return lap_time