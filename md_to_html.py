import markdown 


input_file = 'input.md'  
output_file = 'output.html'  

# Lire le fichier Markdown
with open(input_file, 'r', encoding='utf-8') as md_file:
    md_content = md_file.read()  # Lire le contenu

# Convertir en HTML
html_content = markdown.markdown(md_content)  # Conversion

# Écrire le fichier HTML
with open(output_file, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)  # Écrire le contenu

print("Conversion réussie !")  # Message de succès


