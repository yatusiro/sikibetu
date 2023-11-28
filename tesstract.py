
from PIL import Image
import pytesseract

# 指定 tesseract.exe 的路径
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

# 打开图像
img = Image.open('test2.jpg')  # 替换为你的图片路径

# 可以尝试图像预处理以提高OCR准确性
# img = img.convert('L')  # 转换为灰度图像
# img = img.point(lambda x: 0 if x < 140 else 255)  # 二值化

# 配置 Tesseract 参数，尝试使用不同的PSM模式
custom_config = r'--oem 1 --psm 6'
text = pytesseract.image_to_string(img, lang='jpn', config=custom_config)

# 输出识别的文本
print(text)
