"""
CSSE1001 Assignment 3
Semester 1, 2017
"""
import random as random
import tkinter as tk
from tkinter import messagebox
import model
import view
from highscores import HighScoreManager
from game_regular import RegularGame

# # For alternative game modes
from game_make13 import Make13Game
from game_lucky7 import Lucky7Game
from game_unlimited import UnlimitedGame
from base import BaseLoloApp

__author__ = "Joshua Zhou"
__email__ = "joshua.zhou@uq.net.au"

__version__ = "1.0.2"


class LoloApp(BaseLoloApp):
    """Creates the GUI and other functions for the game. Inherits from
    BaseLoloApp."""

    def __init__(self, master, game):
        """Initialises the GUI and other functions"""
        self._on = False
        self._turns = 0
        self._master = master
        self._game = game
        LoloLogo(master)
        self._gamename = StatusBar(master, game)
        self._gamename.set_game()
        self._lightning = 1
        self.menu()
        self.events()
        self.lightning_btn()
        super().__init__(self._master, self._game)
        name = "{} {} {}".format("Lolo :: ", game.GAME_NAME, "Game")
        master.title(name)
        master.minsize(500, 500)
        master.config(bg="grey")
        master.bind("<Button-1>", self.score(game.get_score()))

    def activate(self, position):
        """Overides the activate method from BaseLoloApp and adds extra
        functionality such as the lightning function and error checking."""
        if self._on == True and self._lightning > 0:
            BaseLoloApp.remove(self, position)
            self._lightning -= 1
            self.lightning_off()
        else:
            try:
                super().activate(position)
                self._turns += 1
                if self._turns == 20:
                    self._lightning += 1
                    self._turns = 0
                    self.lightning_config()
            except IndexError:
                messagebox.showwarning("Error", "You cannot activate this tile.")

    def menu(self):  # High scores button and game mode button does not work.
        """Initialises the filemenu"""
        self._menu = tk.Menu(self._master)
        self._master.config(menu=self._menu)
        self._subMenu = tk.Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label="File", menu=self._subMenu)
        self._subMenu.add_command(label="New Game (ctrl+n)", command=self.reset)
        self._subMenu.add_command(label="High Scores")
        self._subMenu.add_command(label="Switch game mode")
        self._subMenu.add_command(label="Exit", command=self.exit)

    def game_over(self):
        """Game over messagebox."""
        tk.messagebox.showinfo(
            "Game over!",
            "Game over! You cannot activate "
            "anymore tiles (unless you use lightning).",
        )

    def score(self, score):
        """Calls a function to update the score.

        Parameters:
            score: The score that is being updated
        """
        self._score = score
        return self._gamename.set_score(score)

    def reset(self, event=None):
        """resets the game.

        Parameters:
            event: Used to ignored events caused by keyboard shortcuts.
        """
        self._game.reset()
        self._lightning = 1
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.lightning_config()

    def exit(self):
        """exits the game"""
        self._master.destroy()

    def lightning_btn(self):
        """Creates the lightning button."""
        lightning = "{} {} {}".format("Lightning(", self._lightning, ")")
        self._lightning_btn = tk.Button(
            self._master, text=lightning, command=self.lightning_on
        )
        self._lightning_btn.pack(side=tk.BOTTOM, pady=10)

    def lightning_on(self, event=None):
        """Toggles the lightning button on

        Parameters:
            event: Used to ignored events caused by keyboard shortcuts.
        """
        if self._lightning > 0:
            self._lightning_btn.config(text="***Striking***")
            self._on = True
        else:
            self.lightning_off()

    def lightning_off(self):
        """Toggles the lightning button off and disables it
        if there is no lightning.
        """
        lightning = "{} {} {}".format("Lightning(", self._lightning, ")")
        self._lightning_btn.config(text=lightning)
        self._on = False
        if self._lightning < 1:
            self._lightning_btn.config(state=tk.DISABLED)

    def lightning_config(self):
        """Updates the lightning label and makes it's state active."""
        lightning = "{} {} {}".format("Lightning(", self._lightning, ")")
        self._lightning_btn.config(text=lightning, state=tk.ACTIVE)

    def events(self):
        """Binds keyboard shortcuts."""
        self._master.bind("<Control-n>", self.reset)
        self._master.bind("<Control-l>", self.lightning_on)


