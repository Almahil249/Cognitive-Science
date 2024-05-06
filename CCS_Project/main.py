import CCS_tetris as game
import Genetic_Algorithm as GG
import random
random.seed() 
POP_SIZE = 10
G = GG.GA(POP_SIZE)
#G.init_pop(pop_size=10, num_gens=5)
currunt_score = 0
num_selected = 3

# score = 0
# best_weight = []
# [-0.27521385 -0.19055338 -0.54777522 -0.16039307 -0.38306999  0.35059687] -> score = 21,040

output_file = 'training_output.txt'

with open(output_file, 'w') as f:
    for i in range(1, 301):
        score = 0
        currunt_score = 0
        selected_chromo = []
        selected_chromo_index = []
        best_weight = []
        next_gen = []
        #for i2 in range(num_selected):
         #   cromo,index = G.roluate_selection(G.popultion)
          #  selected_chromo_index.append(index)
           # selected_chromo.append(cromo)
        #G.op(selected_chromo)
        #non_score_pop = []*
        #for non in G.popultion:
          #  non_score_pop.append(non[0])
        for chromo in G.popultion:
            game_score = game.run_game_ai(chromo, 1500, 100000)
            next_gen.append(G.fittens(chromo, game_score[2]))
            currunt_score+=game_score[2]
            if(score < game_score[2]):
                score = game_score[2]
                best_weight = chromo
        avg_score = currunt_score//len(G.popultion)
        #G.print_pop()
        for i2 in range(POP_SIZE):
            cromo,index = G.roluate_selection(next_gen)
            selected_chromo_index.append(index)
            selected_chromo.append(cromo)
        print(f'chromo selcted len{len(selected_chromo)}')
        G.selection(selected_chromo)
        f.write(f'=== Gen {i} Best Solution ===\n')
        f.write(f'avg gen Score: {avg_score}')
        f.write(f'Score: {score}\n')
        f.write(f'Best Weight: {best_weight}\n')
        f.write('----------------------------------------------------------------------------\n')
        
        print(f'=== Gen {i} Best Solution ===')
        print(f'avg gen Score: {avg_score}')
        print(f'Score: {score}')
        print(f'Best Weight: {best_weight}')
        print('----------------------------------------------------------------------------')

        if score > 100000:
            break
