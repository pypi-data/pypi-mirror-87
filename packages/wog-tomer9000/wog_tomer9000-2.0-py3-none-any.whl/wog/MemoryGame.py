import random
from time import sleep
from .Utils import Utils
from .Game import Game


class MemoryGame(Game):
    """
    This class is a memory game, it generates a random number/s,
    shows it to the user for 0.7 sec and the user needs to enter the right number/s.
    """
    def __init__(self):
        """
        This func runs automatically every time a user calls
        the class and it initializes the necessary variables.
        """
        Game.__init__(self)
        self.list_rand_numbers = []
        self.list_user_numbers = []
        self.rand_num = random.randint(1, 101)
        self.user_input = 0

    def generate_sequence(self):
        # generates a list (length depends on the game difficulty) of numbers.
        for i in range(self.game_difficulty):
            self.list_rand_numbers.append(self.rand_num)
            self.rand_num = random.randint(1, 101)
        self.list_rand_numbers.sort()

    def get_list_from_user(self):
        # The user needs to enter the numbers he just saw.
        print(f"You need to insert the {self.game_difficulty} numbers that just disappeared ")
        for i in range(self.game_difficulty):
            user_input = input(f"Please insert one of the numbers that you saw ")
            user_input = Utils()._needs_number(user_input)
            self.list_user_numbers.append(user_input)
        self.list_user_numbers.sort()

    def is_list_equal(self):
        # Check if the user is correct and it returns accordingly.
        temp_list = []
        for num in self.list_rand_numbers:
            temp_list.append(num)
        for num in self.list_user_numbers:
            if num in temp_list:
                temp_list.remove(num)
        return len(temp_list) == 0

    def play(self):
        """
        When a user wants to play this game, he needs to call this func
        and it runs the relevant methods in the correct order.
        :return: True/False whether the user wins/loses.
        """
        self.generate_sequence()
        print(self.list_rand_numbers)
        sleep(0.7)
        Utils().screen_cleaner()
        self.get_list_from_user()
        print(f"The computer's numbers are - {self.list_rand_numbers}")
        print(f"Your numbers that you entered are - {self.list_user_numbers}")
        self.winning_status = self.is_list_equal()
