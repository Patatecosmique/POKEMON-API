import requests
import markdown
from md_to_html import convert

def get_dataset(id: int) -> dict:
    """Cette fonction récupère les informations d'un habitat."""

    url = f"https://pokeapi.co/api/v2/pokemon-habitat/{id}/"
    return requests.get(url).json()

def get_pokemon_details(pokemon_name: str) -> dict:
    """Récupère les détails d'un Pokémon (y compris ses statistiques et l'URL de son image)."""

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # l'URL de l'image
        data['image_url'] = data['sprites']['front_default']
        return data


def compute_statistic(dataset: dict) -> dict:
    """Cette fonction calcule les statistiques d'un habitat donné."""

    # Récupération du nom de l'habitat
    name = dataset['name'].capitalize()

    # Nom des pokemons vivant dans l'habitat
    pokemons = dataset.get("pokemon_species", [])
    total_pokemons = len(pokemons)

    # Création d'une liste de pokemon
    pokemon_names = []
    for pokemon in pokemons:
        pokemon_names.append(pokemon["name"])

    # Création d'un dictionnaire pour les statistiques HP
    hp_values = []
    for name in pokemon_names:
        details = get_pokemon_details(name)
        if details:
            hp_values.append(details['stats'][0]['base_stat'])

    # Calcul de la moyenne des HP
    if hp_values:
        avg_hp = sum(hp_values) / total_pokemons
    else:
        avg_hp = 0  
    
    capture_chances = []
    attack_values = []
    defense_values = []
    speed_values = []
    all_types = []


    # Création d'un dictionnaire pour les statistiques d'attaque
    for name in pokemon_names:

        details = get_pokemon_details(name)

        # Récupération des stats de base
        stats = details['stats']
        hp = stats[0]['base_stat']
        attack = stats[1]['base_stat']
        defense = stats[2]['base_stat']
        speed = stats[5]['base_stat']

        # Calcul de la chance de capture
        capture_chance = max(0, 100 - (hp + defense) * 0.5)

        # Ajout des valeurs aux listes correspondantes
        capture_chances.append(capture_chance)
        attack_values.append(attack)
        defense_values.append(defense)
        speed_values.append(speed)

            # Collecte des types
        pokemon_types = [t['type']['name'] for t in details['types']]
        all_types.append(pokemon_types)


        if capture_chances:
            avg_capture_chance = sum(capture_chances) / total_pokemons
        else:
            avg_capture_chance = 0 

        if attack_values:
            avg_attack = sum(attack_values) / total_pokemons
        else:
            avg_attack = 0

        if defense_values:
            avg_defense = sum(defense_values) / total_pokemons
        else:
            avg_defense = 0

        if speed_values:
            avg_speed = sum(speed_values) / total_pokemons
        else:
            avg_speed = 0
    
    return {
        "name": name, 
        "total_pokemons": total_pokemons, 
        "pokemon_names": pokemon_names, 
        "avg_hp": avg_hp,
        "avg_capture_chance": avg_capture_chance,
        "avg_attack": avg_attack,
        "avg_defense": avg_defense,
        "avg_speed": avg_speed,
        "unique_types": len(set(t for ts in all_types for t in ts)),
        "pokemon_types": all_types  
    }


def dataset_to_md(dataset: dict, filename: str) -> None:
    """
    Cette fonction prend le jeu de données au format JSON téléchargé depuis l’API Pokémon, 
    et produit un fichier Markdown présentant les statistiques calculées.
    """
    statistics = compute_statistic(dataset)
    
    with open(filename, 'w', encoding='utf-8') as md_file:
        # En-tête
        md_file.write(f"# Fiche de l'habitat {dataset['name'].capitalize()}\n\n")

        # Statistiques
        md_file.write("## Informations générales\n")
        md_file.write(f"- **Nombre de Pokémon**: {statistics['total_pokemons']}\n")

        # Calcul des statistiques
        md_file.write(f"- **PV moyen**: {statistics['avg_hp']:.2f}\n") # arrondir à 2 décimales
        md_file.write(f"- **Chance moyenne de capture**: {statistics['avg_capture_chance']:.2f}%\n")
        md_file.write(f"- **Attaque moyenne**: {statistics['avg_attack']:.2f}\n")
        md_file.write(f"- **Défense moyenne**: {statistics['avg_defense']:.2f}\n")
        md_file.write(f"- **Vitesse moyenne**: {statistics['avg_speed']:.2f}\n")
        
        md_file.write("\n## Types des Pokémons\n")
        md_file.write(f"- **Nombre de types de pokémon**: {statistics['unique_types']}\n")

        # Récupérer les types de Pokémon
        types_uniques = {t for ts in statistics['pokemon_types'] for t in ts}
        for type_pokemon in types_uniques:
            md_file.write(f"- **{type_pokemon.capitalize()}**\n")
        md_file.write(f"- **Noms des Pokémons**: \n")

        # Liste des noms de Pokémon
        for name in statistics['pokemon_names']:
            details = get_pokemon_details(name)  # Récupérer les détails pour chaque Pokémon
            if details and 'image_url' in details:
                md_file.write(f"    - {name}\n")
                md_file.write(f"      <div>") # Pour coller les images des pokémons a gauche
                md_file.write(f"<img src='{details['image_url']}' alt='{name}' width='100' height='100'>\n")
            else:
                md_file.write(f"    - {name}\n")
                md_file.write("(Image non disponible)\n")
        
        
def infos_locales(habitat_id: int, markdown_filename: str, html_filename: str) -> None:
    """
    Cette fonction utilise toutes les fonctions précédentes pour télécharger un jeu de données,
    calculer des statistiques, et produire des fichiers Markdown et HTML.
    """
    data = get_dataset(habitat_id)
    dataset_to_md(data, markdown_filename)
    convert(markdown_filename, html_filename)
    print(f"Fiche générée: {html_filename}")

# Demande à l'utilisateur de saisir l'ID d'un Habitat
id_habitat = int(input("Entrez l'ID d'un habitat de 1 à 9 : "))

# si le nomnre entree et pas entre 1 et 9 , on affiche un message d'erreur
if 1 <= id_habitat <= 9:
    infos_locales(id_habitat, f"info-habitat_{id_habitat}.md", f"info-habitat_{id_habitat}.html")
else:
    print("Erreur : L'ID doit être entre 1 et 9.")




