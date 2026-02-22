Param(
  [string]$VenvPath = ".venv"
)

if (-Not (Test-Path $VenvPath)) {
  . (Join-Path "scripts" "setup.ps1")
} else {
  . (Join-Path $VenvPath "Scripts/Activate.ps1")
}

if (Test-Path "requirements-dev.txt") {
  pip install -r requirements-dev.txt
}

pytest -q
