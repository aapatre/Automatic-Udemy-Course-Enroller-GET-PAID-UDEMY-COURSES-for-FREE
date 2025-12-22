Param(
  [switch]$Debug,
  [string]$VenvPath = ".venv"
)

if (-Not (Test-Path $VenvPath)) {
  . (Join-Path "scripts" "setup.ps1")
} else {
  . (Join-Path $VenvPath "Scripts/Activate.ps1")
}

$argsList = @("-m", "udemy_enroller.cli")
if ($Debug) { $argsList += "--debug" }

python @argsList
