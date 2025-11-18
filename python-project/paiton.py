import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import warnings
from difflib import get_close_matches

# Suprimir advertencias de Matplotlib (pueden ser ruidosas)
warnings.filterwarnings("ignore", category=UserWarning)

# --- Constantes y Configuración ---
DATA_FILE = "drugs_side_effects_drugs_com.csv"
# Pesos de SIMILITUD (más alto es mejor)
SIMILARITY_SAME_CONDITION_AND_CLASS = 1.0
SIMILARITY_SAME_CONDITION_ONLY = 0.7
SIMILARITY_SAME_CLASS_ONLY = 0.5

# --- 1. Carga y Construcción del Grafo ---

def load_and_build_graph():
    """
    Carga el CSV, limpia los datos y construye el grafo según las reglas
    de ponderación del proyecto (1.0, 0.7, 0.5).
    """
    print(f"Cargando dataset desde '{DATA_FILE}'...")
    try:
        # Cargar datos
        df = pd.read_csv(DATA_FILE)
        
        # Limpieza de datos (crucial para el grafo)
        cols_to_check = ['drug_name', 'medical_condition', 'drug_classes']
        df = df.dropna(subset=cols_to_check)

        # --- AÑADIR ESTA CORRECCIÓN AQUÍ ---
        # Limpiamos espacios en blanco de TODAS las columnas de texto
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].str.strip()
        # --- FIN DE LA CORRECCIÓN ---

        # Continuar con la lógica original
        df = df.drop_duplicates(subset=['drug_name'])
        df = df.set_index('drug_name')

    except FileNotFoundError:
        print(f"--- ERROR ---")
        # ... (resto del bloque except)
        return None, None

    print(f"Datos cargados. {len(df)} medicamentos únicos encontrados.")
    print("Construyendo grafo de relaciones... (Esto puede tardar unos segundos)")

    G = nx.Graph()

    # 1. Agregar todos los medicamentos como nodos con sus atributos
    for drug_name, row in df.iterrows():
        G.add_node(drug_name, **row.to_dict())

    # 2. Crear mapas para una búsqueda eficiente
    # .apply(set) es clave para comparaciones rápidas
    condition_map = df.groupby("medical_condition").groups
    class_map = df.groupby("drug_classes").groups

    edges_to_add = {} # Usamos un dict para no duplicar y guardar el MEJOR peso

    # 3. Añadir aristas
    # Pase 1: Misma condición (Similitud = 0.7)
    for condition, drugs in condition_map.items():
        for drug1, drug2 in itertools.combinations(drugs, 2):
            pair = tuple(sorted((drug1, drug2)))
            edges_to_add[pair] = SIMILARITY_SAME_CONDITION_ONLY

    # Pase 2: Misma clase (Similitud = 0.5 o 1.0)
    for d_class, drugs in class_map.items():
        for drug1, drug2 in itertools.combinations(drugs, 2):
            pair = tuple(sorted((drug1, drug2)))
            
            if pair in edges_to_add:
                # Ya existe (misma condición), actualizamos a 1.0
                edges_to_add[pair] = SIMILARITY_SAME_CONDITION_AND_CLASS
            else:
                # No existe, es solo misma clase
                edges_to_add[pair] = SIMILARITY_SAME_CLASS_ONLY

    # 4. Añadir aristas al grafo con pesos de similitud y 'costo' para Dijkstra
    for (drug1, drug2), similarity in edges_to_add.items():
        # Dijkstra necesita un "costo" (más bajo es mejor)
        # Invertimos la similitud: 1.1 - 1.0 = 0.1 (mejor costo)
        cost = 1.1 - similarity 
        
        G.add_edge(drug1, drug2, similarity=similarity, cost=cost)

    print(f"✅ Grafo construido.")
    print(f"   Nodos (Medicamentos): {G.number_of_nodes()}")
    print(f"   Aristas (Relaciones): {G.number_of_edges()}")
    
    return G, df.reset_index() # Devolvemos df al estado original

