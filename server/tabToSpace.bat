@echo off
setlocal enabledelayedexpansion
for /r "./api" %%i in (*.py) do (
    powershell -Command "(Get-Content '%%i') -replace '\t', '    ' | Set-Content '%%i'"
    echo %%i success!.
)
echo Done!
pause