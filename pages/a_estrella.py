import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import heapq
import pandas as pd



st.markdown("<h1 style='text-align: center;'>Algoritmo A*</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: justify;'>
<br>
<h3>¿Qué es el algoritmo A*?</h3><br>
El algoritmo de <b>Búsqueda A*</b>, se clasifica dentro de los algoritmos de busqueda en grafos de tipo heurístico o informado. <br><br>

El problema de algunos algoritmos de busqueda en grafos como lo es el greedy, es que se guían solamente por el camino de menos corto a simple vista. Esto implicaría no encontrar el camino de coste más bajo. <br><br>
            
El algoritmo <strong>A*</strong> utiliza una función de evaluación 
<strong>f(n) = g(n) + h′(n)</strong>, donde 
<em>h′(n)</em> representa el valor heurístico del nodo a evaluar desde el actual, <em>n</em>, hasta el final, y 
<em>g(n)</em> el coste real del camino recorrido para llegar a dicho nodo, <em>n</em>, desde el nodo inicial. <br><br>

<strong>A*</strong> mantiene dos estructuras de datos auxiliares, que podemos denominar <em>abiertos</em> y <em>cerrados</em>. 
<em>Abiertos</em> se implementa como una cola de prioridad, ordenada por el valor <strong>f(n)</strong> de cada nodo, y <em>cerrados</em> almacena la información de los nodos que ya han sido visitados. <br><br>

Es importante tomar en cuenta que para garantizar la optimización del algoritmo, la función <strong>h(n)</strong> debe ser una heurística <em>admisible</em>, es decir, que no sobrestime el coste real de alcanzar el nodo objetivo.   

<section>
  <h3>¿A* recorre nodos innecesarios?</h3>
  <h4>1. Caso Ideal</h4>
  <ul>
    <li>
      <strong>Descubrir</strong> un nodo meta:  
      Generarlo como vecino de otro nodo e insertarlo en <em>la cola de prioridad</em> con su valor <code>f = g + h</code>.
    </li>
    <li>
      <strong>Expandir</strong> un nodo meta:  
      Sacarlo de la <em>cola de prioridad</em> (con <code>heapq.heappop</code>), marcarlo como visitado y comprobar si es el objetivo.  
      <strong>¡Aquí A* termina!</strong>
    </li>
  </ul>
</section>

<section>
  <h4>2. ¿Qué ocurre si descubro el nodo meta con un valor <code>f</code> alto?</h4>
  <ul>
    <li>
      Al descubrir el nodo meta, lo insertas en la <em>cola prioridad</em>, pero pueden existir otros nodos con <code>f</code> menor, por lo que no se extrae de inmediato.
    </li>
    <li>
      A* continúa expandiendo aquellos nodos en la <em>cola de prioridad</em> que tengan valores <code>f</code> más bajos.
    </li>
    <li>
      Si más adelante encuentras un camino más corto hasta el mismo nodo meta, su <code>g</code> (y por tanto su <code>f</code>) disminuyen:
      <ul>
        <li>Actualizas su entrada en la <em>cola de prioridad</em> con su nuevo valor <code>f</code></li>
        <li>Pasará a estar por delante de otros nodos con <code>f</code> mayor.</li>
      </ul>
    </li>
  </ul>
</section>

<p><b>Nota Importante: </b><strong>A*</strong> no termina al descubrir el nodo meta, sino <em>cuando lo extrae de la cola de prioridad</em>, garantizando que no existan rutas con <code>f</code> menor sin explorar.</p>
     

</div>
""", unsafe_allow_html=True)

# --- NODOS: asignamos x, e y ---
nodes = [
    Node(
        id="Arad", label="Arad\nh(A)=366",
        x=-800, y=0,                       # posición en el eje X, Y
        size=30, color="green",
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
        size=30, color="green",
        font={"color": "white", "size": 27}
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
    height=610, # 550 para laptop
    directed=False,
    physics=False,           # sin simulación física global :contentReference[oaicite:1]{index=1}
    staticGraph=True,        # grafo estático
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    interaction={"dragNodes": False, "zoomView": False}
    
)


# --------------------------RESOLVER A*---------------------------------------

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

distancias = {
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

class Nodo:
    def __init__(self, nombre, g, h, padre):
        self.name = nombre
        self.g = g
        self.h = h
        self.f = g+h
        self.padre = padre
    def __lt__(self, other):
        return self.f < other.f

def solucion_Aestrella(grafo, inicio, meta, heuristica):
    cola_prioridad = []
    nodo_inicial = Nodo(inicio, 0, heuristica[inicio], None)
    heapq.heappush(cola_prioridad, nodo_inicial)

    visitado = {} # se intenta guardar el mejor g hacia un nodo ya visitado 
    visitado[inicio] = nodo_inicial.g  # se guarda como Arad:0

    while cola_prioridad:
        nodo_actual = heapq.heappop(cola_prioridad)
        if nodo_actual.name == meta:
            camino = []
            costoTotal = nodo_actual.g
            ciudad = nodo_actual
            while ciudad is not None:
                camino.append(ciudad.name)
                ciudad = ciudad.padre
            camino.reverse()

            return camino, costoTotal
                
        for vecino in grafo[nodo_actual.name]:
            nueva_g = nodo_actual.g + distancias[nodo_actual.name][vecino]

            if vecino not in visitado or nueva_g < visitado[vecino]:
                visitado[vecino] = nueva_g
                nuevo_nodo = Nodo(vecino, nueva_g, heuristica[vecino], nodo_actual)
                heapq.heappush(cola_prioridad, nuevo_nodo)

    return None


# --------------------------FIN ALGORITMO A*-------------------


# --- Funciones de callback ---
def resolver_ruta():
    # Calculas y guardas la solución en el estado
    camino, costo_total = solucion_Aestrella(ciudades, "Arad", "Bucharest", heuristica)
    st.session_state['solucion'] = (camino, costo_total)
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
                "Resolver ruta Arad -> Bucharest",
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

# --- Mostrar solución si existe ---
if 'solucion' in st.session_state:
    with st.container():
        st.subheader("Solución encontrada")
        camino, costo_total = st.session_state['solucion']
        
        # Crear un contenedor centrado con ancho específico
        col1, col2, col3 = st.columns([1, 3, 1])  # Columnas para centrado (1 | 3 | 1)
        
        with col2:  # Columna central (la que contiene la tabla)
            # DataFrame con estilo
            df = pd.DataFrame(camino, columns=["Ciudad"])
            
            # Usar st.table para mejor control del ancho (opcional)
            st.table(df)
            
            
            st.success(f"**Costo total:** {costo_total}")