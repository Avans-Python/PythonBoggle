from models.Game import Game


class GameController:
    def __init__(self):
        self.game = None

    def new_game(self, size, timer, username, id):
        self.game = Game(size, timer, username, id)
        self.game.generate_grid()

    def check_word(self, word):
        if self.game:
            if self.game.check_word(word):
                return True
            else:
                return False
        else:
            return "Game has not started. There is currently no game."

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
        
    
    def check_game_over(self):
        if self.game:
            return self.game.is_time_up()
        return False
    
