@echo off
rmdir build /s /q
rmdir dist /s
pyinstaller --icon icon.ico --noconsole Buchungstool.py
rem pyinstaller --icon icon.ico kursbuch.py
rem cd dist
rem powershell Compress-Archive kursbuch\* kursbuch.zip