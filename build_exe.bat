@echo off
cd /d "%~dp0"
pip install pyinstaller pywebview
pyinstaller --noconsole --noconfirm --name ELE-TRON --icon icon.ico --add-data "ui;ui" main.pyw
echo.
echo Done. Your app: dist\ELE-TRON\ELE-TRON.exe
pause
