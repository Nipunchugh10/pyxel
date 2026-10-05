$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$Jupyter = Join-Path $ScriptDir ".venv\Scripts\jupyter-lab.exe"
$Notebook = Join-Path $ScriptDir "visual_engine\notebook.ipynb"

Write-Host "==> Launching Pyxel Jupyter Lab..." -ForegroundColor Cyan
Start-Process $Jupyter -ArgumentList "`"$Notebook`""
