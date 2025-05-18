from collections import deque


mapa = [
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
]


# print(len(mapa[0])) nos indica las columnas 
# print(len(mapa)) nos indica las filas 

def valid(visitados, x, y):

    filas = len(mapa)
    columnas = len(mapa[0])

    # validamos que este dentro de una coordenada valida
    if not (0 <= x < filas and 0 <= y < columnas):
        return False
    
    # que no se haya visitado ya esta coordenada
    if (x,y) in visitados:
        return False
    
    # para ignorar en caso de que se encuentre un obstaculo
    if mapa[x][y] == 1:
        return False

    return True

# definimos los movimientos que podemos hacer derecha, izquierda, arriba y abajo
movimientos = [(1,0), (-1,0), (0,1), (0,-1)]

# funcion para resolver el algoritmo 
def resolver_BFS(origen, destino):
    fifo = deque()  # fifo first in first out, cola indispensable para logar este algoritmo 
    padre = {origen:None} # diccinario para poder saber de donde viene cada coordenada y reconstruir el camino
    visitados = set() # un set para poder llevar un registro de las coordenada que ya se visitaron 
    visitados.add(origen) # añadimos como visitado la coordenada de origen 
    fifo.append(origen) # añadimos a la fifo la coordenada de origen 

    # se hace de forma iterativa el recorrido para encontrar el camino 

    # mientras la fifo no este vacia
    while fifo: 
        actual = fifo.popleft() # sacamos el primer elemento conforme se fueron añadiendo a la fifo

        # cuando ya encontremos el destino 
        if actual == destino:
            camino = [] # arreglo para trazar el camino final 
            nodo = actual 
            while nodo is not None:
                camino.append(nodo) # añadimos el nodo actual al camino
                nodo = padre[nodo] # el valor de key nodo ahora es el nodo actual. Asi sabemos de donde viene cada coordenada
            camino.reverse()

            return print(camino)
        
        cx, cy = actual # definimos las coordenadas x e y 

        for px, py in movimientos:

            nx, ny = cx + px, cy + py # los posibles caminos que puede tomar actualmente

            if valid(visitados, nx, ny): # validamos que el siguiente movimiento sea valido 
                visitados.add((nx,ny)) # si es valido entonces lo añadimos a visitados 
                padre[(nx, ny)] = actual  # añadimos la coordenada valida en el diccionario padre para saber de donde vino
                fifo.append((nx,ny)) # añadimos las coordenadas validas a la fifo
    
    return None # en caso de que no se encuentre el camino 

origen = (0,0)
destino = (9,9)

sol = resolver_BFS(origen, destino)

