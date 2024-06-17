# Arbol-de-extensión-minima
Implementación de un solucionador de grafos por medio del método del árbol de extensión minima en Python.

Este programa ofrece una interfaz gráfica para la construcción y análisis de grafos, permitiendo al usuario visualizar el árbol de extensión mínima (MST) de un grafo ponderado no dirigido. Utiliza la librería NetworkX para el manejo de grafos y matplotlib para la visualización, junto con Tkinter para la interfaz gráfica.

# Características

Interfaz Gráfica: Proporciona una interfaz gráfica amigable para la introducción de nodos y pesos de aristas, permitiendo visualizaciones claras y manejo directo de los datos.

Modificación Dinámica de Nodos: Permite al usuario modificar la cantidad de nodos del grafo en tiempo de ejecución.

Visualización de MST: Ofrece una animación para visualizar la construcción del árbol de extensión mínima paso a paso.

Estilos Visuales Personalizados: Utiliza estilos personalizados para mejorar la experiencia del usuario y la legibilidad de la interfaz y los datos.

# Dependencias

Para ejecutar este programa, asegúrate de tener instaladas las siguientes librerías en Python:

tkinter

Pillow

networkx

matplotlib

Puedes instalar estas dependencias utilizando pip:

pip install pillow networkx matplotlib

# Estructura del código

El código se divide en varias funciones clave:

apply_styles(): Define y aplica los estilos de los componentes de la interfaz.

get_number_of_nodes(): Solicita al usuario ingresar el número de nodos del grafo.

create_table(n): Crea una tabla dinámica para que el usuario pueda ingresar los pesos de las aristas.

solve_mst(entries): Calcula el árbol de extensión mínima utilizando Kruskal.

show_results(entries, graph, mst): Muestra los resultados en diferentes pestañas dentro de la interfaz.
