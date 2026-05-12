import sys
import json
import random
import numpy as np
from PIL import Image

def run_codepic(image_path, lexicon_path, output_width=100, ratio=1.3):
    # 1. Load Lexicon
    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon = json.load(f)
    
    levels = lexicon['levels']
    mapping = {item['level']: item['chars'] for item in lexicon['codebook']}
    defined_levels = sorted(mapping.keys())

    # 2. Image Pre-processing
    img = Image.open(image_path).convert('L')
    w, h = img.size
    target_height = int((h / w) * output_width / ratio)
    img_resized = img.resize((output_width, target_height), Image.Resampling.LANCZOS)
    pixel_array = np.array(img_resized)

    # 3. Codepic Generation
    output = []
    for row in pixel_array:
        line = ""
        for pixel in row:
            # Linear quantization to find the index
            idx = int(pixel / 256 * levels)
            # Find closest defined level in codebook
            closest = min(defined_levels, key=lambda x: abs(x - idx))
            line += random.choice(mapping[closest])
        output.append(line)
    
    return "\n".join(output)

if __name__ == "__main__":
    # Example execution: python render.py input.jpg lexicons/zh_nature.json
    result = run_codepic(sys.argv[1], sys.argv[2])
    print(result)
