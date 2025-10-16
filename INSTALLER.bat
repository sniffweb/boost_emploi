@echo off
chcp 65001 >nul
title Installation BOOST EMPLOIE - DEV BY SNIFFWEB
color 0B

echo.
echo ========================================
echo   INSTALLATION BOOST EMPLOIE
echo        DEV BY SNIFFWEB
echo ========================================
echo.

echo Verification de l'installation...
python verifier_installation.py

echo.
echo Installation terminee !
echo Pour lancer BOOST EMPLOIE: DEMARRER.bat
echo.
pause
