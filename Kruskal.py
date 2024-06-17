import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('Treeview',
                    background='#ffffff',
                    foreground='black',
                    rowheight=30,
                    fieldbackground='#ffffff',
                    font=('Calibri', 12))
    
    style.configure('Treeview.Heading',
                    background='#10439F',
                    foreground='white',
                    font=('Calibri', 12, 'bold'))
    
    style.map('Treeview.Heading',
              background=[('active', '#874CCC'), ('pressed', '#C65BCF')])
    
    style.configure('TButton',
                    background='#10439F',
                    foreground='white',
                    font=('Calibri', 12, 'bold'),
                    padding=5)
    
    style.map('TButton',
              background=[('active', '#874CCC'), ('pressed', '#C65BCF')],
              foreground=[('active', 'white'), ('pressed', 'white')])
    
    style.configure('TLabel',
                    background='#F27BBD',
                    foreground='black',
                    font=('Calibri', 18, 'bold'))

def show_table():
    frame_welcome.pack_forget()
    frame_table.pack(fill='both', expand=True)
    root.geometry("800x600")

def modify_nodes():
    n = simpledialog.askinteger("Modificar Nodos", "Ingrese el nuevo número de nodos:", parent=root, minvalue=1, maxvalue=26)
    if n is not None:
        create_table(n)

def get_number_of_nodes():
    n = simpledialog.askinteger("Input", "Número de nodos en el grafo:", parent=root, minvalue=1, maxvalue=26)
    if n is not None:
        create_table(n)
        show_table()

def on_entry_change(row, col, entry, entries):
    value = entry.get()
    sym_entry = entries[col][row]
    if sym_entry.get() != value:
        sym_entry.delete(0, tk.END)
        sym_entry.insert(0, value)

def solve_mst(entries):
    n = len(entries)
    G = nx.Graph()
    for i in range(n):
        for j in range(i+1, n):
            value = entries[i][j].get()
            if value != '-' and value.isdigit():
                G.add_edge(i, j, weight=int(value))

    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
    show_results(entries, G, mst)

def animate_solution(graph, mst, fig, ax, pos, canvas):
    def update(num):
        ax.clear()
        nx.draw(graph, pos, with_labels=True, labels={i: str(i + 1) for i in range(len(graph))},
                node_color='#10439F', node_size=500, font_size=10, font_color='white', font_weight='bold', ax=ax)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        if num > 0:
            edges = list(mst.edges(data=True))[:num]
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v) for u, v, _ in edges], edge_color='#F27BBD', width=2, ax=ax)
            nx.draw_networkx_nodes(graph, pos, nodelist=list(set(sum(([u, v] for u, v, _ in edges), []))),
                                   node_color='#F27BBD', node_size=500, ax=ax)

    ani = FuncAnimation(fig, update, frames=len(mst.edges()) + 1, interval=1000, repeat=False)
    canvas.draw()