class StatusBar(tk.Frame):
    """Inherits from tk.Frame and sets up the framework for the statusbar"""

    def __init__(self, master, game):
        """Creates the necessary variables and creates the label for the score.

        Parameters:
            master: The parent wedgit.
            game: The game that is going to be played.
        """
        super().__init__(master)
        self._master = master
        self._game = game
        self.frame = tk.Frame(master, bg="grey")
        self.frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        score = "{} {}".format("Score: ", self._game.get_default_score())
        self._score = tk.Label(self._master, text=score, bg="grey")
        self._score.pack(in_=self.frame, side=tk.RIGHT)

    def set_game(self):
        """Generates the label for the game mode"""
        name = "{} {}".format(self._game.GAME_NAME, "Mode")
        self._gamename = tk.Label(self._master, text=name, bg="grey")
        self._gamename.pack(in_=self.frame, side=tk.LEFT)

    def set_score(self, score):
        """Updates the current score when called

        Parameters:
            score: The score that is being updated.
        """
        score = "{} {}".format("Score: ", score)
        self._score.config(text=score)


class LoloLogo(tk.Canvas):
    """Inherits from tk.Canvas to help create the logo."""

    def __init__(self, master):
        """Creates the logo using tkinter shapes

        Parameters:
            master: parent wedgit.
        """
        super().__init__(master)
        logo = tk.Canvas(master, width=425, height=200, bg="grey", highlightthickness=0)
        logo.pack(side=tk.TOP)
        logo.create_rectangle(25, 200, 0, 50, fill="purple", outline="")
        logo.create_rectangle(75, 200, 25, 175, fill="purple", outline="")
        logo.create_oval(100, 100, 200, 200, fill="purple", outline="")
        logo.create_oval(125, 125, 175, 175, fill="grey", outline="")
        logo.create_rectangle(250, 200, 225, 50, fill="purple", outline="")
        logo.create_rectangle(300, 200, 250, 175, fill="purple", outline="")
        logo.create_oval(425, 100, 325, 200, fill="purple", outline="")
        logo.create_oval(400, 125, 350, 175, fill="grey", outline="")


class AutoPlayingGame(BaseLoloApp):  # Sometimes causes the "AttributeError".
    """Will create a game that plays it self automatically. Inherits from
    BaseLoloApp."""

    def __init__(self, master, game):
        """Initialises events and functions.

        Parameters:
            master: parent wedgit.
            game: the game that is being played.
        """
        super().__init__(master)
        self._master = master
        self._game = game
        self._move_delay = 2000
        self.bind_events()
        self.resolve()
        self.move()

    def bind_events(self):
        """Binds relevant events."""
        self._game.on("resolve", self.resolve)

    def resolve(self, delay=None):
        """Makes a move after a given movement delay."""
        if delay is None:
            delay = self._move_delay

        self._master.after(delay, self.move)

    def move(self):
        """Finds a connected tile randomly and activates it."""
        connections = list(self._game.find_groups())

        if connections:
            self._cells = list()

            for connection in connections:
                for cell in connection:
                    self._cells.append(cell)

            self.delay()
        else:
            self._game_over = True
            self._reset()

    def delay(self):
        """Adds a delay to the activation of a tile."""
        self.activate(random.choice(self._cells))

    def _reset(self):
        """resets the game."""
        self._game.reset()
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self.resolve()
        self.move()


