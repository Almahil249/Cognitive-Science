import CCS_tetris as game
import Genetic_Algorithm as GG

G = GG.GA()
G.init_pop(pop_size=100, num_gens=4)
currunt_score = 0
# score = 0
# best_weight = []
# [-0.27521385 -0.19055338 -0.54777522 -0.16039307 -0.38306999  0.35059687] -> score = 21,040

output_file = 'training_output.txt'

with open(output_file, 'w') as f:
    for i in range(1, 301):
        score = 0
        currunt_score = 0
        best_weight = []
        for chromo in G.popultion:
            game_score = game.run_game_ai(chromo, 700, 100000)
            G.fittens(chromo, game_score[2])
            currunt_score+=game_score[2]
            if(score < game_score[2]):
                score = game_score[2]
                best_weight = chromo
        avg_score = currunt_score//len(G.popultion)
        G.selection()

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
