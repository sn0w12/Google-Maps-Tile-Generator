from tkinter import Tk, filedialog
from PIL import Image
import argparse
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def compress_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.save(file_path, "PNG", optimize=True, quality=65)
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

def compress_all_images(directory):
    if not directory:  # If no directory is selected, exit the script
        print("No directory selected. Exiting...")
        return

    # Find all PNG images within the specified directory
    files_to_compress = [os.path.join(root, file)
                         for root, dirs, files in os.walk(directory)
                         for file in files if file.lower().endswith('.png')]

    # Initialize tqdm for the list of files to compress
    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(compress_image, files_to_compress), total=len(files_to_compress), desc="Compressing images"))

def ask_directory(title="Select Folder"):
    print(title)
    root = Tk()
    root.withdraw()  # hide the main window
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory

def ask_open_file(title="Select File", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*"))):
    print(title)
    root = Tk()
    root.withdraw()  # hide the main window
    filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return filepath

def make_square(image, background_color=(0, 0, 0, 0)):
    x, y = image.size
    size = max(x, y)
    new_image = Image.new("RGBA", (size, size), color=background_color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return new_image

def scale_image(image, zoom_level, background_color):
    square_image = make_square(image, background_color)
    if zoom_level == 0:
        return square_image.resize((256, 256), Image.LANCZOS)
    else:
        new_size = 256 * (2 ** zoom_level)
        return square_image.resize((new_size, new_size), Image.LANCZOS)

def save_tile(tile_data):
    tile, tile_filename = tile_data
    tile.save(tile_filename)

def slice_and_save_image(image, zoom_level, output_directory, background_color):
    tile_size = 256
    scaled_image = scale_image(image, zoom_level, background_color)
    num_tiles = 2 ** zoom_level
    tasks = []

    for x in range(num_tiles):
        for y in range(num_tiles):
            left = x * tile_size
            upper = y * tile_size
            right = left + tile_size
            lower = upper + tile_size
            
            tile = scaled_image.crop((left, upper, right, lower))
            output_dir = f"{output_directory}/{zoom_level}/{x}"
            os.makedirs(output_dir, exist_ok=True)
            tile_filename = f"{output_dir}/{y}.png"
            tasks.append((tile, tile_filename))
    
    with ThreadPoolExecutor(max_workers=min(32, multiprocessing.cpu_count() + 4)) as executor:
        list(tqdm(executor.map(save_tile, tasks), total=len(tasks), desc=f"Processing zoom level {zoom_level}"))

def parse_color_argument(background_color_arg):
    if background_color_arg.lower() == 'transparent' or background_color_arg == "":
        return (0, 0, 0, 0)
    else:
        return tuple(int(background_color_arg[i:i+2], 16) for i in (0, 2, 4)) + (255,)

def create_google_maps_tiles(input_image_path, output_directory, min_zoom, max_zoom, background_color):
    image = Image.open(input_image_path).convert("RGBA")
    for zoom_level in range(min_zoom, max_zoom + 1):
        slice_and_save_image(image, zoom_level, output_directory, background_color)

def main():
    parser = argparse.ArgumentParser(description='Create Google Maps tiles from an image.')
    parser.add_argument('-i', '--input_image_path', type=str, help='Path to the input image.')
    parser.add_argument('-o', '--output_directory', type=str, help='Path to the output directory.')
    parser.add_argument('--min_zoom', type=int, help='Minimum zoom level.')
    parser.add_argument('--max_zoom', type=int, help='Maximum zoom level.')
    parser.add_argument('--background_color', type=str, help='Background color (transparent, or a hex code without #).')
    parser.add_argument('--compress', action='store_true', help='Compress images after processing.')

    args = parser.parse_args()

    # If not executed with command-line arguments, ask the user for the info
    if args.input_image_path and args.output_directory:
        input_image_path = args.input_image_path
        output_directory = args.output_directory
    else:
        input_image_path = ask_open_file("Select Input Image")
        output_directory = ask_directory("Select Output Directory")

    min_zoom = args.min_zoom if args.min_zoom is not None else int(input("Please enter the minimum zoom level (usually 0): "))
    max_zoom = args.max_zoom if args.max_zoom is not None else int(input("Please enter the maximum zoom level: "))
    background_color = parse_color_argument(args.background_color if args.background_color is not None else input("Enter background color (transparent or hex code without #): "))
    
    create_google_maps_tiles(input_image_path, output_directory, min_zoom, max_zoom, background_color)

    # Ask for compression if not specified in command-line arguments
    compress_images = args.compress
    if not args.compress:
        compress_response = input("Do you want to compress the images? (yes/no): ").lower()
        compress_images = compress_response in ['yes', 'y']

    if compress_images:
        compress_all_images(output_directory)

if __name__ == "__main__":
    main()