from aadhar_ocr import front, back
import cv2
import json



front_img = cv2.imread(r'C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\front_img.jpeg')
back_img = cv2.imread(r'C:\Users\YADAV\OneDrive\Desktop\Aadhaar ocr\back_img.jpeg')

front_det = front(front_img)
back_det = back(back_img)

print(front_det)
print(back_det)

aadhar_dict = front_det | back_det

with open("extract.json","w") as outfile:
    json.dump(aadhar_dict,outfile)