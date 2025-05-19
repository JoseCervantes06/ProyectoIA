import streamlit as st

pages = {
    "Algoritmos de Busqueda": [
        st.Page("pages/BFS.py", title="Algoritmo BFS"), # Algoritmo de Busqueda por Anchura
        st.Page("pages/DFS.py", title="Algoritmo DFS"), # Algoritmo de Busqueda por Profundidad 
    ],
    "Algoritmos Informados":[
        st.Page("pages/greedy.py", title="Algortimo Greedy"),
        st.Page("pages/a_estrella.py", title="Algoritmo A*"),
        st.Page("pages/hillClimbing.py", title="Algoritmo Hill Climbing"),
    ],
    "Algoritmo para Toma de Deicisiones": [
        st.Page("pages/miniMax.py", title="Algortimo Minimax"),
        st.Page("pages/alfabeta.py", title="Algortimo Minimax con poda Alfa-Beta"),
    ],
}

pg = st.navigation(pages)
pg.run()