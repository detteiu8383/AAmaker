from AAutils import AA
import cv2

AA = AA()
input_path = "input_002.png"
output_path = "output_001.png"

img = AA.open_image(input_path)
img = AA.paste_img(img)
gray = AA.image2gray(img)
AA.image2str_brightness(gray, 80, 2)