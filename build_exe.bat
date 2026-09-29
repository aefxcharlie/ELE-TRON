@echo off
cd /d "%~dp0"
pip install pyinstaller pywebview

REM Optional extras: MP3/WAV metadata+artwork (mutagen), tray icon (pystray),
REM live Apple Music sync (winsdk). App still works fully without these.
pip install mutagen pystray winsdk >nul 2>nul

set EXTRA=
pip show mutagen >nul 2>nul && set EXTRA=%EXTRA% --collect-all mutagen
pip show pystray >nul 2>nul && set EXTRA=%EXTRA% --collect-all pystray
pip show winsdk >nul 2>nul && set EXTRA=%EXTRA% --collect-all winsdk

pyinstaller --noconsole --noconfirm --name ELE-TRON --icon icon.ico --add-data "ui;ui" %EXTRA% main.pyw
echo.
echo Done. Your app: dist\ELE-TRON\ELE-TRON.exe
pause
