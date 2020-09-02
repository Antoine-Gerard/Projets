from random import randint
import random
import numpy as np

class StickGame(object):
    """
    Stickgame.
    """

    def __init__(self, nb):                 
        super(StickGame, self).__init__()
        self.original_nb = nb
        self.nb = nb

    def is_finished(self):
        if self.nb <= 0:
            return True
        return False

    def reset(self):
        self.nb = self.original_nb
        return self.nb

    def display(self):
        print("| " * self.nb)
        
    def step(self, action):
        self.nb -= action
        if self.nb <= 0:
            return None, -1
        else:
            return self.nb, 0

    
class StickPlayer(object):
    def __init__(self,
                 is_human,
                 size,
                 trainable=True):

        super(StickPlayer, self).__init__()
        self.is_human = is_human
        self.history = []
        self.V = {}

        for s in range(1, size+1):
            self.V[s] = 0

        self.win_nb = 0
        self.lose_nb = 0
        self.rewards = []
        self.eps = 0.99
        self.trainable = trainable

    def reset_stat(self):
        self.win_nb = 0
        self.lose_nb = 0
        self.rewards = []

    def greedy_step(self, state):
        actions = [1, 2, 3]
        vmin = None
        vi = None

        for i in range(0,3):
            a = actions[i]
            if state - a > 0 and (vmin is None or vmin > self.V[state-a]):
                vmin = self.V[state - a]
                vi = i
            
        return actions[vi if vi is not None else 1]

    def play(self, state):
        if self.is_human is False:
            if random.uniform(0, 1) < self.eps:
                action = randint(1,3)
            else:
                action = self.greedy_step(state)
        else:
            action = int(input("$>"))

        return action

    def add_transition(self, n_tuple):
        # Add one transition to the history: tuple (s, a , r, s')
        self.history.append(n_tuple)
        s, a, r, sp = n_tuple
        self.rewards.append(r)

    def train(self):
        if not self.trainable or self.is_human is True:
            return

        for transition in reversed(self.history):
            s, a, r, sp = transition

            if r==0:
                self.V[s] = self.V[s] + 0.001 * (self.V[sp] - self.V[s])
            else:
                self.V[s] = self.V[s] + 0.001 * (r - self.V[s])

        self.history = []

def play(game, p1, p2, train=True):
    state = game.reset()
    players = [p1, p2]
    random.shuffle(players)
    p = 0

    while game.is_finished() is False:

        if players[p%2].is_human:
            game.display()

        action = players[p%2].play(state)
        n_state, reward = game.step(action)

        if (reward != 0):
            players[p%2].lose_nb +=1 if reward == -1 else 0
            players[p%2].win_nb +=1 if reward == 1 else 0

            players[(p+1)%2].lose_nb += 1. if reward == 1 else 0
            players[(p+1)%2].win_nb += 1. if reward == -1 else 0
            
        if p!=0:
            s, a, r, sp = players[(p+1)%2].history[-1]
            players[(p+1)%2].history[-1] = (s, a, reward * -1, n_state)

        players[p%2].add_transition((state, action, reward, None))

        state = n_state
        p +=1

    if train:
        p1.train()
        p2.train()

if __name__ == '__main__':
    game = StickGame(12)

    p1 = StickPlayer(is_human=False, size=12, trainable=True)
    p2 = StickPlayer(is_human=False, size=12, trainable=True)

    human = StickPlayer(is_human=True, size=12, trainable=False)
    random_player = StickPlayer(is_human=False, size=12, trainable=False)

    for i in range(0, 10000):
        if i % 10 == 0:
            p1.eps = max(p1.eps*0.996, 0.05)
            p2.eps = max(p2.eps*0.996, 0.05)
        play(game, p1, p2)
    p1.reset_stat()

    for key in p1.V:
        print(key, p1.V[key])
    print("--------------------------")

    for _ in range(0, 1000):
        play(game, p1, random_player, train=False)
    print("p1 win rate", p1.win_nb/(p1.win_nb + p1.lose_nb))
    print("p1 win mean", np.mean(p1.rewards))
    
    while True:
        play(game, p1, human, train=False)
