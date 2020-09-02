import itertools
import random

class MorpionPlayer():
    def __init__(self,
                 is_human,
                 player,
                 trainable = True):

        self.is_human = is_human
        self.player = player
        
        self.history = []
        self.V = {}

        #for s in itertools.product(range(0,3), range(0,3)):
        #    V[s] = 0

        self.win = 0
        self.lose = 0
        self.draw = 0
        
        self.eps = 0.99
        self.greedy_move = 0
        self.move = 0
        self.trainable = trainable

    def reset_stat(self):
        self.win = 0
        self.lose = 0
        self.draw = 0
        self.move = 0
        self.greedy_move = 0
        
    @staticmethod
    def hash_board(board):
        symbol_to_val = {'-': 0, 'x':1, 'o':2}
        
        hash_board = itertools.chain(*list(board))
        hash_board = list(map(lambda s: symbol_to_val[s], hash_board))

        return sum([x * 3**i for i, x in enumerate(hash_board)])

    def greedy_step(self, game):
        available_actions = game.available_actions
        vmax = -1000
        
        for action in available_actions:
            next_board = game.board.copy()
            next_board[action] = game.symbols[self.player]
            next_board_hash = self.hash_board(next_board)
                        
            
            value = 0 if self.V.get(next_board_hash) is None \
                else self.V.get(next_board_hash)
            
            if (value > vmax):
                vmax = value
                v_action = action

        return v_action
                

    def play(self, game):
        available_actions = game.available_actions
        if self.is_human is False:
            if random.uniform(0, 1) < self.eps:
                action = random.choice(available_actions)
                self.move += 1
            else:
                action = self.greedy_step(game)
                self.greedy_move += 1
        else:
            row = int(input("Ligne: "))
            col = int(input("Colonne: "))

            action = (row, col)

        return action

    def add_state(self, sp):
        self.history.append(sp)

    def feed_reward(self, reward):
        if not self.trainable or self.is_human is True:
            return

        for transition in reversed(self.history):
            sp = transition

            if self.V.get(sp) is None:
                self.V[sp] = 0

            self.V[sp] = self.V[sp] + 0.2 * (reward - self.V[sp])
            reward = self.V[sp]
            

        self.history = []

    
