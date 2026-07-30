@echo off
echo Select Language / Επιλογή Γλώσσας
echo.
echo [1] Greek / Ελληνικά
echo [2] English
echo.
set /p choice=Enter 1 or 2: 

if "%choice%"=="1" (
    start "" "Xenios_GR.exe"
) else if "%choice%"=="2" (
    start "" "Xenios_EN.exe"
) else (
    echo Invalid choice. / Λάθος επιλογή.
    pause
)
