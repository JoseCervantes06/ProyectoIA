import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import heapq
import pandas as pd
import random



st.markdown("<h1 style='text-align: center;'>Algoritmo Hill Climbing</h1>", unsafe_allow_html=True)


st.markdown("""
<div style='text-align: justify;'>
<br>
<h3>¿Qué es el algoritmo Hill Climbing?</h3><br>
Tambien conocido como <strong>Algoritmo de Escalada Simple</strong> o <strong>Ascenso de Colinas</strong> es una tecnica de optimización perteneciente a la familia de algoritmos de busqueda local. Es un algoritmo iterativo que comienza en un nodo aleatorio, luego intenta encontar una mejor solución, es decir una mejor heurística que la del nodo actual. Si se encuentra una mejor solución, se vuelve a buscar otro cambio que sea mejor al actual, repitiendose este proceso hasta no se pueda encontrar mejoras. <br><br>

Usualmente el algoritmo <strong>Hill Climbing</strong> se utiliza para encontrar un óptimo local (una solución que ya no se puede mejorar) pero no garantiza encontrar siempre la mejor solución posible (óptimo global) de todas las posibles soluciones. <br><br>

</div>
""", unsafe_allow_html=True)


# --- NODOS: asignamos x, e y ---
nodes = [
    Node(
        id="Arad", label="Arad\nh(A)=366",
        x=-800, y=0,                       # posición en el eje X, Y
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Zerind", label="Zerind\nh(Z)=374",
        x=-750, y=-350,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Sibiu", label="Sibiu\nh(S)=253",
        x=-300, y=100,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Timisoara", label="Timisoara\nh(T)=329",
        x=-760, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Oradea", label="Oradea\nh(O)=380",
        x=-700, y=-620,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Lugoj", label="Lugoj\nh(L)=244",
        x=-425, y=350,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Mehadia", label="Mehadia\nh(M)=241",
        x=-390, y=620,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Drobeta", label="Drobeta\nh(D)=242",
        x=-400, y=890,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Craiova", label="Craiova\nh(C)=160",
        x=100, y=900,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="RV", label="Rimnicu Vilcea\nh(RV)=193",
        x=-100, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Fagaras", label="Fagaras\nh(F)=176",
        x=200, y=120,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Pitesti", label="Pitesti\nh(P)=100",
        x=350, y=500,
        size=30, color="steelblue",
        font={"color": "white", "size": 27}
    ),
    Node(
        id="Bucharest", label="Bucharest\nh(B)=0",
        x=750, y=670,
        size=30, color="red",
        font={"color": "white", "size": 27}
    ),
]

