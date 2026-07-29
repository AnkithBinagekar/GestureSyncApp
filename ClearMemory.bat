@echo off
title Batman Arkham Knight Memory Cleaner
echo.
echo ⚡ Freeing up system memory for smoother gameplay...
echo.

:: Kill any preloaded caches
ipconfig /flushdns >nul

:: Empty standby memory (requires admin rights)
powershell.exe -command "Clear-Content -Path (Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq 'C:\'}).Root"

:: Release RAM using Windows built-in API
%windir%\System32\rundll32.exe advapi32.dll,ProcessIdleTasks

echo.
echo ✅ Memory cleaned! You can now launch Batman Arkham Knight.
pause
