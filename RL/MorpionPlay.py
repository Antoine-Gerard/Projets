from Morpion import Morpion
from MorpionPlayer import MorpionPlayer
import random
import itertools

def play(game, p1, p2, train=True):
    board = game.reset()
    players = [p1, p2]

    random.shuffle(players)
    p = 0

    while game.is_finished() is False:
        if players[p%2].is_human:
            game.display()

        action = players[p%2].play(game)
        sp = game.step(action, players[p%2].player)

        players[p%2].add_state(sp)
        p += 1
        
        
        
    game.give_reward(train = train)
    #if (not train):
    #    game.display()

if __name__ == '__main__':
    p1 = MorpionPlayer(is_human = False,
                       player = 1)
    p2 = MorpionPlayer(is_human = False,
                       player = 2)


    game = Morpion(p1 = p1, p2 = p2)
    
    for i in range(50000):
        if i % 1000 == 0:
            p1.eps = max(p1.eps*0.8, 0.05)
            p2.eps = max(p2.eps*0.8, 0.05)
            print("Itération: {}".format(i))
    
        play(game, p1, p2)
    
    p1.reset_stat()
    p2.reset_stat()
    
    random_player = MorpionPlayer(is_human = False, player = 2)
    game = Morpion(p1 = p1, p2 = random_player)
    for _ in range(10000):
        play(game, p1, random_player, train = False)

    print("p1 win rate: {}%".format(100 * p1.win / (p1.win + p1.lose + p1.draw)))
    
    human = MorpionPlayer(is_human = True, player = 2)
    game = Morpion(p1 = p1, p2 = human)
    while True:
        play(game, p1, human, train=False)
