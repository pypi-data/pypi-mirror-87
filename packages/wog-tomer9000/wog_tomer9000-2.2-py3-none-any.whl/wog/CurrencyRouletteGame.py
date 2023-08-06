import requests
import random
from inputimeout import inputimeout, TimeoutOccurred
from .Game import Game


class CurrencyRouletteGame(Game):
    """
    This class returns True if the user replies correctly on the value
    (generated between 1-100) from USD to ILS, else it returns False.
    """
    def __init__(self):
        """
        This func runs automatically every time a user calls
        the class and it initializes the necessary variables.
        """
        Game.__init__(self)
        exchage_rate_site = requests.get("https://api.exchangeratesapi.io"
                                         "/latest?base=USD&symbols=ILS")
        self.currency_exchange_rate = exchage_rate_site.json()["rates"]["ILS"]
        self.generated_number = random.randint(1, 100)
        self.final_value = self.generated_number * self.currency_exchange_rate
        self.final_value = round(self.final_value, 2)

    def get_money_interval(self):
        # Calculates the interval min and max value.
        self.min_value = self.final_value - (5 - self.game_difficulty)
        self.max_value = self.final_value + (5 - self.game_difficulty)

    def get_guess_from_user(self):
        """
        Gives the user a time to guess the answer
        and save the answer to a var self.user_input.
        """
        try:
            self.user_input = inputimeout(prompt=f"You have 5 seconds to answer, "
                                          f"what is the value of {self.generated_number} "
                                          f"in ILS? ", timeout=5)
        except TimeoutOccurred:
            self.user_input = "No"
        if self.user_input.isdigit() or self.user_input.replace(".", "", 1).isdigit():
            self.user_input = float(self.user_input)
        elif self.user_input == "No":
            pass
        else:
            self.user_input = 0

    def play(self):
        """
        When a user wants to play this game, he needs to call this func
        and it runs the relevant methods in the correct order.
        :return: True/False whether the user wins/loses.
        """
        self.get_money_interval()
        self.get_guess_from_user()
        if self.user_input == "No":
            print("It's been 5 seconds, sorry.")
            return False
        elif self.user_input == 0:
            print("You needed to enter a number")
            return False
        print(f"The correct value is {self.final_value}₪, "
              f"you needed to enter a number between {self.min_value} and {self.max_value}")
        self.winning_status = ((self.user_input > self.min_value) and (self.user_input < self.max_value))