class LoadingScreen(object):
    """Creates the loading screen for LoloApp."""

    def __init__(self, master, game):
        """Initialises the loading screen.

        Parameters:
            master: the parent wedgit.
            game: the game that is going to be played (defaults to regular).
        """
        self._game_mode = tk.IntVar()
        self._name = None
        self._master = master
        self._game = game
        self._new_game = game
        self.name_logo(master)
        self.auto_game_mod(master)
        self.buttons(master)
        master.minsize(1200, 750)
        master.title("LoloApp")
        master.config(bg="grey", bd=0)

    def buttons(self, master):
        """Generates each of the buttons for the loading screen.

        Parameters:
            master: parent wedgit.
        """
        frame = tk.Frame(master, bg="grey")
        frame.pack(side=tk.LEFT)
        play_game = tk.Button(frame, text="Play Game", command=self.start_game)
        play_game.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=100, ipadx=200)
        game_mode = tk.Button(frame, text="Game Mode", command=self.game_mode)
        game_mode.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=100, ipadx=196)
        high_score = tk.Button(
            frame, text="High Scores", command=self.high_score_window
        )
        high_score.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=100, ipadx=197)
        exit_game = tk.Button(frame, text="Exit Game", command=self.exit_game)
        exit_game.pack(side=tk.TOP, anchor=tk.W, pady=50, padx=100, ipadx=202)

    def name_logo(self, master):
        """Creates the logo and the entry field for name entry.

        Parameters:
            master: parent wedgit.
        """
        frame = tk.Frame(master, bg="grey")
        frame.pack(side=tk.TOP, fill=tk.BOTH)
        LoloLogo(frame)
        lbl_name = tk.Label(frame, text="Enter your name:", bg="grey", bd=10)
        lbl_name.pack(side=tk.TOP, pady=10)
        self._entry = tk.Entry(frame, width=50)
        self._entry.pack(side=tk.TOP)

    def auto_game_mod(self, master):
        """Autoplaying game.

        Parameters:
            master: parent wedgit.
        """
        frame = tk.Frame(master, bg="grey")
        frame.pack(side=tk.RIGHT, padx=50, pady=50)
        auto_game = AutoPlayingGame(frame, self._game)

    def user_name(self):
        """Returns the name input from the entry box."""
        self._name = self._entry.get()
        return self._name

    @staticmethod
    def high_score_window():
        """Creates the high score window and displays the top 10 players."""
        window = tk.Toplevel()
        window.minsize(500, 500)
        highscore = HighScore(window)

    def start_game(self):
        """Starts the selected game and checks to see if
        a name has been given."""
        self.user_name()
        if self._name == None or len(self._name) == 0:
            tk.messagebox.showinfo(
                "Please enter your name!", "A name is " "required to play."
            )
        else:
            window = tk.Toplevel()
            name = "{} {} {}".format("Lolo :: ", self._game.GAME_NAME, "Game")
            window.title(name)
            game = self._game.__class__
            new_game = game()
            LoloApp(window, new_game)

    def exit_game(self):
        """Exits the game window."""
        self._master.destroy()

    def game_mode(self):
        """GUI for radio buttons to change game mode."""
        window = tk.Toplevel()
        frame = tk.Frame(window)
        frame.pack(side=tk.BOTTOM)
        tk.Radiobutton(
            window,
            text="Regular Mode",
            variable=self._game_mode,
            value=1,
            command=self.change_game_mode,
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            window,
            text="Make 13 Mode",
            variable=self._game_mode,
            value=2,
            command=self.change_game_mode,
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            window,
            text="Lucky 7 Mode",
            variable=self._game_mode,
            value=3,
            command=self.change_game_mode,
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            window,
            text="Unlimited Mode",
            variable=self._game_mode,
            value=4,
            command=self.change_game_mode,
        ).pack(anchor=tk.W)
        confirm = tk.Button(frame, text="Ok", command=window.destroy, width=20)
        confirm.pack(side=tk.BOTTOM)

    def change_game_mode(self):
        """Changes the game mode bsed on user input."""
        if self._game_mode.get() == 1:
            self._game = RegularGame()
            return self._game
        elif self._game_mode.get() == 2:
            self._game = Make13Game()
            return self._game
        elif self._game_mode.get() == 3:
            self._game = Lucky7Game()
            return self._game
        elif self._game_mode.get() == 4:
            self._game = UnlimitedGame()
            return self._game


