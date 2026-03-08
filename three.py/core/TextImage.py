from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# note: font/background color should be specified with ranges [0-255], not [0-1]
# note: if image width/height not declared, will be set according to rendered text size
class TextImage(object):

    def __init__(self, text="Hello, world!", fontFileName=None, fontSize=24,
        fontColor=[0,0,0], backgroundColor=[255,255,255], transparent=False,
        antialias=True, width=None, height=None,
        alignHorizontal="LEFT", alignVertical="TOP"):
        
        self.text = text
        if fontFileName is None:
            defaultFont = Path(__file__).resolve().parent.parent / "fonts" / "LiberationSans.ttf"
            try:
                self.font = ImageFont.truetype(str(defaultFont), fontSize)
            except OSError:
                self.font = ImageFont.load_default()
        else:
            fontPath = Path(fontFileName)
            if not fontPath.exists():
                fontPath = Path(__file__).resolve().parent.parent / fontPath
            self.font = ImageFont.truetype(str(fontPath), fontSize)

        self.fontColor = fontColor
        self.backgroundColor = backgroundColor
        self.transparent = transparent
        self.antialias = antialias
        self.width = width
        self.height = height
        self.alignHorizontal = alignHorizontal
        self.alignVertical = alignVertical
        
        self.renderImage()
        
    # can call to recaluate surface if text has changed
    def renderImage(self):
    
        tempImage = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        tempDraw = ImageDraw.Draw(tempImage)
        left, top, right, bottom = tempDraw.textbbox((0, 0), self.text, font=self.font)
        textWidth = right - left
        textHeight = bottom - top

        # if image dimensions are not specified, use font surface size as default
        if self.width is None:
            self.width = textWidth
        if self.height is None:
            self.height = textHeight
            
        # create image with transparency channel
        background = (0, 0, 0, 0) if self.transparent else tuple(self.backgroundColor) + (255,)
        self.surface = Image.new("RGBA", (self.width, self.height), background)
        draw = ImageDraw.Draw(self.surface)
        
        # values used for alignment; 
        #  only has an effect if image size is set larger than rendered text size
        if (self.alignHorizontal == "LEFT"):
            alignX = 0.0
        elif (self.alignHorizontal == "CENTER"):
            alignX = 0.5
        elif (self.alignHorizontal == "RIGHT"):
            alignX = 1.0
        if (self.alignVertical == "TOP"):
            alignY = 0.0
        elif (self.alignVertical == "MIDDLE"):
            alignY = 0.5
        elif (self.alignVertical == "BOTTOM"):
            alignY = 1.0
            
        textX = alignX * (self.width - textWidth) - left
        textY = alignY * (self.height - textHeight) - top
        draw.text((textX, textY), self.text, font=self.font, fill=tuple(self.fontColor))

