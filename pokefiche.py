import requests
import markdown
from md_to_html import convert

# Fonction pour télécharger les données d'un pokémon depuis l'API
def download_poke(id: int) -> dict:
    # URL de l'API pour récupérer les données d'un pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    # Récupération des données sous forme de JSON
    return requests.get(url).json()


def poke_to_md(data: dict, filename: str) -> None:
    # Récupération du nom du pokémon
    name = data['name'].capitalize()
    
    # Récupération de la taille et du poids du pokémon
    height, weight = data['height'], data['weight']

    # Récupération des types du pokémon
    types = ','.join(t['type']['name'] for t in data['types'])

    # Récupération des statistiques du pokémon
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

    # Récupération de l'image du pokémon
    sprite = data['sprites']['front_default']


    # Création du fichier Markdown
    with open(filename, 'w', encoding='utf-8') as md_file:
        # Écriture du titre du fichier
        md_file.write(f"# Fiche de {name}\n\n")
        
        # Écriture de l'image du pokémon
        md_file.write(f"\n![{name}]({sprite})\n")

        # Écriture des informations du pokémon
        md_file.write("## Informations\n")
        md_file.write(f"- **Taille (m)**: {height / 10}\n") # On divise par 10 pour convertir en mètre
        md_file.write(f"- **Poids (kg)**: {weight / 10}\n") # On divise par 10 pour convertir en kg
        md_file.write(f"- **Types**: {types}\n")
        
        # Écriture des statistiques du pokémon
        md_file.write("## Statistiques\n")
        for stat_name, stat_value in stats.items():
            md_file.write(f"  - **{stat_name}**: {stat_value}\n")



# Fonction pour générer la fiche d'un pokémon
def fiche_pokemon(id: int) -> None:
    # Téléchargement des données du pokémon
    data = download_poke(id)
    # Nom du fichier
    filename = f"pokemon_{id}"

    # Conversion des données en fichier Markdown
    poke_to_md(data, f"{filename}.md")

    # Conversion du fichier Markdown en fichier HTML
    convert(f"{filename}.md", f"{filename}.html")
    
    # Affichage du message de réussite
    print(f"Fiche générée: {filename}.html")


# Demande à l'utilisateur de saisir l'ID du Pokémon
id_pokemon = input("Entrez l'ID du Pokémon: ")

if id_pokemon == str(int(id_pokemon)):
    fiche_pokemon(int(id_pokemon))
else:
    print("L'ID doit être un nombre entier.")
