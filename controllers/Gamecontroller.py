from flask import render_template, redirect

from models.Game import Game


class GameController:
    def __init__(self):
        self.game = None

    def new_game(self, size, timer, username):
        self.game = Game(size, timer, username)
    
    def check_word(self, word):
        if self.game:
            if self.game.check_word(word):
                return "valid"
            else:
                return "invalid"
        else:
            return "Game moet nog starten, er bestaat momenteel geen game"
        
    def get_remaining_time(self):
        if self.game:
            remaining_time = self.game.get_remaining_time()
            if remaining_time is not None:
                return round(remaining_time)
        return None

    def end_game(self):
        if self.game:
            self.game.end_game()
            score = self.game.score
            self.game = None
            return score
        else:
            return "Game not started"        







    def show_game(self):
        self.redirectIfNone()
        return render_template('game.html', game=self.Game)

    def redirectIfNone(self):
        if self.Game is None:
            return self.new_game()

    def won_game(self):
        return render_template('game_won.html')
    
    def stats_game(self):
        return render_template('game_stats.html')