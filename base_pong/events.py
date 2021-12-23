from base_pong.utility_classes import HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
class Event:
    def is_continuous(self, event):
        if HistoryKeeper.get_last(id(self)) and event:
            return True
        return False

    def run(self, event):
        HistoryKeeper.add(event, id(self), False)

class TimedEvent:
    time_needed = 0
    is_started = False
    restarts_upon_completion = False
    current_time = 0

    def __init__(self, time_needed, restarts_upon_completion):
        self.time_needed = time_needed
        self.restarts_upon_completion = restarts_upon_completion

    def is_done(self):
        is_finished = self.is_started

        if self.current_time < self.time_needed:
            is_finished = False

        if is_finished and self.restarts_upon_completion:
            self.start()
            self.current_time = 0

        return is_finished

    def run(self, reset_event, start_event):
        if reset_event:
            self.reset()

        elif start_event:
            self.start()

        if self.is_started:
            self.current_time += VelocityCalculator.time

    def start(self):
        self.is_started = True

    def reset(self):
        self.is_started = False
        self.current_time = 0
