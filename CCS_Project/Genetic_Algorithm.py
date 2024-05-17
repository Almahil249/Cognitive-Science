import random
import numpy as np
import CCS_tetris as game
import math

class GA:
    popultion = []
    new_pop = []
    pop_size = 0
    
    def __init__(self, pop_size=10, num_gens=7):
        self.pop_size = pop_size
        self.popultion = []
        pop = []
        for i in range(pop_size):
            # gen1 = np.random.uniform(-10, -0.99)    # max_height
            # gen2 = np.random.uniform(0.99, 10)      # min_height
            # gen3 = np.random.uniform(0.99, 10)      # num_removed_lines
            # gen4 = np.random.uniform(-10, -0.99)    # total_holes
            # gen5 = np.random.uniform(-10, -0.99)    # bumpiness
            # chromo = [gen1, gen2, gen3, gen4, gen5]
            chromo = np.random.uniform(-10, 10, size=num_gens)
            # Ensure randomness
            #print('lol')
            # chromo = [-0.27521385, -0.19055338, -0.54777522, -0.16039307, -0.38306999,  0.35059687]
            self.popultion.append(chromo)
        #for crom in pop:
            #new_crom = [crom,0]
            #self.popultion.append(new_crom)


    
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
        return new_gen
    def roluate_selection(self,pop):
         selected_chromo = []
         selected_chromo_index = []
         #print(self.pop_size)
         while(len(selected_chromo) != 10):
            total_fitness = sum(chrom[1] for chrom in pop)
            random.shuffle(pop)
            selection_point = random.uniform(0, total_fitness)
            current_sum = 0
            for i in range(int(len(pop))):
                current_sum += pop[i][1]
                #p = list(pop[i][0])
                #s =list(selected_chromo)
                is_exact_match = any(np.array_equal(pop[i][0], item) for item in selected_chromo)
                #print(f'is_exact_match {is_exact_match}')
                if current_sum >= selection_point and is_exact_match == False:
                    selected_chromo_index.append(i)
                    selected_chromo.append(pop[i][0])
                    break
         #print(f'selcted_chromo {selected_chromo}')
         return selected_chromo,selected_chromo_index
            
       

    def op(self,chromoes):
        offspring = []
        offspring = self.cross_over_selecte(chromoes)
        offspring = self.mutat(offspring)
        #print(f'off spring :{len(offspring)}')
        return offspring
    def selection(self,pop,mutat_rate=0.1,crossover_rate=0.7):
       
        old_exe = pop
        #exe = []
        
        #exe = old_exe[-3:]
       # for i in range(math.ceil((len(sorted_chromo_pop)*0.3)-3)):
        #    lucky = random.choice(old_exe)
         #   exe.append(lucky)
        #print(f'exe :{len(exe)}')
        #print(f'wigths before cross over :{old_exe}')
        genes = self.cross_over_selecte(old_exe,crossover_rate)
        
        #print(len(genes))
        genes = self.mutat(genes,mutat_rate)
        #print(f'wigths after mutation :{len(genes)}')
        final_pop = list(old_exe) + list(genes)
        
        #final_pop = self.replacement(final_pop)
        #print(f'wigths after update :{len(final_pop)}')
       
        self.update_Wigths(final_pop)
    
    def mutat(self,pop,mutat_rate):
        new_pop = []
        #print(f'mutat {len(pop)}')
        for chromo in pop:
            rand = np.random.rand(len(chromo))
            #print(rand)
            indices = np.where(rand < mutat_rate)[0]
            for i in indices:
                chromo[i] = random.uniform(-1, 1)
            # print(f'mutat:{len(chromo)}')
            new_pop.append(chromo)
        return new_pop
    def cross_over_selecte(self,pop,cross_over_rate):
        rand = np.random.rand(len(pop))
        indices = np.where(rand < cross_over_rate)[0]
        cross_selected = []
        for i in indices:
            cross_selected.append(pop[i])
        forlis = 0
        #print(f'corss len{len(cross_selected)}')
        if(len(cross_selected)%2 != 0):
            forlis = (len(cross_selected)//2)+1
        else:
            forlis = (len(cross_selected)//2)
        genes = []
        #print(cross_selected[0])
        for new_i in range(forlis):
            for i2 in range(new_i+1,len(cross_selected)):
                genes.append(self.cross_over(cross_selected[new_i], cross_selected[i2]))
        #print(f'gens len {len(genes)}')
        return genes

    def cross_over(self,corm1,corm2):
        list1_length = len(corm1)
        cut_point = random.randint(1, list1_length - 1)
        combined = list(corm1[:cut_point]) + list(corm2[cut_point:])
        combined = np.array(combined)
        #print(f'crom1 {combined}')
        return combined
    def calc_best_move(self, board, piece, chromo):
        best_x = 0
        best_y = 0
        best_z = 0
        best_score = -999
        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        pumb = game.board_bumpiness(np.array(board))
        #print(f'pumb_before: {pumb}')
        for r in range(len(game.PIECES[piece['shape']])):
            for x in range(-2,game.BOARDWIDTH-2):
                
                move_info = game.calc_move_info(board,piece,x,r,num_holes_bef,num_blocking_blocks_bef)
                # move_info = [True, max_height, num_removed_lines, new_holes, new_blocking_blocks]
                #pumb_after = game.calc_bumpiness(np.array(board))
                #print(f'pumb_after: {pumb_after}')
                # calc features
                #num_removed_lines = move_info[2]
                #new_holes = move_info[3]
                #new_blocking_blocks = move_info[4]
                #max_height, min_height = game.max_min_height(np.array(board))
                #dv_height = game.deepest_valley_height(np.array(board))
                #total_holes, _ = game.calc_initial_move_info(board)
                bumpiness = game.calc_move_bumpiness(np.array(board),piece,x,r)
                
                #print(f'bumpiness after :{bumpiness}')

                #features = [num_removed_lines, new_holes, new_blocking_blocks, max_height, min_height, dv_height, total_holes, bumpiness]
                # features = move_info[1:]
                
                if(move_info[0]):
                    move_score = 0
                    #k = min(len(chromo), len(features))
                    #print(f'chromo2 {chromo}')
                    pumbness = pumb - bumpiness
                    move_score += chromo[0] * move_info[1]
                    move_score += chromo[1] * move_info[2]
                    move_score += chromo[2] * move_info[3]
                    move_score += chromo[3] * move_info[4]
                    move_score += chromo[4] * move_info[5]
                    move_score += chromo[5] * move_info[6]
                    move_score += chromo[6] * move_info[7]
                    #move_score += chromo[7] * move_info[8]

                   # print('------------------')
                    #print(f'move {move_score}')
                    #print(f'best {best_score}')
                    if(move_score > best_score):
                        best_score = move_score
                        best_x = x
                        best_z = r
                        best_y = piece['y']
        piece['y'] = best_y
        #print(f'X :{best_x}')
        piece['x'] = best_x
        piece['rotation'] = best_z
        piece['y'] = 0
        
        return best_x, best_z, chromo, best_score