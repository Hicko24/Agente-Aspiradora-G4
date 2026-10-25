import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment2x2:
    def __init__(self):
        # Cuadrícula 2x2: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(2, 2))
        # Posición inicial aleatoria (fila, columna)
        self.agent_pos = [random.randint(0, 1), random.randint(0, 1)]
        
        # Configuración del gráfico interactivo
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action):
        self.ax.clear()
        # Dibujar la cuadrícula (colores cambian según limpieza)
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        
        # Dibujar al agente como un punto rojo grande
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)
        
        # Etiquetas de estado
        for i in range(2):
            for j in range(2):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center', 
                             color='black', weight='bold', fontsize=12)

        self.ax.set_title(f"Paso: {step} | Acción: {action}", pad=20)
        self.ax.set_xticks([0, 1])
        self.ax.set_yticks([0, 1])
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        
        plt.draw()
        plt.pause(1.5) # Pausa para visualizar la animación

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):
        if action == 'Suck':
            self.grid[self.agent_pos[0], self.agent_pos[1]] = 0
        elif action == 'Up' and self.agent_pos[0] > 0:
            self.agent_pos[0] -= 1
        elif action == 'Down' and self.agent_pos[0] < 1:
            self.agent_pos[0] += 1
        elif action == 'Left' and self.agent_pos[1] > 0:
            self.agent_pos[1] -= 1
        elif action == 'Right' and self.agent_pos[1] < 1:
            self.agent_pos[1] += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

class RandomVacuumAgent:
    def act(self, percept):
        pos, status = percept
        
        # Regla principal: Si está sucio, limpia.
        if status == 1:
            return 'Suck'
        
        # Movimiento aleatorio válido si está limpio
        movimientos_posibles = []
        if pos[0] > 0: movimientos_posibles.append('Up')
        if pos[0] < 1: movimientos_posibles.append('Down')
        if pos[1] > 0: movimientos_posibles.append('Left')
        if pos[1] < 1: movimientos_posibles.append('Right')
        
        return random.choice(movimientos_posibles)

if __name__ == "__main__":
    env = VisualEnvironment2x2()
    agent = RandomVacuumAgent()

    env.render(step=0, action="Inicio")

    for paso in range(1, 16):
        percept = env.get_percept()
        action = agent.act(percept)
        env.execute_action(action)
        env.render(step=paso, action=action)
        
        if env.is_completely_clean() and action != 'Suck':
            print("¡Entorno 2x2 completamente limpio!")
            break

    plt.ioff()
    plt.show()