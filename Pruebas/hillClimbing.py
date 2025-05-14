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

# lo que diferencia este algoritmo hill Climbing es que si ver que los vecinos ya no son menores o no puede optimizarse mas entonces se queda en el mismo nodo. Obteniendo así un minimo local
# en cambio greedy sigue avanzando sin importar que no llegue al destino eficientemente. 

# funcion para obtener los vecinos del nodo actual 
def ObtenerVecinos(nodo_actual, grafo):
    vecinos = []
    for n in grafo[nodo_actual]:
        vecinos.append(n)
    return vecinos # se retorna un arreglo con los vecinos 

def solucionHillClimbing(grafo, heuristica, inicio, meta):
    nodo_actual = inicio # Se establece el nodo actual como el inicio del grafo 
    camino = [] # arreglo para guardar el camino 
    camino.append(nodo_actual) # por defecto se guarda el nodo de inicio 

    while True:

        # verificamos si es la meta 
        if nodo_actual == meta:
            return print(f"El camino a {meta} es {camino}") # devolvemos el camino en un arreglo

        # obtenemos los vecinos 
        vecinos = ObtenerVecinos(nodo_actual, grafo)

        # en caso de que ya no haya mas camino
        if not vecinos:
            return print(f"Se llego al nodo{nodo_actual}, pero no hay mas camino") # devolvemos el nodo en que nos quedamos 
        
        # comparamos los vecinos y sacamos el de menor valor heuristico
        mejor_vecino = min(vecinos, key = lambda ciudad: heuristica[ciudad])

        # aqui es el punto clave de hill Climbing porque se intenta encontrar una heuristica mas baja que la actual 
        if heuristica[mejor_vecino] >= heuristica[nodo_actual]:
            return print(f"No se encontro un camino a{meta}") # marcamos que no se pudo llegar a la meta porque se quedo en un punto optimo local 
        
        camino.append(mejor_vecino) # en caso de que si haya una mejor opcion entonces lo añadimos a arreglo camino
        nodo_actual = mejor_vecino # actualizamos el nodo acutal al mejor vecino que se encontro 


solucionHillClimbing(ciudades, heuristica, "Arad", "Bucharest")