import random
import numpy as np
import CCS_tetris as game
import math


class GA:
    population = []
    new_pop = []
    pop_size = 0
    
    def __init__(self, pop_size=10, num_gens=7):
        """
        Initializes a Genetic Algorithm object.

        Parameters:
        pop_size (int): The size of the population (default is 10).
        num_gens (int): The number of genes in each chromosome (default is 7).

        Returns:
        None
        """
        self.pop_size = pop_size
        self.population = []
        pop = []
        for i in range(pop_size):
            chromo = np.random.uniform(-10, 10, size=num_gens)
            self.population.append(chromo)

    def update_Weights(self, new):
        """
        Updates the weights of the genetic algorithm population.

        Parameters:
        new (list): The new population of weights.

        Returns:
        None
        """
        self.population = []
        self.new_pop = []
        self.population = new

    def print_pop(self):
        """
        Prints the current population.

        Returns:
        None
        """
        print(self.population)
    
    def replacement(self, new_pop):
        """
        Replaces a portion of the current population with the best individuals from the new population.

        Args:
            new_pop (list): The new population to be integrated into the current population.

        Returns:
            list: The updated population after replacement.
        """
        sorted_pop = sorted(self.new_pop, key=lambda x: x[1])
        k = int(self.pop_size * 0.1)
        for i in range(1, k):
            new_pop.append(sorted_pop[-i][0])
        return new_pop
    
    def fittens(self, chromo, score):
        """
        Creates a new generation by combining the chromosome and its fitness score.

        Parameters:
        chromo (object): The chromosome object.
        score (float): The fitness score of the chromosome.

        Returns:
        list: A list containing the chromosome and its fitness score.
        """
        new_gen = [chromo, score]
        return new_gen

    def roulette_selection(self, pop):
        """
        Selects chromosomes from the population based on their fitness values.

        Args:
            pop (list): The population of chromosomes.

        Returns:
            tuple: A tuple containing two lists - selected_chromo and selected_chromo_index.
                - selected_chromo (list): The selected chromosomes.
                - selected_chromo_index (list): The indices of the selected chromosomes in the population.
        """
        selected_chromo = []
        selected_chromo_index = []
        while(len(selected_chromo) != 10):
            total_fitness = sum(chrom[1] for chrom in pop)
            random.shuffle(pop)
            selection_point = random.uniform(0, total_fitness)
            current_sum = 0
            for i in range(int(len(pop))):
                current_sum += pop[i][1]
                is_exact_match = any(np.array_equal(pop[i][0], item) for item in selected_chromo)
                if current_sum >= selection_point and is_exact_match == False:
                    selected_chromo_index.append(i)
                    selected_chromo.append(pop[i][0])
                    break
        return selected_chromo, selected_chromo_index


    def op(self, chromosomes):
        """
        Perform genetic operations on the given chromosomes.

        Args:
            chromosomes (list): The list of chromosomes to perform operations on.

        Returns:
            list: The offspring generated after performing crossover and mutation operations.
        """
        offspring = []
        offspring = self.cross_over_select(chromosomes)
        offspring = self.mutate(offspring)
        return offspring


    def selection(self, pop, mutate_rate=0.1, crossover_rate=0.7):
        """
        Performs selection, crossover, and mutation operations on the population.

        Args:
            pop (list): The current population.
            mutate_rate (float): The mutation rate (default is 0.1).
            crossover_rate (float): The crossover rate (default is 0.7).

        Returns:
            None
        """
        old_exe = pop
        genes = self.cross_over_select(old_exe, crossover_rate)
        genes = self.mutate(genes, mutate_rate)
        final_pop = list(old_exe) + list(genes)
        self.update_Weights(final_pop)
    
    def mutate(self, pop, mutate_rate):
        """
        Performs mutation operation on the given population.

        Args:
            pop (list): The population to perform mutation on.
            mutate_rate (float): The mutation rate.

        Returns:
            list: The population after mutation.
        """
        new_pop = []
        for chromo in pop:
            rand = np.random.rand(len(chromo))
            indices = np.where(rand < mutate_rate)[0]
            for i in indices:
                chromo[i] = random.uniform(-1, 1)
            new_pop.append(chromo)
        return new_pop
    
    def cross_over_select(self, pop, crossover_rate):
        """
        Performs crossover operation on the given population.

        Args:
            pop (list): The population to perform crossover on.
            crossover_rate (float): The crossover rate.

        Returns:
            list: The offspring generated after crossover.
        """
        rand = np.random.rand(len(pop))
        indices = np.where(rand < crossover_rate)[0]
        cross_selected = []
        for i in indices:
            cross_selected.append(pop[i])
        forlis = 0
        if(len(cross_selected) % 2 != 0):
            forlis = (len(cross_selected) // 2) + 1
        else:
            forlis = (len(cross_selected) // 2)
        genes = []
        for new_i in range(forlis):
            for i2 in range(new_i + 1, len(cross_selected)):
                genes.append(self.cross_over(cross_selected[new_i], cross_selected[i2]))
        return genes

    def cross_over(self, corm1, corm2):
        """
        Performs crossover operation on two chromosomes.

        Args:
            corm1 (list): The first chromosome.
            corm2 (list): The second chromosome.

        Returns:
            list: The offspring generated after crossover.
        """
        list1_length = len(corm1)
        cut_point = random.randint(1, list1_length - 1)
        combined = list(corm1[:cut_point]) + list(corm2[cut_point:])
        combined = np.array(combined)
        return combined

    def calc_best_move(self, board, piece, chromo):
        """
        Calculates the best move for a given board and piece using the genetic algorithm.

        Args:
            board (list): The game board.
            piece (dict): The current piece.
            chromo (list): The chromosome containing the weights.

        Returns:
            tuple: A tuple containing the best x-coordinate, best rotation, updated chromosome, and best score.
        """
        best_x = 0
        best_y = 0
        best_z = 0
        best_score = -999
        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        pumb = game.board_bumpiness(np.array(board))
        for r in range(len(game.PIECES[piece['shape']])):
            for x in range(-2, game.BOARDWIDTH - 2):
                move_info = game.calc_move_info(board, piece, x, r, num_holes_bef, num_blocking_blocks_bef)
                bumpiness = game.calc_move_bumpiness(np.array(board), piece, x, r)
                if(move_info[0]):
                    move_score = 0
                    pumbness = pumb - bumpiness
                    move_score += chromo[0] * move_info[1]
                    move_score += chromo[1] * move_info[2]
                    move_score += chromo[2] * move_info[3]
                    move_score += chromo[3] * move_info[4]
                    move_score += chromo[4] * move_info[5]
                    move_score += chromo[5] * move_info[6]
                    move_score += chromo[6] * move_info[7]

                    if(move_score > best_score):
                        best_score = move_score
                        best_x = x
                        best_z = r
                        best_y = piece['y']
        piece['y'] = best_y
        piece['x'] = best_x
        piece['rotation'] = best_z
        piece['y'] = 0
        
        return best_x, best_z, chromo, best_score