# --- ARISTAS: etiquetas de peso ---
edges = [
    Edge(source="Arad", target="Zerind", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Arad", target="Sibiu", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Arad", target="Timisoara", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Zerind", target="Oradea", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Oradea", target="Sibiu", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Timisoara", target="Lugoj", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Lugoj", target="Mehadia", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Mehadia", target="Drobeta", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Drobeta", target="Craiova", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Sibiu", target="RV", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="RV", target="Craiova", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Sibiu", target="Fagaras", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="RV", target="Pitesti", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Craiova", target="Pitesti", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Pitesti", target="Bucharest", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Fagaras", target="Bucharest", label="", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
]

# Configuración: podemos desactivar la física global si queremos
config = Config(
    width="100%",
    height=610, # 550 para laptop
    directed=False,
    physics=False,           # sin simulación física global :contentReference[oaicite:1]{index=1}
    staticGraph=True,        # grafo estático
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    interaction={"dragNodes": False, "zoomView": False}
    
)


# --------------------------RESOLVER HILL CLIMBING---------------------------------------

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

def solucionHillClimbing(grafo, inicio, meta, heuristica):
    nodo_actual = inicio # Se establece el nodo actual como el inicio del grafo 
    camino = [] # arreglo para guardar el camino 
    camino.append(nodo_actual) # por defecto se guarda el nodo de inicio 

    while True:

        # verificamos si es la meta 
        if nodo_actual == meta:
            return  camino # devolvemos el camino en un arreglo

        # obtenemos los vecinos 
        vecinos = ObtenerVecinos(nodo_actual, grafo)

        # en caso de que ya no haya mas camino
        if not vecinos:
            return camino # devolvemos el nodo en que nos quedamos 
        
        # comparamos los vecinos y sacamos el de menor valor heuristico
        mejor_vecino = min(vecinos, key = lambda ciudad: heuristica[ciudad])

        # aqui es el punto clave de hill Climbing porque se intenta encontrar una heuristica mas baja que la actual 
        if heuristica[mejor_vecino] >= heuristica[nodo_actual]:
            return camino # marcamos que no se pudo llegar a la meta porque se quedo en un punto optimo local 
        
        camino.append(mejor_vecino) # en caso de que si haya una mejor opcion entonces lo añadimos a arreglo camino
        nodo_actual = mejor_vecino # actualizamos el nodo acutal al mejor vecino que se encontro 

# --------------------------FIN ALGORITMO HILL CLIMBING-------------------


# --- Funciones de callback ---
def resolver_ruta():
    # Calculas y guardas la solución en el estado
    ciudad_aleatoria = random.choice(list(ciudades.keys()))
    camino = solucionHillClimbing(ciudades, ciudad_aleatoria, "Bucharest", heuristica)
    st.session_state['solucion'] = (camino)
    st.session_state['camino_encontrado'] = camino

def reiniciar():
    # Limpiar el estado
    st.session_state.pop('solucion', None)
    st.session_state.pop('camino_encontrado', None)

# cambiar color grafo
def actualizar_grafo(nodos_originales, camino_encontrado):
    nuevos_nodos = []
    
    for nodo in nodos_originales:
        # Copia del nodo original
        nuevo_nodo = Node(
            id=nodo.id,
            label=nodo.label,
            x=nodo.x,
            y=nodo.y,
            size=nodo.size,
            color=nodo.color,  # Color original por defecto
            font=nodo.font
        )
        
        # Si el nodo está en el camino solución, cambiar a verde
        if nodo.id in camino_encontrado:
            nuevo_nodo.color = "#4CAF50"  # Verde
        
        nuevos_nodos.append(nuevo_nodo)
    
    return nuevos_nodos


if 'camino_encontrado' in st.session_state:
    nodosMostrados = actualizar_grafo(nodes, st.session_state['camino_encontrado'])
else:
    nodosMostrados = nodes

# dibujar grafo

agraph(nodes=nodosMostrados, edges=edges, config=config)



# Botones

# CSS para personalizar el botón verde con efectos de hover y active
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #008DC0;
        color: black;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        transition: background-color 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #00569D;
    }
    div.stButton > button:first-child:active {
        background-color: #00569D;
    }
    div.stButton > button:first-child:focus {
        color: black !important;
        outline: none;
    }
      
    </style>
""", unsafe_allow_html=True)


with st.container():
        col1, col2 = st.columns(
            [1, 1]
        )

        with col1:
            st.button(
                "Resolver ruta a Bucharest",
                key=None,
                on_click=resolver_ruta,
                use_container_width=True,
            )
        with col2:
            st.button(
                "Reiniciar",
                key=None,
                on_click=reiniciar,
                use_container_width=True,
            )

# --- Contenedor para la solución ---
resultado_slot = st.empty()

if 'solucion' in st.session_state:
    camino = st.session_state['solucion']
    
    # Si el último nodo NO es Bucharest, es un óptimo local
    if camino[-1] != "Bucharest":
        st.error(f"¡Se alcanzó un óptimo local en {camino[-1]}!")
    else:
        st.success("¡Llegaste a Bucharest!")
    
    # Mostrar siempre el recorrido encontrado
    st.subheader("Recorrido ejecutado")
    df = pd.DataFrame(camino, columns=["Ciudad"])
    st.table(df)