import streamlit as st
import pandas as pd

class Nodo:
    def __init__(self, tablero, hijos=None, valor=None):
        self.hijos = hijos or []          # lista de Nodos o enteros (hojas)
        self.valor = valor                # -1, 0, 1 ó None
        self.tablero = tablero            # matriz 3×3 de ints

def evaluar(tablero):
    # Horizontales
    for i in range(3):
        s = sum(tablero[i])
        if s == 3:  return 1
        if s == -3: return -1
    # Verticales
    for j in range(3):
        s = sum(tablero[r][j] for r in range(3))
        if s == 3:  return 1
        if s == -3: return -1
    # Diagonales
    diag1 = tablero[0][0] + tablero[1][1] + tablero[2][2]
    diag2 = tablero[0][2] + tablero[1][1] + tablero[2][0]
    if diag1 == 3 or diag2 == 3:   return 1
    if diag1 == -3 or diag2 == -3: return -1
    # Empate
    if all(tablero[i][j] != 0 for i in range(3) for j in range(3)):
        return 0
    return None                     # no terminal

# Contador de hojas
hojas_contadas = 0

def generarArbol(n, nodito):
    global hojas_contadas
    for i in range(3):
        for j in range(3):
            if nodito.tablero[i][j] == 0:       # Casilla libre
                nuevoTablero = [fila[:] for fila in nodito.tablero]
                nuevoTablero[i][j] = 1 if (n % 2 == 1) else -1
                valorNodo = evaluar(nuevoTablero)
                nodito.hijos.append(Nodo(nuevoTablero, valor=valorNodo))
                if valorNodo is not None:      # Si es hoja, la contamos
                    hojas_contadas += 1
    for hijo in nodito.hijos:
        if hijo.valor is None:
            generarArbol(n + 1, hijo)
    return nodito

def minimax(nodo, es_maximizador):
    # Hoja
    if nodo.valor is not None:
        return nodo.valor
    # Recorre hijos
    for hijo in nodo.hijos:
        valor_hijo = minimax(hijo, not es_maximizador)
        if nodo.valor is None:
            nodo.valor = valor_hijo
        else:
            if es_maximizador:
                nodo.valor = max(nodo.valor, valor_hijo)
            else:
                nodo.valor = min(nodo.valor, valor_hijo)
    return nodo.valor

def mejor_jugada(tablero_actual, turno_maquina=-1):
    global hojas_contadas
    hojas_contadas = 0  # Reiniciar el contador de hojas
    jugados = sum(1 for i in range(3) for j in range(3) if tablero_actual[i][j] != 0)
    n_inicial = jugados + 1
    raiz = Nodo([fila[:] for fila in tablero_actual])
    generarArbol(n_inicial, raiz)   # genera árbol desde el estado actual
    minimax(raiz, es_maximizador=(turno_maquina == 1))
    # Elegir el primer hijo óptimo para O (MIN => valor mínimo)
    objetivo = min(h.valor for h in raiz.hijos)
    for h in raiz.hijos:
        if h.valor == objetivo:
            for i in range(3):
                for j in range(3):
                    if tablero_actual[i][j] != h.tablero[i][j]:
                        return i, j
    return None

# ------------------- Streamlit ----------------------

st.set_page_config(page_title="Gato contra la máquina")

# ----------- Estado global: tablero y mensaje ---------------------
if "board" not in st.session_state:
    st.session_state.board = [[0]*3 for _ in range(3)]   # 0=vacío, 1=X, -1=O
    st.session_state.message = ""
    st.session_state.hojas = 0

def reiniciar():
    st.session_state.board = [[0]*3 for _ in range(3)]
    st.session_state.message = ""
    st.session_state.hojas = 0

st.markdown("<h2 style='text-align:center;'>Tic-Tac-Toe (Gato) — Tú eres X</h2>",
            unsafe_allow_html=True)

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
                    mov = mejor_jugada(st.session_state.board, turno_maquina=-1)
                    st.session_state.hojas = hojas_contadas  # Guardar las hojas calculadas
                    if mov:
                        i, j = mov
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

st.write(f" Hojas calculadas en el árbol: **{st.session_state.hojas}**")
st.button("Reiniciar partida", on_click=reiniciar, type="primary")
