# Push to GitHub without persisting or printing the token.
#
# The PAT is read from .env at runtime. It is sent as an HTTP Authorization
# header for this one invocation, and the credential helper is disabled, so
# nothing is written to .git/config, the Windows credential store, or the URL
# that git prints.
#
# Usage:
#   powershell -File scripts/push.ps1
#   powershell -File scripts/push.ps1 -Branch main

param(
    [string]$Branch = "main",
    [string]$RemoteUrl = "https://github.com/tedngai/datacenter-efficiency-study.git"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $root ".env"

if (-not (Test-Path $envPath)) {
    throw ".env not found at $envPath. Ask the owner for a GITHUB_PAT and create the file."
}

$token = $null
foreach ($line in Get-Content $envPath) {
    if ($line -match '^\s*GITHUB_PAT\s*=\s*(.+?)\s*$') {
        $token = $Matches[1].Trim('"').Trim("'")
    }
}

if ([string]::IsNullOrWhiteSpace($token)) {
    throw "GITHUB_PAT not found in .env."
}

# Fail fast instead of hanging on an interactive credential prompt.
$env:GIT_TERMINAL_PROMPT = "0"

# HTTP basic auth: base64("x-access-token:<token>"). Sent as a header, never
# embedded in the remote URL, so git's output cannot echo the secret.
$pair = "x-access-token:$token"
$b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$header = "AUTHORIZATION: basic $b64"

Push-Location $root
try {
    Write-Host "Pushing HEAD to $Branch ..."
    git -c credential.helper= -c "http.https://github.com/.extraheader=$header" `
        push $RemoteUrl "HEAD:$Branch"
    if ($LASTEXITCODE -ne 0) {
        throw "git push failed with exit code $LASTEXITCODE"
    }
    Write-Host "Push complete."
}
finally {
    Pop-Location
}
