from PIL import Image
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def compress_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.save(file_path, "PNG", optimize=True, quality=65)
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

def main(directory):
    # Find all PNG images within the specified directory
    files_to_compress = [os.path.join(root, file)
                         for root, dirs, files in os.walk(directory)
                         for file in files if file.lower().endswith('.png')]
    
    # Initialize tqdm for the list of files to compress
    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(compress_image, files_to_compress), total=len(files_to_compress), desc="Compressing images"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress_images.py <directory>")
        sys.exit(1)
    main(sys.argv[1])