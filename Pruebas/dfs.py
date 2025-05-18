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

def valid(visitados,x,y):

    filas = len(mapa) # obtenemos el numero de filas
    columnas = len(mapa[0]) # obtnemos el numero de columnas

    # en caso de que no este dentro del mapa 
    if not (0 <= x < filas and 0 <= y < columnas): 
        return False 
    
    # en caso de que ya este en visitados
    if (x,y) in visitados:
        return False
    
    # en caso de que se encuentre con obstaculos 
    if mapa[x][y] == 1:
        return False
    
    return True

movimientos = [(1,0), (-1,0), (1,0), (0,1)] # definimos los movimientos arriba, abajo, izquierda, derecha

def solucionarDFS(origen, destino):
    stack = deque() # se inicializa la pila que en este caso es una lifo Last in First Out
    stack.append(origen)
    padre = {origen:None} # diccionario para saber de donde vino cada coordenada
    visitados = set(origen) # set para guardar las coordenada ya visitadas

    while stack:

        actual = stack.pop() # sacamos el ultimo elemento ingresado en la pila

        if actual == destino: # en caso de que lleguemos al destino obtenemos el camino por el cual llego
            camino = []
            nodo = actual
            while nodo is not None:
                camino.append(nodo)
                nodo = padre[nodo]
            camino.reverse()

            return print(camino)
        
        # coordenada actuales 
        cx, cy = actual 

        # posibles movimientos
        for px, py in movimientos:
            nx, ny = cx+px, cy+py # posibles coordenadas

            if valid(visitados, nx, ny): # en caso de que las coordenadas sean validas
                visitados.add((nx,ny)) # se agregra a visitados 
                padre[(nx,ny)] = actual # guardamos de donde vino la coordenada
                stack.append((nx,ny)) # agregamos el nuevo valor a la pila 

    return False



origen = (0,0)
destino = (9,9)

sol = solucionarDFS(origen, destino)
