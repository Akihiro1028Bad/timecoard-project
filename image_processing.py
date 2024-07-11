# image_processing.py
import io
from PIL import Image, ImageEnhance, ImageFilter
import base64

def preprocess_image(image_path, max_size=(2400, 2400), quality=95):
    with Image.open(image_path) as img:
        # グレースケールに変換
        img = img.convert('L')
        
        # コントラスト強調
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # ノイズ除去
        img = img.filter(ImageFilter.MedianFilter(size=3))
        
        # シャープネス強調
        img = img.filter(ImageFilter.SHARPEN)
        
        # リサイズ
        img.thumbnail(max_size, Image.LANCZOS)
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=quality, optimize=True)
    
    processed_image = buffered.getvalue()
    print(f"Preprocessed image size: {len(processed_image)} bytes")
    return processed_image

def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')