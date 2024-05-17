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


# score = 0
# best_weight = []
# [-0.27521385 -0.19055338 -0.54777522 -0.16039307 -0.38306999  0.35059687] -> score = 21,040
def train(pop_size=10,iteration = 301,mutat_rate=0.3,crossover_rate=0.7, speed=60000000000, max_score=100000):
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
                    #for i2 in range(num_selected):
                    #   cromo,index = G.roluate_selection(G.popultion)
                    #  selected_chromo_index.append(index)
                    # selected_chromo.append(cromo)
                    #G.op(selected_chromo)
                    #non_score_pop = []*
                    #for non in G.popultion:
                    #  non_score_pop.append(non[0])
                    for chromo in G.popultion:
                        game_score = game.main(chromo, speed, max_score ,i,weight_idnex)
                        next_gen.append(G.fittens(chromo, game_score))
                        currunt_score+=game_score
                        if(best_gen_score < game_score):
                            best_gen_score = game_score
                            best_weight = chromo
                        elif(snd_best_gen_score < game_score):
                            snd_best_gen_score = game_score
                            snd_best_weight = chromo
                        weight_idnex += 1
                    avg_score = currunt_score//len(G.popultion)
                    #G.print_pop()
                    selected_chromo,selected_chromo_index = G.roluate_selection(next_gen)
                    #print(f'chromo selcted len{selected_chromo}')
                    G.selection(selected_chromo,mutat_rate,crossover_rate)
                    f.write(f'=== Gen {i} Best Solution ===\n')
                    f.write(f'Game palyed {weight_idnex}\n')
                    f.write(f'avg gen Score: {avg_score}\n')
                    f.write(f'first best gen Score: {best_gen_score}\n')
                    f.write(f'first best gen Weight: {best_weight}\n')
                    f.write(f'Sencond best gen Score: {snd_best_gen_score}\n')
                    f.write(f'Sencond best gen Weight: {snd_best_weight}\n')
                    f.write('----------------------------------------------------------------------------\n')
                    
                    print(f'=== Gen {i} Best Solution ===')
                    print(f'Game palyed {weight_idnex}')
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
    plt.plot(i)
def test(speed=6000,num_tries=600, max_score=100000):
    best_weight =  [-0.02419719 , 0.01720026 , -0.377108 , -0.19824389 , 0.72086437 , 0.39539414, 0.67665313]
    for i in range(num_tries):
        game.main(best_weight, speed, max_score ,True)

def read():
    file = open('training_output.txt', 'r')
    lines = file.readlines()
    first_scores = []
    second_scores = []
    avg_score = []

    for line in lines:
        if line.__contains__('Best Weight:'):
            score = re.findall('[0-9].*', line)[0]
            first_scores.append(score)
    first_scores = np.array(first_scores, dtype=int)

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