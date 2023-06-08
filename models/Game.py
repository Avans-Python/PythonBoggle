import datetime
from datetime import timedelta
import time
import random
import string
from models.Player import Player
from models.Dice import Dice

class Game:
    def __init__(self, size, timer, username, id):
        self.id = id
        self.player = Player(username)
        self.size = int(size)
        self.timer = timer
        self.score = 0
        self.grid = []
        self.dices = []
        self.words = []
        if self.timer:
            self.start_time = datetime.datetime.now()
            self.end_time = self.start_time + timedelta(minutes=3)

        letters = [
            ["A", "E", "A", "N", "E", "G"],
            ["A", "H", "S", "P", "C", "O"],
            ["A", "S", "P", "F", "F", "K"],
            ["O", "B", "J", "O", "A", "B"],
            ["I", "O", "T", "M", "U", "C"],
            ["R", "Y", "V", "D", "E", "L"],
            ["L", "R", "E", "I", "X", "D"],
            ["E", "I", "U", "N", "E", "S"],
            ["W", "N", "G", "E", "E", "H"],
            ["L", "N", "H", "N", "R", "Z"],
            ["T", "S", "T", "I", "Y", "D"],
            ["O", "W", "T", "O", "A", "T"],
            ["E", "R", "T", "T", "Y", "L"],
            ["T", "O", "E", "S", "S", "I"],
            ["T", "E", "R", "W", "H", "V"],
            ["N", "U", "I", "H", "M", "Q"]
        ]

        for dice_letters in letters:
            self.dices.append(Dice(dice_letters))
            
    def generate_grid(self):
            random.shuffle(self.dices)
            self.grid = [[random.choice(self.dices[i % len(self.dices)].letters) for i in range(self.size)] for _ in range(self.size)]
            return

    def check_word(self, word):
        if self.is_valid_word(word) and self.is_word_on_grid(word) and word not in self.words:
            self.words.append(word)
            self.update_score(str(word))
            return True

        return False

    def is_valid_word(self, word):
        english_words = self.load_word_list('boggle_wordlist.txt')
        dutch_words = self.load_word_list('boggle_wordlist_NL.txt')

        if word in english_words:
            return True
        elif word in dutch_words:
            return True
        else:
            return False

    def load_word_list(self, file_name):
        with open(file_name, 'r') as file:
            word_list = [line.strip() for line in file]

        return word_list

    #set uppercase input words
    def uppercase_input(func):
        def wrapper(self, arg):
            arg = str(arg).upper()
            return func(self, arg)
        return wrapper
    
    @uppercase_input
    def is_word_on_grid(self, word):
        used_positions = set() 
        index = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.search_word(word, row, col, used_positions, index):
                    return True
        return False

    def search_word(self, word, row, col, used_positions, index):
    
        if (
            row < 0 or col < 0 or row >= self.size or col >= self.size or
            (row, col) in used_positions or self.grid[row][col] != word[index]
        ):
            return False

        if index == len(word) - 1:
            return True

        used_positions.add((row, col))
        #range were its looking in at the grid
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:  # Skip the current position
                    continue
                new_row = row + i
                new_col = col + j

                if (
                    new_row < 0 or new_col < 0 or new_row >= self.size or new_col >= self.size
                ):
                    continue

                new_used_positions = set(used_positions)

                if self.search_word(word, new_row, new_col, new_used_positions, index + 1):
                    return True

        used_positions.remove((row, col))
        return False
    
    def is_time_up(self):
        if self.timer and datetime.datetime.now() >= self.end_time:
            return True
        return False
    
    def get_remaining_time(self):
        if self.timer:
            remaining_time = self.end_time - datetime.datetime.now()
            return remaining_time.total_seconds()
        return None

    def update_score(self, word):
        word_length = len(word)
        print(word_length)
        if word_length >= 8:
            self.score += 11
        elif word_length >= 7:
            self.score += 5
        elif word_length >= 6:
            self.score += 3
        elif word_length >= 5:
            self.score += 2
        elif word_length >= 3:
            self.score += 1
        elif word_length < 3:
            self.score += 0