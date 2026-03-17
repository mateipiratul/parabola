import json
import time
from chrompop import ChromPop

def read_population(file_path):
    with open(file_path, 'r') as f:
        temp = json.load(f)
        return temp['samples']

def simulate(chrom_pop: ChromPop, i: int):
    sample_data = {
        'sample_index': i,
        'configuration': {
            'dimension': chrom_pop.dimension,
            'domain': chrom_pop.domain,
            'funct_params': chrom_pop.funct_params,
            'precision': chrom_pop.precision,
            'crossover_prob': chrom_pop.crossover_prob,
            'mutation_prob': chrom_pop.mutation_prob,
            'it_num': chrom_pop.it_num,
            'chrom_len': chrom_pop.chrom_len,
            'disc_step': chrom_pop.disc_step,
        },
        'iterations': []
    }
    
    for iteration in range(chrom_pop.it_num):
        current_pop_data = [
            {'idx': p[0], 'bin': p[1], 'val': p[2], 'fit': p[3]}
            for p in chrom_pop.population
        ]

        selected_pop, selection_logs = chrom_pop.selection_procedure()
        crossed_pop, participation_logs, crossover_logs = chrom_pop.crossover_procedure(selected_pop)
        final_pop, mutation_logs = chrom_pop.mutation_procedure(crossed_pop)
        max_fit = max(p[3] for p in chrom_pop.population)

        iteration_data = {
            'iteration_number': iteration + 1,
            'max_fitness': max_fit,
            'mean_fitness': sum(p[3] for p in chrom_pop.population) / chrom_pop.dimension,
            'population': current_pop_data,
            'selected_population': [{'idx': p[0], 'bin': p[1], 'val': p[2], 'fit': p[3]} for p in selected_pop],
            'crossed_population': [{'idx': p[0], 'bin': p[1], 'val': p[2], 'fit': p[3]} for p in crossed_pop],
            'selection_intervals': chrom_pop.intervals,
            'selection_logs': selection_logs,
            'mutation_logs': mutation_logs,
            'crossover_logs': crossover_logs,
            'mutation_logs': mutation_logs
        }

        sample_data['iterations'].append(iteration_data)
        chrom_pop.eval_new_gen(final_pop)

    return sample_data

def main(input_path='population_samples.json', output_path='results.json'):
    raw_data = read_population(input_path)
    all_results = []

    for i, data in enumerate(raw_data):
        chrom_pop = ChromPop(
            data['dimension'], 
            tuple(data['domain']), 
            tuple(data['funct_params']), 
            data['precision'], 
            data['crossover_prob'], 
            data['mutation_prob'], 
            data['it_num']
        )
        
        sample_historic = simulate(chrom_pop, i)
        all_results.append(sample_historic)

    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"total execution time: {end - start:.2f} seconds")
