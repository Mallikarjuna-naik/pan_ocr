from document_parser.base_parser import DocumentBaseParser
from django.conf import settings
import pytesseract
import numpy as np
import cv2
import ftfy
import json
import io
import re
import urllib
import tempfile
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class PANParser(DocumentBaseParser):

    def findword(self, textlist, wordstring):
        lineno = -1
        for wordline in textlist:
            xx = wordline.split()
            if ([w for w in xx if re.search(wordstring, w)]):
                lineno = textlist.index(wordline)
                textlist = textlist[lineno+1:]
                return textlist

        return textlist

    def get_old_pan_details(self, text):

        # Initializing data variable
        name = None
        fname = None
        text0 = []
        text1 = []
        # Searching for PAN
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = lin.replace('\n', '')
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)

        text1 = list(filter(None, text1))
        text0 = self.remove_text(text1)
        # Contains all the relevant extracted text in form of a list - uncomment to check
        print(text0)

        try:
            # Cleaning first names, better accuracy
            name = text0[0]
            name = name.rstrip()
            name = name.lstrip()
            name = name.replace("8", "B")
            name = name.replace("0", "D")
            name = name.replace("6", "G")
            name = name.replace("1", "I")
            name = re.sub('[^a-zA-Z] +', ' ', name)

            # Cleaning Father's name
            fname = text0[1]
            fname = fname.rstrip()
            fname = fname.lstrip()
            fname = fname.replace("8", "S")
            fname = fname.replace("0", "O")
            fname = fname.replace("6", "G")
            fname = fname.replace("1", "I")
            fname = fname.replace("\"", "A")
            fname = re.sub('[^a-zA-Z] +', ' ', fname)

        except:
            pass

        # Making tuples of data
        data = {}
        data['Name'] = name
        data['Father Name'] = fname
        data['Date of Birth'] = self.get_date(text)
        data['PAN'] = self.get_pan(text)  # pan

        return data

    def all_details(self, text):
        name = None
        fathername = None
        text0 = []
        text1 = []

        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)

        text1 = list(filter(None, text1))
        text0 = self.remove_text(text1)
        print(text0)

        try:
            print("llllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
            if "name " in text.lower() or "date of birth " in text.lower() or "father  name" in text.lower() or "birth" in text.lower():
                print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                try:
                    if "name" in text.lower():
                        word1 = '(/NAME|/Name|NAME|Name)$'
                        text0 = self.findword(text0, word1)
                        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                        print(text0)
                        name = text0[0]
                        print(name)
                        text0 = text0[1:]
                        # Searching for fathers name
                        word3 = '(Fathers Name |Father Name|Fother Name |/Fathers Name)$'
                        text0 = self.findword(text0, word3)
                        text0 = text0[1:]
                        print("tttttttttttttttttttttttttttttttttttt")
                        print(text0)
                        fathername = text0[0]
                        print(fathername)

                except Exception as ex:
                    print(ex)
                    pass

            else:  # "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():

                name = text0[0]
                name = name.rstrip()
                name = name.lstrip()
                name = name.replace("8", "B")
                name = name.replace("0", "D")
                name = name.replace("6", "G")
                name = name.replace("1", "I")
                name = re.sub('[^a-zA-Z] +', ' ', name)

                # Cleaning Father's name
                fathername = text0[1]
                fathername = fathername.rstrip()
                fathername = fathername.lstrip()
                fathername = fathername.replace("8", "S")
                fathername = fathername.replace("0", "O")
                fathername = fathername.replace("6", "G")
                fathername = fathername.replace("1", "I")
                fathername = fathername.replace("\"", "A")
                fathername = re.sub('[^a-zA-Z] +', ' ', fathername)
        except Exception as ex:
            print(ex)
            pass

        data = {}
        data['Name'] = name
        data['Father Name'] = fathername
        data['Date of Birth'] = self.get_date(text)
        data['PAN'] = self.get_pan(text)
        return data

    def get_new_pan_details(self, text):
        # Initializing data variable
        name = None
        fname = None
        text0 = []
        text1 = []

        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)

        text1 = list(filter(None, text1))
        text0 = self.remove_text(text1)
        print(text0)

        try:
            word1 = '(/NAME|/Name|NAME|Name)$'
            text0 = self.findword(text0, word1)
            print(text0)
            nameline1 = text0[0]
            text0 = text0[1:]
            word2 = '(/FATHERS| NAME|/FATHERS NAME|/FATHER S NAME|/FATHER NAME|/FATHER|\
                    /Fathers Name|/Father|/Fathers|/Father Name|FATHERS NAME|FATHER S \
                    NAME|FATHER NAME|FATHER|Fathers Name|Father|Fathers|Father Name|fathors name|fathor)$'
            text0 = self.findword(text0, word2)
            nameline2 = text0[0]
            print(nameline2)

            text0 = text0[1:]
            # print(text0)
        except Exception as ex:
            print(ex)
            pass

        try:

            word2 = '(/FATHERS| NAME|/FATHERS NAME|/FATHER S NAME|/FATHER NAME|/FATHER|\
                    /Fathers Name|/Father|/Fathers|/Father Name|FATHERS NAME|FATHER S \
                    NAME|FATHER NAME|FATHER|Fathers Name|Father|Fathers|Father Name)$'
            text0 = self.findword(text0, word2)
            nameline2 = text0[0]
            text0 = text0[1:]

        except Exception as ex:
            print(ex)
            pass
        # Searching for Name and finding closest name in database
        try:
            name = nameline1
            fname = nameline2
        except Exception as ex:
            print(ex)
            pass

        # Making tuples of data
        data = {}
        data['Name'] = name
        data['Father Name'] = fname
        data['Date of Birth'] = self.get_date(text)
        data['PAN'] = self.get_pan(text)
        return data

    def pan_get_details(self):
        """
        This function will handle the core OCR processing of images and  returning key features in dictionary format
        """
        temp_file = tempfile.mktemp()
        response = urllib.request.urlopen(self.doc_url)
        fobj = open(temp_file, 'wb')
        fobj.write(response.read())
        fobj.close()

        # Get image of page 1
        images = convert_from_bytes(self.doc_content)
        temp_file2 = tempfile.mktemp()
        images[0].save(temp_file2, 'JPEG')
        images[0].save("./media/panimg.jpg", 'JPEG')

        img = cv2.imread(temp_file2, cv2.IMREAD_COLOR)
        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = 255 - cv2.threshold(img, 0, 255,
                                     cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh, lang='eng')
        text = text.replace("                        ", '\n\n')

        # Cleaning all the gibberish text
        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)
        # return text

        if "name " in text.lower() or "date of birth " in text.lower() or "father  name" in text.lower() or "birth" in text.lower():
            data = self.get_new_pan_details(text)

        elif "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
            data = self.get_old_pan_details(text)

        else:
            return("Upload Valid Document And Check Again")

        data2 = self.all_details(text)

        return data2

    def is_valid_document(self):
        return True
    # Searches for the Data of Birth using regex

    def get_date(self, text):
        try:
            dob_regex = r"\d{1,2}\/\d{1,2}\/\d{4}"
            for i in text:
                dob = re.findall(dob_regex, text)
            if len(dob) > 0:
                dob = dob[0]
                dob = dob.rstrip()
                dob = dob.lstrip()
                dob = dob.replace('l', '/')
                dob = dob.replace('L', '/')
                dob = dob.replace('I', '/')
                dob = dob.replace('i', '/')
                dob = dob.replace('|', '/')
                return dob
        except:
            print("Error in DOB extraction")

    # Searches for the PAN number using regex
    def get_pan(self, text):
        try:
            pan_regex = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
            for i in text:
                pan = re.findall(pan_regex, text)
            if len(pan) > 0:
                pan = pan[0]
                # print(pan)
                return pan
        except:
            print("Error in PAN Number Extraction")

    def remove_text(self, text1):
        # To remove any text read from the image file which lies before the line 'Income Tax Department'
        lineno = 0  # To start from the first line of the text file.
        for wordline in text1:
            xx = wordline.split('\n')
            if ([w for w in xx if re.search('(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
                text1 = list(text1)
                lineno = text1.index(wordline)
                break
        text0 = text1[lineno+1:]
        return text0
