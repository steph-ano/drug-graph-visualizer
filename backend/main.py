from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import base64
import os
from typing import Optional

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GraphParams(BaseModel):
    max_nodes: Optional[int] = None
    layout_speed: str = "complete"  # "fast" o "complete"
    use_full_dataset: bool = True

@app.get("/")
def read_root():
    return {"message": "Drug Graph Visualizer API - Ready"}

@app.post("/generar-grafo")
async def generar_grafo(params: GraphParams):
    try:
        # Leer CSV
        try:
            df = pd.read_csv("drugs_side_effects_drugs_com.csv")
            df = df.dropna(subset=['drug_name', 'medical_condition'])
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="El archivo CSV no fue encontrado")

        # Limitar nodos si se especifica
        if params.max_nodes and params.max_nodes > 0:
            df = df.head(params.max_nodes * 10)  # Aproximación

        # Agrupar por condición médica
        condition_groups = df.groupby("medical_condition")["drug_name"].apply(list).to_dict()

        # Crear grafo
        G = nx.Graph()

        for drug in df["drug_name"].unique():
            G.add_node(drug)

        for condition, drugs in condition_groups.items():
            if len(drugs) > 1:
                for i in range(len(drugs)):
                    for j in range(i + 1, len(drugs)):
                        drug1 = drugs[i]
                        drug2 = drugs[j]

                        peso = 1

                        if G.has_edge(drug1, drug2):
                            G[drug1][drug2]['weight'] += peso
                        else:
                            G.add_edge(drug1, drug2, weight=peso)

        # Layout según velocidad
        iterations = 70 if params.layout_speed == "complete" else 30
        pos = nx.spring_layout(G, k=0.08, iterations=iterations, seed=42)

        weights = nx.get_edge_attributes(G, 'weight')
        max_weight = max(weights.values()) if weights else 1

        edge_widths = [weights[edge] / max_weight * 0.5 + 0.1 for edge in G.edges()]

        # Generar visualización
        plt.figure(figsize=(30, 30))

        nx.draw_networkx_nodes(G, pos,
                               node_size=5,
                               node_color="#00AEEF",
                               alpha=0.8)

        nx.draw_networkx_edges(G, pos,
                               edge_color="#333333",
                               width=edge_widths,
                               alpha=0.1)

        plt.title(f"Estructura Global de los {G.number_of_nodes()} Medicamentos y sus Relaciones",
                  size=28, color="#333333")
        plt.axis('off')
        plt.tight_layout()

        # Guardar imagen
        output_path = "grafo_output.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        # Convertir a base64
        with open(output_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        return {
            "success": True,
            "image": f"data:image/png;base64,{encoded_string}",
            "stats": {
                "nodes": G.number_of_nodes(),
                "edges": G.number_of_edges()
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando grafo: {str(e)}")

@app.get("/download-graph")
def download_graph():
    file_path = "grafo_output.png"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png", filename="grafo_medicamentos.png")
    raise HTTPException(status_code=404, detail="Grafo no encontrado. Genera uno primero.")