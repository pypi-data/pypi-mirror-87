import os
import wog


class Utils:
    """
    A general purpose python file. This file will contain general information
    and operations we need for our game.
    """
    def __init__(self):
        self.scores_file_name = "Scores.txt"
        self.bad_return_code = 1
        self.path_files = os.path.dirname(wog.__file__)

    def screen_cleaner(self):
        # A function to clear the screen.
        os.system('cls' if os.name == 'nt' else 'clear')

    def _needs_number(self, user_input):
        """
        An inturnal use func, it forces the user to enter a number.
        :param user_input: The user input, which will be checked if it is a number.
        :return: returns an integer number.
        """
        while not user_input.isdigit():
            user_input = input("You need to enter a number ")
        return int(user_input)
