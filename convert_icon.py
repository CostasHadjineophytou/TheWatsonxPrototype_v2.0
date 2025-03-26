from PIL import Image
import os

def convert_to_ico():
    input_path = os.path.join('frontend', 'assets', 'images', 'watsonx_icon.png')
    output_path = os.path.join('frontend', 'assets', 'images', 'watsonx_icon.ico')
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return
    
    try:
        # Open the PNG image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create ICO file
        img.save(output_path, format='ICO')
        print(f"Successfully created {output_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

if __name__ == "__main__":
    convert_to_ico() 