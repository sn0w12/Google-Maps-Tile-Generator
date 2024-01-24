@echo off
setlocal enabledelayedexpansion

python check_dependencies.py > missing_packages.txt
SET DEPENDENCY_CHECK=%ERRORLEVEL%
IF !DEPENDENCY_CHECK! EQU 1 (
    echo Missing packages found.
    set /p UserResponse=Do you want to install missing packages? [Y/n]: 
    IF /I "!UserResponse!"=="Y" (
        echo Installing missing packages...
        for /F "tokens=*" %%i in (missing_packages.txt) do pip install %%i
    ) ELSE (
        echo Skipping package installation.
        exit
    )
)

python map.py

echo Script execution completed.
pause