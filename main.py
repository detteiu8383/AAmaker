from AAutils import AA
import cv2

AA = AA()
input_path = "input_002.png"
output_path = "output_001.png"

img = AA.open_image(input_path)
img = AA.paste_img(img)
threshold = AA.gray2line(AA.image2gray(img))
AA.images2str_lines(threshold, 40)
