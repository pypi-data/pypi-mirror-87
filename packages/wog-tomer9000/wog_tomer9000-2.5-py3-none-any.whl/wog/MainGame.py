def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true',
                        help="testing code by starting flask, "
                             "used for another file to test - e2e.py")
    arg = parser.parse_args()
    if arg.test:
        from .MainScores import MainScores

        MainScores().start_option()

    else:
        from .Live import welcome, load_game

        user_name = input("Hi, What is your name? ")
        print(f"{welcome(user_name)}\n")
        load_game()
