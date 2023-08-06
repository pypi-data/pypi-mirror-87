import random
from .Utils import Utils
from .Game import Game


class GuessGame(Game):
    """
    This game generates a number which the user needs to guess,
    butween 1 to the difficult of the game.
    """
    def __init__(self):
        """
        This func runs automatically every time a user calls
        the class and it initializes the necessary variables.
        """
        Game.__init__(self)
        self.user_guess = 0

    def generate_number(self):
        # Generates a number that the user needs to guess.
        self.secret_number = random.randint(1, self.game_difficulty)

    def get_guess_from_user(self):
        # User guess the generated number.
        while self.user_guess < 1 or self.user_guess > self.game_difficulty:
            self.user_guess = input(f"Guess a number between 1 and {self.game_difficulty} ")
            self.user_guess = Utils()._needs_number(self.user_guess)

    def compare_results(self):
        """
        Check if the user guessed correcrly.
        :return: True/False depends if the user corrects.
        """
        return self.secret_number == self.user_guess

    def play(self):
        """
        When a user wants to play this game, he needs to call this func
        and it runs the relevant methods in the correct order.
        :return: True/False whether the user wins/loses.
        """
        self.generate_number()
        self.get_guess_from_user()
        print(f"The generated number is - {self.secret_number}")
        print(f"Your guess is - {self.user_guess}")
        self.winning_status = self.compare_results()
