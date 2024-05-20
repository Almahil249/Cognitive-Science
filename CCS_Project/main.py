import CCS_tetris as game
import Genetic_Algorithm as GG
import random
import sys
import numpy as np
import re
import os
import time

# Specify the path to the directory containing the module
module_path = ''
sys.path.append(module_path)

# Now you can import the module
import matplotlib.pyplot as plt
random.seed() 


def train(pop_size=10, iteration=301, mutat_rate=0.3, crossover_rate=0.7, speed=60000000000, max_score=100000):
    """
    Trains a genetic algorithm model.

    Args:
        pop_size (int): The population size.
        iteration (int): The number of iterations to run the genetic algorithm.
        mutat_rate (float): The mutation rate.
        crossover_rate (float): The crossover rate.
        speed (int): The speed parameter for the game.
        max_score (int): The maximum score threshold.

    Returns:
        None
    """
    output_file = 'training_output.txt'
    best_weights_file = 'best_weights_file.txt'
    POP_SIZE = pop_size
    G = GG.GA(POP_SIZE)
    currunt_score = 0
    with open(best_weights_file, 'a') as bf:
        with open(output_file, 'w') as f:
            for i in range(1, iteration):
                best_gen_score = 0
                snd_best_gen_score = 0
                currunt_score = 0
                selected_chromo = []
                selected_chromo_index = []
                best_weight = []
                snd_best_weight = []
                next_gen = []
                weight_idnex = 0
                for chromo in G.population:
                    game_score = game.main(chromo, speed, max_score, i, weight_idnex)
                    next_gen.append(G.fittens(chromo, game_score))
                    currunt_score += game_score
                    if best_gen_score < game_score:
                        best_gen_score = game_score
                        best_weight = chromo
                    elif snd_best_gen_score < game_score:
                        snd_best_gen_score = game_score
                        snd_best_weight = chromo
                    weight_idnex += 1
                avg_score = currunt_score // len(G.population)
                selected_chromo, selected_chromo_index = G.roulette_selection(next_gen)
                G.selection(selected_chromo, mutat_rate, crossover_rate)
                f.write(f'=== Gen {i} Best Solution ===\n')
                f.write(f'Game played {weight_idnex}\n')
                f.write(f'avg gen Score: {avg_score}\n')
                f.write(f'first best gen Score: {best_gen_score}\n')
                f.write(f'first best gen Weight: {best_weight}\n')
                f.write(f'Second best gen Score: {snd_best_gen_score}\n')
                f.write(f'Second best gen Weight: {snd_best_weight}\n')
                f.write('----------------------------------------------------------------------------\n')

                print(f'=== Gen {i} Best Solution ===')
                print(f'Game played {weight_idnex}')
                print(f'avg gen Score: {avg_score}')
                print(f'first best gen Score: {best_gen_score}')
                print(f'first best gen Weight: {best_weight}')
                print(f'Second best gen Score: {snd_best_gen_score}')
                print(f'Second best gen Weight: {snd_best_weight}')
                print('----------------------------------------------------------------------------')

                if best_gen_score > max_score:
                    bf.write(f'=== Gen {i} Best Solution ===\n')
                    bf.write(f'avg gen Score: {avg_score}\n')
                    bf.write(f'Score: {best_gen_score}\n')
                    bf.write(f'Best Weight: {best_weight}\n')
                    break

def test(speed=6000, num_tries=600, max_score=100000):
    """
    Run a test of the game with the specified parameters.

    Args:
        speed (int, optional): The speed of the game. Defaults to 6000.
        num_tries (int, optional): The number of tries to run the game. Defaults to 600.
        max_score (int, optional): The maximum score to aim for. Defaults to 100000.
    """
    best_weight = [-0.02419719, 0.01720026, -0.377108, -0.19824389, 0.72086437, 0.39539414, 0.67665313]
    for i in range(num_tries):
        game.main(best_weight, speed, max_score, True)
def test(speed=6000,num_tries=600, max_score=100000):
    best_weight =  [-0.02419719 , 0.01720026 , -0.377108 , -0.19824389 , 0.72086437 , 0.39539414, 0.67665313]
    for i in range(num_tries):
        game.main(best_weight, speed, max_score ,True)

import re
import numpy as np

def read():
    """
    Reads the contents of the 'training_output.txt' file and extracts the first scores.

    Returns:
    - first_scores: A numpy array containing the extracted first scores.
    """
    file = open('training_output.txt', 'r')
    lines = file.readlines()
    first_scores = []

    for line in lines:
        if line.__contains__('Best Weight:'):
            score = re.findall('[0-9].*', line)[0]
            first_scores.append(score)
    first_scores = np.array(first_scores, dtype=int)

    return first_scores

#calculate running time
start_time = time.time()
#test()
train()
runtime = time.time() - start_time
print(f'Runtime: {runtime} seconds')

#print run time in the training_output.txt and best_weights_file.txt
with open('training_output.txt', 'a') as f:
    f.write('\n############################################\n')
    f.write(f'          Runtime: {runtime} seconds\n')
with open('best_weights_file.txt', 'a') as f:
    f.write('\n############################################\n')
    f.write(f'          Runtime: {runtime} seconds\n')