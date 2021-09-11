from django.conf import settings
import pytesseract
import numpy as np
import cv2
import ftfy

from pcard import pan_read

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr(filename):
    """
    This function will handle the core OCR processing of images.
    """
    i = cv2.imread(filename)

    # Convert to gray
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    thresh = 255 - cv2.threshold(i, 0, 255,
                                 cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    thresh = cv2.dilate(thresh, kernel, iterations=1)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    text = pytesseract.image_to_string(i, lang='eng')
    text = text.replace("                        ", '\n\n')

    # Cleaning all the gibberish text
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    # return text

    print(text.lower())
    if "fier" in text.lower() or "name " in text.lower() or "date of birth " in text.lower() or "father  name" in text.lower() or "fathers name" in text.lower() or "father" in text.lower():
        #data = pan_read.pan_read_text(text)
        data = pan_read.all_details(text)

    elif "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
        #data = pan_read.ocr(text)
        data = pan_read.all_details(text)

    else:
        return("Upload Valid Document And Check Again")

    return data  # out_list  # data  # out_list
