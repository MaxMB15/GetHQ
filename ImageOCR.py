import ScreenCapture
from PIL import Image
import textract

def text_balance(img):
	factor = (259 * (100 + 255)) / (255 * (259 - 100))

	def change(c):
		return 128 + factor * ((c * .75) - 128)

	return img.point(change)

result = text_balance(Image.open('screenshot.png'))

result.save("screenshot.png")

text = textract.process("test.jpg")
print(text)