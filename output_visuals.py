import matplotlib.pyplot as plt
import json

def track_fitness_evolution(results_json='results.json'):
    with open(results_json, 'r') as f:
        data_sample = json.load(f)

    for i, data in enumerate(data_sample):
        plt.figure()
        iterations = data['iterations']
        max_fitness_values = [it['max_fitness'] for it in iterations]
        a, b, c = data['configuration']['funct_params']
        l, h = data['configuration']['domain']
        plt.plot(max_fitness_values, label=f"sample {data['sample_index']}")
        plt.xlabel('iteration')
        plt.ylabel('max fitness')
        plt.title(f'evolution of max fitness over iterations for fitness function {a}*x^2 + {b}*x + {c} within domain [{l}, {h}]')
        plt.savefig(f'plots/fitness_evolution_{i}.png')
        plt.close()

def write_txt_file(json_path='results.json', txt_path='evolution.txt'):
    with open(json_path, 'r') as fin:
        data = json.load(fin)[0]

    config = data['configuration']
    iterations = data['iterations']
    first_gen = iterations[0]

    with open(txt_path, 'w') as fout:
        fout.write("formatted output of the first population sample from 'population_samples.json'\n")
        fout.write("\ninitial population:\n")
        initial_pop = first_gen['population']
        sum_f = sum(p['fit'] for p in initial_pop)

        for p in initial_pop:
            fout.write(f"{str(p['idx']).ljust(3)}: b = {p['bin']} | x = {str(p['val']).ljust(20)} | f = {p['fit']}\n")

        fout.write("\nselection probabilities:\n")
        for p in initial_pop:
            prob = p['fit'] / sum_f
            fout.write(f"chromosome {str(p['idx']).ljust(3)} probability {prob}\n")

        fout.write("\nselection probability intervals\n")
        fout.write(" ".join(str(q) for q in first_gen['selection_intervals']) + "\n")

        if 'selection_logs' in first_gen:
            for log in first_gen['selection_logs']:
                fout.write(f"u = {str(log['u']).ljust(20)} selecting chromosome {log['selected_idx']}\n")

        fout.write(f"\ncrossover probability {config['crossover_prob']}")
        if 'participation_logs' in first_gen:
            for log in first_gen['participation_logs']:
                part_str = f" < {config['crossover_prob']} participates" if log['participates'] else ""
                fout.write(f"{log['current_pos']}: {log['binary']} u={log['u']}{part_str}\n")

        fout.write("\n")
        if 'crossover_logs' in first_gen:
            for log in first_gen['crossover_logs']:
                fout.write(f"recombination between chromosome {log['parent1_idx']} and chromosome {log['parent2_idx']}:\n")
                fout.write(f"{log['parent1_binary']} {log['parent2_binary']} cut point {log['cut_point']}\n")
                fout.write(f"result: {log['child1_binary']} {log['child2_binary']}\n")

        fout.write("\nafter crossover:\n")
        if 'crossed_population' in first_gen:
            for p in first_gen['crossed_population']:
                fout.write(f"{str(p['idx']).ljust(3)}: b = {p['bin']} | x = {str(p['val']).ljust(20)} | f = {p['fit']}\n")

        fout.write(f"\nmutation probability for each gene {config['mutation_prob']}\nthe following genes were mutated: ")
        if 'mutation_logs' in first_gen:
            fout.write(", ".join(str(log['chromosome_idx_newgen'] + 1) for log in first_gen['mutation_logs']))
        
        fout.write("\nafter mutation:\n")
        if len(iterations) > 1:
            for p in iterations[1]['population']:
                fout.write(f"{str(p['idx']).ljust(3)}: b = {p['bin']} | x = {str(p['val']).ljust(20)} | f = {p['fit']}\n")

        fout.write("\nevolution of the maximum fitness:\n")
        for i, it in enumerate(iterations):
            fout.write(f"it. {str(i).ljust(3)}: {it['max_fitness']}\n")

if __name__ == "__main__":
    write_txt_file()
    track_fitness_evolution()
