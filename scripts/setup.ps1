Param(
    [string]$PythonExe = "python",
    [string]$VenvPath = ".venv"
)

if (-Not (Test-Path $VenvPath)) {
  & $PythonExe -m venv $VenvPath
}

$env:VIRTUAL_ENV = (Resolve-Path $VenvPath).Path
$activate = Join-Path $VenvPath "Scripts/Activate.ps1"
. $activate

pip install --upgrade pip
pip install -e .
if (Test-Path "requirements-dev.txt") {
  pip install -r requirements-dev.txt
}

Write-Host "Environment ready. To activate later: .\$VenvPath\Scripts\Activate.ps1"
