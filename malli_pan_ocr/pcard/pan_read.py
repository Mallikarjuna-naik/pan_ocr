
import re

# import difflib


def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist


def get_date(text):
    '''
    From the textay of text, searches for the Data of Birth using regex
    '''
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
            print(dob)
            return dob
    except:
        print("Error in DOB extraction")


def get_pan(text):
    '''
    From the Extracted text of Pancard, searches for the PAN number using regex
    '''
    try:
        pan_regex = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
        for i in text:
            # print(i)
            pan = re.findall(pan_regex, text)
            # print(pan)
        if len(pan) > 0:
            pan = pan[0]
            print(pan)
            return pan
    except:
        print("Error in PAN Number Extraction")


def remove_text(text1):
    # to remove any text read from the image file which lies before the line 'Income Tax Department'

    lineno = 0  # to start from the first line of the text file.

    for wordline in text1:
        xx = wordline.split('\n')
        if ([w for w in xx if re.search('(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
            text1 = list(text1)
            lineno = text1.index(wordline)
            break

    text0 = text1[lineno+1:]
    return text0


def all_details(text):
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
    text0 = remove_text(text1)
    print(text0)

    try:
        if "name " in text.lower() or "date of birth " in text.lower() or "father  name" in text.lower() or "birth" in text.lower():
            try:
                if "name" in text.lower():
                    word1 = '(/NAME|/Name|NAME|Name)$'
                    text0 = findword(text0, word1)
                    print(text0)
                    name = text0[0]
                    # print(name)
                    text0 = text0[1:]
                    # Searching for fathers name
                    word3 = '(Fathers Name |Father Name|Fother Name |/Fathers Name)$'
                    text0 = findword(text0, word3)
                    text0 = text0[1:]
                    # print(text0)
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
    data['Date of Birth'] = get_date(text)
    data['PAN'] = get_pan(text)
    return data
