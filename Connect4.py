import numpy as np
from time import time
import random
import functools
'''
Board Storage: starting at the bottom left and going up

5 11 17 23 29 35 41
4 10 16 22 28 34 40
3 9  15 21 27 33 39
2 8  14 20 26 32 38
1 7  13 19 25 31 37
0 6  12 18 24 30 36


AI:
dataframe with 42 colums for each tile, make one for team who is moving, -1 for opponent
43rd with outcome, when predicting, make this "win", options are "win", "lose", "tie
44th column for the move (target) as "string"
'''


### Board Class
class Connect4():
    def __init__(self, p_one_color=1, result = None):
        self.turn = p_one_color
        self.board  = [0 for num in range(42)]
        self.result = result
    
    def __str__(self):
        to_print = "\n| "
        for row in range(6):
            for col in range(7):
                r = 5 - row
                to_print += ("X" if self.board[r + col*6] == 1 else (" " if self.board[r + col*6] == 0 else "O")) + " | "
            to_print += "\n|___|___|___|___|___|___|___|\n| "
        to_print += "1   2   3   4   5   6   7 |\n"
        return to_print

    def deepcopy(self):
        copyObject = Connect4(p_one_color = self.turn, result = self.result)
        copyBoard = [element for element in self.board]
        copyObject.board = copyBoard
        return copyObject

    def get_possible_moves(self):
        moves = []
        for col in [0, 1, 2, 3, 4, 5, 6]: ## could slow my code
            if self.board [col*6 + 5] == 0:
                moves.append(col)
        return moves
    
    def make_move(self, col):
        didMove = False
        for row in [0, 1, 2, 3, 4, 5]:
            if self.board [col*6+row] == 0:
                self.board [col*6+row] = self.turn
                didMove = True
                break
        if didMove:
            self.turn = -self.turn
            self.game_over_speedy(col)
        return didMove

    # def make_oppo_move(self, col):
    #     self.turn = -self.turn
    #     for row in range(6):
    #         if self.board [col*6+row] == 0:
    #             self.board [col*6+row] = self.turn
    #             break

    def undo_move(self, col):
        for row in [ 5- r for r in range(6)]:
            if self.board [col*6+row] != 0:
                self.board [col*6+row] = 0
                break
        self.turn = -self.turn

    def random_move(self):
        didMove = False
        while not didMove:
            didMove = self.make_move(random.choice([0, 1, 2, 3, 4, 5, 6]))

    # @staticmethod
    # def heuristic_compare(move1, move2):
    #     return -abs(move2 - 3) + abs(move1 - 3)

    # def weighted_random_move(self):
    #     choices = sorted(self.get_possible_moves(), key=functools.cmp_to_key(Connect4.heuristic_compare))
    #     weights = []
    #     for i in choices:
    #     ## the higher the last value, the closer to random
    #         weights.append(-abs(i - 3)/4 + 3)
    #     rnd = random.random() * sum(weights)
    #     choice = None

    #     for i, w in enumerate(weights):
    #         rnd -= w
    #         if rnd < 0:
    #             choice = choices[i]
    #             break
    #     #return choice
    #     self.make_move(choice)

    # def smart_random_move(self):
    #     choices = self.get_possible_moves()
    #     for choice in choices:
    #         self.make_move(choice)
    #         if self.result == -self.turn:
    #             return
    #         self.undo_move(choice)
    #     self.random_move()

    # def game_over(self): ##slow mo
    #     ### TODO: SPEED UP BY ONLY LOOKING AT LAST PIECE PLACED
    #     ### Horizontal
    #     for row in range(6):
    #         for col in range(4):
    #             if self.board [col*6+row] == 0:
    #                 continue
    #             if self.board [col*6 + row] == self.board [(col+1)*6 + row] and self.board [col*6 + row] == self.board [(col+2)*6 + row] and self.board [col*6 + row] == self.board [(col+3)*6 + row] and self.board [col*6 + row] != 0:
    #                 self.result = self.board [col*6 + row]
    #                 return True
    #     ### Vertical
    #     for col in range(7):
    #         for row in range(3):
    #             if self.board [col*6+row] == 0:
    #                 continue
    #             if self.board [col*6 + row] == self.board [col*6 + row + 1] and self.board [col*6 + row] == self.board [col*6 + row + 2] and self.board [col*6 + row] == self.board [col*6 + row + 3]:
    #                 self.result = self.board [col*6 + row]
    #                 return True
    #     ### Upward Diag
    #     for col in range(4):
    #         for row in range(3):
    #             if self.board [col*6+row] == 0:
    #                 continue
    #             if self.board [col*6 + row] == self.board [(col+1)*6 + row + 1] and self.board [col*6 + row] == self.board [(col+2)*6 + row + 2] and self.board [col*6 + row] == self.board [(col+3)*6 + row + 3] and self.board [col*6 + row] != 0:
    #                 self.result = self.board [col*6 + row]
    #                 return True
    #     ### Down Diag
    #     for col in range(4):
    #         for row in range(3,6):
    #             if self.board [col*6+row] == 0:
    #                 continue
    #             if self.board [col*6 + row] == self.board [(col+1)*6 + row - 1] and self.board [col*6 + row] == self.board [(col+2)*6 + row - 2] and self.board [col*6 + row] == self.board [(col+3)*6 + row - 3] and self.board [col*6 + row] != 0:
    #                 self.result = self.board [col*6 + row]
    #                 return True
    #     if self.is_tie():
    #         self.result = 0
    #         return True
    #     return False

    def is_tie(self):
        return 0 not in self.board 

    def game_over_speedy(self, lastMove):
        lastCol = lastMove
        lastRow = 5
        for row in [0, 1, 2, 3, 4, 5]:
            if self.board[lastCol*6 + row] == 0:
                lastRow = row - 1
                break
        ### Horizontal
        for col in [0, 1, 2, 3]:
            if self.board [col*6 + lastRow] == 0:
                continue
            if abs(self.board[col*6 + lastRow] + self.board [(col+1)*6 + lastRow] + self.board [(col+2)*6 + lastRow] + self.board [(col+3)*6 + lastRow]) == 4:
                self.result = self.board [col*6 + lastRow]
                return True
        ### Vertical
        if lastRow >= 3 and abs(self.board [lastCol*6 + lastRow] + self.board [lastCol*6 + lastRow - 1] + self.board [lastCol*6 + lastRow - 2] + self.board [lastCol*6 + lastRow - 3]) == 4:
            self.result = self.board [lastCol*6 + lastRow]
            return True

        ##Upwards diag alt
        bottomLeftSpace = min(lastCol, lastRow)
        topRightSpace = min(6 - lastCol, 5 - lastRow) - 3
        for i in range(-bottomLeftSpace, topRightSpace + 1):
            if abs(self.board [(lastCol+i)*6 + lastRow+i] + self.board [(lastCol+1+i)*6 + lastRow + 1+i] + self.board [(lastCol+2+i)*6 + lastRow + 2+i] + self.board [(lastCol+3+i)*6 + lastRow + 3+i]) == 4:
                    self.result = self.board [(lastCol+i)*6 + lastRow+i]
                    return True
        ##DownDiag Aalt
        topLeftSpace = min(lastCol, 5 - lastRow)
        bottomRightSpace = min(6 - lastCol, lastRow) - 3
        for i in range(-topLeftSpace, bottomRightSpace + 1):
            if abs(self.board[(lastCol+i)*6 + lastRow-i] + self.board[(lastCol+1+i)*6 + lastRow - 1-i] + self.board[(lastCol+2+i)*6 + lastRow - 2-i] + self.board[(lastCol+3+i)*6 + lastRow - 3-i]) == 4:
                    self.result = self.board [(lastCol+i)*6 + lastRow-i]
                    return True
        
        if lastRow == 5 and self.is_tie():
            self.result = 0
            return True
        return False

if __name__ == "__main__":
    board = Connect4()
    while board.result == None:
        move = int(input())-1
        board.make_move(move)
        print(board)