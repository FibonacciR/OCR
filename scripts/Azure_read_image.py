
'''This script reads images from a directory and extracts text from them using the Azure Computer Vision service.

The extracted text is displayed and the image is annotated with bounding boxes around the detected text.

The script uses the Azure Cognitive Services Computer Vision SDK for Python, which provides a client library for interacting with the Computer Vision service.'''



# Import the required libraries

from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import the required libraries
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

def main():
    global cv_client

    try:
        # Get Credentials from .env file
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Authenticate the client
        cv_client = ComputerVisionClient(
            ai_endpoint,
            CognitiveServicesCredentials(ai_key)
        )

        # Menu for selecting the image to read
        print('\n1: Usar Read API para imagen (Lincoln.jpg)\n2: Leer escritura a mano (Note.jpg)\nCualquier otra tecla para salir\n')
        command = input('Ingrese un número:')
        if command == '1':
            image_file = os.path.join('images', 'Lincoln.jpg')
            get_text_read(image_file)
        elif command == '2':
            image_file = os.path.join('images', 'Note.jpg')
            get_text_read(image_file)

    except Exception as ex:
        print(ex)

def get_text_read(image_file):
    print('\n')

    # Open File and read the image data
    with open(image_file, "rb") as f:
        image_data = f.read()

    # Use the Function to read the image
    read_response = cv_client.read_in_stream(image_data, raw=True)

    # Get Id from the response
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Wait untill the operation is completed
    while True:
        read_result = cv_client.get_read_result(operation_id)
        if read_result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    # Process the result
    if read_result.status == OperationStatusCodes.succeeded:
        print("\nTexto:")

        # Prepare the image for drawing
        image = Image.open(image_file)
        fig = plt.figure(figsize=(image.width / 100, image.height / 100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                # Show the text extracted
                print(f"  {line.text}")

                # Dibujar el polígono delimitador de la línea
                r = line.bounding_box
                bounding_box = [(r[i], r[i + 1]) for i in range(0, len(r), 2)]
                draw.polygon(bounding_box, outline=color, width=3)

                # Mostrar el polígono delimitador de la línea
                print(f"   Bounding Box: {bounding_box}")

        # Guardar imagen con los cuadros delimitadores
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'text.jpg'
        fig.savefig(outputfile)
        print('\n  Resultados guardados en', outputfile)

if __name__ == "__main__":
    main()