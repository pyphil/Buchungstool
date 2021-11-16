@echo off
rmdir build /s /q
rmdir dist /s
pyinstaller --icon icon.ico --noconsole Buchungstool.py
cd dist
powershell Compress-Archive Buchungstool\* Buchungstool.zip