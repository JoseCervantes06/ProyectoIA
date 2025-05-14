import streamlit as st
import plotly.graph_objects as go


st.markdown("<h1 style='text-align: center;'>Algoritmo DFS </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>(Busqueda por Anchura) </h2>", unsafe_allow_html=True)

# --- Definición del tablero ---
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0],
]

# Colores: 0 → verde, 1 → rojo
colors = ['#6c9a8b', '#e07a5f']

# --- Funciones de callback ---
def resolver():
    # Ruta de ejemplo (puedes reemplazarla con la salida de tu algoritmo BFS)
    ruta = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
    st.session_state['ruta'] = ruta

def reiniciar():
    # Eliminar la ruta del estado de la sesión
    st.session_state.pop('ruta', None)

# --- Inicialización del estado ---
if 'ruta' not in st.session_state:
    st.session_state['ruta'] = None

# --- Creación del tablero con Plotly ---
fig = go.Figure(data=go.Heatmap(
    z=grid,
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
        tickvals=list(range(5)),
        fixedrange=True  # Fijar el rango del eje X
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        autorange='reversed',
        tickvals=list(range(5)),
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
# --- Sección de botones ---
    col1, col2 = st.columns(2)

    with col1:
        st.button("Resolver", on_click=resolver, use_container_width=True)

    with col2:
        st.button("Reiniciar", on_click=reiniciar, use_container_width=True)