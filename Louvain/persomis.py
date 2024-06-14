import networkx as nx
import matplotlib.pyplot as plt
from louvain import *

# Lecture du fichier 'relationsMIS.txt' pour obtenir les relations entre les personnages
with open('Louvain\\relationsMIS.txt', 'r') as fichier:
    relations = {}

    for longueur in fichier:
        longueur = longueur.strip()  # Supprimer les espaces et les sauts de ligne
        if longueur:  # Vérifier si la ligne n'est pas vide
            parties = longueur.split(';')

            for partie in parties:
                if ':' in partie:  # Vérifier si la partie contient ':'
                    X, YZ = partie.split(':', 1)  # Limiter la division à la première occurrence de ':'
                    X = int(X)
                    Y, Z = map(int, YZ[1:-1].split(','))
                    if X not in relations:
                        relations[X] = []
                    relations[X].append((Y, Z))

# Fonction pour charger les noms des personnages à partir du fichier 'personnagesMIS.txt'
def charger_personnages():
    personnages = {}
    with open('Louvain\\personnagesMIS.txt', 'r') as file:
        content = file.read()
        try:
            personnages = eval(content)
        except (SyntaxError, NameError):
            print("Erreur dans le fichier")
    return personnages

# Charger les noms des personnages
personnages = charger_personnages()

# Initialisation d'un graphe vide
G = nx.Graph()

# Ajout des nœuds et des arêtes au graphe en utilisant les noms des personnages
for X, liste_relations in relations.items():
    for (Y, Z) in liste_relations:
        nom_x = personnages[X]  # Obtenir le nom du personnage pour X
        nom_y = personnages[Y]  # Obtenir le nom du personnage pour Y
        G.add_node(nom_x)  # Ajouter le nœud X par son nom
        G.add_node(nom_y)  # Ajouter le nœud Y par son nom
        G.add_edge(nom_x, nom_y, weight=Z)  # Ajouter une arête avec le poids Z

# Création d'un dictionnaire qui associe chaque nœud à une liste de ses voisins et de leur poids
graph_dict = {node: [(neighbor, data['weight']) for neighbor, data in G[node].items()] for node in G.nodes()}

# Utilisation de l'algorithme de Louvain pour détecter les communautés
communities, modularity_evolution, intra_community_density_evolution = louvain(graph_dict)

# Génération d'une palette de couleurs pour les communautés
unique_communities = set(communities.values())
cmap = plt.get_cmap('rainbow')  # Utiliser get_cmap pour récupérer la colormap
community_to_color = {comm: cmap(i / (len(unique_communities) - 1))  # Créer un dictionnaire associant chaque communauté unique à une couleur
                      for i, comm in enumerate(unique_communities)}

# Coloration des nœuds en fonction de leur communauté
node_colors = [community_to_color[communities[node]] for node in G.nodes()]

# Dessin du graphe
plt.figure(figsize=(12, 12))
pos = nx.kamada_kawai_layout(G)  # choix du layout
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=200, alpha=0.8)
nx.draw_networkx_edges(G, pos, alpha=0.2)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.axis('off')  # Pour ne pas afficher le cadre autour du graphe
plt.show()

# Affichage de l'évolution de la modularité et de la densité intra-communautaire
display_modularity_evolution(modularity_evolution, intra_community_density_evolution)
display_intra_community_density(communities, intra_community_density_evolution, community_to_color)