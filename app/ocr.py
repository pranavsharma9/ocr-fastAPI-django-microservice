import pathlib
import pytesseract
from PIL import Image

BASE_DIR=pathlib.Path(__file__).parent
IMAGE_DIR=BASE_DIR/"images"

img_path=IMAGE_DIR/"img_1.png"
img=Image.open(img_path)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
preds=pytesseract.image_to_string(img)

print(preds)