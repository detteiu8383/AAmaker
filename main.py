from AAutils import AA

AA = AA()
input_path = "input_001.jpg"
output_path = "imgs/test_002/"
font_path = "C:\Windows\Fonts\msgothic.ttc"

img = AA.open_image(input_path)
img = AA.paste_img(img)
AAtext = AA.image2text_brightness(img, 250, 2)
AAimg = AA.create_text_image(AAtext, AA.MSGOTHIC_PATH, 18, (0,0,0), (255,255,255,255))
AA.save_image(AAimg, "output_001.png")
