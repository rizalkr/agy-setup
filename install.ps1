$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 (Join-Path $RepoDir "install.py") @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python (Join-Path $RepoDir "install.py") @args
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
  & python3 (Join-Path $RepoDir "install.py") @args
} else {
  throw "Python 3 is required. Install Python 3 and re-run install.ps1."
}

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

$LocalBin = Join-Path $env:USERPROFILE ".local\bin"
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ([string]::IsNullOrEmpty($UserPath)) {
  [Environment]::SetEnvironmentVariable("Path", $LocalBin, "User")
  Write-Host "Added $LocalBin to User PATH. Restart terminal to use agy-index-skills."
} elseif (($UserPath -split ";") -notcontains $LocalBin) {
  [Environment]::SetEnvironmentVariable("Path", "$UserPath;$LocalBin", "User")
  Write-Host "Added $LocalBin to User PATH. Restart terminal to use agy-index-skills."
}
