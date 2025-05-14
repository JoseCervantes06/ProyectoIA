import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import heapq
import pandas as pd

st.markdown("<h1 style='text-align: center;'>Algoritmo Greedy</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Best-First Search</h2>", unsafe_allow_html=True)


# --- NODOS: asignamos x, e y ---
nodes = [
    Node(
        id="Arad", label="Arad\nh(A)=366",
        x=-800, y=0,                       # posición en el eje X, Y
        size=30, color="green",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Zerind", label="Zerind\nh(Z)=374",
        x=-750, y=-250,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Sibiu", label="Sibiu\nh(S)=253",
        x=-300, y=100,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Timisoara", label="Timisoara\nh(T)=329",
        x=-760, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Oradea", label="Oradea\nh(O)=380",
        x=-650, y=-500,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Lugoj", label="Lugoj\nh(L)=244",
        x=-425, y=410,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Mehadia", label="Mehadia\nh(M)=241",
        x=-390, y=650,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Drobeta", label="Drobeta\nh(D)=242",
        x=-400, y=890,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Craiova", label="Craiovah\nh(C)=160",
        x=100, y=900,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="RV", label="Rimnicu Vilcea\nh(RV)=193",
        x=-100, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Fagaras", label="Fagaras\nh(F)=176",
        x=200, y=120,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Pitesti", label="Pitesti\nh(P)=100",
        x=350, y=500,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Bucharest", label="Bucharest\nh(B)=0",
        x=750, y=670,
        size=30, color="green",
        font={"color": "white", "size": 31}
    ),
]

# --- ARISTAS: etiquetas de peso ---
edges = [
    Edge(source="Arad", target="Zerind", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Arad", target="Sibiu", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Arad", target="Timisoara", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Zerind", target="Oradea", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Oradea", target="Sibiu", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Timisoara", target="Lugoj", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Lugoj", target="Mehadia", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Mehadia", target="Drobeta", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Drobeta", target="Craiova", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Sibiu", target="RV", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="RV", target="Craiova", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Sibiu", target="Fagaras", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="RV", target="Pitesti", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Craiova", target="Pitesti", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Pitesti", target="Bucharest", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
    Edge(source="Fagaras", target="Bucharest", width=3, color="#FEC38D", font={"size":30, "strokeWidth": 0, "color":"white"}),
]

# Configuración: podemos desactivar la física global si queremos
config = Config(
    width="100%",
    height=590, # 600 para laptop
    directed=False,
    physics=False,           # sin simulación física global :contentReference[oaicite:1]{index=1}
    staticGraph=True,        # grafo estático
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    interaction={"dragNodes": False, "zoomView": False}
    
)


# Logica para los botones

# Inicializar el estado de la aplicación
if 'mostrar_ruta' not in st.session_state:
    st.session_state.mostrar_ruta = False

# Función para reiniciar el grafo
def reiniciar():
    st.session_state.mostrar_ruta = False

# --------------------------RESOLVER GREEDY---------------------------------------

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

# ----------------------- Algortimo Greedy ----------------------------------------
class Nodo:
    def __init__(self, nombre, heuristica):
        self.name = nombre
        self.heuristica = heuristica
    def __lt__(self, other):
        return self.heuristica < other.heuristica 
    
def solucion_greedy(grafo, inicio, meta, heuristica):
    cola_prioridad = [] # Se inicializa la cola de prioridad 
    nodoIncial = Nodo(inicio, heuristica[inicio]) # Se crea el nodo inicial de Arad con respectiva heuristica 
    heapq.heappush(cola_prioridad, nodoIncial) # Se agrega Arad a la cola de prioridad

    visitados = set() # Set para llevar un control sobre los visitados y evitar ciclos repetidos
    camino = [] # Se inicializa el arreglo que llevara el camino hasta Bucharest 

    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad) # Pop del nodo con menor valor en la heuristica


        # Se van añadiendo los nodos al arreglo del camino
        if nodo_actual.name not in camino:
            camino.append(nodo_actual.name)

        # Verificamos si el nodo actual es la meta
        if nodo_actual.name == meta:
            datos_camino = [(ciudad, heuristica[ciudad]) for ciudad in camino] # Tupla para poder representar la ciudad con su heuristica
            return camino, datos_camino, 
        
        visitados.add(nodo_actual.name) # Se van añadiendo al arreglo de visitados 

        # se recorren vecinos del nodo actual 
        for vecino in grafo[nodo_actual.name]:
            if vecino not in visitados:
                nuevoNodo = Nodo(vecino, heuristica[vecino]) # se crea el nodo del vecino 
                heapq.heappush(cola_prioridad, nuevoNodo)  # se agrega nodo a la cola de prioridad y se acomoda automaticamente
                
    return None



# -----------------------------Fin Algoritmo Greedy----------------------------------------------


# --- Funciones de callback ---
def resolver_ruta():
    # Calculas y guardas la solución en el estado
    camino, datos_ruta = solucion_greedy(ciudades, "Arad", "Bucharest", heuristica)
    st.session_state['solucion'] = (camino, datos_ruta)
    st.session_state['camino_encontrado'] = camino

def reiniciar():
    # Limpiar el estado
    st.session_state.pop('solucion', None)
    st.session_state.pop('camino_encontrado', None)
 
# cambiar color de grafo
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

# Dibujar grafo

agraph(nodes=nodosMostrados, edges=edges, config=config)

# Area botones

# --- CSS para personalizar el botón ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #008DC0;
        color: white;
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
        color: white !important;
        outline: none;
    }
      
    </style>
""", unsafe_allow_html=True)

# --- Botones en columnas ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Resolver ruta Arad → Bucharest",
            on_click=resolver_ruta,
            use_container_width=True
        )
    with col2:
        st.button(
            "Reiniciar",
            on_click=reiniciar,
            use_container_width=True
        )

# --- Contenedor para la solución ---
resultado_slot = st.empty()


# --- Mostrar solución si ya fue calculada ---
if 'solucion' in st.session_state:
    with resultado_slot.container():
        st.subheader("Solución encontrada")
        camino, datos_ruta = st.session_state['solucion']
        
        # Crear DataFrame para mostrar la tabla
        df = pd.DataFrame(datos_ruta, columns=["Ciudad", "Heurística (h)"])
        
        # Mostrar tabla con estilo
        st.dataframe(df.style.format({"Heurística (h)": "{:.0f}"}), 
                    use_container_width=True)