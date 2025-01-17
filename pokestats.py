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
    """
    Cette fonction calcule des statistiques sur les Pokémon dans un habitat donné.
    """
    name = dataset['name'].capitalize()
    pokemons = dataset.get("pokemon_species", [])
    total_pokemons = len(pokemons)

    # Liste des noms des Pokémon
    pokemon_names = [pokemon["name"] for pokemon in pokemons]
    
    # Calcul de la moyenne des PV des Pokémon
    total_hp = sum(get_pokemon_details(name)["stats"][0]["base_stat"] for name in pokemon_names)
    avg_hp = total_hp / total_pokemons if total_pokemons > 0 else 0
    
    # Calcul des chances de capture (en pourcentage)
    capture_chance_sum = 0
    for name in pokemon_names:
        details = get_pokemon_details(name)
        hp = details['stats'][0]['base_stat']  # HP
        defense = details['stats'][2]['base_stat']  # Defense
        
        # Supposons que chaque point de HP ou Defense réduit la chance de capture de 0.1% 
        # avec un maximum de 100% de réduction pour une capture impossible (juste un exemple)
        capture_chance = max(0, 100 - (hp + defense) * 0.1)  
        capture_chance_sum += capture_chance
        
    avg_capture_chance = capture_chance_sum / total_pokemons if total_pokemons > 0 else 0
    
    return {
        "name": name, 
        "total_pokemons": total_pokemons, 
        "pokemon_names": pokemon_names, 
        "avg_hp": avg_hp,
        "avg_capture_chance": avg_capture_chance
        
    }


def dataset_to_md(dataset: dict, filename: str) -> None:
    """
    Cette fonction prend le jeu de données au format JSON téléchargé depuis l’API Pokémon, 
    et produit un fichier Markdown présentant les statistiques calculées.
    """
    statistics = compute_statistic(dataset)
    
    with open(filename, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# Fiche de l'habitat {statistics['name']}\n\n")
        
        md_file.write("## Informations\n")
        md_file.write(f"- **Nombre de Pokémon**: {statistics['total_pokemons']}\n")
        md_file.write(f"- **Noms des Pokémon**: \n")
        for name in statistics['pokemon_names']:
            md_file.write(f"{name}\n")
        md_file.write(f"- **PV moyen**: {statistics['avg_hp']:.2f}\n")
        md_file.write(f"- **Chance moyenne de capture**: {statistics['avg_capture_chance']:.2f}%\n")


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


