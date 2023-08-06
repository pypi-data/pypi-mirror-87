from .GuessGame import GuessGame
from .MemoryGame import MemoryGame
from .CurrencyRouletteGame import CurrencyRouletteGame
from .MainScores import MainScores


def welcome(name):
    # Welcomes the user.
    return f"Hello {name} and welcome to the World of Games (WoG).\n" \
           f"Here you can find many cool games to play."


def load_game():
    # This func loads the option that the user chooses, and it start this option.
    option = input("Please choose one of the following options:\n"
                         "\t1. Memory Game - a sequence of numbers will "
                         "appear for 1 second and you have to guess it back\n"
                         "\t2. Guess Game - guess a number and see "
                         "if you chose like the computer\n"
                         "\t3. Currency Roulette - try and guess the value "
                         "of a random amount of USD in ILS\n"
                         "\t4. Showing result - Running on http://127.0.0.1:5000/ "
                         "accumulation of your winnings ")
    while not (option == "1" or option == "2" or option == "3" or option == "4"):
        option = input("Please choose the game to play, 1,2,3 or 4 ")
    dict_options = {"1": MemoryGame(), "2": GuessGame(), "3": CurrencyRouletteGame(), "4": MainScores()}
    option_chosen = dict_options[option]
    option_chosen.start_option()
