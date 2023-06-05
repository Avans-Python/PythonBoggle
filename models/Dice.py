import random

class Dice:
    def __init__(self, letters):
        self.letters = letters

    def roll(self):
        return random.choice(self.letters)
