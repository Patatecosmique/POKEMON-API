import requests
from md_to_html import convert

def get_dataset(endpoint: str) -> dict:
    """
    Récupère les données depuis l'API Pokémon en fonction de l'endpoint spécifié
    """
    url = f"https://pokeapi.co/api/v2/{endpoint}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur lors de la récupération des données: {response.status_code}")


def compute_statistics(habitats_data: dict) -> dict:
    """
    Calcule des statistiques sur les habitats et les Pokémons.
    """
    stats = {}

    # Pour chaque habitat, calculer la moyenne des HP et le % de types de Pokémons
    for habitat in habitats_data['results']:
        habitat_name = habitat['name']
        habitat_url = habitat['url']
        habitat_details = requests.get(habitat_url).json()

        # Initialisation des données pour cet habitat
        stats[habitat_name] = {
            'total_pokemons': 0,
            'total_hp': 0,
            'types_count': {}
        }

        # Parcourir les Pokémons de cet habitat
        for pokemon_species in habitat_details['pokemon_species']:
            pokemon_name = pokemon_species['name']
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
            pokemon_details = requests.get(pokemon_url).json()

            # Ajouter les HP à la somme totale
            hp = pokemon_details['stats'][0]['base_stat']
            stats[habitat_name]['total_hp'] += hp
            stats[habitat_name]['total_pokemons'] += 1

            # Compter les types de Pokémons
            for type_info in pokemon_details['types']:
                type_name = type_info['type']['name']
                if type_name in stats[habitat_name]['types_count']:
                    stats[habitat_name]['types_count'][type_name] += 1
                else:
                    stats[habitat_name]['types_count'][type_name] = 1

        # Calculer la moyenne des HP pour cet habitat
        if stats[habitat_name]['total_pokemons'] > 0:
            stats[habitat_name]['average_hp'] = stats[habitat_name]['total_hp'] / stats[habitat_name]['total_pokemons']
        else:
            stats[habitat_name]['average_hp'] = 0

        # Calculer le pourcentage de chaque type dans cet habitat
        for type_name, count in stats[habitat_name]['types_count'].items():
            stats[habitat_name]['types_count'][type_name] = (count / stats[habitat_name]['total_pokemons']) * 100

    return stats


def dataset_to_md(stats: dict, filename: str) -> None:
    """
    Génère un fichier Markdown à partir des statistiques calculées.
    """
    with open(filename, 'w') as md_file:
        # Écrire le titre principal
        md_file.write("# Statistiques sur les habitats des Pokémons\n\n")

        # Parcourir chaque habitat et écrire ses statistiques
        for habitat, data in stats.items():
            md_file.write(f"## Habitat : {habitat.capitalize()}\n")
            md_file.write(f"- **Nombre total de Pokémons** : {data['total_pokemons']}\n")
            md_file.write(f"- **Moyenne des points de vie (HP)** : {data['average_hp']:.2f}\n")
            md_file.write("- **Répartition des types de Pokémons** :\n")

            # Écrire la répartition des types
            for type_name, percentage in data['types_count'].items():
                md_file.write(f"  - {type_name.capitalize()} : {percentage:.2f}%\n")

            # Ajouter une ligne vide pour séparer les habitats
            md_file.write("\n")



def infos_locales(md_filename: str, html_filename: str) -> None:
    """
    Télécharge les données, calcule les statistiques, génère un fichier Markdown et le convertit en HTML.
    """
    # 1. Récupérer les données des habitats
    print("Téléchargement des données depuis l'API Pokémon...")
    habitats_data = get_dataset("pokemon-habitat")

    # 2. Calculer les statistiques
    print("Calcul des statistiques...")
    stats = compute_statistics(habitats_data)

    # 3. Générer le fichier Markdown
    print(f"Génération du fichier Markdown : {md_filename}...")
    dataset_to_md(stats, md_filename)

    # 4. Convertir le fichier Markdown en HTML
    print(f"Conversion du fichier Markdown en HTML : {html_filename}...")
    convert(md_filename, html_filename)  # Utilisation de la fonction convert importée

    print("Terminé ! Les fichiers ont été générés avec succès.")

