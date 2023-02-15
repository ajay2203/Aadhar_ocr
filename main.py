import final_front
import final_back
import cv2



front_img = cv2.imread(r'C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\front_img.jpeg')
back_img = cv2.imread(r'C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\back_img.jpeg')

front_det=final_front(front_img)

back_det=final_back(back_img)

import json
json_string = json.dumps(front_det,back_det)