# Google Maps Tile Generator

This Python script generates Google Maps/ Leaflet tiles from a given image and compresses all PNG images within a specified directory. It's designed to run either through a command line interface with arguments or interactively with a user interface.

## Features

- Generate Map tiles at specified zoom levels.
- Compress PNG images to reduce file size.
- Support for both command line and GUI operations.

## Requirements

- Python 3.x
- Pillow (PIL Fork)
- tqdm
- pngquant

## Installation

### Installing pngquant

#### Windows

1. **Download pngquant**: Visit the pngquant website at https://pngquant.org/ and download the latest version for Windows.
2. **Extract the ZIP File**: Once downloaded, extract the ZIP file to a location on your computer, such as `C:\Program Files\pngquant`.
3. **Add to PATH**: To use pngquant from the command line, you need to add it to your system's PATH environment variable.
   - Right-click on **This PC** or **My Computer** and select **Properties**.
   - Click on **Advanced system settings** and then on the **Environment Variables** button.
   - In the System Variables section, scroll down and select the **Path** variable, then click **Edit**.
   - Click **New** and add the path to the folder where you extracted pngquant (e.g., `C:\Program Files\pngquant`).
   - Click **OK** to close all dialogs.

#### macOS

1. **Install Homebrew**: If not already installed, install Homebrew by pasting the following command in a terminal:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   ```
2. **Install pngquant**: With Homebrew installed, run the following command to install pngquant:
   ```
   brew install pngquant
   ```

#### Linux (Ubuntu/Debian)

1. **Install pngquant**: Open a terminal and run the following command to install pngquant:
   ```
   sudo apt-get update && sudo apt-get install pngquant
   ```

### Google-Maps-Tile-Generator


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
python map.py -i <input_image_path> -o <output_directory> --min_zoom <min_zoom> --max_zoom <max_zoom> --background_color <background_color>
```


Arguments:
- `-i` or `--input_image_path`: Path to the input image.
- `-o` or `--output_directory`: Path to the output directory for the tiles.
- `--min_zoom`: Minimum zoom level (0).
- `--max_zoom`: Maximum zoom level.
- `--background_color`: Background color for the image. Can be 'transparent' or a hex code without '#'.

### User Interface

If the script is run without any arguments, it will prompt the user to select the input image and output directory through a GUI dialog. Then it will prompt the user for the min zoom, max zoom and background color in the console.

### Image Compression

After generating tiles, the script automatically compresses all PNG images in the output directory to optimize for web usage.

## Note

Ensure all scripts, batch files, and the `requirements.txt` file are in the same directory for the batch operation to function correctly.

