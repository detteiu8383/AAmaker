from AAutils import AA

AA = AA()
input_path = "mirei.jpg"
output_path = "imgs/test_002/"
font_path = "C:\Windows\Fonts\msgothic.ttc"

img = AA.open_image(input_path)
img = AA.paste_img(img)
AAtext = AA.image2text_brightness(img, 130, 2.3, inv=True)
AAimg = AA.create_text_image(AAtext, AA.MSGOTHIC_PATH, 18, (255,255,255), (0,0,0,255))
AA.save_image(AA.resize_ratio(AAimg, 0.5), "output_003.png")
print(AAtext)



