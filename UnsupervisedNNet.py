# ## a script to create an NNet from self-play

from Connect4 import Connect4
import numpy as np
from NNet import Network
import random

class SelfPlayer():
    SIZES = [42, 64, 64, 7]

    def __init__(self, batch_size, nnet = None):
        if nnet:
            self.nnet = nnet
        else:
            self.nnet = Network(SelfPlayer.SIZES)
        self.batch_size = batch_size
        self.training_data = []
        # self.generate_training_data(batch_size, nnet)

    def get_training_data(self):
        random.shuffle(self.training_data)
        return self.training_data

    def update_model(self):
        self.generate_training_data(self.batch_size)
        self.nnet.SGD(self.get_training_data(), 100, (self.batch_size // 4) + 1, 0.01)

    def generate_training_data(self, batch_size, nnet = None):
        #training_data = []
        if nnet:
            pass
        for iteration in range(batch_size):
            mini_batch = self.run_one_game()
            for elem in mini_batch:
                self.training_data.append(elem)

    def run_one_game(self):
        result = []
        connect4 = Connect4()
        ## run thru a game
        while connect4.result == None: ## maybe dont need ==
            connect4.random_move()
            result.append(self.convert_to_input(connect4))

        ## back propogate
        game_result = connect4.result
        for index in range(len(result)):
            win = game_result if index % 2 else -game_result
            result[index] = (result[index], win)
        return result

    def convert_to_input(self, connect4):
        if connect4.turn == 1:
            return np.array(connect4.board, dtype = np.dtype('int'))
        else:
            return np.array(connect4.board, dtype = np.dtype('int')) * -1
            #return [-elem for elem in connect4.board]

if __name__ == "__main__":
    player = SelfPlayer(2)
    player.update_model()
