import cv2
import numpy as np
from PIL import Image
import math

class AA:

    default_brightness_map = " " * 64 + "." * 64 + "+" * 64 + "8" * 64

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

    def split_image_auto_sqare(self, image, h_split):
        h_size = image.shape[1] // h_split
        h_trim = h_size * h_split

        v_size = h_size
        v_split = image.shape[0] // v_size
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


    def images2str_lines(self, threshold, h_split, ratio):
        split_images = self.split_image_from_ratio(threshold, h_split, ratio)
        out_str = ""
        for row in split_images:
            for split in row:
                char = self.line2char(split)
                out_str += char
                #print(char,end="")
            out_str += "\n"
            #print("")
        return out_str

    def image2str_brightness(self, image, h_split, ratio, char_map=default_brightness_map):
        gray = self.image2gray(image)
        split_images = self.split_image_from_ratio(gray, h_split, ratio)
        out_str = ""
        for row in split_images:
            for split in row:
                char = self.gray2char(split, char_map)
                out_str += char
                #print(char,end="")
            out_str += "\n"
            #print("")
        return out_str
        

