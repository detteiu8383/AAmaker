from AAutils import AA

AA = AA()
input_path = "input_001.jpg"
output_path = "imgs/test_002/"
font_path = "C:\Windows\Fonts\msgothic.ttc"

img = AA.open_image(input_path)
img = AA.paste_img(img)
gray = AA.image2gray(img)
threshold = AA.gray2line(AA.resize_ratio(gray, 1), 3, 28)
AA.save_image(threshold, "output_001.png")
AAtext = AA.image2text_lines(threshold, 70, 1.25)
AAimg = AA.create_text_image(AAtext, AA.MSGOTHIC_PATH, 18, (0,0,0), (255,255,255,255))
AA.save_image(AAimg, "output_002.png")
print(AAtext)
AAtext2 = AA.image2text_brightness(img, 140, 2.5)
print("\n\n\n\n\n")
print(AAtext2)