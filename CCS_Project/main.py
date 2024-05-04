import CCS_tetris as game
import Genetic_Algorithm as GG

G = GG.GA()
G.init_pop(10, num_gens=6)
# score = 0
# best_weight = []
# [-0.27521385 -0.19055338 -0.54777522 -0.16039307 -0.38306999  0.35059687] -> score = 21,040

output_file = 'E:\FCAI\Thrid Year\Second Term\Cognitive\Github_Project\Cognitive-Science\CCS_Project\\training_output.txt'

with open(output_file, 'w') as f:
    for i in range(1, 301):
        score = 0
        best_weight = []
        for chromo in G.popultion:
            game_score = game.run_game_ai(chromo, 600, 30000)
            G.fittens(game_score[4], game_score[2])
            G.selection()
            if(score < game_score[2]):
                score = game_score[2]
                best_weight = chromo
            G.selection()

        f.write(f'=== Gen {i} Best Solution ===\n')
        f.write(f'Score: {score}\n')
        f.write(f'Best Weight: {best_weight}\n')
        f.write('----------------------------------------------------------------------------\n')
        
        print(f'=== Gen {i} Best Solution ===')
        print(f'Score: {score}')
        print(f'Best Weight: {best_weight}')
        print('----------------------------------------------------------------------------')
        
        if score > 30000:
            break

    print(score)
    print(best_weight)