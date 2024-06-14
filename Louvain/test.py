import networkx as nx
import matplotlib.pyplot as plt
from louvain import *

# Initialisation du graphe pour le réseau de métro de Lyon avec les temps de trajet
metro_lyon = nx.Graph()

# Données pour les lignes de métro avec temps de trajet
lignes = {
    'A': {
        ('Perrache', 'Ampère'): 3,
        ('Ampère', 'Bellecour'): 2,
        ('Bellecour', 'Cordeliers'): 2,
        ('Cordeliers', 'Hôtel de Ville'): 3,
        ('Hôtel de Ville', 'Foch'): 4,
        ('Foch', 'Charpennes'): 5,
        ('Charpennes', 'Masséna'): 3,
        ('Masséna', 'République - Villeurbanne'): 4,
        ('République - Villeurbanne', 'Gratte-Ciel'): 3,
        ('Gratte-Ciel', 'Flachet - Alain Gilles'): 4,
        ('Flachet - Alain Gilles', 'Cusset'): 3,
        ('Cusset', 'Laurent Bonnevay - Astroballe'): 3,
        ('Laurent Bonnevay - Astroballe', 'Vaulx-en-Velin - La Soie'): 4
    },
    'B': {
        ('Charpennes', 'Brotteaux'): 3,
        ('Brotteaux', 'Part-Dieu'): 2,
        ('Part-Dieu', 'Place Guichard'): 2,
        ('Place Guichard', 'Saxe - Gambetta'): 3,
        ('Saxe - Gambetta', 'Jean Macé'): 4,
        ('Jean Macé', 'Debourg'): 5
    },
    'C': {
        ('Hôtel de Ville', 'Croix-Paquet'): 3,
        ('Croix-Paquet', 'Croix-Rousse'): 2,
        ('Croix-Rousse', 'Hénon'): 3,
        ('Hénon', 'Cuire'): 4
    },
    'D': {
        ('Gorge de Loup', 'Vieux Lyon'): 2,
        ('Vieux Lyon', 'Bellecour'): 2,
        ('Bellecour', 'Saxe - Gambetta'): 3,
        ('Saxe - Gambetta', 'Guillotière - Gabriel Péri'): 2,
        ('Guillotière - Gabriel Péri', 'Sans Souci'): 3,
        ('Sans Souci', 'Grange Blanche'): 4,
        ('Grange Blanche', 'Laënnec'): 3,
        ('Laënnec', 'Mermoz - Pinel'): 3,
        ('Mermoz - Pinel', 'Parilly'): 4,
        ('Parilly', 'Gare de Vénissieux'): 3
    },
    'E': {
        ('Vieux Lyon', 'Perrache'): 3,
        ('Perrache', 'Stade de Gerland'): 3,
        ('Stade de Gerland', 'Debourg'): 4
    }
}

# Palette de couleurs pour chaque ligne
couleurs_lignes = {
    'A': 'red',
    'B': 'blue',
    'C': 'green',
    'D': 'orange',
    'E': 'purple'
}

# Ajout des stations et des connexions au graphe avec les temps comme poids et les lignes comme attributs
for ligne, connexions in lignes.items():
    for stations, temps in connexions.items():
        metro_lyon.add_edge(*stations, weight=temps, ligne=ligne)


def afficher_graphe(graphe):
    pos = nx.spring_layout(graphe, seed=42)
    edges = graphe.edges(data=True)

    nx.draw_networkx_nodes(graphe, pos, node_size=50, node_color="lightblue")
    for ligne, couleur in couleurs_lignes.items():
        nx.draw_networkx_edges(graphe, pos, edgelist=[(u, v) for u, v, d in edges if d['ligne'] == ligne], width=2, edge_color=couleur)
    
    label_pos = {key: [value[0], value[1] + 0.05] for key, value in pos.items()}
    nx.draw_networkx_labels(graphe, label_pos, font_size=8, font_weight="bold")

    plt.title("Réseau de métro de Lyon")
    plt.axis('off')
    plt.show()

afficher_graphe(metro_lyon)

graph_dict = {node: [(neighbor, data['weight']) for neighbor, data in metro_lyon[node].items()] for node in metro_lyon.nodes()}
G = nx.Graph()

# Utilisation de l'algorithme de Louvain sur le dictionnaire graph_dict
communities, modularity_evolution, intra_community_density_evolution = louvain(graph_dict)

# Génération d'une palette de couleurs pour les communautés
unique_communities = set(communities.values())

# Utiliser get_cmap pour récupérer la colormap
cmap = plt.get_cmap('rainbow')  

# On donne une couleur à chaque communauté en utilisant directement la colormap
# Crée un dictionnaire qui associe chaque communauté unique à une couleur
community_to_color = {
    comm: cmap(i / (len(unique_communities) - 1))  
    for i, comm in enumerate(unique_communities)
}

# Coloration des nœuds en fonction de leur communauté
node_colors = [community_to_color[communities[node]] for node in G.nodes()]

# Affichage de l'évolution de la modularité et de la densité intra-communautaire
display_modularity_evolution(modularity_evolution, intra_community_density_evolution)
display_intra_community_density(communities, intra_community_density_evolution,community_to_color)

# Affichage du graphe de métro de Lyon avec les communautés détectées
commu_lyon(metro_lyon, communities)