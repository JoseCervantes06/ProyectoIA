import streamlit as st
import pandas as pd

# ------------------ Algoritmo con Poda Alfa-Beta ------------------

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

def generarArbol(n, nodito):
    for i in range(3):
        for j in range(3):
            if nodito.tablero[i][j] == 0:
                nuevoTablero = [fila[:] for fila in nodito.tablero] 
                nuevoTablero[i][j] = 1 if (n % 2 == 1) else -1
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

def mejor_jugada(tablero_actual, turno_maquina=-1):
    global contador
    contador = 0  # Reset del contador
    jugados = sum(1 for i in range(3) for j in range(3) if tablero_actual[i][j] != 0)
    n_inicial = jugados + 1
    raiz = Nodo([fila[:] for fila in tablero_actual])
    generarArbol(n_inicial, raiz)
    minimax_alpha_beta(raiz, es_maximizador=(turno_maquina == 1))
    
    objetivo = min(h.valor for h in raiz.hijos)
    for h in raiz.hijos:
        if h.valor == objetivo:
            for i in range(3):
                for j in range(3):
                    if tablero_actual[i][j] != h.tablero[i][j]:
                        return i, j, contador
    return None, None, contador

# ------------------- Streamlit ----------------------

st.set_page_config(page_title="Gato con Poda Alfa-Beta")

# ----------- Estado global: tablero y mensaje ---------------------
if "board" not in st.session_state:
    st.session_state.board = [[0]*3 for _ in range(3)]   # 0=vacío, 1=X, -1=O
    st.session_state.message = ""
    st.session_state.hojas = 0

def reiniciar():
    st.session_state.board = [[0]*3 for _ in range(3)]
    st.session_state.message = ""
    st.session_state.hojas = 0

st.markdown("<h2 style='text-align:center;'>Tic-Tac-Toe (Gato) con poda Alfa-Beta — Tú eres X</h2>",
            unsafe_allow_html=True)

st.markdown("""
<div style='text-align: justify;'>
<br>
<h3>¿Qué es el algoritmo Minimax con poda alfa-beta?</h3><br>
La poda alfa-beta es otra técnica de busqueda adicional que reduce el número de nodos evaluados en un árbol de juego hecho por el algoritmo Minimax. Es conveniente utilizarlo en juegos entre adversarios como ajedrez.  <br><br>

<h3>Tú eres X</h3>
</div>
""", unsafe_allow_html=True)

# ----------- Cuadrícula de botones (inputs) ----------------------
for r in range(3):
    cols = st.columns(3, gap="small")
    for c in range(3):
        if cols[c].button(" ", key=f"{r}-{c}"):
            if st.session_state.board[r][c] == 0 and st.session_state.message == "":
                # 1) Movimiento del jugador (X)
                st.session_state.board[r][c] = 1
                res = evaluar(st.session_state.board)
                if res == 1:
                    st.session_state.message = "¡Ganaste! 🎉"
                elif res == 0:
                    st.session_state.message = "Empate."
                else:
                    # 2) Turno de la máquina (O)
                    i, j, hojas = mejor_jugada(st.session_state.board, turno_maquina=-1)
                    st.session_state.hojas = hojas
                    if i is not None and j is not None:
                        st.session_state.board[i][j] = -1
                    res = evaluar(st.session_state.board)
                    if res == -1:
                        st.session_state.message = "Gana la computadora 😔"
                    elif res == 0:
                        st.session_state.message = "Empate."

# ----------- Mostrar el tablero como tabla (outputs) -------------
def vista(h):
    return "" if h == 0 else ("X" if h == 1 else "O")

tabla_vista = [[vista(x) for x in fila] for fila in st.session_state.board]
st.table(pd.DataFrame(tabla_vista))

# ----------- Mensaje de estado y botón Reiniciar -----------------
if st.session_state.message:
    st.success(st.session_state.message)

st.write(f"Hojas evaluadas con poda alfa-beta: **{st.session_state.hojas}**")
st.button("Reiniciar partida", on_click=reiniciar, type="primary")
