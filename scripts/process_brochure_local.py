import os
import pdfplumber

# Directorios
input_dir = "../data/pdf/"
output_dir = "../outputs/"

# Asegurarse de que el directorio de salida exista
os.makedirs(output_dir, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF usando pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text  # Corregido para devolver la variable 'text'

def process_brochures():
    """Procesa todos los PDFs en la carpeta de brochures."""
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Procesando: {filename}")
            
            # Extraer texto
            extracted_text = extract_text_from_pdf(pdf_path)
            
            # Guardar el texto extraído
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
                print(f"Texto guardado en: {output_path}")

if __name__ == "__main__":
    process_brochures()

