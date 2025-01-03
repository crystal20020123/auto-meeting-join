@echo off
REM Create the directory if it doesn't exist
if not exist "C:\chrome\1005" mkdir "C:\chrome\1005"

start chrome.exe -remote-debugging-port=1005 --user-data-dir="C:\chrome\1005"


pause
