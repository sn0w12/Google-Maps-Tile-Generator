# Google Maps Tile Generator

This Python script generates Google Maps tiles from a given image and compresses all PNG images within a specified directory. It's designed to run either through a command line interface (CLI) with arguments or interactively with a graphical user interface (GUI).

## Features

- Generate Google Maps tiles at specified zoom levels.
- Compress PNG images to reduce file size with customizable quality settings.
- Support for both command line and GUI operations.

## Requirements

- Python 3.x
- Pillow (PIL Fork)
- tqdm

## Installation
Git clone the repo
```
git clone https://github.com/sn0w12/Google-Maps-Tile-Generator
```

Before running the script, ensure you have Python installed. You can install the required packages using:

```
pip install -r requirements.txt
```

Or simply run the run.bat file, it should automatically detect the dependencies you need and download them for you.


## Usage

### Command Line Interface

To run the script with command line arguments:

```
python map.py -i <input_image_path> -o <output_directory> --min_zoom <min_zoom> --max_zoom <max_zoom> --background_color <background_color>  --compress
```


Arguments:
- `-i` or `--input_image_path`: Path to the input image.
- `-o` or `--output_directory`: Path to the output directory for the tiles.
- `--min_zoom`: Minimum zoom level (0).
- `--max_zoom`: Maximum zoom level.
- `--background_color`: Background color for the image. Can be 'transparent' or a hex code without '#'. Default is 'transparent'.
- `--compress`: Add if you want to compress all of the images after the run.

### User Interface

If the script is run without any arguments, it will prompt the user to select the input image and output directory through a GUI dialog. Then it will prompt the user for the min zoom, max zoom and background color in the console.

### Image Compression

After generating tiles, the script automatically compresses all PNG images in the output directory to optimize for web usage.

## Note

Ensure all scripts, batch files, and the `requirements.txt` file are in the same directory for the batch operation to function correctly.

