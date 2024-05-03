import CCS_tetris as game
import Genetic_Algorithm as GG
G = GG.GA()
G.init_pop(10)
i = 0
score = 0
best_wight = 0

while(score<30000):
    for chromo in G.popultion:
        game_score = game.run_game_ai(chromo,600,30000)
        G.fittens(game_score[4],game_score[2])
        if(score<game_score[2]):
            score = game_score[2]
            best_wight = chromo
    print(f'level:{i}')
    i +=1
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    i +=1
    G.selection()   
    G.update_Wigths()
print(score)
print(best_wight)