class HighScore(BaseLoloApp):
    """Class for the High Score."""

    def __init__(self, master):
        """Initialises the window and functions.

        Parameters:
            master: parent wedgit.
        """
        window = tk.Frame(master)
        window.pack(side=tk.TOP)
        self.high_scores()
        top_title = tk.Frame(window)
        top_title.pack(side=tk.TOP)
        top_scorer_name = "Best Player: {} with {} points!".format(
            self._name[0], self._score[0]
        )
        top_scorer = tk.Label(top_title, text=top_scorer_name)
        top_scorer.pack(side=tk.TOP)
        super().__init__(window, RegularGame.deserialize(self.get_grid()[0]))
        title_frame = tk.Frame(window)
        title_frame.pack(side=tk.TOP)
        title = tk.Label(title_frame, text="Leaderboards")
        title.pack(fill=tk.BOTH)
        name_frame = tk.Frame(window)
        name_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        score_frame = tk.Frame(window)
        score_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        master.title("High Scores")
        try:  # ¯\_(ツ)_/¯
            name1 = tk.Label(name_frame, text=self._name[0])
            name1.pack(side=tk.TOP)
            score1 = tk.Label(score_frame, text=self._score[0])
            score1.pack(side=tk.TOP)
            name2 = tk.Label(name_frame, text=self._name[1])
            name2.pack(side=tk.TOP)
            score2 = tk.Label(score_frame, text=self._score[1])
            score2.pack(side=tk.TOP)
            name3 = tk.Label(name_frame, text=self._name[2])
            name3.pack(side=tk.TOP)
            score3 = tk.Label(score_frame, text=self._score[2])
            score3.pack(side=tk.TOP)
            name4 = tk.Label(name_frame, text=self._name[3])
            name4.pack(side=tk.TOP)
            score4 = tk.Label(score_frame, text=self._score[3])
            score4.pack(side=tk.TOP)
            name5 = tk.Label(name_frame, text=self._name[4])
            name5.pack(side=tk.TOP)
            score5 = tk.Label(score_frame, text=self._score[4])
            score5.pack(side=tk.TOP)
            name6 = tk.Label(name_frame, text=self._name[5])
            name6.pack(side=tk.TOP)
            score6 = tk.Label(score_frame, text=self._score[5])
            score6.pack(side=tk.TOP)
            name7 = tk.Label(name_frame, text=self._name[6])
            name7.pack(side=tk.TOP)
            score7 = tk.Label(score_frame, text=self._score[6])
            score7.pack(side=tk.TOP)
            name8 = tk.Label(name_frame, text=self._name[7])
            name8.pack(side=tk.TOP)
            score8 = tk.Label(score_frame, text=self._score[7])
            score8.pack(side=tk.TOP)
            name9 = tk.Label(name_frame, text=self._name[8])
            name9.pack(side=tk.TOP)
            score9 = tk.Label(score_frame, text=self._score[8])
            score9.pack(side=tk.TOP)
            name10 = tk.Label(name_frame, text=self._name[9])
            name10.pack(side=tk.TOP)
            score10 = tk.Label(score_frame, text=self._score[9])
            score10.pack(side=tk.TOP)
        except IndexError:
            pass

    def high_scores(self):  # Does not work for other game modes (only regular)
        """Reads a file containing the high scores."""
        self._highscore = HighScoreManager()
        self._highscore.__init__()
        count = self._highscore.__len__()
        self._name = []
        self._score = []
        self._grid = []
        i = 0
        while count > 0:
            highest = self._highscore.get_sorted_data()[i]
            name_list = highest["name"]
            score_list = highest["score"]
            grid_list = highest["grid"]
            self._name.append(name_list)
            self._score.append(score_list)
            self._grid.append(grid_list)
            count -= 1
            i += 1

    def get_grid(self):
        """Returns the grid to be deserialised."""
        return self._grid


def main():
    game = RegularGame()
    # game = Make13Game()
    # game = Lucky7Game()
    # game = UnlimitedGame()

    root = tk.Tk()
    # app = LoloApp(root, game)
    # app = AutoPlayingGame(root, game)
    app = LoadingScreen(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()

# Objective Game Mode not implemented.
