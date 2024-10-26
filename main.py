from interface import run_interface

def load_map(map_file):
    """
    Función que carga un archivo de texto que representa el map del juego
    y lo convierte en una lista bidimensional.
    """
    try:
        with open(map_file, 'r') as file:
            map = []
            for line in file:
                fila = line.strip().split(',')
                map.append(fila)
        return map
    except FileNotFoundError:
        print(f"Error: File not found {map_file}")
        return None

if __name__ == "__main__":
    map = load_map('maps/map3.txt') 
    width = len(map[0]) 
    high = len(map)     

    # Ejecutar la interfaz gráfica
    run_interface(width, high, map)
