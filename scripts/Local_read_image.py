
''' This script reads images from a directory and extracts text from them using pytesseract.

The extracted text is saved to a text file with the same name as the image in the output directory.

The script uses the pytesseract library, which is a Python wrapper for the Google Tesseract OCR engine.
'''



# Import the required libraries
import os
from PIL import Image
import pytesseract

# Configure pytesseract to use the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Directories
input_dir = "../data/images/"
output_dir = "../outputs/"

# Asure That the output directory exists
os.makedirs(output_dir, exist_ok=True)

def extract_text_from_image(image_path):
    """Extrae texto de una imagen usando pytesseract."""
    try:
        # Load Image
        print(f"Cargando imagen: {image_path}")
        image = Image.open(image_path)
        
        # Save a temporary copy of the loaded image
        temp_image_path = os.path.join(output_dir, "temp_image.png")
        image.save(temp_image_path)
        print(f"Imagen cargada guardada temporalmente en: {temp_image_path}")
        
        # Extract text from the image
        print("Extrayendo texto...")
        text = pytesseract.image_to_string(image)
        print(f"Texto extraído: {text[:100]}")  # Show the first 100 characters
        return text
    except Exception as e:
        print(f"Error procesando {image_path}: {e}")
        return ""

def process_images():
    """Procesa todas las imágenes en la carpeta de entrada."""
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, filename)
            print(f"Procesando: {filename}")
            text = extract_text_from_image(image_path)
            if text:
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Texto guardado en: {output_path}")
            else:
                print(f"No se extrajo texto de {filename}")

if __name__ == "__main__":
    process_images()