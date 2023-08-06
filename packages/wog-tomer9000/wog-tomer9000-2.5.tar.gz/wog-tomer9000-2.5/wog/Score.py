from .Utils import *
import os


class Score(Utils):
    """
    A class that is in charge of managing the scores file.
    """
    def __init__(self, difficulty):
        """
        This runs every time a user calls the class
        and it initializes necessary variables.
        """
        Utils.__init__(self)
        self.difficulty = difficulty
        self.points_of_winning = (self.difficulty * 3) + 5

    def add_score(self):
        """
        The function will try to read the current score in the scores file,
        if it fails it will create a new one and will use it to save the current score.
        """
        if not (os.path.exists(os.path.join(self.path_files, self.scores_file_name))):
            with open(os.path.join(self.path_files, self.scores_file_name), "w+") as scores_file:
                scores_file.write("0")
        with open(os.path.join(self.path_files, self.scores_file_name), "a+") as scores_file:
            scores_file.seek(0)
            sum_score = scores_file.read()
            sum_score = int(sum_score)
            sum_score = sum_score + self.points_of_winning
            scores_file.seek(0)
            scores_file.truncate()
            scores_file.write(str(sum_score))
