import requests
from md_to_html import convert

def get_dataset(habitat_id: int) -> dict:
    """
    Télécharge les données d'un habitat de Pokémon au format JSON.

    :param habitat_id: L'ID de l'habitat à récupérer.
    :return: Un dictionnaire contenant les données de l'habitat.
    """
    url = f"https://pokeapi.co/api/v2/pokemon-habitat/{habitat_id}/"
    response = requests.get(url)
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
    return response.json()

def compute_statistics(habitat_id: int) -> dict:
    """
    Calcule des statistiques sur les Pokémon d'un habitat donné, notamment la moyenne des points de vie (PV).

    :param habitat_id: L'ID de l'habitat pour lequel calculer les statistiques.
    :return: Un dictionnaire contenant la moyenne des PV et le nombre de Pokémon.
    """
    data = get_dataset(habitat_id)
    total_hp = 0
    total_species = 0

    for species in data['pokemon_species']:
        try:
            pokemon_data = requests.get(species['url']).json()
            if 'stats' in pokemon_data:
                hp = next((stat['base_stat'] for stat in pokemon_data['stats'] if stat['stat']['name'] == 'hp'), 0)
                total_hp += hp
                total_species += 1
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données pour {species['name']}: {e}")

    average_hp = total_hp / total_species if total_species > 0 else 0
    return {
        'average_hp': average_hp,
        'total_species': total_species
    }

def dataset_to_md(dataset: dict, statistics: dict, filename: str) -> None:
    """
    Génère un fichier Markdown à partir des données de l'habitat et des statistiques calculées.

    :param dataset: Les données de l'habitat au format JSON.
    :param statistics: Les statistiques calculées (moyenne des PV, nombre de Pokémon).
    :param filename: Le nom du fichier Markdown à créer.
    """
    with open(filename, 'w') as f:
        f.write(f"# Habitat ID: {dataset['id']}\n")
        f.write(f"## Nom: {dataset['name']}\n")
        f.write(f"## Nombre d'espèces de Pokémon: {statistics['total_species']}\n")
        f.write(f"## Moyenne des PV: {statistics['average_hp']:.2f}\n")
        f.write("## Espèces de Pokémon:\n")
        for species in dataset['pokemon_species']:
            f.write(f"- {species['name']}\n")

def infos_locales(habitat_id: int) -> None:
    """
    Utilise toutes les fonctions précédentes pour télécharger un jeu de données, 
    calculer les statistiques, et construire un fichier Markdown et un fichier HTML.

    :param habitat_id: L'ID de l'habitat à analyser.
    """
    dataset = get_dataset(habitat_id)
    statistics = compute_statistics(habitat_id)
    dataset_to_md(dataset, statistics, 'habitat_data.md')
    
    # Convertir le Markdown en HTML
    convert('habitat_data.md', 'habitat_data.html')
    
    print(f"Les données pour l'habitat {habitat_id} ont été enregistrées dans 'habitat_data.md' et 'habitat_data.html'.")

# Exemple d'utilisation
if __name__ == "__main__":
    habitat_id = 2  # Remplacez par l'ID de l'habitat que vous souhaitez analyser
    infos_locales(habitat_id)