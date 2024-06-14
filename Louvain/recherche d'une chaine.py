import random
import networkx as nx


ensemble_vide = []  
def chaine(graphe, depart, arrivee):
    ensemble_vide = []
    visited = ensemble_vide()
    chemin = []
    def trouver_chemin(courant,arrivee,visited,chemin):
        visited.append(courant)
        chemin.append(courant)
        if courant == arrivee:
            return True

        for voisin in graphe[courant]:
            if voisin not in visited:
                if trouver_chemin(voisin, arrivee, visited, chemin):
                    return True

        chemin.pop()
        return False

    if trouver_chemin(graphe, depart, arrivee, visited, chemin):
        return chemin
    else:
        return None
                    
                          