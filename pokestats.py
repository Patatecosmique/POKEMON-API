import requests
import markdown
from md_to_html import convert

def get_dataset(id: int) -> dict:
    """Cette fonction récupère les informations d'un habitat."""
    url = f"https://pokeapi.co/api/v2/pokemon-habitat/{id}/"
    return requests.get(url).json()

def get_pokemon_details(pokemon_name: str) -> dict:
    """Récupère les détails d'un Pokémon (y compris ses statistiques)."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    return requests.get(url).json()


def compute_statistic(dataset: dict) -> dict:
    name = dataset['name'].capitalize()
    pokemons = dataset.get("pokemon_species", [])
    total_pokemons = len(pokemons)
    pokemon_names = [pokemon["name"] for pokemon in pokemons]

    hp_values = [get_pokemon_details(name)['stats'][0]['base_stat'] for name in pokemon_names if get_pokemon_details(name) is not None]
    avg_hp = sum(hp_values) / total_pokemons if hp_values else 0
    
    # Calcul des chances de capture, stats et types
    capture_chances = []
    attack_values = []
    defense_values = []
    speed_values = []
    all_types = []

    for name in pokemon_names:
        details = get_pokemon_details(name)
        if details is not None:
            hp = details['stats'][0]['base_stat']  # HP
            attack = details['stats'][1]['base_stat']  # Attack
            defense = details['stats'][2]['base_stat']  # Defense
            speed = details['stats'][5]['base_stat']  # Speed
            
            capture_chance = max(0, 100 - (hp + defense) * 0.5)
            capture_chances.append(capture_chance)
            attack_values.append(attack)
            defense_values.append(defense)
            speed_values.append(speed)
            
            # Collecte des types
            pokemon_types = [t['type']['name'] for t in details['types']]
            all_types.append(pokemon_types)

    avg_capture_chance = sum(capture_chances) / total_pokemons if capture_chances else 0
    avg_attack = sum(attack_values) / total_pokemons if attack_values else 0
    avg_defense = sum(defense_values) / total_pokemons if defense_values else 0
    avg_speed = sum(speed_values) / total_pokemons if speed_values else 0
    
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
        "pokemon_types": all_types  # Liste de listes des types de chaque Pokémon
    }


def dataset_to_md(dataset: dict, filename: str) -> None:
    """
    Cette fonction prend le jeu de données au format JSON téléchargé depuis l’API Pokémon, 
    et produit un fichier Markdown présentant les statistiques calculées.
    """
    statistics = compute_statistic(dataset)
    
    with open(filename, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# Fiche de l'habitat {statistics['name']}\n\n")
        
        md_file.write("## Informations général\n")
        md_file.write(f"- **Nombre de Pokémon**: {statistics['total_pokemons']}\n")
        md_file.write(f"- **Noms des Pokémons**: \n")
        for name in statistics['pokemon_names']:
            md_file.write(f"        - {name}\n")
        md_file.write(f"- **PV moyen**: {statistics['avg_hp']:.2f}\n")
        md_file.write(f"- **Chance moyenne de capture**: {statistics['avg_capture_chance']:.2f}%\n")
        md_file.write(f"- **Attaque moyenne**: {statistics['avg_attack']:.2f}\n")
        md_file.write(f"- **Défense moyenne**: {statistics['avg_defense']:.2f}\n")
        md_file.write(f"- **Vitesse moyenne**: {statistics['avg_speed']:.2f}\n")
        md_file.write(f"- **Nombre de types uniques**: {statistics['unique_types']}\n")
        md_file.write("\n## Types de Pokémon\n")
        all_types = set(t for types in statistics['pokemon_types'] for t in types)
        for pokemon_type in sorted(all_types):
            md_file.write(f"- **{pokemon_type.capitalize()}**\n")

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
id_habitat = input("Entrez l'ID d'un habitat de 1 à 9 : ")

infos_locales(int(id_habitat), f"info-habitat_{id_habitat}.md", f"info-habitat_{id_habitat}.html")


