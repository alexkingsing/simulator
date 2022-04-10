# THIS WILL HOLD ALL CLASSES
import numpy as np

class Station():

    def __init__(self, stage) -> None:
        self.name = stage
        self.machines = 1
        self.work_in_progress = 0
        self.queue = 0
        self.queue_hist = []

    def add_machine(self):
        self.machines += 1

    def sell_machine(self):
        if self.machines == 1:
            print("You can't sell all machines!")
            pass
        else:
            self.machines -= 1

    def add_work(self):
        self.work_in_progress += 1

    def add_to_queue(self):
        self.queue += 1

    def finish_work(self):
        self.work_in_progress -=1

    def move_from_queue_to_work(self):
        self.queue -= 1
        self.work_in_progress += 1
