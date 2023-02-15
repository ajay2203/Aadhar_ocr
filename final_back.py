
import cv2
import pytesseract
import re
import numpy as np
import os 

pytesseract.pytesseract.tesseract_cmd =r"C:\\Users\\YADAV\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread(r"C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\back_img.jpeg")
dict_back = {}
def back(img):
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
    dst = img


    res_string_address = pytesseract.image_to_string(dst)
    res_string_address = res_string_address.split(":")

    # print("res_string_address",res_string_address[1])

    blank_line_regex = r"(?:\r?\n){2,}"
    resm = re.split(blank_line_regex, res_string_address[1].strip())
    rem = resm[0].replace("\n"," ")
    dict_back = {"Address":rem}
    print(dict_back)
    # print("===resm==",resm[0])
back(img)