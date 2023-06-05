import datetime
from datetime import timedelta
import random
from models.Player import Player
from models.Dice import Dice

class Game:
    def __init__(self, size, timer, username):
        self.player = Player(username)
        self.size = int(size)
        self.timer = timer
        self.score = 0
        self.grid = []
        self.dices = []
        self.words = []
        if self.timer:
            self.start_time = datetime.now()
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
            grid = []
            dice_index = 0

            for i in range(self.size):
                row = []
                for j in range(self.size):
                    dice = self.dices[dice_index]
                    letter = random.choice(dice.letters)
                    row.append(letter)
                    dice_index = (dice_index + 1) % len(self.dices)
                grid.append(row)

            return grid
    
    def check_word(self, word):
        if word in self.words:
            return False
        self.words.append(word)
        if self.is_valid_word(word) and self.is_word_on_grid(word):
            self.score += self.calculate_score(word)
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

    def is_word_on_grid(self, word):
        used_positions = set()
        for row in range(self.size - 1):
            for col in range(self.size - 1):
                if self.search_word(word, row, col, used_positions):
                    return True
        return False

    def search_word(self, word, row, col, used_positions, index=0):
        if index == len(word):
            return True

        if (
            row < 0 or col < 0 or row >= self.size - 1 or col >= self.size - 1 or
            (row, col) in used_positions or self.grid[row][col] != word[index]
        ):
            return False

        used_positions.add((row, col))

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:  # Skip the current position
                    continue
                if self.search_word(word, row + i, col + j, used_positions, index + 1):
                    return True

        used_positions.remove((row, col))
        return False
    
    def is_time_up(self):
        # Implementeer de logica om te controleren of de tijd voorbij is (alleen als timer is ingesteld) hier
        if self.timer and datetime.now() >= self.end_time:
            return True
        return False
    
    def get_remaining_time(self):
        # Implementeer de logica om de resterende tijd terug te geven (alleen als timer is ingesteld) hier
        if self.timer:
            remaining_time = self.end_time - datetime.now()
            return remaining_time.total_seconds()
        return None

    def end_game(self):
        self.player.update_total_score(self.score)
        # Implementeer de logica om het spel te beëindigen en de eindscore weer te geven
        if self.timer:
            if self.is_time_up():
                print("Tijd is op! Eindscore: {}".format(self.score))
            else:
                print("Spel is beëindigd! Eindscore: {}".format(self.score))
        else:
            print("Spel is beëindigd! Eindscore: {}".format(self.score))

    def update_score(self, word):
        word_length = len(word)
        score = word_length * 2  # Scoreberekening (bijvoorbeeld: elke letter is 2 punten waard)
        self.score += score
        self.player.add_word(word, score)

    def update_score(self, word):
        # Implementeer de logica voor het bijwerken van de score van het spel hier
        word_length = len(word)
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