@echo off
setlocal
cd /d "%~dp0"

echo Launching Pyxel Jupyter Lab...
start "" ".venv\Scripts\jupyter-lab.exe" visual_engine\notebook.ipynb
