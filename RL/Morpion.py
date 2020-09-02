import numpy as np
import random
import itertools
from MorpionPlayer import MorpionPlayer

class Morpion():

    def __init__(self, p1, p2):
        self.board = np.array([['-']*3]*3)
        self.symbols = {0: '-', 1: 'x', 2:'o'}

        self.available_actions = \
            list(itertools.product(range(0,3), range(0,3)))

        self.p1 = p1
        self.p2 = p2

    def get_combinations(self):
        """
        Compute all combinations in the current tic-tac-toe board. 

        :returns: All combinations
        :rtype: list(str)

        """

        # Line combinations
        combinations = ["".join(row) for row in self.board]

        # Column combinations
        combinations.extend(["".join(row) for row in self.board.transpose()])

        # Diagonal combinations
        combinations.extend(["".join(row) \
                             for row in [self.board.diagonal(),
                                         np.fliplr(self.board).diagonal()]])
        return combinations
        
    def is_finished(self):
        combinations = self.get_combinations()

        if ((np.all(self.board != '-'))
            or ('xxx' in combinations)
            or ('ooo' in combinations)):
            return True
        return False

    def reset(self):
        self.board = np.array([['-']*3]*3)
        self.available_actions = \
            list(itertools.product(range(0,3), range(0,3)))

        return self.board

    def display(self):
        print(self.board)

    def step(self, action, player):

        # Play action
        self.board[action] = self.symbols[player]

        # Hash the new board
        sp = MorpionPlayer.hash_board(self.board)

        # Remove current action from available actions
        self.available_actions.remove(action)
        
        return sp
    def give_reward(self, train=True):
        combinations = self.get_combinations()
        
        if ('xxx' in combinations):
            if (train):
                self.p1.feed_reward(1)
                self.p2.feed_reward(-1)
                
            self.p1.win += 1
            self.p2.lose +=1
        elif ('ooo' in combinations):
            if (train):
                self.p1.feed_reward(-1)
                self.p2.feed_reward(1)

            self.p1.lose += 1
            self.p2.win += 1
        else:
            if (train):
                self.p1.feed_reward(0.1)
                self.p2.feed_reward(0.1)

            self.p1.draw += 1
            self.p2.draw += 1


