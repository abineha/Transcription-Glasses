import speech_recognition as sr
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

# Initialize the OLED display
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(ImageFont.load_default().font, size=26)


# Initialize Speech Recognition
r = sr.Recognizer()

def scroll_text(text):
    max_width, _ = draw.textsize(text, font=font)
    for i in range(max_width + width):
        # Clear image buffer
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        # Calculate x position
        x = width - i
        # Draw text
        draw.text((x, 0), text, font=font, fill=255)
        # Display image
        disp.image(image)
        disp.display()
        time.sleep(0.00001)

def record_and_display_text():
    while True:
        try:
            with sr.Microphone() as source2:
                # Adjust for ambient noise
                r.adjust_for_ambient_noise(source2, duration=1.0)

                # Listen for speech
                audio2 = r.listen(source2)

                # Convert speech to text
                MyText = r.recognize_google(audio2)
                print(MyText)

                # Scroll the text from right to left
                scroll_text(MyText)

                print("Next sentence")

        except sr.RequestError as e:
            print("Could not request result; {0}".format(e))

        except sr.UnknownValueError as e:
            print("")

record_and_display_text()
