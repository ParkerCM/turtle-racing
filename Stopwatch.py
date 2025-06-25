from time import time

class Stopwatch:
    def __init__(self):
        self.__start_time = time()
        self.__end_time = time()
        self.__lap_time = time()

    def getStartTime(self):
        return self.__start_time

    def getEndTime(self):
        return self.__end_time

    def start(self):
        self.__start_time = time()

    def stop(self):
        self.__end_time = time()

    def elapsedTime(self):
        return self.__end_time - self.__start_time

    def lap_time(self):
        self.__lap_time = time() - self.__lap_time
        return self.__lap_time