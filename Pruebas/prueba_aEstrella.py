import heapq

ciudades = {
    "Arad": ["Zerind", "Sibiu", "Timisoara"],
    "Zerind": ["Oradea", "Arad"],
    "Timisoara": ["Arad", "Lugoj"],
    "Sibiu": ["Fagaras", "RV", "Oradea", "Arad"],
    "Oradea": ["Sibiu", "Zerind"],
    "Lugoj": ["Mehadia", "Timisoara"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "RV": ["Sibiu", "Pitesti", "Craiova"],
    "Mehadia": ["Drobeta", "Lugoj"],
    "Pitesti": ["Bucharest", "RV", "Craiova"],
    "Craiova": ["Pitesti", "RV", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Bucharest": []
}

heuristica = {
     "Arad": 366,
     "Zerind": 374,
     "Sibiu": 253,
     "Timisoara": 329,
     "Oradea": 380,
     "Lugoj": 244,
     "Mehadia": 241,
     "Drobeta": 242,
     "Craiova": 160,
     "RV": 193,
     "Pitesti": 100,
     "Fagaras": 176,
     "Bucharest": 0
}

distancias = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Sibiu": {"Fagaras": 99, "RV": 80, "Oradea": 151, "Arad": 140},
    "Oradea": {"Sibiu": 151, "Zerind": 71},
    "Lugoj": {"Mehadia": 70, "Timisoara": 111},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "RV": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Mehadia": {"Drobeta": 75, "Lugoj": 70},
    "Pitesti": {"Bucharest": 101, "RV": 97, "Craiova": 138},
    "Craiova": {"Pitesti": 138, "RV": 146, "Drobeta": 120},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Bucharest": {}  # No tiene conexiones 
}


class Nodo:
    def __init__(self, nombre, g, h, padre):
        self.name = nombre
        self.g = g
        self.h = h
        self.f = g+h
        self.padre = padre
    def __lt__(self, other):
        return self.f < other.f

def solucion_Aestrella(grafo, inicio, meta, heuristica):
    cola_prioridad = []
    nodo_inicial = Nodo(inicio, 0, heuristica[inicio], None)
    heapq.heappush(cola_prioridad, nodo_inicial)

    visitado = {} # se intenta guardar el mejor g hacia un nodo ya visitado 
    visitado[inicio] = nodo_inicial.g  # se guarda como Arad:0

    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad)
        print(f"El nodo actual es {nodo_actual.name} con valor {nodo_actual.f}")
        if nodo_actual.name == meta:
            camino = []
            costoTotal = nodo_actual.g
            ciudad = nodo_actual
            while ciudad is not None:
                camino.append(ciudad.name)
                ciudad = ciudad.padre
            camino.reverse()

            return print(camino, costoTotal, visitado)
        
        for vecino in grafo[nodo_actual.name]:
            nueva_g = nodo_actual.g + distancias[nodo_actual.name][vecino]

            if vecino not in visitado or nueva_g < visitado[vecino]:
                print(visitado)
                visitado[vecino] = nueva_g
                nuevo_nodo = Nodo(vecino, nueva_g, heuristica[vecino], nodo_actual)
                heapq.heappush(cola_prioridad, nuevo_nodo)

    return None

solucion_Aestrella(ciudades, "Arad", "Bucharest", heuristica)