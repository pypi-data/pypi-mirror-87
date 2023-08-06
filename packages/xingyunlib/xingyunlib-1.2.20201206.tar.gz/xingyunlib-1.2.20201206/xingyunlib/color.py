class Colorx:
    def __init__(self,color,from_color):
        self.color = color
        self.from_color = from_color
    def _color16_to_rgb(self, color16):
        if color16[0] != "#" or len(color16) != 7:
            raise ValueError("传入的颜色值不符合16进制颜色的标准")
        r16 = "0x"+color16[1:3]
        g16 = "0x"+color16[3:5]
        b16 = "0x"+color16[5:7]
        try:
            r = int(r16,16)
            g = int(g16,16)
            b = int(b16,16)
        except:
            raise ValueError("传入的颜色值不符合16进制颜色的标准")
        return (r,g,b)
    def _rgb_to_color16(self, rgb):
        if len(rgb) != 3 or rgb[0] > 255 or rgb[0] < 0 or rgb[1] > 255 or rgb[1] < 0 or rgb[2] > 255 or rgb[2] < 0:
            raise ValueError("传入的颜色值不符合RGB颜色的标准")
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        try:
            r16 = hex(r)
            g16 = hex(g)
            b16 = hex(b)
        except:
            raise ValueError("传入的颜色值不符合RGB颜色的标准")
        r16text = str(r16)[2:4].upper()
        if len(r16text) == 1:
            r16text = "0"+r16text
        g16text = str(g16)[2:4].upper()
        if len(g16text) == 1:
            g16text = "0"+g16text
        b16text = str(b16)[2:4].upper()
        if len(b16text) == 1:
            b16text = "0"+b16text
        return "#"+r16text+g16text+b16text
    def _hsv_to_rgb(self, hsv):
        import math
        if len(hsv) != 3 or hsv[0] > 360 or hsv[0] < 0 or hsv[1] > 1 or hsv[1] < 0 or hsv[2] > 1 or hsv[2] < 0:
            raise ValueError("传入的颜色值不符合HSV颜色的标准")
        h = float(hsv[0])
        s = float(hsv[1])
        v = float(hsv[2])
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b
    def _rgb_to_hsv(self, rgb):
        import math
        if len(rgb) != 3 or rgb[0] > 255 or rgb[0] < 0 or rgb[1] > 255 or rgb[1] < 0 or rgb[2] > 255 or rgb[2] < 0:
            raise ValueError("传入的颜色值不符合RGB颜色的标准")
        r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        return h, s, v
    def _hsv_to_color16(self, hsv):
        if len(hsv) != 3 or hsv[0] > 360 or hsv[0] < 0 or hsv[1] > 1 or hsv[1] < 0 or hsv[2] > 1 or hsv[2] < 0:
            raise ValueError("传入的颜色值不符合HSV颜色的标准")
        rgb = self._hsv_to_rgb(hsv)
        color16 = self._rgb_to_color16(rgb)
        return color16
    def _color16_to_hsv(self, color16):
        if color16[0] != "#" or len(color16) != 7:
            raise ValueError("传入的颜色值不符合16进制颜色的标准")
        rgb = self._color16_to_rgb(color16)
        hsv = self._rgb_to_hsv(rgb)
        return hsv
    def color_to(self,to_color:"str",change_color:"bool"=False):

        if self.from_color == to_color:
            # print("本来就是原来的格式啦~")
            return self.color

        if self.from_color == "hex" and to_color == "rgb":
            if change_color:
                self.color=self._color16_to_rgb(self.color)
                self.from_color="hex"
            return self._color16_to_rgb(self.color)
        elif self.from_color == "rgb" and to_color == "hex":
            if change_color:
                self.color=self._rgb_to_color16(self.color)
                self.from_color = "rgb"
            return self._rgb_to_color16(self.color)
        elif self.from_color == "hsv" and to_color == "rgb":
            if change_color:
                self.color=self._hsv_to_rgb(self.color)
                self.from_color = "hsv"
            return self._hsv_to_rgb(self.color)
        elif self.from_color == "rgb" and to_color == "hsv":
            if change_color:
                self.color=self._rgb_to_hsv(self.color)
                self.from_color = "rgb"
            return self._rgb_to_hsv(self.color)
        elif self.from_color == "hsv" and to_color == "hex":
            if change_color:
                self.color=self._hsv_to_color16(self.color)
                self.from_color = "hsv"
            return self._hsv_to_color16(self.color)
        elif self.from_color == "hex" and to_color == "rgb":
            if change_color:
                self.color=self._color16_to_hsv(self.color)
                self.from_color="hex"
            return self._color16_to_hsv(self.color)

        else:
            raise ValueError("传入的颜色类型未收录")
