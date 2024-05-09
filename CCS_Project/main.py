import CCS_tetris as game
import Genetic_Algorithm as GG
import random
random.seed() 


# score = 0
# best_weight = []
# [-0.27521385 -0.19055338 -0.54777522 -0.16039307 -0.38306999  0.35059687] -> score = 21,040
def train(pop_size=10,iteration = 300,mutat_rate=0.1,crossover_rate=0.7):
    output_file = 'CCS_Project/training_output.txt'
    best_weights_file = 'best_weights_file.txt'
    POP_SIZE = pop_size
    G = GG.GA(POP_SIZE)
    currunt_score = 0
    #with open(best_weights_file, 'w') as bf:
    with open(output_file, 'w') as f:
            for i in range(1, iteration+1):
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
                    game_score = game.main(chromo, 5000, 200000,i,weight_idnex)
                    next_gen.append(G.fittens(chromo, game_score[2]))
                    currunt_score+=game_score[2]
                    if(best_gen_score < game_score[2]):
                        best_gen_score = game_score[2]
                        best_weight = chromo
                    elif(snd_best_gen_score < game_score[2] and best_gen_score != game_score[2]):
                        snd_best_gen_score = game_score[2]
                        snd_best_weight = chromo
                    weight_idnex += 1
                avg_score = currunt_score//len(G.popultion)
                #G.print_pop()
                selected_chromo,selected_chromo_index = G.roluate_selection(next_gen)
                #print(f'chromo selcted len{selected_chromo}')
                G.selection(selected_chromo,mutat_rate,crossover_rate)
                f.write(f'=== Gen {i} Best Solution ===\n')
                f.write(f'Game palyed {weight_idnex}')
                f.write(f'avg gen Score: {avg_score}\n')
                f.write(f'first best gen Score: {best_gen_score}\n')
                f.write(f'first best gen Weight: {best_weight}\n')
                f.write(f'Sencond best gen Score: {snd_best_weight}\n')
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

                if best_gen_score > 200000:
                    #bf.write(f'=== Gen {i} Best Solution ===\n')
                    #bf.write(f'avg gen Score: {avg_score}\n')
                    #bf.write(f'Score: {best_gen_score}\n')
                    #bf.write(f'Best Weight: {best_weight}\n')
                    break
def test(speed=3000,num_tries=600):
    best_weight =  [-0.02419719 , 0.01720026 , -0.377108 , -0.19824389 , 0.72086437 , 0.39539414, 0.67665313]
    for i in range(num_tries):
        game.main(best_weight, 3000, 200000,True)
#test()
train()
