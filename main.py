from AAutils import AA
import cv2

AA = AA()
input_path = "input_002.png"
output_path = "imgs/test_002/"
font_path = "C:\Windows\Fonts\msgothic.ttc"

text = "abcdefghijklmnopqrstuvwxyzABCDEFGHRJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'(=~|-^@[;:,./`{+*<?_ "
ii = 0
for i in text:
    img = AA.create_text_image(i, font_path, 18, (0,0,0), (255,255,255,255))
    img = AA.resize_ratio(img, 10)
    gray = AA.image2gray(img)
    brightness = AA.gray_mean(gray)
    print("{}: {}".format(i, brightness))
    AA.save_image(img, output_path + "out_{:0>3}.png".format(ii))
    ii += 1