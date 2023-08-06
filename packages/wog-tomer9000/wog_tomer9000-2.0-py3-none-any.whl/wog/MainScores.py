import os
from flask import Flask, render_template
from .Utils import Utils


class MainScores(Utils):
    """
    serve the user’s score currently in the scores.txt file over HTTP with HTML.
    """
    def __init__(self):
        """
        This runs every time a user calls the class
        and it initializes necessary variables.
        """
        Utils.__init__(self)
        self.app = Flask(__name__, template_folder=self.path_files)
        try:
            with open(os.path.join(self.path_files, self.scores_file_name), "r") as scores_file:
                scores_file.seek(0)
                self.score_from_file = scores_file.read()
            self.bad_return_code = 0
        except FileNotFoundError:
            self.bad_return_code = 1

    def start_option(self):
        """
        This function will serve the score. It will read the score
        from the scores file and will return an HTML.
        """
        if self.bad_return_code == 0:
            @self.app.route("/")
            def score_server():
                return render_template("scores_html.html", SCORE=self.score_from_file)
            self.app.run(port=1000)

        else:
            @self.app.route("/")
            def score_server():
                return render_template("error_html.html", ERROR="PROBLEM showing the result")
            self.app.run(port=1000)
