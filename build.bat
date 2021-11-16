@echo off
rmdir build /s /q
rmdir dist /s
pyinstaller --icon icon.ico --noconsole Buchungstool.py
cd dist
powershell Compress-Archive Buchungstool\* Buchungstool-1.0.2-win64.zip