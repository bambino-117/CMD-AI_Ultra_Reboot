@echo off
echo Starting System Monitor Server...
set FLASK_APP=extensions/System_monitor/ancrage_sys_mon.py
C:\Users\boris\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe -m flask run --port=5001
