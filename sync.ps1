$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 (Join-Path $RepoDir "sync.py")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python (Join-Path $RepoDir "sync.py")
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
  & python3 (Join-Path $RepoDir "sync.py")
} else {
  throw "Python 3 is required. Install Python 3 and re-run sync.ps1."
}
