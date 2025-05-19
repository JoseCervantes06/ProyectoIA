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
        if sum(tablero[r][j] for r in range(3)) == 3: return 1
        if sum(tablero[r][j] for r in range(3)) == -3: return -1

    # Diagonal:
    if tablero[0][0] + tablero[1][1] + tablero[2][2] == 3: return 1
    if tablero[0][0] + tablero[1][1] + tablero[2][2] == -3: return -1
    if tablero[0][2] + tablero[1][1] + tablero[2][0] == 3: return 1
    if tablero[0][2] + tablero[1][1] + tablero[2][0] == -3: return -1

    if all(tablero[i][j] != 0 for i in range(3) for j in range(3)):
        return 0  # Empate

    return None

tableroInicial = [[0, 1, 0],
                [0, 0, 0],
                [0, 0, 0]]

def generarArbol(n, nodito=None):
    if n == 1:
        nodito = Nodo(tableroInicial)

    for i in range(3):
        for j in range(3):
            if nodito.tablero[i][j] == 0:
                nuevoTablero = [fila[:] for fila in nodito.tablero] 
                nuevoTablero[i][j] = (-1) ** n
                valorNodo = evaluar(nuevoTablero)
                nodito.hijos.append(Nodo(nuevoTablero, valor=valorNodo))

    for hijo in nodito.hijos:
        if hijo.valor is None:
            generarArbol(n + 1, hijo)

    return nodito

contador = 0

def minimax_alpha_beta(nodo, es_maximizador, alfa=-float('inf'), beta=float('inf')):
    global contador

    if nodo.valor is not None:
        contador += 1
        return nodo.valor

    if es_maximizador:
        max_valor = -float('inf')
        for hijo in nodo.hijos:
            valor_hijo = minimax_alpha_beta(hijo, False, alfa, beta)
            max_valor = max(max_valor, valor_hijo)
            alfa = max(alfa, max_valor)
            if alfa >= beta:
                break
        nodo.valor = max_valor
        return max_valor

    else:
        min_valor = float('inf')
        for hijo in nodo.hijos:
            valor_hijo = minimax_alpha_beta(hijo, True, alfa, beta)
            min_valor = min(min_valor, valor_hijo)
            beta = min(beta, min_valor)
            if beta <= alfa:
                break
        nodo.valor = min_valor
        return min_valor

arbol = generarArbol(1)
resultado = minimax_alpha_beta(arbol, es_maximizador=True)
print(f"Nodos evaluados: {contador}")
