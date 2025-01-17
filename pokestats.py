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
    
    return {
        "name": name, 
        "total_pokemons": total_pokemons, 
        "pokemon_names": pokemon_names, 
        "avg_hp": avg_hp
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
            md_file.write(f"  - {name}\n")
        md_file.write(f"- **PV moyen**: {statistics['avg_hp']:.2f}\n")

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
id_habitat = input("Entrez l'ID d'un habitat: ")

if id_habitat.isdigit():
    infos_locales(int(id_habitat), f"info-habitat_{id_habitat}.md", f"info-habitat_{id_habitat}.html")
else:
    print("L'ID doit être un nombre entier.")