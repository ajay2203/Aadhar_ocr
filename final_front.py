import cv2
import pytesseract
import re
import numpy as np
import spacy

pytesseract.pytesseract.tesseract_cmd =r"C:\\Users\\YADAV\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

def front(img):
    regex_name = None
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((10, 10), np.uint8))       
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=250, norm_type=cv2.NORM_MINMAX,
                                                    dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    dst = cv2.fastNlMeansDenoisingColored(result_norm, None, 10, 10, 7, 11)            

    text = pytesseract.image_to_string(dst).upper().replace(" ", "")
    text_name = pytesseract.image_to_string(dst)


    NER = spacy.load("en_core_web_sm")

    name=NER(text)

    #extracting name
    for word in name.ents:
        if word.label_ == "PERSON":
            regex_name  = re.findall("[A-Z][a-z]+", word.text)
    if not regex_name:
        x = text_name.split("\n")
        str_list = list(filter(None, x))
        # print(str_list)
        regex_name = str_list[0]
        # print("str_list",str_list[0])
        # regex_name = re.findall("[A-Z][a-z]+", text)

    # print("==name==",name)


    date = str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text)).replace("]", "").replace("[","").replace("'", "")
    print(date)
    if date=="":
        regex_dob = re.findall("(\d\d\d\d){1}", text)
        for dob in regex_dob:
            dob = int(dob)
            if dob<2023 and dob>1870:
                regex_dob=dob
    # print("Name:",regex_name)
    # print("DOB:",regex_dob)
    number = str(re.findall(r"[0-9]{11,12}", text)).replace("]", "").replace("[","").replace("'", "")
    # print("Aadhar_Number:",number)
    gender = str(re.findall(r"MALE|FEMALE", text)).replace("[","").replace("'", "").replace("]", "")
    # print("Gender:",gender)

    fl_number = number[8:]
    print("fl",fl_number)
    number = "XXXXXXXX" + str(fl_number)
    my_dict = {"Name":[],"Dob":[],"Aadhar_Number":[],"Gender":[]}

    my_dict["Name"].append(regex_name)
    my_dict["Dob"].append(regex_dob)
    my_dict["Aadhar_Number"].append(number)
    my_dict["Gender"].append(gender)
    print(my_dict)
ims = cv2.imread(r"C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\front_img.jpeg")
front(ims)