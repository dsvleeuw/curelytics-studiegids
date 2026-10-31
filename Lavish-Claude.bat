@echo off
chcp 65001 >nul
title CureLytics - Lavish naar Claude
cd /d "%~dp0"
where pwsh >nul 2>nul
if %errorlevel%==0 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0_tools\lavish-claude.ps1" %*
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0_tools\lavish-claude.ps1" %*
)
echo.
pause
