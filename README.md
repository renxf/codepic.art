# Codepic.art

A character-based image rendering tool that maps pixel density to multilingual script lexicons. Designed with a focus on aspect ratio compensation for monospaced environments and character alignment for consistent visual integrity.

## 1. Image Pre-processing

The objective of this stage is to convert a continuous raw image into a discrete grayscale matrix while correcting geometric distortion caused by text editor line-heights.

### 1.1 Workflow

1. **ROI Extraction**: Selection of the target Region of Interest.
2. **Grayscale Conversion**: Converting the RGB signal into a 256-level grayscale matrix.
3. **Geometric Compensation**: Introducing a $1.3x$ correction factor to counteract the vertical stretching inherent in monospaced fonts.
4. **Resampling**: Downsampling the image to a target grid (e.g., 100x100) using Lanczos interpolation.

### 1.2 Implementation

```python
from PIL import Image
import numpy as np

def preprocess_image(input_path, target_width=100, ratio=1.3):
    """
    Converts an image into a grayscale matrix suitable for character mapping.
    :param ratio: Compensation factor for editor line-height (typically 1.3).
    """
    # Load and convert to grayscale (L mode)
    img = Image.open(input_path).convert('L')
    
    # Calculate height with geometric compensation
    w, h = img.size
    target_height = int((h / w) * target_width / ratio)
    
    # Downsample to target grid
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    return np.array(img_resized)

```

## 2. Lexicon & Grayscale Mapping

The character set is defined as a **Physical Density Codebook**. Characters are categorized into grayscale levels based on their stroke density within a standard grid.

### 2.1 Codebook Schema

Lexicons are stored in JSON format, supporting full sets or thematic subsets.

```json
{
  "lexicon_id": "standard_zh_v1",
  "levels": 16,
  "codebook": [
    {"level": 0, "chars": ["攀", "巍", "麓"], "desc": "High physical density"},
    {"level": 8, "chars": ["兰", "草", "竹"], "desc": "Medium physical density"},
    {"level": 15, "chars": ["　"], "desc": "Zero density (U+3000)"}
  ]
}

```

### 2.2 Character Selection Rules

To maintain visual integrity, the following criteria must be met:

* **Full-Width Guarantee**: Must use full-width characters (CJK) or U+3000 whitespace to ensure a strict 1:1 grid alignment in text environments.
* **Physical Centroid**: Priority is given to characters with a centered visual weight to avoid local geometric shifts.
* **Quantization**: Characters are assigned levels based on their Black Pixel Ratio (BPR) under a reference font (e.g., Source Han Sans).

## 3. Codepic Generation

Mapping the pre-processed pixel matrix $P_{m,n}$ to the character matrix $C_{m,n}$.

### 3.1 Mapping Logic

For any pixel $p \in [0, 255]$, the index $i$ within an $L$-level codebook is calculated as:


$$i = \lfloor \frac{p}{256} \times L \rfloor$$

### 3.2 Implementation

```python
import random

def generate_codepic(pixel_array, codebook, levels=16):
    """
    Generates a character grid based on the grayscale matrix.
    """
    mapping = {item['level']: item['chars'] for item in codebook}
    defined_levels = sorted(mapping.keys())

    output = []
    for row in pixel_array:
        line = ""
        for pixel in row:
            # Linear quantization index
            target = int(pixel / 256 * levels)
            # Match the nearest defined grayscale level
            closest = min(defined_levels, key=lambda x: abs(x - target))
            line += random.choice(mapping[closest])
        output.append(line)
    
    return "\n".join(output)

```

## 4. Philosophy

**Codepic.art** explores image representation through the lens of Information Theory and Semantic Art. By treating characters as physical density tokens, it achieves extreme visual compression (approx. 0.1 bpp) while retaining high-fidelity human features through semantic compensation.

---

## License

MIT
