from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from player.models import Player


TOKEN_CHOICES = {"X": "X", "O": "O"}
BLANK = "-"


class Game(models.Model):
    """Class representing a game of tic tac toe"""

    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(Player)
    starting_token = models.CharField(choices=TOKEN_CHOICES, max_length=1)
    board = models.CharField(default=BLANK * 9, max_length=9, blank=True)
    turn = models.IntegerField(default=0, blank=True)
    active = models.BooleanField(default=True, blank=True)

    def is_win_state(self) -> bool:
        """Function to check if board is in a win state,
        it asumes that the previous start was not winning"""
        res = False
        for i in range(0, 3):
            row = self.board[3 * i] == self.board[3 * i + 1] == self.board[3 * i + 2]
            column = self.board[i] == self.board[3 + i] == self.board[6 + i]
            if (row or column) and self.board[4 * i] != BLANK:
                res = True
                break
        if (self.board[0] == self.board[4] == self.board[8]) and self.board[4] != BLANK:
            res = True
        if (self.board[2] == self.board[4] == self.board[6]) and self.board[4] != BLANK:
            res = True
        return res

    def is_full(self) -> int:
        """Check if the board is full"""
        return len([x for x in self.board if x != BLANK]) == 9

    def move(self, token, row, column):
        """Makes a move in the board"""
        if token not in "XO":
            raise Exception
        new_board = list(self.board)
        new_board[3 * row + column] = token
        self.board = "".join(new_board)