# --- 2. Funcionalidades del Aplicativo ---

def get_drug_info(df, drug_name):
    """Muestra la información detallada de un solo medicamento."""
    try:
        # Usamos .loc[0] porque df ya no tiene drug_name como índice
        info = df[df['drug_name'] == drug_name].iloc[0]
        print(f"\n--- Información de: {drug_name} ---")
        print(f"  Condición Médica: {info['medical_condition']}")
        print(f"  Clase de Droga:   {info['drug_classes']}")
        print(f"  Nombre Genérico:  {info['generic_name']}")
        print(f"  Acceso (Rx/OTC):  {info['rx_otc']}")
        print(f"  Cat. Embarazo:    {info['pregnancy_category']}")
        print(f"  CSA (Controlada): {info['csa']}")
        print(f"  Efectos Secundarios: {info['side_effects'][:100]}...")
        print("-" * (24 + len(drug_name)))
    except IndexError:
        print(f"No se encontró información para '{drug_name}'.")

def find_shortest_path(G, drug1, drug2):
    """
    FUNCIONALIDAD 1: Usa Dijkstra para encontrar el camino más corto
    (el de mayor similitud acumulada) entre dos medicamentos.
    """
    if drug1 not in G:
        print(f"Error: Medicamento '{drug1}' no encontrado en el grafo.")
        return
    if drug2 not in G:
        print(f"Error: Medicamento '{drug2}' no encontrado en el grafo.")
        return

    print(f"\nBuscando el camino de mayor similitud (Dijkstra) entre '{drug1}' y '{drug2}'...")
    
    try:
        # Usamos el 'cost' (1.1 - similitud) que creamos para Dijkstra
        path = nx.shortest_path(G, source=drug1, target=drug2, weight='cost')
        length = nx.shortest_path_length(G, source=drug1, target=drug2, weight='cost')
        
        print(f"\n---  ruta encontrada (Costo Total: {length:.2f}) ---")
        for i, drug in enumerate(path):
            print(f"  {i+1}. {drug}")
            if i < len(path) - 1:
                # Mostrar la similitud entre este nodo y el siguiente
                edge_data = G.get_edge_data(path[i], path[i+1])
                sim = edge_data['similarity']
                print(f"     | (Similitud: {sim * 100}%)")
                
    except nx.NetworkXNoPath:
        print(f"\nNo se encontró una ruta de relación entre '{drug1}' y '{drug2}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def find_alternatives(G, drug, top_n=10):
    """
    FUNCIONALIDAD 2: Encuentra los medicamentos más similares (vecinos directos)
    a un medicamento dado, ordenados por la mayor similitud.
    """
    if drug not in G:
        print(f"Error: Medicamento '{drug}' no encontrado en el grafo.")
        return

    print(f"\nBuscando las {top_n} alternativas más similares a '{drug}'...")
    
    try:
        # G[drug] devuelve todos los vecinos y sus datos de arista
        neighbors = G[drug]
        
        if not neighbors:
            print(f"'{drug}' no tiene alternativas directas registradas en el grafo.")
            return

        # Ordenar los vecinos por el atributo 'similarity' de la arista, de mayor a menor
        sorted_neighbors = sorted(
            neighbors.items(), 
            key=lambda item: item[1]['similarity'], 
            reverse=True
        )
        
        print(f"\n--- Alternativas para: {drug} (Condición: {G.nodes[drug]['medical_condition']}) ---")
        for i, (neighbor, data) in enumerate(sorted_neighbors[:top_n]):
            sim = data['similarity']
            neighbor_condition = G.nodes[neighbor]['medical_condition']
            
            print(f"  {i+1}. {neighbor} (Similitud: {sim * 100}%)")
            print(f"      Trata: {neighbor_condition}")

        # Devolvemos los nodos para el plot
        return [n for n, d in sorted_neighbors[:top_n]]

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []


def filter_by_criteria(df, cache, **kwargs):
    """
    FUNCIONALIDAD 3: Filtra el DataFrame de medicamentos usando Linear Scan
    y guarda el resultado en caché (Programación Dinámica).
    (VERSIÓN CORREGIDA para sensibilidad de mayúsculas)
    """
    # Crear una clave única para el caché basada en los filtros
    cache_key = tuple(sorted(kwargs.items()))
    
    if cache_key in cache:
        print("\n(Resultado obtenido desde el caché)")
        return cache[cache_key]
        
    print("\nRealizando búsqueda (Linear Scan)...")
    
    results = df.copy()
    
    # Aplicar cada filtro
    if 'condition' in kwargs:
        # Esta lógica ya era correcta (case=False)
        results = results[results['medical_condition'].str.contains(kwargs['condition'], case=False, na=False)]
    
    if 'preg_cat' in kwargs:
        # CORRECCIÓN: Comparamos .str.upper() == .upper()
        clean_input = kwargs['preg_cat'].upper()
        results = results[results['pregnancy_category'].str.upper() == clean_input]
        
    if 'rx_otc' in kwargs:
        # CORRECCIÓN: Comparamos .str.upper() == .upper() (Este era el error principal)
        clean_input = kwargs['rx_otc'].upper()
        results = results[results['rx_otc'].str.upper() == clean_input]

    if 'csa' in kwargs:
        # CORRECCIÓN: Comparamos .str.upper() == .upper()
        clean_input = kwargs['csa'].upper()
        results = results[results['csa'].str.upper() == clean_input]

    # Guardar en caché antes de devolver
    cache[cache_key] = results
    return results

def plot_alternatives_subgraph(G, origin_drug, alternative_nodes):
    """
    Visualiza un subgrafo con el medicamento original y sus alternativas.
    """
    if not alternative_nodes:
        print("No hay alternativas para graficar.")
        return
        
    print("\nGenerando visualización del subgrafo de alternativas...")
    
    # Nodos a incluir: el original + sus alternativas
    nodes_to_plot = [origin_drug] + alternative_nodes
    sub_g = G.subgraph(nodes_to_plot)
    
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(sub_g, k=0.8, seed=42)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(sub_g, pos, 
                           node_color=['#FF5733' if n == origin_drug else '#33A1FF' for n in sub_g.nodes()],
                           node_size=2000)
    
    # Dibujar aristas con su peso (similitud)
    nx.draw_networkx_edges(sub_g, pos, width=2, alpha=0.5, edge_color='#555555')
    
    # Etiquetas de Nodos (nombres)
    nx.draw_networkx_labels(sub_g, pos, font_size=10, font_weight='bold')
    
    # Etiquetas de Aristas (similitud)
    edge_labels = {
        (u, v): f"{d['similarity']*100:.0f}%" 
        for u, v, d in sub_g.edges(data=True)
    }
    nx.draw_networkx_edge_labels(sub_g, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title(f"Red de Alternativas para: {origin_drug}", size=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def get_valid_drug_name(G, prompt):
    """Pide un nombre al usuario y lo valida contra el grafo (case-insensitive)."""
    all_drugs = list(G.nodes())
    # Crear un diccionario para búsqueda case-insensitive
    drugs_lower = {drug.lower(): drug for drug in all_drugs}
    
    while True:
        drug_name = input(prompt).strip()
        drug_lower = drug_name.lower()
        
        # Buscar en modo case-insensitive
        if drug_lower in drugs_lower:
            return drugs_lower[drug_lower]  # Devolver el nombre original del grafo
        
        # Sugerir nombres
        matches = get_close_matches(drug_name, all_drugs, n=3, cutoff=0.7)
        if matches:
            print(f"'{drug_name}' no encontrado. Quizás quisiste decir:")
            for m in matches:
                print(f"- {m}")
        else:
            print(f"'{drug_name}' no encontrado. Intenta de nuevo.")

# --- 3. Menú Principal del Aplicativo ---

def main_menu():
    """
    Inicia el bucle principal del aplicativo de consola.
    """
    # Cargar los datos una sola vez al inicio
    G, df = load_and_build_graph()
    if G is None:
        return # Salir si el archivo no se cargó

    # Caché para la Funcionalidad 3 (Linear Scan + DP)
    filter_cache = {}

    # Advertencia requerida por el proyecto
    print("\n" + "="*70)
    print(" " * 28 + "ADVERTENCIA")
    print("Este aplicativo es un proyecto académico y no reemplaza la opinión")
    print("de un profesional de la salud. No consuma medicamentos sin")
    print("primero consultar a su médico.")
    print("="*70)

    while True:
        print("\n--- Menú Principal: Gestor de Medicamentos ---")
        print("1. Buscar camino entre dos medicamentos (Dijkstra)")
        print("2. Buscar alternativas a un medicamento")
        print("3. Filtrar medicamentos por criterios (Linear Scan)")
        print("4. Ver información de un medicamento")
        print("5. Salir")
        
        choice = input("Seleccione una opción (1-5): ").strip()

        if choice == '1':
            # --- Funcionalidad 1: Dijkstra ---
            try:
                drug1 = get_valid_drug_name(G, "Ingrese el nombre del primer medicamento: ")
                drug2 = get_valid_drug_name(G, "Ingrese el nombre del segundo medicamento: ")
                if drug1 == drug2:
                    print("Error: Los medicamentos deben ser diferentes.")
                else:
                    find_shortest_path(G, drug1, drug2)
            except Exception as e:
                print(f"Error en la entrada: {e}")

        elif choice == '2':
            # --- Funcionalidad 2: Alternativas ---
            try:
                drug_name = get_valid_drug_name(G, "Ingrese el nombre del medicamento: ")
                # Obtenemos la lista de alternativas
                alternatives = find_alternatives(G, drug_name, top_n=7)
                
                if alternatives:
                    plot_choice = input("¿Desea ver el grafo de estas alternativas? (s/n): ").strip().lower()
                    if plot_choice == 's':
                        plot_alternatives_subgraph(G, drug_name, alternatives)
            except Exception as e:
                print(f"Error en la entrada: {e}")

        elif choice == '3':
            # --- Funcionalidad 3: Filtrado ---
            print("\n--- Filtrar Medicamentos ---")
            print("(Deje en blanco para ignorar un filtro)")
            
            filters = {}
            cond = input("  Filtrar por condición (contiene): ").strip()
            preg = input("  Filtrar por Cat. Embarazo (A, B, C, D, X, N): ").strip()
            access = input("  Filtrar por Acceso (Rx, OTC, Rx/OTC): ").strip()
            csa_val = input("  Filtrar por CSA (N, M, U, 1, 2, 3, 4, 5): ").strip()

            if cond: filters['condition'] = cond
            if preg: filters['preg_cat'] = preg
            if access: filters['rx_otc'] = access
            if csa_val: filters['csa'] = csa_val

            if not filters:
                print("No se ingresaron filtros.")
                continue

            # Llamar a la función de filtrado con caché
            results_df = filter_by_criteria(df, filter_cache, **filters)
            
            if results_df.empty:
                print("\nNo se encontraron medicamentos que cumplan con todos los criterios.")
            else:
                print(f"\n--- {len(results_df)} Medicamentos Encontrados ---")
                # Mostrar solo las columnas relevantes
                cols_to_show = ['drug_name', 'medical_condition', 'pregnancy_category', 'rx_otc', 'csa']
                print(results_df[cols_to_show].to_string(index=False))

        elif choice == '4':
            # --- Info Adicional ---
            try:
                drug_name = get_valid_drug_name(G, "Ingrese el nombre del medicamento a consultar: ")
                get_drug_info(df, drug_name)
            except Exception as e:
                print(f"Error en la entrada: {e}")

        elif choice == '5':
            # --- Salir ---
            print("Saliendo del aplicativo. ¡Gracias!")
            break
            
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

# --- Ejecutar el programa ---
if __name__ == "__main__":
    main_menu()