import matplotlib.pyplot as plt
import numpy as np
import random


class VisualEnvironment3x3:
    def __init__(self):
        # 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(3, 3))

        # Posicion inicial aleatoria
        self.agent_pos = [
            random.randint(0, 2),
            random.randint(0, 2)
        ]

        # Metricas de rendimiento 
        self.initial_dirty = int(np.sum(self.grid))
        self.cleaned_cells = 0
        self.score = 0
        self.cost_per_move = -1
        self.reward_per_clean = 10

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def render(self, step, action, visited):
        self.ax.clear()

        self.ax.matshow(
            self.grid,
            cmap="Blues",
            vmin=0,
            vmax=1.5
        )

        # Dibujar la aspiradora
        self.ax.plot(
            self.agent_pos[1],
            self.agent_pos[0],
            "ro",
            markersize=25
        )

        # Mostrar estado y si la casilla fue visitada
        for i in range(3):
            for j in range(3):
                pos = (i, j)

                estado = (
                    "SUCIO" if self.grid[i, j] == 1
                    else "LIMPIO"
                )

                marca = "\nVisitada" if pos in visited else ""

                self.ax.text(
                    j, i,
                    estado + marca,
                    ha="center",
                    va="center",
                    color="black",
                    weight="bold",
                    fontsize=9
                )

        self.ax.set_title(
            f"Paso: {step} | Accion: {action} | Puntaje: {self.score}",
            pad=20
        )

        self.ax.set_xticks(range(3))
        self.ax.set_yticks(range(3))

        self.ax.set_xticks(
            np.arange(-0.5, 3, 1), minor=True
        )
        self.ax.set_yticks(
            np.arange(-0.5, 3, 1), minor=True
        )

        self.ax.grid(
            which="minor",
            color="black",
            linewidth=2
        )

        plt.draw()
        plt.pause(0.8)

    def get_percept(self):
        fila, columna = self.agent_pos

        return (
            self.agent_pos.copy(),
            self.grid[fila, columna]
        )

    def execute_action(self, action):
        fila, columna = self.agent_pos

        # Toda accion incurre en un costo energetico (-1)
        self.score += self.cost_per_move

        if action == "Suck":
            if self.grid[fila, columna] == 1:
                self.grid[fila, columna] = 0
                self.cleaned_cells += 1
                self.score += self.reward_per_clean  # Recompensa (+10)

        elif action == "Up" and fila > 0:
            self.agent_pos[0] -= 1

        elif action == "Down" and fila < 2:
            self.agent_pos[0] += 1

        elif action == "Left" and columna > 0:
            self.agent_pos[1] -= 1

        elif action == "Right" and columna < 2:
            self.agent_pos[1] += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0


class VacuumAgentWithMemory:
    def __init__(self, total_casillas=9):
        # Memoria de todas las posiciones visitadas
        self.visited = set()

        # Camino actual: permite retroceder
        self.path = []

        # Total de casillas para verificar cobertura completa
        self.total_casillas = total_casillas

    def act(self, percept):
        pos, status = percept

        pos = tuple(pos)

        if not self.path:
            self.path.append(pos)
            self.visited.add(pos)

        if status == 1:
            return "Suck"

        if len(self.visited) >= self.total_casillas:
            return "Stop"

        fila, columna = pos

        vecinos = {
            "Up": (fila - 1, columna),
            "Down": (fila + 1, columna),
            "Left": (fila, columna - 1),
            "Right": (fila, columna + 1)
        }

        movimientos_validos = {
            accion: destino
            for accion, destino in vecinos.items()
            if 0 <= destino[0] < 3
            and 0 <= destino[1] < 3
        }

        # Buscar vecinos 
        movimientos_nuevos = [
            (accion, destino)
            for accion, destino in movimientos_validos.items()
            if destino not in self.visited
        ]

        # Prioridad 1
        if movimientos_nuevos:
            accion, destino = random.choice(movimientos_nuevos)

            self.visited.add(destino)
            self.path.append(destino)

            return accion

        # Prioridad 2
        if len(self.path) > 1:
            self.path.pop()
            anterior = self.path[-1]

            # Encontrar la accion para regresar
            for accion, destino in movimientos_validos.items():
                if destino == anterior:
                    return accion

        # No quedan posiciones nuevas por explorar
        return "Stop"


if __name__ == "__main__":
    env = VisualEnvironment3x3()
    agent = VacuumAgentWithMemory(total_casillas=9)

    env.render(0, "Inicio", agent.visited)

    total_pasos = 0
    for paso in range(1, 101):
        total_pasos = paso
        percept = env.get_percept()
        action = agent.act(percept)

        if action == "Stop":
            env.render(paso, "Stop", agent.visited)
            print("Exploracion terminada.")
            break

        env.execute_action(action)
        env.render(paso, action, agent.visited)

    print("Posiciones visitadas:", agent.visited)
    print("Total de posiciones visitadas:", len(agent.visited))
    print("Pasos totales:", total_pasos)
    print("Casillas limpiadas:", env.cleaned_cells)
    print("Puntaje final:", env.score)

    plt.ioff()
    plt.show()
