import CCS_Project.CCS_tetris as game
import CCS_Project.Genetic_Algorithm as GG
G = GG.GA()
G.init_pop(10)
i = 0
for chromo in G.popultion:
    game_score = game.run_game_ai(chromo,25)
    G.fittens(game_score[4],game_score[2])
    print(i)
    i +=1
G.selection()