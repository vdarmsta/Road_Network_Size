import overpy
import geopandas as gpd
from shapely.geometry import LineString
import sys

def get_roads_from_overpass(commune_nom):
    """
    Récupère les routes d'une commune en Belgique depuis l'API Overpass.
    """
    # Initialiser l'API Overpass
    api = overpy.Overpass()
    
    # Requête Overpass pour récupérer les routes dans la commune en Belgique
    query = f"""
        area["name"="Belgique"]->.pays;
        area["name"="{commune_nom}"](area.pays)->.commune;
        (
            way["highway"~"motorway|trunk|primary|secondary|tertiary|unclassified|residential|living_street|track"]
            (area.commune);
        );
        out body;
        >;
        out skel qt;
    """
    
    # Exécuter la requête
    result = api.query(query)
    return result

def calculate_road_length(result):
    """
    Calcule la longueur totale du réseau routier à partir des résultats Overpass.
    """
    # Dictionnaire pour stocker les routes uniques
    unique_roads = {}
    
    # Parcourir les ways (routes) dans le résultat
    for way in result.ways:
        # Extraire les nœuds de la route
        nodes = [(float(node.lon), float(node.lat)) for node in way.nodes]
        
        # Créer une LineString à partir des nœuds
        if len(nodes) >= 2:
            line = LineString(nodes)
            
            # Utiliser l'identifiant de la route comme clé pour éviter les doublons
            unique_roads[way.id] = line
    
    # Convertir les routes uniques en GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=list(unique_roads.values()), crs="EPSG:4326")
    
    # Reprojecter en un système de coordonnées projetées (UTM pour la Belgique)
    gdf = gdf.to_crs(epsg=32631)  # UTM zone 31N pour la Belgique
    
    # Calculer la longueur totale du réseau routier
    longueur_totale = gdf.length.sum()
    
    # Retourner la longueur en kilomètres
    return longueur_totale / 1000

def main():
    """
    Fonction principale qui prend le nom de la commune comme argument.
    """
    # Vérifier que le nom de la commune est fourni en argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <nom_de_la_commune>")
        sys.exit(1)
    
    # Récupérer le nom de la commune depuis les arguments
    commune_nom = sys.argv[1]
    
    # Récupérer les routes depuis Overpass
    result = get_roads_from_overpass(commune_nom)
    
    # Calculer la longueur du réseau routier
    longueur = calculate_road_length(result)
    
    # Afficher le résultat
    print(f"La longueur du réseau routier de {commune_nom} (Belgique) est de {longueur:.2f} km.")

if __name__ == "__main__":
    main()