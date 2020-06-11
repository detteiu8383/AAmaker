import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import math
import unicodedata

class AA:

    default_brightness_map = "M" * 13 + "W" * 15 + "N" * 20 + "B" * 21 + "RRRRDDKHHHQU8&GG666$O00AAAAASSSdX##@bCV4445555kkkhE%222222ZZZZZZYYJFFFFFF*******fffTTIL7????1111111{{{{[[[||||jjjjllll<<<<!!;;i(=====////////\"\"\"\"~~~~~~^^^^^--;;;:::````''',,,,.......     "
    MSGOTHIC_PATH = "C:\Windows\Fonts\msgothic.ttc"

    def open_image(self, path):
        image = cv2.imread(path, -1)
        return image

    def save_image(self, image, path):
        cv2.imwrite(path, image)
        print("saved Image!")
        return

    def pil2cv(self, image):
        ''' PIL型 -> OpenCV型 '''
        new_image = np.array(image, dtype=np.uint8)
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        return new_image

    def cv2pil(self, image):
        ''' OpenCV型 -> PIL型 '''
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image

    def RGB_mean(self, image):
        b = image.T[0].flatten().mean()
        g = image.T[1].flatten().mean()
        r = image.T[2].flatten().mean()
        return (r, g, b)

    def HSV_mean(self, HSV_image):
        h = HSV_image.T[0].flatten().mean()
        s = HSV_image.T[1].flatten().mean()
        v = HSV_image.T[2].flatten().mean()
        return (h, s, v)

    def gray_mean(self, gray):
        bw = gray.mean()
        return bw

    def resize_ratio(self, image, ratio):
        width, height = image.shape[:2]
        if ratio >= 1:
            image = cv2.resize(image, (height * ratio, width * ratio))
        else:
            image = cv2.resize(image, (int(height * ratio), int(width * ratio)), interpolation = cv2.INTER_AREA)
        return image

    def RGB_image2HSV_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def image2gray(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return gray

    def gray2line(self, gray, dilate_size=3, threshold=15):
        neiborhood = np.ones((dilate_size, dilate_size))
        dilated = cv2.dilate(gray, neiborhood, iterations=1)
        diff = cv2.absdiff(dilated, gray)
        ret, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        return thresh

    def paste_img(self, image, back_color=(255,255,255)):
        width, height = image.shape[:2]
        
        pil_image = self.cv2pil(image)
        back = Image.new("RGB", (height, width), back_color)

        if len(image.shape)==3 and image.shape[2] == 4:
            back.paste(pil_image, (0,0), pil_image.split()[3])
        else:
            back.paste(pil_image, (0,0))
        return self.pil2cv(back)

    def triming(self, image, height, width):
        source_height = image.shape[0]
        source_width = image.shape[1]
        a = (source_height - height) // 2
        b = (source_height - height) // 2 + height
        c = (source_width - width) // 2
        d = (source_width - width) // 2 + width
        trim_image = image[ a : b, c : d ]
        return trim_image

    def split_image(self, image, h_split, v_split):
        split_imgs = []
        [split_imgs.append(np.hsplit(h_img, h_split)) for h_img in np.vsplit(image, v_split)]
        return split_imgs

    def split_image_auto(self, image, h_split, v_split):
        h_size = image.shape[1] // h_split
        h_trim = h_size * h_split

        v_size = image.shape[0] // v_split
        v_trim = v_size * v_split

        trimed_image = self.triming(image, v_trim, h_trim)
        split_images = self.split_image(trimed_image, h_split, v_split)
        return split_images

    def split_image_from_size(self, image, h_size, v_size):
        h_split = image.shape[1] // h_size
        h_trim = h_size * h_split

        v_split = image.shape[0] // v_size
        v_trim = v_size * v_split

        trimed_image = self.triming(image, v_trim, h_trim)
        split_images = self.split_image(trimed_image, h_split, v_split)
        return split_images

    def split_image_from_ratio(self, image, h_split, ratio):
        h_size = image.shape[1] // h_split
        h_trim = h_size * h_split
        
        v_size = round(h_size * ratio)
        v_split = image.shape[0] // v_size
        v_trim = v_size * v_split
              
        trimed_image = self.triming(image, v_trim, h_trim)
        split_images = self.split_image(trimed_image, h_split, v_split)
        return split_images

    def line2char(self, threshold):
        resize_split_img = cv2.resize(threshold, (100, 100))
        lines = cv2.HoughLinesP(resize_split_img, 1, np.pi/180, 70, 50, 10)
        if lines is None:
            return "　"
        else:
            for x1, y1, x2, y2 in lines[0]:
                if x2 - x1 == 0:
                    theta = 90
                else:
                    theta = int(round(math.degrees(math.atan((y2-y1)/(x2-x1))) * -1 + 90, 0))
                return theta

    def gray2char(self, gray, char_map):
        bw = self.gray_mean(gray)
        return char_map[int(bw)]

    def image2text_lines(self, threshold, h_split, ratio):
        split_images = self.split_image_from_ratio(threshold, h_split, ratio)
        out_text = ""
        for row in split_images:
            for split in row:
                char = self.line2char(split)
                out_text += char
            out_text += "\n"
        return out_text

    def image2text_brightness(self, image, h_split, ratio, char_map=default_brightness_map):
        gray = self.image2gray(image)
        split_images = self.split_image_from_ratio(gray, h_split, ratio)
        out_text = ""
        for row in split_images:
            out_text += "\n"
            for split in row:
                char = self.gray2char(split, char_map)
                out_text += char
            
        return out_text[1:]
        
    def add_text_to_image(self, image, text, font_path, font_size, font_color, height, width):
        pil_image = self.cv2pil(image)
        position = (width, height)
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)
        draw.text(position, text, font_color, font=font)

        return self.pil2cv(pil_image)

    def create_text_image(self, text, font_path, font_size, font_color, background_color):
        font = ImageFont.truetype(font_path, font_size)
        tmp = Image.new('RGBA', (1, 1), (0,0,0,0))
        tmp_d = ImageDraw.Draw(tmp)
        text_size = tmp_d.textsize(text, font)
        img = Image.new('RGBA', text_size, background_color)
        img_d = ImageDraw.Draw(img)
        img_d.text((0, 0), text, fill=font_color, font=font)

        return self.pil2cv(img)

    def make_cahr_map_half(self, text):
        text += " "
        char_set = set(text)
        char_list = []
        for moji in char_set:
            if unicodedata.east_asian_width(moji) in ["H", "Na"]:
                char_list.append(moji)
        return 

    def sort_in_brightness(self, char_list):
        brightness_list = []
        for moji in char_list:
            text_img = self.create_text_image(moji, self.MSGOTHIC_PATH, 18, (0,0,0), (255,255,255,255))
            brightness = self.gray_mean(self.image2gray(text_img))
            brightness_list.append([brightness_list, moji])
        
        brightness_list.sort()
        
        
        
        
        return
