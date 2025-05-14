import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.markdown("<h1 style='text-align: center;'>Algoritmo Greedy</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Grafo Personalizado</h1>", unsafe_allow_html=True)

# Definir nodos con posiciones específicas
nodes = [
    Node(id="A", label="Nodo A", size=25, color="green", font={"color": "white"}, x=0, y=0),
    Node(id="B", label="Nodo B", size=25, color="blue", font={"color": "white"}, x=150, y=100),
    Node(id="C", label="Nodo C", size=25, color="red", font={"color": "white"}, x=150, y=-100),
    Node(id="D", label="Nodo D", size=25, color="orange", font={"color": "white"}, x=300, y=0),
    Node(id="E", label="Nodo E", size=25, color="purple", font={"color": "white"}, x=450, y=100),
    Node(id="F", label="Nodo F", size=25, color="brown", font={"color": "white"}, x=450, y=-100),
    Node(id="G", label="Nodo G", size=25, color="pink", font={"color": "white"}, x=600, y=0)
]

# Definir aristas con colores personalizados
edges = [
    Edge(source="A", target="B", label="234", color="gray", font={"color": "white", "size": 18, "strokeWidth": 0, "background": "black"}),
    Edge(source="A", target="C", color="gray"),
    Edge(source="B", target="D", color="gray"),
    Edge(source="C", target="D", color="gray"),
    Edge(source="D", target="E", color="gray"),
    Edge(source="D", target="F", color="gray"),
    Edge(source="E", target="G", color="gray"),
    Edge(source="F", target="G", color="gray")
]

# Configuración del grafo
config = Config(
    width=700,
    height=400,
    directed=False,
    physics=False,  # Desactiva la simulación física
    staticGraph=True,  # Establece el grafo como estático
    staticGraphWithDragAndDrop=False,  # Desactiva el arrastre manual de nodos
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    
    interaction={
        "dragNodes": False,
        "dragView": False,
        "zoomView": False
    }
)

# Renderizar el grafo
agraph(nodes=nodes, edges=edges, config=config)
