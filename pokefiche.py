# Importation des bibliothèques nécessaires
import requests
import markdown
# Pour que sa ouvre automatiquement une page Web
import webbrowser
from md_to_html import convert_markdown_to_html

# Fonction pour télécharger les données d'un Pokémon depuis l'API PokeAPI
def download_poke(id: int) -> dict:
    """Télécharge les données d'un Pokémon depuis l'API PokeAPI."""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return None

# Fonction pour générer un fichier Markdown à partir des données d'un Pokémon
def poke_to_md(data: dict, filename: str) -> None:
    """Génère un fichier Markdown à partir des données d'un Pokémon."""
    if data is None:
        return
    try:
        name = data['name'].capitalize()
        weight = data['weight']
        height = data['height']
        types = [t['type']['name'] for t in data['types']]
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        image_url = data['sprites']['front_default']

        with open(filename, 'w') as f:
            f.write(f"# Fiche de {name}\n\n")
            f.write(f"![{name}]({image_url})\n\n")
            f.write(f"## Informations\n")
            f.write(f"- **Poids**: {weight}\n")
            f.write(f"- **Taille**: {height}\n")
            f.write(f"- **Types**: {', '.join(types)}\n")
            f.write(f"\n## Statistiques\n")
            for stat, value in stats.items():
                f.write(f"- **{stat}**: {value}\n")
    except KeyError as e:
        print(f"Erreur lors de la génération du fichier Markdown : {e}")

# Fonction pour générer une fiche Markdown et une fiche HTML pour un Pokémon donné
def fiche_pokemon(id: int) :
    """Génère une fiche Markdown et une fiche HTML pour un Pokémon donné."""
    data = download_poke(id)
    md_filename = f"pokemon_{id}.md"
    html_filename = f"pokemon_{id}.html"

    poke_to_md(data, md_filename)
    if data is not None:
        html_content = convert_markdown_to_html(md_filename)

        with open(html_filename, 'w') as f:
            f.write("<html><head><title>Fiche de Pokémon</title></head><body>")
            f.write(html_content)
            f.write("</body></html>")

        print(f"Fiche générée : {md_filename} et {html_filename}")
        webbrowser.open(html_filename)

# Point d'entrée du programme
if __name__ == "__main__":
    while True:
        try:
            pokemon_id = int(input("Veuillez entrer l'ID du Pokémon : "))
            fiche_pokemon(pokemon_id)
            break
        except ValueError:
            print("Erreur : l'ID doit être un entier.")

