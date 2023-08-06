from PIL import Image



def resize(imgfile,xy):
	Image.open(imgfile).resize(
		xy, Image.ANTIALIAS).save(imgfile)

def cloud(text,font_path,savafile=None,image=None,background_color="white",color=True):
    import PIL.Image
    import numpy as np
    import wordcloud
    cut_text = "".join(text)
    if image!=None:
        background_image = np.array(PIL.Image.open(image))
        c = wordcloud.WordCloud(
            font_path=font_path,
            background_color=background_color,
            mask=background_image).generate(cut_text)
    else:
        c = wordcloud.WordCloud(
            font_path=font_path,
            background_color=background_color).generate(cut_text)
    if color and image!=None:
        image_colors = wordcloud.ImageColorGenerator(background_image)
        c=c.recolor(color_func=image_colors)
    # print(type(c))
    if savafile!=None:
        c.to_file(savafile)
    return c


def add_text(img, text, font: "tuple" = ('C:/windows/fonts/Dengl.ttf', 20), XY=(0, 0), fillColor="#000000",
             show_img: "bool" = False, change_name=None):
    import PIL.ImageDraw
    import PIL.ImageFont
    setFont = PIL.ImageFont.truetype(*font)

    # img=imglist[x]
    image = Image.open(img)
    draw = PIL.ImageDraw.Draw(image)
    width, height = image.size
    if type(XY) == type(""):
        X, Y = eval(XY)
        XY = (X, Y)
    draw.text(XY, text, font=setFont, fill=fillColor)
    if change_name != None:
        img = change_name
    image.save(img)

    if show_img:
        image.show()