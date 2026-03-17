import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_evolution(json_path='results.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)[0]

    config = data['configuration']
    iterations = data['iterations']

    a, b, c = config['funct_params']
    domain_min, domain_max = config['domain']

    x_curve = np.linspace(domain_min, domain_max, 500)
    y_curve = a * x_curve**2 + b * x_curve + c

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_curve, y_curve, label=f'f(x) = {a}x² + {b}x + {c}', color='#1f77b4', linewidth=2)
    scatter = ax.scatter([], [], color='#ff7f0e', s=60, zorder=5, edgecolors='black', label='Chromosomes')
    ax.set_xlim(domain_min - 0.5, domain_max + 0.5)
    
    y_padding = (max(y_curve) - min(y_curve)) * 0.1
    ax.set_ylim(min(y_curve) - y_padding, max(y_curve) + y_padding)
    
    ax.set_xlabel('Valoarea X')
    ax.set_ylabel('Fitness f(X)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right')

    def update(frame):
        current_gen = iterations[frame]
        pop = current_gen['population']
        
        x_vals = [ind['val'] for ind in pop]
        y_vals = [ind['fit'] for ind in pop]
        
        scatter.set_offsets(np.c_[x_vals, y_vals])
        
        ax.set_title(f"Generația: {current_gen['iteration_number']} / {config['it_num']} | Max Fitness: {current_gen['max_fitness']:.4f}", fontsize=14)
        
        return scatter,

    print("incepe animatia... (inchide fereastra graficului pentru a opri scriptul)")
    ani = FuncAnimation(fig, update, frames=len(iterations), interval=200, blit=False, repeat=False)
    plt.show()

if __name__ == "__main__":
    animate_evolution()
