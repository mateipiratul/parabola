from math import log2, ceil
import random

def string_gen(n, l):
    return [(''.join(random.choice('01') for _ in range(l))) for _ in range(n)]


class ChromPop:
    def __init__(self, dimension: int, domain: tuple[float, float], funct_params: tuple[int, int, int], precision: float, crossover_prob: float, mutation_prob: float, it_num: int):
        self.dimension = dimension
        self.domain = domain
        self.funct_params = funct_params
        self.precision = precision
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.it_num = it_num
        self.chrom_len = ceil(log2((domain[1] - domain[0]) * 10**precision))
        self.disc_step = float(self.domain[1] - self.domain[0]) / 2**self.chrom_len
        self.population = self._init_population()
        self.intervals = self._selection_intervals()

    def _function_value(self, x):
        return self.funct_params[0] * x**2 + self.funct_params[1] * x + self.funct_params[2]

    def _init_population(self):
        strings = string_gen(self.dimension, self.chrom_len)
        real_vals = [self._decoding(string) for string in strings]
        function_vals = [self._function_value(x) for x in real_vals]
        idxs = [i for i in range(1, self.dimension + 1)]
        return list(zip(idxs, strings, real_vals, function_vals))

    def _compute_bin(self, x):
        binary_str = bin(x)[2:]
        return binary_str.zfill(self.chrom_len)

    def _encoding(self, real_val):
        real_val = float(real_val)
        idx = int((real_val - self.domain[0]) / self.disc_step)
        idx = min(idx, 2**self.chrom_len - 1)
        return self._compute_bin(idx)

    def _decoding(self, bytes):
        return self.domain[0] + int(bytes, 2) * self.disc_step

    def _selection_intervals(self):
        fitness_values = [t[3] for t in self.population]
        total_fitness = sum(fitness_values)

        intervals = [0]
        curr_sum = 0
        for i in range(self.dimension):
            curr_sum += fitness_values[i]
            intervals.append(curr_sum / total_fitness) 
        return intervals

    def _binary_search(self, u):
        low, high = 0, len(self.intervals) - 1
        
        while low < high:
            mid = low + (high - low) // 2
            if self.intervals[mid] < u:
                low = mid + 1
            else:
                high = mid
        return low

    def selection_procedure(self):
        new_population = []
        selection_logs = []

        best_individual = max(self.population, key=lambda x: x[3])
        new_population.append(best_individual)

        for _ in range(self.dimension - 1):
            u = random.random()
            idx = self._binary_search(u)
            
            selected_ind = self.population[idx - 1]
            new_population.append(self.population[idx - 1])
            selection_logs.append({'u': u, 'selected_idx': selected_ind[0]})

        return new_population, selection_logs

    def _crossover(self, parent1_bin, parent2_bin, point=None):
        point = self.chrom_len // 2 if point is None else point
        child1_bin = parent1_bin[:point] + parent2_bin[point:]
        child2_bin = parent2_bin[:point] + parent1_bin[point:]
        return child1_bin, child2_bin

    def crossover_procedure(self, selected_pop):
        new_pop = selected_pop.copy()

        participants_indices = []
        participation_logs = []

        for i in range(1, len(selected_pop)):
            ind = selected_pop[i]
            u = random.random()
            participates = u < self.crossover_prob

            participation_logs.append({
                'current_pos': i + 1,
                'binary': ind[1],
                'u': u,
                'participates': participates
            })

            if participates:
                participants_indices.append(i)


        random.shuffle(participants_indices)
        crossover_logs = []

        for i in range(0, len(participants_indices) - 1, 2):
            idx1 = participants_indices[i]
            idx2 = participants_indices[i + 1]
            parent1 = new_pop[idx1]
            parent2 = new_pop[idx2]
            point = random.randint(1, self.chrom_len - 1)
            child1_bin, child2_bin = self._crossover(parent1[1], parent2[1], point)
            
            child1_val = self._decoding(child1_bin)
            child1_f = self._function_value(child1_val)
            new_pop[idx1] = (idx1 + 1, child1_bin, child1_val, child1_f)
            child2_val = self._decoding(child2_bin)
            child2_f = self._function_value(child2_val)
            new_pop[idx2] = (idx2 + 1, child2_bin, child2_val, child2_f)

            crossover_logs.append({
                'parent1_idx': idx1 + 1,
                'parent1_binary': parent1[1],
                'parent2_idx': idx2 + 1,
                'parent2_binary': parent2[1],
                'cut_point': point,
                'child1_binary': child1_bin,
                'child2_binary': child2_bin            
            })

        final_pop = [(i + 1, ind[1], ind[2], ind[3]) for i, ind in enumerate(new_pop)]
        return final_pop, participation_logs, crossover_logs

    def _mutation(self, individual, mutation_bits):
        individual_list = list(individual)
        for bit in mutation_bits:
            if 0 <= bit < len(individual_list):
                individual_list[bit] = '1' if individual_list[bit] == '0' else '0'
        return ''.join(individual_list)

    def mutation_procedure(self, current_pop):
        mutated_population = []
        mutation_logs = []

        for i, ind in enumerate(current_pop):
            if i == 0:
                mutated_population.append(ind)
                continue
        
            bin_str = ind[1]
            mutated_bits = []
            for bit_idx in range(self.chrom_len):
                if random.random() < self.mutation_prob:
                    mutated_bits.append(bit_idx)
            
            if mutated_bits:
                new_bin_str = self._mutation(bin_str, mutated_bits)
                
                new_val = self._decoding(new_bin_str)
                new_f = self._function_value(new_val)
                mutated_population.append((i + 1, new_bin_str, new_val, new_f))

                mutation_logs.append({
                    'chromosome_idx_newgen': i, 
                    'og_bin': bin_str,
                    'mutated_bits_indices': mutated_bits,
                    'new_bin': new_bin_str
                })
            else:
                mutated_population.append(ind)
        
        return mutated_population, mutation_logs

    def eval_new_gen(self, final_pop):
        self.population = final_pop
        self.intervals = self._selection_intervals()
        return
