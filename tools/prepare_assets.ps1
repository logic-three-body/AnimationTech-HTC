param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$cacheRoot = Join-Path $repoRoot ".cache"
$lafanFailureStamp = Join-Path $cacheRoot "lafan1.unavailable.txt"
$lafanZip = Join-Path $cacheRoot "lafan1.zip"
$lafanExtracted = Join-Path $cacheRoot "lafan1_extracted"
$lafanTarget = Join-Path $repoRoot "resources\lafan1\bvh"
$lafanUrl = "https://media.githubusercontent.com/media/ubisoft/ubisoft-laforge-animation-dataset/refs/heads/master/lafan1/lafan1.zip"

New-Item -ItemType Directory -Force -Path $cacheRoot, $lafanTarget | Out-Null

$hasTargetData = (Test-Path $lafanTarget) -and ((Get-ChildItem -Path $lafanTarget -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
if ($hasTargetData -and -not $Force) {
    Write-Host "lafan1 data already prepared at $lafanTarget"
    exit 0
}

try {
    if ($Force) {
        Remove-Item -Path $lafanZip, $lafanExtracted -Force -Recurse -ErrorAction SilentlyContinue
    }

    if (-not (Test-Path $lafanZip)) {
        $ProgressPreference = "SilentlyContinue"
        Invoke-WebRequest -Uri $lafanUrl -OutFile $lafanZip -UseBasicParsing
    }

    Remove-Item -Path $lafanExtracted -Force -Recurse -ErrorAction SilentlyContinue
    Expand-Archive -Path $lafanZip -DestinationPath $lafanExtracted -Force

    $bvhFiles = Get-ChildItem -Path $lafanExtracted -Filter "*.bvh" -File -ErrorAction Stop
    if (($bvhFiles | Measure-Object).Count -eq 0) {
        throw "Downloaded lafan1 archive did not contain any BVH files."
    }

    Copy-Item -Path (Join-Path $lafanExtracted "*.bvh") -Destination $lafanTarget -Force
    Remove-Item -Path $lafanFailureStamp -Force -ErrorAction SilentlyContinue
    Write-Host "lafan1 data prepared at $lafanTarget"
}
catch {
    $message = "Unable to retrieve lafan1 BVH files from the public archive URL."
    Set-Content -Path $lafanFailureStamp -Value ($message + "`n") -Encoding UTF8
    throw $message
}
