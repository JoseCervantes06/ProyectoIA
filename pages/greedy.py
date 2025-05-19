import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import heapq
import pandas as pd

st.markdown("<h1 style='text-align: center;'>Algoritmo Greedy</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: justify;'>
<br>
<h3>¿Qué es el algoritmo Greedy?</h3><br>
El algoritmo <b>Greedy</b>, tambien conocido como algoritmo voraz, es una estrategia de busqueda informada, la cual consiste en elegir la opción mas optima en cada paso local con la posibilidad de llegar a la mejor solución. <br><br>
            
En resumen, toma decisiones en función de la información que esta disponible en el momento. Una vez que se toma la decisión no se vuelve a replantear en el futuro, esto hace que el algoritmo sea rapido y facil de implementar. Sin embargo, no siempre alcanza una solución optima global. <br><br>
            
En este ejemplo se utilizo un grafo ponderado para probar el algoritmo Greedy, en pocas palabras evalua solamente los vecinos del nodo actual y escoge el de menos peso en la arista. Repite lo mismo hasta encontrar la ciudad destino. 
            

</div>
""", unsafe_allow_html=True)

# --- NODOS: asignamos x, e y ---
nodes = [
    Node(
        id="Arad", label="Arad",
        x=-800, y=0,                       # posición en el eje X, Y
        size=30, color="green",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Zerind", label="Zerind",
        x=-750, y=-250,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Sibiu", label="Sibiu",
        x=-300, y=100,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Timisoara", label="Timisoara",
        x=-760, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Oradea", label="Oradea",
        x=-650, y=-500,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Lugoj", label="Lugoj",
        x=-425, y=410,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Mehadia", label="Mehadia",
        x=-390, y=650,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Drobeta", label="Drobeta",
        x=-400, y=890,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Craiova", label="Craiova",
        x=100, y=900,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="RV", label="Rimnicu Vilcea",
        x=-100, y=300,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Fagaras", label="Fagaras",
        x=200, y=120,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Pitesti", label="Pitesti",
        x=350, y=500,
        size=30, color="steelblue",
        font={"color": "white", "size": 31}
    ),
    Node(
        id="Bucharest", label="Bucharest",
        x=750, y=670,
        size=30, color="green",
        font={"color": "white", "size": 31}
    ),
]

# --- ARISTAS: etiquetas de peso ---
edges = [
    Edge(source="Arad", target="Zerind", label="75", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Arad", target="Sibiu", label="140", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Arad", target="Timisoara", label="118", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Zerind", target="Oradea", label="71", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Oradea", target="Sibiu", label="151", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Timisoara", target="Lugoj", label="111", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Lugoj", target="Mehadia", label="70", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Mehadia", target="Drobeta", label="75", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Drobeta", target="Craiova", label="120", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Sibiu", target="RV", label="80", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="RV", target="Craiova", label="146", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Sibiu", target="Fagaras", label="99", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="RV", target="Pitesti", label="97", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Craiova", target="Pitesti", label="138", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Pitesti", target="Bucharest", label="101", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
    Edge(source="Fagaras", target="Bucharest", label="211", width=2, color="#FEC38D", font={"size":30, "strokeWidth": 15, "color":"black"}),
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


mapa = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Sibiu": {"Fagaras": 99, "RV": 80, "Oradea": 151, "Arad": 140},
    "Oradea": {"Sibiu": 151, "Zerind": 71},
    "Lugoj": {"Mehadia": 70, "Timisoara": 111},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "RV": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Mehadia": {"Drobeta": 75, "Lugoj": 70},
    "Pitesti": {"Bucharest": 101, "RV": 97, "Craiova": 138},
    "Craiova": {"Pitesti": 138, "RV": 146, "Drobeta": 120},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Bucharest": {}  # No tiene conexiones 
}

# ----------------------- Algortimo Greedy ----------------------------------------
class Nodo:
    def __init__(self, nombre, costo):
        self.name = nombre
        self.costo = costo
    def __lt__(self, other):
        return self.costo < other.costo 
    
def solucion_greedy(grafo, inicio, meta, mapa):
    cola_prioridad = [] # Se inicializa la cola de prioridad 
    nodoIncial = Nodo(inicio, 0) # Se crea el nodo inicial de Arad con respectiva distancias 
    heapq.heappush(cola_prioridad, nodoIncial) # Se agrega Arad a la cola de prioridad

    visitados = set() # Set para llevar un control sobre los visitados y evitar ciclos repetidos
    camino = [] # Se inicializa el arreglo que llevara el camino hasta Bucharest 

    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad) # Pop del nodo con menor valor en la distancias

        cola_prioridad.clear()

        # Se van añadiendo los nodos al arreglo del camino
        if nodo_actual.name not in camino:
            camino.append(nodo_actual.name)

        # Verificamos si el nodo actual es la meta
        if nodo_actual.name == meta:
            return camino 
        
        visitados.add(nodo_actual.name) # Se van añadiendo al arreglo de visitados 

        # se recorren vecinos del nodo actual 
        for vecino in grafo[nodo_actual.name]:
            if vecino not in visitados:
                costo = mapa[nodo_actual.name][vecino]
                nuevoNodo = Nodo(vecino, costo) # se crea el nodo del vecino 
                heapq.heappush(cola_prioridad, nuevoNodo)  # se agrega nodo a la cola de prioridad y se acomoda automaticamente
                
    return None


# -----------------------------Fin Algoritmo Greedy----------------------------------------------


# --- Funciones de callback ---
def resolver_ruta():
    # Calculas y guardas la solución en el estado
    camino = solucion_greedy(ciudades, "Arad", "Bucharest", mapa)
    st.session_state['solucion'] = camino
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
        camino = st.session_state['solucion']
        
        df = pd.DataFrame(camino, columns=["Ciudad"])
        st.dataframe(df, use_container_width=True)
