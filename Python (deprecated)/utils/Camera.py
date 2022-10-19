import camera
import ubinascii

class __Camera:
    def __init__(self):
        # Disable camera initialization
        camera.deinit()
        
        # Enable camera initialization
        camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                    format=camera.JPEG, framesize=camera.FRAME_VGA, 
                    xclk_freq=camera.XCLK_20MHz,
                    href=23, vsync=25, reset=-1, pwdn=-1,
                    sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)

        camera.framesize(camera.FRAME_HVGA) # Set the camera resolution
        # The options are the following:
        # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
        # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
        # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA
        # Note: The higher the resolution, the more memory is used.
        # Note: And too much memory may cause the program to fail.
        
        camera.flip(0)                       # Flip up and down window: 0-1
        camera.mirror(0)                     # Flip window left and right: 0-1
        camera.saturation(-2)                 # saturation: -2,2 (default 0). -2 grayscale 
        camera.brightness(0)                 # brightness: -2,2 (default 0). 2 brightness
        camera.contrast(0)                   # contrast: -2,2 (default 0). 2 highcontrast
        camera.quality(10)                   # quality: # 10-63 lower number means higher quality
        # Note: The smaller the number, the sharper the image. The larger the number, the more blurry the image
        
        camera.speffect(camera.EFFECT_NONE)  # special effects:
        # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
        camera.whitebalance(camera.WB_NONE)  # white balance
        # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

    @property
    def frame(self):
        return ubinascii.b2a_base64(camera.capture())

Camera = __Camera()

if __name__ == '__main__':
    print("hi")
    try:
        print(f"B64 len: {len(Camera.frame)}")
    except:
        print("err")
