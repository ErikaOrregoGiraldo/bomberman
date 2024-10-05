class Helpers:

    def is_adjacent(self, pos1, pos2):
        """Verifica si dos posiciones están una al lado de la otra."""
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def reconstruct_path(self, came_from, current):
        path = []
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_neighbors_in_orthogonal_order(self, pos, model):
        x, y = pos
        # Orden ortogonal: arriba, derecha, abajo, izquierda
        neighbors = [
            (x, y + 1),  # Arriba
            (x + 1, y),  # Derecha
            (x, y - 1),  # Abajo
            (x - 1, y)   # Izquierda
        ]
        # Filtrar los vecinos válidos que están dentro de los límites del mapa y son caminos
        valid_neighbors = [n for n in neighbors if model.grid.out_of_bounds(n) == False]
        return valid_neighbors