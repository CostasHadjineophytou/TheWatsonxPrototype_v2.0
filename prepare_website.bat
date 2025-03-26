@echo off
echo ===== Creating Watsonx Prototype Installer =====

echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo Installing required packages...
pip install pyinstaller
pip install gitpython

echo Building installer...
pyinstaller setup.spec --clean

echo ===== DONE! =====
echo Your installer is ready in the dist\WatsonxPrototype_Installer folder
echo Copy the entire folder to your website's downloads directory
pause 