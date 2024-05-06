import random
import numpy as np
import CCS_tetris as game
import math

class GA:
    popultion = []
    new_pop = []
    pop_size = 0
    
    def __init__(self, pop_size=100, num_gens=5):
        self.pop_size = pop_size
        self.popultion = []
        for i in range(pop_size):
            # gen1 = np.random.uniform(-10, -0.99)    # max_height
            # gen2 = np.random.uniform(0.99, 10)      # min_height
            # gen3 = np.random.uniform(0.99, 10)      # num_removed_lines
            # gen4 = np.random.uniform(-10, -0.99)    # total_holes
            # gen5 = np.random.uniform(-10, -0.99)    # bumpiness
            # chromo = [gen1, gen2, gen3, gen4, gen5]
            chromo = np.random.uniform(-1, 1, size=num_gens)
            # Ensure randomness
            #print('lol')
            # chromo = [-0.27521385, -0.19055338, -0.54777522, -0.16039307, -0.38306999,  0.35059687]
            self.popultion.append(chromo)
    
    def update_Wigths(self,new):
        self.popultion = []
        self.new_pop = []
        self.popultion = new
    
    #def init_pop():
       
        
    
    def print_pop(self):
        print(self.popultion)
    
    def replacement(self,new_pop):
        sorted_pop = sorted(self.new_pop , key = lambda x: x[1])
        k = int(self.pop_size * 0.1)
        for i in range(1, k):
            new_pop.append(sorted_pop[-i][0])
        return new_pop
    
    def fittens(self,chromo,score):
        new_gen = [chromo, score]
        self.new_pop.append(new_gen)
        return new_gen
    
    def selection(self):
        new_gen = []
        sorted_chromo_pop = sorted(self.new_pop , key = lambda x: x[1])
        print(f'sorted pop {len(sorted_chromo_pop)}')
        new_gen = sorted_chromo_pop

        old_exe = []
        exe = []
        for gen in new_gen:
            old_exe.append(gen[0])
        exe = old_exe[-3:]
        genes = []
        forlis = 0
        
        if(len(exe)%2 != 0):
            forlis = (len(exe)//2)+1
        else:
            forlis = (len(exe)//2)
        
        for i in range(math.ceil((len(sorted_chromo_pop)*0.3)-3)):
            lucky = random.choice(old_exe)
            exe.append(lucky)
        print(f'exe :{len(exe)}')
        for new_i in range(forlis):
            for i2 in range(new_i+1,len(exe)):
                genes.append(self.cross_over(exe[new_i], exe[i2]))
        print(f'genes len after the cross over {len(genes)}')
        
        genes = self.mutat(genes)
        final_pop = list(exe) + list(genes)
        print(f'wigths before update :{len(final_pop)}')
        final_pop = self.replacement(final_pop)
        print(f'wigths after update :{len(final_pop)}')
        if(len(final_pop) < len(sorted_chromo_pop)):
            num_of_new = len(sorted_chromo_pop) - len(final_pop)
            for i in range(num_of_new):
                final_pop.append(random.choice(old_exe[-int(len(sorted_chromo_pop)*0.5):]))
        print(f'wigths after adding :{len(final_pop)}')
        self.update_Wigths(final_pop)
    
    def mutat(self,pop):
        new_pop = []
        for chromo in pop:
            rand = np.random.rand(len(chromo))
            #print(rand)
            indices = np.where(rand < 0.1)[0]
            for i in indices:
                chromo[i] = chromo[i] * random.uniform(0.90, 1.1)
            # print(f'mutat:{len(chromo)}')
            new_pop.append(chromo)
        return new_pop
    
    def cross_over(self,corm1,corm2):
        combined = list(corm1[:int(0.5 * len(corm1))]) + list(corm2[int(0.5 * len(corm2)):])
        combined = np.array(combined)
        # print(f'cross over{len(combined)}')
        # print(combined)
        return combined
    
    def calc_best_move(self, board, piece, chromo, show_game = True):
        best_x = 0
        best_y = 0
        best_z = 0
        best_score = -999
        best_bumpiness = 999
        best_holes_num = 999
        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        # pumb = game.calc_bumpiness(np.array(board))
        # print(f'pumb_before: {pumb_before}')
        # print('-----------------------')
        for r in range(len(game.PIECES[piece['shape']])):
            for x in range(-2,game.BOARDWIDTH-2):
                
                # move_info = [True, max_height, num_removed_lines, new_holes, new_blocking_blocks]
                move_info = game.calc_move_info(board,piece,x,r,num_holes_bef,num_blocking_blocks_bef)
                bumpiness = game.calc_move_bumpiness(board, piece, x, r)

                max_height = move_info[1]
                num_removed_lines = move_info[2]
                new_holes = move_info[3]
                new_blocking_blocks = move_info[4]
                
                if(move_info[0]):
                    move_score = 0
                    move_score -= abs(chromo[0] * max_height)
                    move_score += (chromo[1] * num_removed_lines)**2 # todo: 10 *
                    move_score -= abs(chromo[2] * new_holes)
                    move_score -= chromo[3] * new_blocking_blocks
                    move_score += (chromo[4] * - bumpiness)**3

                   # print('------------------')
                    #print(f'move {move_score}')
                    #print(f'best {best_score}')
                    if(move_score > best_score):
                        best_bumpiness = bumpiness
                        best_holes_num = new_holes
                        best_score = move_score
                        best_x = x
                        best_z = r
                        best_y = piece['y']
        # print(f'Best Bump = {best_bumpiness}')
        # print(f'Best Num Holes = {best_holes_num}')
        if (show_game):
            piece['y'] = best_y
        else:
            piece['y'] = -2
        #print(f'X :{best_x}')
        piece['x'] = best_x
        piece['rotation'] = best_z
        piece['y'] = 0
        
        return best_x, best_z, chromo, best_score