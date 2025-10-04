

class Beaver:
    def __init__(self, x: int = 0, y: int = 0, energy: int = 100):
        self.x: int = x
        self.y: int = y
        self.energy = 100
        self.inventory = {"logs": 0}
        self.sleep_ticks_remaining = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def eat(self):
        if self.inventory["logs"] > 0:
            self.inventory["logs"] -= 1
            self.energy += 10

    def sleep(self, ticks: int):
        self.sleep_ticks_remaining = ticks
