class Nodo:
    def __init__(self, tablero, hijos=None, valor=None):
        self.hijos = hijos or []  # lista de Nodos o enteros (hojas)
        self.valor = valor
        self.tablero = tablero

def evaluar(tablero):
    # Horizontal:
    for i in range(3):
        if sum(tablero[i]) == 3: return 1  # Victoria de X (MAX)
        if sum(tablero[i]) == -3: return -1  # Victoria de O (MIN)

    # Vertical:
    for j in range(3):
        if sum(tablero[r][j] for r in range(3)) == 3: return 1 # Victoria de X (MAX)
        if sum(tablero[r][j] for r in range(3)) == -3: return -1 # Victoria de O (MIN)

    # Diagonal:
    if tablero[0][0] + tablero[1][1] + tablero[2][2] == 3: return 1
    if tablero[0][0] + tablero[1][1] + tablero[2][2] == -3: return -1
    if tablero[0][2] + tablero[1][1] + tablero[2][0] == 3: return 1
    if tablero[0][2] + tablero[1][1] + tablero[2][0] == -3: return -1

    # Si no hay ceros en el tablero, es empate
    if all(tablero[i][j] != 0 for i in range(3) for j in range(3)):
        return 0  # Empate

    return None  # No es estado terminal

tableroInicial = [[0, 1, 0],
                [0, 0, 0],
                [0, 0, 0]]

def generarArbol(n, nodito=None):
    n = n
    if n == 1:
        nodito = Nodo(tableroInicial)
    else:
        nodito = nodito
    for i in range (3):
        for j in range(3):
            if nodito.tablero[i][j] == 0:  # Casilla libre
                nuevoTablero = [fila[:] for fila in nodito.tablero] 
                nuevoTablero[i][j] = (-1)**n
                valorNodo = evaluar(nuevoTablero) # Verifica si es hoja o no; si lo es, le asigna un valor
                nodito.hijos.append(Nodo(nuevoTablero, valor = valorNodo))
    for hijo in nodito.hijos:
        if hijo.valor is None:  # Solo expande si no es hoja
            generarArbol(n + 1, hijo)
    
    return nodito

contador = 0
def minimax(nodo, es_maximizador):
    # Caso base: hoja
    if nodo.valor is not None:
        global contador
        contador+=1
        return nodo.valor

    for hijo in nodo.hijos:
        valor_hijo = minimax(hijo, not es_maximizador)

        if nodo.valor is None:
            nodo.valor = valor_hijo
        else:
            if es_maximizador:
                print(f"Comparando para MAX: {nodo.valor} vs {valor_hijo}")
                nodo.valor = max(nodo.valor, valor_hijo)
            else:
                print(f"Comparando para MIN: {nodo.valor} vs {valor_hijo}")
                nodo.valor = min(nodo.valor, valor_hijo)
    return nodo.valor


arbol = generarArbol(1) ## 1 para que empiece X
resultado = minimax(arbol, es_maximizador=True)
print(contador)