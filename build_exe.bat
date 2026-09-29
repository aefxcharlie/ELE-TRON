@echo off
cd /d "%~dp0"

REM ELE-TRON needs Python 3.13 or newer.
python -c "import sys; sys.exit(0 if sys.version_info >= (3,13) else 1)"
if errorlevel 1 (
    echo ELE-TRON requires Python 3.13 or newer. Install it from python.org and tick "Add python.exe to PATH".
    pause
    exit /b 1
)

pip install pyinstaller
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Fix the error above and run again.
    pause
    exit /b 1
)

pyinstaller --noconsole --noconfirm --name ELE-TRON --icon icon.ico --add-data "ui;ui" --add-data "icon.ico;." ^
  --collect-all mutagen --collect-all pystray --collect-all PIL ^
  --collect-all winrt.runtime ^
  --collect-all winrt.windows.foundation --collect-all winrt.windows.foundation.collections ^
  --collect-all winrt.windows.storage --collect-all winrt.windows.storage.streams ^
  --collect-all winrt.windows.media.control ^
  main.pyw
echo.
echo Done. Your app: dist\ELE-TRON\ELE-TRON.exe
pause
