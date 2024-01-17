from django.db import models
from player.models import Player


class Game(models.Model):
    player_x = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_o = models.ForeignKey(Player, on_delete=models.CASCADE)
    board = models.CharField(default=" " * 9, max_length=9)

    def is_win_state(self) -> bool:
        res = False
        for i in range(0, 3):
            row = self.board[3 * i] == self.board[3 * i + 1] == self.board[3 * i + 2]
            column = self.board[i] == self.board[3 + i] == self.board[6 + i]
            if (row or column) and self.board[4 * i] != " ":
                res = True
                break
        if (self.board[0] == self.board[4] == self.board[8]) and self.board[0] != " ":
            res = True
        if (self.board[2] == self.board[4] == self.board[6]) and self.board[0] != " ":
            res = True
        return res

    def is_full(self) -> int:
        return len([x for x in self.board if x != " "]) == 9

    def move(self, token, row, column):
        if token not in "XO":
            raise Exception
        new_board = list(self.board)
        new_board[3 * column + row] = token
        self.board = "".join(new_board)
