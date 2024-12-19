import markdown
import sys

try:
    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")
    return

print(f"Successfully converted '{input_file}' to '{output_file}'")


