import numpy as np
from PIL import Image, ImageFont, ImageDraw

def calculate_bpr(char, font_path, size=100):
    """
    计算单个字符在特定字体下的黑色像素占比 (Black Pixel Ratio)
    """
    # 创建正方形画布 (全角字)
    canvas = Image.new('1', (size, size), 1) # '1'模式为二值图，1为白色
    draw = ImageDraw.Draw(canvas)
    
    try:
        font = ImageFont.truetype(font_path, int(size * 0.8)) # 留出边距
        # 获取文字偏移量，确保居中
        left, top, right, bottom = draw.textbbox((0, 0), char, font=font)
        draw.text(((size-(right-left))//2 - left, (size-(bottom-top))//2 - top), 
                  char, font=font, fill=0) # 0为黑色
        
        # 计算黑色像素比例
        pixels = np.array(canvas)
        return (pixels == 0).sum() / (size * size)
    except:
        return None

# 执行逻辑：
# 遍历 unicode 范围，将结果存入 256 个“桶”
# bins = {i: [] for i in range(256)}
