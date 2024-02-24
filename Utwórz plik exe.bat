@echo off
cd /d %~dp0
pyinstaller --onefile --name "generator danych dobowo godzinowych" gui.pyw
echo Cleaning up...
rd /s /q build
del /f /q "generator danych dobowo godzinowych.spec"

echo Moving the .exe file...
if exist "generator danych dobowo godzinowych.exe" del /f /q "generator danych dobowo godzinowych.exe"
move /y dist\"generator danych dobowo godzinowych.exe" .\
echo .exe file moved.

echo Removing dist folder...
rd /s /q dist
echo Done.
pause