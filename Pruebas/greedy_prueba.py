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


mapa = {
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

# ----------------------- Algortimo Greedy ----------------------------------------
class Nodo:
    def __init__(self, nombre, costo):
        self.name = nombre
        self.costo = costo
    def __lt__(self, other):
        return self.costo < other.costo 
    
def solucion_greedy(grafo, inicio, meta, mapa):
    cola_prioridad = [] # Se inicializa la cola de prioridad 
    nodoIncial = Nodo(inicio, 0) # Se crea el nodo inicial de Arad con respectiva distancias 
    heapq.heappush(cola_prioridad, nodoIncial) # Se agrega Arad a la cola de prioridad

    visitados = set() # Set para llevar un control sobre los visitados y evitar ciclos repetidos
    camino = [] # Se inicializa el arreglo que llevara el camino hasta Bucharest 

    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad) # Pop del nodo con menor valor en la distancias
        cola_prioridad.clear()

        # Se van añadiendo los nodos al arreglo del camino
        if nodo_actual.name not in camino:
            camino.append(nodo_actual.name)

        # Verificamos si el nodo actual es la meta
        if nodo_actual.name == meta:
            return print(camino) 
        
        visitados.add(nodo_actual.name) # Se van añadiendo al arreglo de visitados 

        # se recorren vecinos del nodo actual 
        for vecino in grafo[nodo_actual.name]:
            if vecino not in visitados:
                costo = mapa[nodo_actual.name][vecino]
                nuevoNodo = Nodo(vecino, costo) # se crea el nodo del vecino 
                heapq.heappush(cola_prioridad, nuevoNodo)  # se agrega nodo a la cola de prioridad y se acomoda automaticamente
                
    return None


sol = solucion_greedy(ciudades, "Arad", "Bucharest", mapa)
# -----------------------------Fin Algoritmo Greedy----------------------------------------------

