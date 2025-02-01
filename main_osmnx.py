import osmnx as ox

def calculer_longueur_reseau(commune_nom):
    # Récupérer le réseau routier de la commune
    graph = ox.graph_from_place(commune_nom, network_type='drive')

    # Reprojecter le graphe dans un système de coordonnées projetées (UTM)
    graph_proj = ox.project_graph(graph)
    print(ox.graph_to_gdfs(graph_proj, nodes=False, edges=True).crs)

    # Simplifier le graphe en fusionnant les segments connectés
    graph_proj = ox.consolidate_intersections(graph_proj, tolerance=15, rebuild_graph=True)

    # Calculer la longueur totale du réseau routier
    edges = ox.graph_to_gdfs(graph_proj, nodes=False, edges=True)

    # Dédoublonner les arêtes en utilisant leur géométrie comme clé unique
    edges_dedoublonnees = edges.drop_duplicates(subset=['geometry'])
    
    # Calculer la longueur totale du réseau routier
    longueur_totale = edges_dedoublonnees['length'].sum()
    # longueur_totale = edges['length'].sum()

    # Retourner la longueur en kilomètres
    return longueur_totale / 1000

# Exemple d'utilisation
commune = "Rixensart, Belgique"
longueur = calculer_longueur_reseau(commune)
print(f"La longueur du réseau routier de {commune} est de {longueur:.2f} km.")