def show_results(entries, graph, mst):
    result_window = tk.Toplevel(root)
    result_window.title("Resultados del Árbol de Extensión Mínima")
    result_window.geometry("800x600")

    notebook = ttk.Notebook(result_window)
    notebook.pack(fill='both', expand=True)

    # Pestaña 1: Tabla ingresada
    frame_input_table = ttk.Frame(notebook)
    notebook.add(frame_input_table, text="Tabla Ingresada")
    n = len(entries)
    
    tree = ttk.Treeview(frame_input_table, columns=["#"] + [str(i+1) for i in range(n)], show="headings", height=n)
    tree.pack(fill='both', expand=True)
    
    tree.heading("#", text="#")
    tree.column("#", width=50, anchor='center')
    for j in range(n):
        tree.heading(str(j+1), text=str(j+1))
        tree.column(str(j+1), width=100, anchor='center')
        
    for i in range(n):
        values = [entries[i][j].get() for j in range(n)]
        tree.insert('', 'end', values=[str(i+1)] + values)

    # Pestaña 2: Gráfico del Grafo
    frame_graph = ttk.Frame(notebook)
    notebook.add(frame_graph, text="Gráfico del Grafo")
    fig, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(graph)
    labels = {i: str(i + 1) for i in range(len(graph))}
    nx.draw(graph, pos, with_labels=True, labels=labels, ax=ax, node_color='#10439F', node_size=500, font_size=10, font_color='white', font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # Botón para mostrar el grafo de solución
    solve_button = ttk.Button(frame_graph, text="Mostrar Solución óptima en el grafo", command=lambda: animate_solution(graph, mst, fig, ax, pos, canvas))
    solve_button.pack(pady=10)

    # Pestaña 3: Tabla de Solución
    frame_solution_table = ttk.Frame(notebook)
    notebook.add(frame_solution_table, text="Tabla Solución Optima")

    solution_tree = ttk.Treeview(frame_solution_table, columns=("Desde Nodo", "Hasta Nodo", "Distancia/Costo"), show="headings", height=10)
    solution_tree.pack(fill='both', expand=True)

    solution_tree.heading("Desde Nodo", text="Desde el Nodo")
    solution_tree.column("Desde Nodo", anchor='center', width=200)
    solution_tree.heading("Hasta Nodo", text="Hasta el Nodo")
    solution_tree.column("Hasta Nodo", anchor='center', width=200)
    solution_tree.heading("Distancia/Costo", text="Costo")
    solution_tree.column("Distancia/Costo", anchor='center', width=200)

    total_cost = 0
    for u, v, d in mst.edges(data=True):
        from_node = str(u + 1)
        to_node = str(v + 1)
        cost = d['weight']
        total_cost += cost
        solution_tree.insert('', 'end', values=(from_node, to_node, cost))

    # Insertar fila de coste total
    total_row_id = solution_tree.insert('', 'end', values=("Solución óptima", "", total_cost))
    solution_tree.item(total_row_id, tags=('total_row',))

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Calibri', 12, 'bold'))
    style.configure("Treeview", font=('Calibri', 12), rowheight=30)
    style.configure("Treeview", font=('Calibri', 12), rowheight=30)
    style.configure('total_row.Treeview', font=('Calibri', 12, 'bold'))

    solution_tree.tag_configure('total_row', font=('Calibri', 12, 'bold'))

    solution_tree.pack(fill='both', expand=True)
    
def create_table(n):
    for widget in frame_table.winfo_children():
        widget.destroy()

    frame_table.columnconfigure(0, weight=1)
    for col in range(1, n+1):
        frame_table.columnconfigure(col, weight=3)
    frame_table.rowconfigure(list(range(n+2)), weight=1)

    entries = []
    # Etiquetar las columnas
    for j in range(n):
        ttk.Label(frame_table, text=str(j+1), font=('Calibri', 12)).grid(row=0, column=j+1, sticky='nsew', padx=5, pady=5)
    # Crear las entradas y etiquetar las filas
    for i in range(n):
        ttk.Label(frame_table, text=str(i+1), font=('Calibri', 12)).grid(row=i+1, column=0, sticky='nsew', padx=5, pady=5)
        row = []
        for j in range(n):
            entry = ttk.Entry(frame_table, width=10)
            entry.grid(row=i+1, column=j+1, sticky="nsew", padx=5, pady=5)
            entry.insert(0, '-')
            entry.bind("<KeyRelease>", lambda e, row=i, col=j, entry=entry: on_entry_change(row, col, entry, entries))
            row.append(entry)
        entries.append(row)

    
    ttk.Button(frame_table, text="Resolver por árbol de extensión mínima", command=lambda: solve_mst(entries)).grid(row=n+1, column=0, columnspan=n//2+1, sticky="nsew", padx=10, pady=10)
    ttk.Button(frame_table, text="Modificar nodos", command=modify_nodes).grid(row=n+1, column=n//2+1, columnspan=n-n//2, sticky="nsew", padx=10, pady=10)

root = tk.Tk()
root.title("Solucionador árbol de extensión mínima")
root.geometry("600x400")

apply_styles()

frame_welcome = ttk.Frame(root)
frame_welcome.pack(expand=True, fill='both')

welcome_label = ttk.Label(frame_welcome, text="Solucionador árbol de extensión mínima")
welcome_label.pack(pady=5)

image_path = 'E:/Documentos/metodos/Arbol de extension minima/principal.png'
original_image = Image.open(image_path)
resized_image = original_image.resize((500, 300), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)
label_image = tk.Label(frame_welcome, image=photo)
label_image.image = photo
label_image.pack(pady=2)

start_button = ttk.Button(frame_welcome, text="Ingresar número de nodos", command=get_number_of_nodes)
start_button.pack(pady=1)

frame_table = ttk.Frame(root)

root.mainloop()
