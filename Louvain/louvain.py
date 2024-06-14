import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Définition de la fonction Louvain pour la détection de communautés
def louvain(graph):
    modularity_evolution = []  # Liste pour enregistrer l'évolution de la modularité
    intra_community_density_evolution = []  # Liste pour enregistrer l'évolution de la densité intra-communautaire
    
    # Fonction pour initialiser les communautés
    def initialize_communities(graph):
        return {node: i for i, node in enumerate(graph)}

    # Fonction pour obtenir les voisins d'un nœud dans le graphe
    def neighbors(node, graph):
        return [neighbor for neighbor, _ in graph[node]]

    # Fonction pour déplacer un nœud vers une autre communauté
    def move_node(node, neighbor, communities):
        new_communities = communities.copy()
        new_communities[node] = new_communities[neighbor]
        return new_communities
    
    # Fonction pour calculer la modularité du graphe avec les communautés actuelles
    def calculate_modularity(graph, communities):   
        modularity = 0
        total_edges = sum(sum(weight for _, weight in neighbors) for neighbors in graph.values()) // 2

        for pair_communities in combinations(set(communities.values()), 2):
            fraction_intra_community = calculate_fraction_intra_community(graph, pair_communities, communities, total_edges)
            modularity += fraction_intra_community - ((calculate_weighted_edges_in_community(graph, pair_communities[0], communities) / total_edges) ** 2)
            
        return modularity
    
    # Fonction pour calculer la fraction des arêtes intra-communautaires
    def calculate_fraction_intra_community(graph, pair_communities, communities, total_edges):
        edges_intra_community = calculate_weighted_edges_between_communities(graph, pair_communities, communities)
        edges_total = calculate_weighted_edges_within_community(graph, pair_communities[0], communities)
        return edges_intra_community / edges_total if edges_total != 0 else 0

    # Fonction pour calculer le nombre total d'arêtes pondérées entre deux communautés
    def calculate_weighted_edges_between_communities(graph, pair_communities, communities):
        return sum(weight for node in graph for neighbor, weight in graph[node]
                   if communities[node] == pair_communities[0] and communities[neighbor] == pair_communities[1])

    # Fonction pour calculer le nombre total d'arêtes pondérées dans une communauté donnée
    def calculate_weighted_edges_within_community(graph, community, communities):
        return sum(weight for node in graph for neighbor, weight in graph[node]
                   if communities[node] == community and communities[neighbor] == community)

    # Fonction pour calculer le nombre total d'arêtes pondérées dans une communauté donnée
    def calculate_weighted_edges_in_community(graph, community, communities):
        return sum(weight for node in graph for neighbor, weight in graph[node]
                   if communities[node] == community)
    
    # Fonction pour calculer la densité intra-communautaire d'une communauté donnée
    def calculate_intra_community_density(graph, community, communities):
        intra_community_edges = calculate_weighted_edges_within_community(graph, community, communities)
        nodes_in_community = [node for node, comm in communities.items() if comm == community]
        possible_edges = len(nodes_in_community) * (len(nodes_in_community) - 1) / 2  # Complete graph
        return intra_community_edges / possible_edges if possible_edges != 0 else 0

    # Initialisation : chaque nœud est sa propre communauté
    communities = initialize_communities(graph)
    best_modularity = calculate_modularity(graph, communities)
    best_density = [calculate_intra_community_density(graph, community, communities) for community in set(communities.values())]
    
    # Boucle principale de l'algorithme de Louvain
    while True:
        for node in graph:
            for neighbor in neighbors(node, graph):
                new_communities = move_node(node, neighbor, communities)
                current_modularity = calculate_modularity(graph, new_communities)
                current_density = [calculate_intra_community_density(graph, community, new_communities) for community in set(new_communities.values())]

                if current_modularity > best_modularity:
                    best_modularity = current_modularity
                    best_density = current_density
                    communities = new_communities
                    modularity_evolution.append(best_modularity)
                    intra_community_density_evolution.append(best_density)
        # Si la modularité n'évolue plus, terminer
        if best_modularity == calculate_modularity(graph, communities):
            break

    return communities, modularity_evolution, intra_community_density_evolution

# Fonction pour afficher l'évolution de la modularité
def display_modularity_evolution(modularity_evolution, intra_community_density_evolution):
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(modularity_evolution)), modularity_evolution, marker='o', linestyle='-', color='b')
    plt.title('Evolution de la Modularité')
    plt.xlabel('Itération')
    plt.ylabel('Modularité')
    plt.grid(True)
    plt.xticks(range(len(modularity_evolution)))

# Fonction pour afficher l'évolution de la densité intra-communautaire
def display_intra_community_density(communities, intra_community_density_evolution, community_to_color):
    if intra_community_density_evolution:
        plt.figure(figsize=(10, 6))
        filtered_communities = [comm for i, comm in enumerate(set(communities.values())) if intra_community_density_evolution[-1][i] > 0]
        filtered_densities = [density for density in intra_community_density_evolution[-1] if density > 0]

        for i, comm in enumerate(filtered_communities):
            if comm in community_to_color:
                plt.bar(i + 1, filtered_densities[i], color=community_to_color[comm], alpha=0.7)

        plt.xlabel('Communautés')
        plt.ylabel('Densité Intra-Communautaire')
        plt.title('Densité Intra-Communautaire pour chaque communauté')
        plt.xticks(range(1, len(filtered_communities) + 1), labels=[f'{comm}' for comm in filtered_communities])
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()
    else:
        print("La liste 'intra_community_density_evolution' est vide. Assurez-vous que l'algorithme de Louvain a été exécuté avec succès.")

# Fonction pour afficher le graphe du métro de Lyon avec les communautés détectées
def commu_lyon(graph, communities):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, seed=42)
    cmap = plt.get_cmap('rainbow')
    unique_communities = set(communities.values())
    community_colors = {community: cmap(i / len(unique_communities)) for i, community in enumerate(unique_communities)}
    node_colors = [community_colors[communities[node]] for node in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos, node_size=100, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    plt.title('Graphe Métro de Lyon avec communautés')
    plt.axis('off')
    plt.show()

