import easyocr
import time
import re

def apply_text_replacements(text):
    # 映射表：直接替换错误文本
    mappings = {
        'm8': 'mg',
        'm呂': 'mg',
        '算' : '質',
        '脂肺' :'脂肪',
        # 其他映射规则
    }

    # 应用映射表替换
    for incorrect, correct in mappings.items():
        text = text.replace(incorrect, correct)

    # 正则表达式替换
    # 将所有前一个字符或后一个字符是数字的'o'替换为'0'
    text = re.sub(r'(?<=\d)o|o(?=\d)', '0', text)

    # 将所有前一个字符是数字且后一个字符是字母的'o'替换为'0'
    text = re.sub(r'(?<=\d)o(?=[a-zA-Z])', '0', text)

    # 将所有前一个字符是字母的'0'替换为'o'
    text = re.sub(r'(?<=[a-zA-Z])0', 'o', text)

    # 将所有前一个字符是'm'后接'1'的情况替换为'ml'
    text = re.sub(r'm1', 'ml', text)

    return text

def recognize_image(image_path):
    # 初始化 EasyOCR reader
    reader = easyocr.Reader(['en', 'ja'], gpu=True)

    # 读取并处理图像
    results = reader.readtext(image_path)

    # 用于存储所有修正后的文本结果
    corrected_texts = []

    # 处理每个检测到的文本
    for (bbox, text, prob) in results:
        # 应用文本替换规则
        corrected_text = apply_text_replacements(text)

        # 将修正后的文本添加到结果列表中
        corrected_texts.append(corrected_text)

    return corrected_texts

# reader = easyocr.Reader(['en', 'ja'], gpu=True)

# # 设定信赖度阈值
# confidence_threshold = 0.5

# # 开始处理时间
# processtime = time.time()

# # 读取并处理图像
# results = reader.readtext('test.jpg')

# # 用于存储所有文本结果（包括修正后的）
# all_texts = []

# # 处理每个检测到的文本
# for (bbox, text, prob) in results:
#     # 应用文本替换规则
#     corrected_text = apply_text_replacements(text)

#     # 将修正后的文本添加到结果列表中
#     all_texts.append(corrected_text)

#     # 打印出低信赖度的文本及其原始信赖度
#     if prob < confidence_threshold:
#         print(f"Detected text: {text}, Confidence: {prob}")

# # 输出处理时间和平均信赖度
# time_taken = time.time() - processtime
# average_confidence = sum(prob for _, _, prob in results) / len(results)
# print(f"Time taken: {time_taken}")
# print(f"Average confidence: {average_confidence}")

# # 输出所有识别到的内容
# print("All detected texts after corrections:")
# for text in all_texts:
#     print(text)
