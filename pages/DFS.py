import streamlit as st
import plotly.graph_objects as go
from collections import deque

st.markdown("<h1 style='text-align: center;'>Algoritmo DFS </h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: justify;'>
<br>
<h3>¿Qué es el algoritmo DFS?</h3><br>
El algoritmo <b>DFS</b> (Depth First Search o Busqueda por Profundidad) se trata de un algoritmo de busqueda no informado. Su funcionamiento consiste en ir expandiendo todos y cada unos de los nodos que va localizando desde la raiz en un camino concreto. Cuando ya no quedan mas nodos que visitar en dicho camino, entonces regresa a la raiz de modo que repite el mismo proceso con cada uno de los hermanos del nodo ya procesado anteriormete. <br><br> 
            
Este algoritmo utiliza una Stack de tipo LIFO ("Last in First Out") con el proposito de recorrer los caminos desde las raiz hasta las hojas. 
<br><br>
En este caso, se aplica sobre un mapa parecido al juego de Frozen Lake donde <span style='color:#e07a5f;'>las celdas rojas representan obstáculos</span> y <span style='color:#6c9a8b;'>las verdes caminos transitables</span>.
</div>
""", unsafe_allow_html=True)

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

# -------------- Inicio algoritmo DFS -------------------

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

            return camino
        
        # coordenada actuales 
        cx, cy = actual 

        # posibles movimientos
        for px, py in movimientos:
            nx, ny = cx+px, cy+py # posibles coordenadas

            if valid(visitados, nx, ny): # en caso de que las coordenadas sean validas
                visitados.add((nx,ny)) # se agregra a visitados 
                padre[(nx,ny)] = actual # guardamos de donde vino la coordenada
                stack.append((nx,ny)) # agregamos el nuevo valor a la pila 

    return None

# ------------------ Fin algoritmo DFS ----------------------------

# --- Funciones de callback ---
def resolver():
    origen = (0,0)
    destino = (9,9)
    # Ruta de ejemplo (puedes reemplazarla con la salida de tu algoritmo BFS)
    ruta = solucionarDFS(origen, destino)
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
        tickvals=list(range(len(mapa))),
        fixedrange=True  # Fijar el rango del eje X
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        autorange='reversed',
        tickvals=list(range(len(mapa[0]))),
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
