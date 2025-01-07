import markdown


def convert(md_file, html_file):
    # Lire le contenu du fichier Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convertir le Markdown en HTML
    html_content = markdown.markdown(md_content)
    
    # Écrire le contenu HTML dans le fichier de sortie
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
