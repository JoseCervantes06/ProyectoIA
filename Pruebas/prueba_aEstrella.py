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

# diccionario de diccionarios con las heuristicas
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

# se crea una clase nodo para poder guardar atributos fundamentales de cada ciudad como lo son el nombre, la heuristica, la distancia g, la funcion f y el padre que es de donde viene cada ciudad, lo cual es fundamental para reconstruir el camino
class Nodo:
    def __init__(self, nombre, g, h, padre):
        self.name = nombre
        self.g = g
        self.h = h
        self.f = g+h
        self.padre = padre
    def __lt__(self, other):
        return self.f < other.f # lower than, es importante para ordenar la cola de prioridad 

# funcion para resolver el algoritmo A*, recibe el grafo con el que se va a trabajar, el inicio, la meta y las heuristicas
def solucion_Aestrella(grafo, inicio, meta, heuristica):
    cola_prioridad = [] # se inicializa la cola de prioridad que en si pues es un arreglo ordenado
    nodo_inicial = Nodo(inicio, 0, heuristica[inicio], None) # se crea el nodo de la ciudad de inicio
    heapq.heappush(cola_prioridad, nodo_inicial) # se añade a la cola de prioridad el primer nodo

    visitado = {} # se intenta guardar el mejor g hacia un nodo ya visitado 
    visitado[inicio] = nodo_inicial.g  # se guarda como Arad:0

    # mientras la cola de prioridad no este vacia 
    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad) # se saca el menor valor de f en la cola de prioridad 
        print(f"El nodo actual es {nodo_actual.name} con valor {nodo_actual.f}") 

        # en caso de que lleguemos a la menta reconstruimos el camino
        if nodo_actual.name == meta:
            camino = [] # se inicializa un arreglo para guardar el camino
            costoTotal = nodo_actual.g # el costo total o distancia total 
            ciudad = nodo_actual 
            while ciudad is not None:
                camino.append(ciudad.name) # añadimos al arreglo los padres de cada ciudad hasta llegar al inicio 
                ciudad = ciudad.padre # ahora la ciudad es el padre 
            camino.reverse() # volteamos el arreglo para tener el camino en orden 

            return print(camino, costoTotal, visitado)
        
        # recorremos los vecinos del nodo actual (que es el de menor f)
        for vecino in grafo[nodo_actual.name]:
            # calculamos la nueva distancia recorrida hasta los vecinos 
            nueva_g = nodo_actual.g + distancias[nodo_actual.name][vecino]
            # en caso de que el vecino no este en visitados o si ya fue visitado pero resulta que el camino es mas corto 
            if vecino not in visitado or nueva_g < visitado[vecino]:
                print(visitado)
                visitado[vecino] = nueva_g # el valor de la key vecino ahora es nueva_g
                nuevo_nodo = Nodo(vecino, nueva_g, heuristica[vecino], nodo_actual) # se crea un nuevo nodo con todos sus atributos
                heapq.heappush(cola_prioridad, nuevo_nodo) # se añade el nuevo nodo a la cola de priorida donde automaticamente se acomoda por su valor en f

    return None

solucion_Aestrella(ciudades, "Arad", "Bucharest", heuristica)