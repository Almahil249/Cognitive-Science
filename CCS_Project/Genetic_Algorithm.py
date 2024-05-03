import random
import numpy as np
import CCS_Project.CCS_tetris as game
class GA:
    popultion = []
    new_pop = []
    pop_size = 0
    def __init__(self):
        pass
    def init_pop(self,pop_size):
        self.pop_size = pop_size
        for i in range(pop_size):
            chromo = np.random.uniform(-1,1,size=4)
            self.popultion.append(chromo)
    def print_pop(self):
        print(self.popultion)
    def fittens(self,chromo,score):
        new_gen = [chromo,score]
        self.new_pop.append(new_gen)
    def selection(self):
        new_gen = []
        sorted_chromo_pop = sorted(self.new_pop , key = lambda x: x[1])
        new_gen = sorted_chromo_pop[-3:]
        exe = []
        for gen in new_gen:
            exe.append(gen[0])
        for i in range(int(self.pop_size*0.3)-3):
            lucky = random.choice(self.popultion[:-5])
            exe.append(lucky)
        print(exe)
        exe = self.mutat(exe)
        print(exe)
    def mutat(self,pop):
        new_pop = []
        for chromo in pop:
            rand = np.random.rand(len(chromo))
            indices = np.where(rand < 0.1)[0]
            for i in indices:
                chromo[i] = chromo[i]/4
            new_pop.append(chromo)
        return new_pop
    def calc_best_move(self, board, piece,chromo,show_game = True):
        best_x = 0
        best_y = 0
        best_z = 0
        best_score = -999
        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        print(len(game.PIECES[piece['shape']]))
        for r in range(len(game.PIECES[piece['shape']])):
            for x in range(-2,game.BOARDWIDTH-2):
                move_info = game.calc_move_info(board,piece,x,r,num_holes_bef,num_blocking_blocks_bef)
                print(move_info)
                if(move_info[0]):
                    move_score = 0
                    for i in range(len(chromo)):
                        move_score += chromo[i]*move_info[i+1]
                    if(move_score>best_score):
                        best_score= move_score
                        best_x = x
                        best_z = r
        piece['x'] = best_x
        piece['rotation'] = best_z
        
        return best_x,best_z,chromo,best_score

