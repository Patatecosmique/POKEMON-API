
import requests
import markdown
from md_to_html import convert

# Fonction pour télécharger les données d'un pokémon depuis l'API
def get_dataset(id: int) -> dict:
    """Cette fonction récupére les informations d'un habitat."""

    url = f"https://pokeapi.co/api/v2/pokemon-habitat/{id}/"
    # Récupération des données sous forme de JSON
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
    pokemon_names = [pokemon["name"] for pokemon in pokemons]

    # Calcul de la moyenne des PV des Pokémon
    total_hp = 0
    for name in pokemon_names:
        details = get_pokemon_details(name)
        # Les PV se trouvent dans la liste "stats", où "stat.name" == "hp"
        hp_stat = next((stat["base_stat"] for stat in details["stats"] if stat["stat"]["name"] == "hp"), 0)
        total_hp += hp_stat

    avg_hp = total_hp / total_pokemons if total_pokemons > 0 else 0
    return {"name": name, "total_pokemons": total_pokemons, "pokemon_names": pokemon_names, "avg_hp": avg_hp}

def dataset_to_md(dataset: dict, filename: str) -> None:

    """Cette fonction prend le jeu de donnée au format JSON téléchargé depuis l’API Pékomon, et produit un fichier Markdown
    présentant les statistiques calculées."""
# Création du fichier Markdown
    with open(filename, 'w', encoding='utf-8') as md_file:
        # Écriture du titre du fichier
        md_file.write(f"# Fiche de l'habitat{dataset['name'].capitalize()}\n\n")
        


        # Écriture des informations du pokémon
        md_file.write("## Informations\n")
        md_file.write(f"- **Nombre de Pokemon**: {len(dataset.get('pokemon_species', []))}\n")
        md_file.write(f"- **Noms des pokemons**: {[pokemon['name'] for pokemon in dataset.get('pokemon_species', [])]}\n")
        md_file.write(f"- **Especes**: {dataset.get('pokemon_species', [])}\n")
        total_hp = 0
        pokemon_names = [pokemon["name"] for pokemon in dataset.get("pokemon_species", [])]
        for name in pokemon_names:
            details = get_pokemon_details(name)
            hp_stat = next(stat["base_stat"] for stat in details["stats"] if stat["stat"]["name"] == "hp")
            total_hp += hp_stat
        avg_hp = total_hp / len(pokemon_names) if len(pokemon_names) > 0 else 0
        md_file.write(f"- **PV moyen**: {avg_hp}\n")
        

def infos_locales(habitat_id: int, markdown_filename: str, html_filename: str) -> None:
    """
    Cette fonction utilise toutes les fonctions précédentes pour télécharger un jeu de données,
    calculer des statistiques, et produire des fichiers Markdown et HTML.
    """
    # Télécharger le jeu de données
    data = get_dataset(habitat_id)
    # Nom du fichier
    filename = f"pokemon_{habitat_id}"
    # Calculer les statistiques
    statistics = compute_statistic(data)
    # Générer le fichier Markdown
    dataset_to_md(data, f"{filename}.md")
    # Convertir le fichier Markdown en HTML
    convert(f"{filename}.md", f"{filename}.html")

    # Affichage du message de réussite
    print(f"Fiche générée: {filename}.html")

# Demande à l'utilisateur de saisir l'ID d'un Habitat
id_habitat = input("Entrez l'ID d'un habitat: ")

if id_habitat.isdigit():
    infos_locales(int(id_habitat), f"pokemon_{id_habitat}.md", f"pokemon_{id_habitat}.html")
else:
    print("L'ID doit être un nombre entier.")


