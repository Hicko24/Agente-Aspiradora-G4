import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

        plt.ion()
        self.fig = plt.figure(figsize=(12, 6))
        gs = gridspec.GridSpec(
            1, 2, width_ratios=[1, 1], wspace=0.3
        )
        self.ax = self.fig.add_subplot(gs[0])
        self.ax_metrics = self.fig.add_subplot(gs[1])

    def render(
        self, step, action, visited,
        metricas=None
    ):
        # --- Panel izquierdo: cuadricula ---
        self.ax.clear()

        self.ax.imshow(
            self.grid,
            cmap="Blues",
            vmin=0,
            vmax=1.5,
            aspect="equal"
        )

        # Ajustar limites para que las celdas queden centradas
        self.ax.set_xlim(-0.5, 2.5)
        self.ax.set_ylim(2.5, -0.5)

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
            f"Paso: {step} | Accion: {action}",
            pad=20,
            fontsize=13,
            weight="bold"
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

        # --- Panel derecho: metricas ---
        self.ax_metrics.clear()
        self.ax_metrics.axis("off")

        self.ax_metrics.set_title(
            "Metricas de Rendimiento",
            pad=20,
            fontsize=13,
            weight="bold"
        )

        if metricas is not None:
            lineas = metricas
        else:
            lineas = ["Esperando inicio..."]

        # Posicion vertical inicial y espaciado
        y_start = 0.92
        y_step = 0.065

        for idx, linea in enumerate(lineas):
            y_pos = y_start - idx * y_step

            # Detectar lineas de encabezado (empiezan con ─)
            if linea.startswith("─"):
                self.ax_metrics.text(
                    0.05, y_pos, linea,
                    transform=self.ax_metrics.transAxes,
                    fontsize=8,
                    color="#888888",
                    fontfamily="monospace",
                    verticalalignment="top"
                )
            # Detectar lineas con valor (contienen ":")
            elif ":" in linea:
                partes = linea.split(":", 1)
                etiqueta = partes[0] + ":"
                valor = partes[1]

                self.ax_metrics.text(
                    0.05, y_pos, etiqueta,
                    transform=self.ax_metrics.transAxes,
                    fontsize=9,
                    color="#333333",
                    fontfamily="monospace",
                    verticalalignment="top"
                )
                self.ax_metrics.text(
                    0.65, y_pos, valor.strip(),
                    transform=self.ax_metrics.transAxes,
                    fontsize=9,
                    color="#0066cc",
                    weight="bold",
                    fontfamily="monospace",
                    verticalalignment="top"
                )
            else:
                self.ax_metrics.text(
                    0.05, y_pos, linea,
                    transform=self.ax_metrics.transAxes,
                    fontsize=9,
                    color="#333333",
                    fontfamily="monospace",
                    verticalalignment="top"
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

        if action == "Suck":
            self.grid[fila, columna] = 0

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
    def __init__(self):
        # Memoria de posiciones visitadas
        self.visited = set()

        # Camino actual para poder retroceder
        self.path = []

    def act(self, percept):
        pos, status = percept
        pos = tuple(pos)

        # Registrar posicion inicial
        if not self.path:
            self.path.append(pos)
            self.visited.add(pos)

        # Limpiar si la casilla esta sucia
        if status == 1:
            return "Suck"

        fila, columna = pos

        # Posiciones vecinas
        vecinos = {
            "Up": (fila - 1, columna),
            "Down": (fila + 1, columna),
            "Left": (fila, columna - 1),
            "Right": (fila, columna + 1)
        }

        # Filtrar movimientos validos
        movimientos_validos = {
            accion: destino
            for accion, destino in vecinos.items()
            if 0 <= destino[0] < 3
            and 0 <= destino[1] < 3
        }

        # Buscar casillas nuevas
        movimientos_nuevos = [
            (accion, destino)
            for accion, destino in movimientos_validos.items()
            if destino not in self.visited
        ]

        # Prioridad 1: explorar casilla nueva
        if movimientos_nuevos:
            accion, destino = random.choice(
                movimientos_nuevos
            )

            self.visited.add(destino)
            self.path.append(destino)

            return accion

        # Prioridad 2: retroceder por el camino
        if len(self.path) > 1:
            self.path.pop()
            anterior = self.path[-1]

            for accion, destino in movimientos_validos.items():
                if destino == anterior:
                    return accion

        # No quedan posiciones nuevas
        return "Stop"


def calcular_metricas(
    env,
    agent,
    suciedad_inicial,
    movimientos,
    limpiezas
):
    """Calcula las metricas y devuelve una lista de
    lineas de texto para mostrar en el panel."""
    total_casillas = env.grid.size

    casillas_visitadas = len(agent.visited)
    suciedad_restante = int(np.sum(env.grid))
    casillas_limpias = total_casillas - suciedad_restante

    # 1. Porcentaje de cobertura
    cobertura = (
        casillas_visitadas / total_casillas
    ) * 100

    # 2. Porcentaje de casillas limpias
    limpieza_entorno = (
        casillas_limpias / total_casillas
    ) * 100

    # 3. Porcentaje de suciedad inicial eliminada
    if suciedad_inicial > 0:
        suciedad_eliminada = (
            (suciedad_inicial - suciedad_restante)
            / suciedad_inicial
        ) * 100
    else:
        suciedad_eliminada = 100.0

    lineas = []

    lineas.append("─── Cobertura ───")
    lineas.append(
        f"Visitadas: {casillas_visitadas}/{total_casillas}"
    )
    lineas.append(f"Cobertura: {cobertura:.1f}%")

    lineas.append("")
    lineas.append("─── Limpieza ───")
    lineas.append(
        f"Casillas limpias: {casillas_limpias}/{total_casillas}"
    )
    lineas.append(
        f"Limpieza entorno: {limpieza_entorno:.1f}%"
    )

    lineas.append("")
    lineas.append("─── Suciedad ───")
    lineas.append(
        f"Inicial: {suciedad_inicial}"
    )
    lineas.append(
        f"Restante: {suciedad_restante}"
    )
    lineas.append(
        f"Eliminada: {suciedad_eliminada:.1f}%"
    )

    lineas.append("")
    lineas.append("─── Acciones ───")
    lineas.append(f"Movimientos: {movimientos}")
    lineas.append(f"Limpiezas: {limpiezas}")

    # 4. Eficiencia del recorrido
    if casillas_visitadas == total_casillas:
        minimo_teorico = total_casillas - 1

        lineas.append("")
        lineas.append("─── Eficiencia ───")

        if movimientos > 0:
            eficiencia = (
                minimo_teorico / movimientos
            ) * 100

            lineas.append(
                f"Eficiencia: {eficiencia:.1f}%"
            )
        else:
            lineas.append("Eficiencia: N/A")

        lineas.append(
            f"Min. teorico: {minimo_teorico} mov."
        )

    return lineas


if __name__ == "__main__":
    env = VisualEnvironment3x3()
    agent = VacuumAgentWithMemory()

    # Guardar las condiciones iniciales
    suciedad_inicial = int(np.sum(env.grid))

    movimientos = 0
    limpiezas = 0

    # Metricas iniciales
    metricas = calcular_metricas(
        env, agent, suciedad_inicial,
        movimientos, limpiezas
    )
    env.render(0, "Inicio", agent.visited, metricas)

    for paso in range(1, 101):
        percept = env.get_percept()
        action = agent.act(percept)

        if action == "Stop":
            # Renderizar estado final antes de salir
            metricas = calcular_metricas(
                env, agent, suciedad_inicial,
                movimientos, limpiezas
            )
            env.render(
                paso, "Stop", agent.visited, metricas
            )
            break

        # Ejecutar la accion
        env.execute_action(action)

        # Contabilizar movimientos y limpiezas
        if action in ["Up", "Down", "Left", "Right"]:
            movimientos += 1

        elif action == "Suck":
            limpiezas += 1

        # Registrar la posicion actual
        agent.visited.add(tuple(env.agent_pos))

        # Calcular metricas actualizadas
        metricas = calcular_metricas(
            env, agent, suciedad_inicial,
            movimientos, limpiezas
        )

        # Mostrar la animacion con metricas
        env.render(paso, action, agent.visited, metricas)

        # Si todo esta limpio, detener la simulacion
        if env.is_completely_clean():
            break

    plt.ioff()
    plt.show()