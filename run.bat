@echo off
CALL "C:\ProgramData\anaconda3\Scripts\activate.bat"

echo Please enter the full path to your input image:
set /p inputImagePath="Input image path: "

echo Please enter the full path to your output directory:
set /p outputDirectory="Output directory: "

echo Please enter the minimum zoom level (usually 0):
set /p minZoom="Minimum zoom level: "

echo Please enter the maximum zoom level:
set /p maxZoom="Maximum zoom level: "

python map.py "%inputImagePath%" "%outputDirectory%" --min_zoom %minZoom% --max_zoom %maxZoom%

echo Compressing all images in %outputDirectory%
python compress_images.py "%outputDirectory%"

echo Script execution completed.
pause