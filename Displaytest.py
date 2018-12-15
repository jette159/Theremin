import os
from PIL import ImageFont

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
#from demo_opts import get_device

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    
    font = make_font("C&C Red Alert [INET].ttf", 40)
    
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black", outline="white")
        draw.text((60,15 ), text="c'",fill= "white", font=font)

if __name__ == "__main__":
    try:
        device = ssd1306(serial)
        while True:
            main()
    except KeyboardInterrupt:
        pass
    
    
    #device.bounding_box
