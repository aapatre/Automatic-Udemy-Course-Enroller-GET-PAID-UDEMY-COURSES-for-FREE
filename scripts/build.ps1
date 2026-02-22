Param(
  [string]$VenvPath = ".venv"
)

if (Test-Path $VenvPath) { . (Join-Path $VenvPath "Scripts/Activate.ps1") }

pip install build
python -m build
