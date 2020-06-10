from AAutils import AA
import cv2

AA = AA()
input_path = "input_001.png"
output_path = "imgs/test_002/"
font_path = "C:\Windows\Fonts\msgothic.ttc"



img = AA.open_image(input_path)
img = AA.paste_img(img)
AAtext = AA.image2text_brightness(img, 150, 2)
print(AAtext)



"""
text = "bdfhijklABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'(=~|-^@[;:,./`{+*<? "
brightness_list = []
ii = 0
for i in text:
    img = AA.create_text_image(i, font_path, 18, (0,0,0), (255,255,255,255))
    img = AA.resize_ratio(img, 10)
    gray = AA.image2gray(img)
    brightness = AA.gray_mean(gray)
    brightness_list.append([brightness, i])
    print("{}: {}".format(i, brightness))
    AA.save_image(img, output_path + "out_{:0>3}.png".format(ii))
    ii += 1

brightness_list.sort()

for sets in brightness_list:
    print(sets[0], sets[1], sep="	")
"""