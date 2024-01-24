from PIL import Image
import argparse
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def make_square(image, border_color=(0, 0, 0, 0)):
    x, y = image.size
    size = max(x, y)
    new_image = Image.new("RGBA", (size, size), color=border_color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return new_image

def scale_image(image, zoom_level, border_color):
    square_image = make_square(image, border_color)
    if zoom_level == 0:
        return square_image.resize((256, 256), Image.LANCZOS)
    else:
        new_size = 256 * (2 ** zoom_level)
        return square_image.resize((new_size, new_size), Image.LANCZOS)

def save_tile(tile_data):
    tile, tile_filename = tile_data
    tile.save(tile_filename)

def slice_and_save_image(image, zoom_level, output_directory, border_color):
    tile_size = 256
    scaled_image = scale_image(image, zoom_level, border_color)
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

def parse_color_argument(border_color_arg):
    if border_color_arg.lower() == 'transparent':
        return (0, 0, 0, 0)
    else:
        return tuple(int(border_color_arg[i:i+2], 16) for i in (0, 2, 4)) + (255,)

def create_google_maps_tiles(input_image_path, output_directory, min_zoom, max_zoom, border_color):
    image = Image.open(input_image_path).convert("RGBA")
    for zoom_level in range(min_zoom, max_zoom + 1):
        slice_and_save_image(image, zoom_level, output_directory, border_color)

def main():
    parser = argparse.ArgumentParser(description='Create Google Maps tiles from an image.')
    parser.add_argument('input_image_path', type=str, help='Path to the input image.')
    parser.add_argument('output_directory', type=str, help='Path to the output directory.')
    parser.add_argument('--min_zoom', type=int, default=0, help='Minimum zoom level.')
    parser.add_argument('--max_zoom', type=int, default=5, help='Maximum zoom level.')
    parser.add_argument('--border_color', type=str, default='transparent', help='Border color.')

    args = parser.parse_args()
    border_color = parse_color_argument(args.border_color)
    
    create_google_maps_tiles(args.input_image_path, args.output_directory, args.min_zoom, args.max_zoom, border_color)

if __name__ == "__main__":
    main()