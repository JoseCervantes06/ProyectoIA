import streamlit as st
import plotly.graph_objects as go
from collections import deque


st.markdown("<h1 style='text-align: center;'>Algoritmo BFS </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>(Busqueda por Anchura) </h2>", unsafe_allow_html=True)

# --- Definición del tablero ---
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

# Colores: 0 → verde, 1 → rojo
colors = ['#6c9a8b', '#e07a5f']

# --------------- Algoritmo BFS -------------------------


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
        actual = fifo.popleft() # sacamos el ultimo elemento ingresado a la fifo

        # cuando ya encontremos el destino 
        if actual == destino:
            camino = [] # arreglo para trazar el camino final 
            nodo = actual 
            while nodo is not None:
                camino.append(nodo) # añadimos el nodo actual al camino
                nodo = padre[nodo] # el valor de key nodo ahora es el nodo actual. Asi sabemos de donde viene cada coordenada
            camino.reverse()

            return camino
        
        cx, cy = actual # definimos las coordenadas x e y 

        for px, py in movimientos:

            nx, ny = cx + px, cy + py # los posibles caminos que puede tomar actualmente

            if valid(visitados, nx, ny): # validamos que el siguiente movimiento sea valido 
                visitados.add((nx,ny)) # si es valido entonces lo añadimos a visitados 
                padre[(nx, ny)] = actual  # añadimos la coordenada valida en el diccionario padre para saber de donde vino
                fifo.append((nx,ny)) # añadimos las coordenadas validas a la fifo
    
    return None

# ----------------- Fin Algoritmo BFS ---------------------

# --- Funciones de callback ---
def resolver():
    origen = (0,0)
    destino = (9,9)
    # Ruta de ejemplo (puedes reemplazarla con la salida de tu algoritmo BFS)
    ruta = resolver_BFS(origen, destino)
    if ruta is not None: 
        st.session_state['ruta'] = ruta
    else: 
        st.session_state['Sin camino'] = True


def reiniciar():
    # Eliminar la ruta del estado de la sesión
    st.session_state.pop('ruta', None)
    st.session_state.pop('Sin camino', None)

# --- Inicialización del estado ---
if 'ruta' not in st.session_state:
    st.session_state['ruta'] = None

if 'Sin camino' not in st.session_state:
    st.session_state['Sin camino'] = None

# --- Creación del tablero con Plotly ---
fig = go.Figure(data=go.Heatmap(
    z=mapa,
    colorscale=[
        [0.0, colors[0]],
        [0.5, colors[0]],
        [0.5, colors[1]],
        [1.0, colors[1]],
    ],
    showscale=False,
    hoverinfo='none'
))

# Superponer la ruta si existe en el estado
if st.session_state['ruta']:
    ruta = st.session_state['ruta']
    fig.add_trace(go.Scatter(
        x=[c for _, c in ruta],
        y=[r for r, _ in ruta],
        mode='lines+markers',
        line=dict(width=4, color='gold'),
        marker=dict(size=12, color='gold'),
        hoverinfo='none'
    ))


# Configuración del diseño del gráfico
fig.update_layout(
    width=400,
    height=400,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickvals=list(range(len(mapa[0]))),
        fixedrange=True  # Fijar el rango del eje X
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        autorange='reversed',
        tickvals=list(range(len(mapa))),
        fixedrange=True  # Fijar el rango del eje Y
    ),
    margin=dict(l=20, r=20, t=20, b=20)
)

# --- Visualización del tablero ---

with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.plotly_chart(fig, use_container_width=False)
    
with st.container():
    if st.session_state['Sin camino']:
        st.error("No se encontro un camino hacia el destino")

with st.container():
# --- Sección de botones ---
    col1, col2 = st.columns(2)

    with col1:
        st.button("Resolver", on_click=resolver, use_container_width=True)

    with col2:
        st.button("Reiniciar", on_click=reiniciar, use_container_width=True)