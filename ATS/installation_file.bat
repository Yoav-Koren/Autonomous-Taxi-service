@echo off
REM Exit if a command fails
setlocal enabledelayedexpansion

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo Installing pygame...
python -m pip install pygame
if errorlevel 1 exit /b 1

echo Installed successfully!
pause