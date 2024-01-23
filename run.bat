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

REM Path to pngquant executable
set "PNGQUANT_PATH=C:\pngquant\pngquant.exe"

echo Compressing all images in %OutputDirectory%
for /r %OutputDirectory% %%i in (*.png) do (
    "%PNGQUANT_PATH%" --force --skip-if-larger --output "%%i" -- "%%i"
)

echo Script execution completed.
pause