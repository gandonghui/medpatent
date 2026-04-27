param(
    [string]$SourceRoot = "c:\Users\pumch\Desktop\medpatent\downloaded_patents",
    [string]$TargetRoot = "C:\Users\pumch\Desktop\patent",
    [switch]$PreCheck,
    [switch]$Force
)

$SkillScript = "c:\Users\pumch\Desktop\medpatent\.agents\skills\markdown-to-docx\scripts\convert.cjs"
$ErrorLog = "c:\Users\pumch\Desktop\medpatent\conversion_errors.log"

# Initialization
if (!(Test-Path $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot | Out-Null
}

$mdFiles = Get-ChildItem -Path $SourceRoot -Filter *.md -Recurse

if ($PreCheck) {
    Write-Host "--- Pre-check Results ---" -ForegroundColor Cyan
    $conflicts = @()
    foreach ($file in $mdFiles) {
        $relativePath = $file.FullName.Substring($SourceRoot.Length + 1)
        $targetPath = Join-Path $TargetRoot ($relativePath.Replace(".md", ".docx"))
        if (Test-Path $targetPath) {
            $conflicts += $targetPath
        }
    }

    Write-Host "Total files to convert: $($mdFiles.Count)"
    Write-Host "Found $($conflicts.Count) potential conflicts (existing .docx files)." -ForegroundColor Yellow
    
    if ($conflicts.Count -gt 0) {
        Write-Host "Examples of conflicts:"
        $conflicts | Select-Object -First 10 | ForEach-Object { Write-Host " - $_" }
    }
    exit
}

# Actual Conversion
Write-Host "Starting batch conversion..." -ForegroundColor Green
$errorCount = 0
if (Test-Path $ErrorLog) { Remove-Item $ErrorLog }

foreach ($file in $mdFiles) {
    $relativePath = $file.FullName.Substring($SourceRoot.Length + 1)
    $targetFile = $relativePath.Replace(".md", ".docx")
    $targetPath = Join-Path $TargetRoot $targetFile
    $targetDir = Split-Path $targetPath

    # Ensure target directory exists
    if (!(Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }

    if ((Test-Path $targetPath) -and !$Force) {
        Write-Host "Skipping existing: $($file.Name)" -ForegroundColor Gray
        continue
    }

    Write-Host "Converting: $($file.Name) ..."
    try {
        # Using Bypass for execution policy consistency
        $cmd = "node $SkillScript -i $($file.FullName) -o $targetPath"
        $result = powershell -ExecutionPolicy Bypass -Command $cmd | ConvertFrom-Json
        
        if ($result.success -ne $true) {
            throw "Conversion failed for $($file.Name)"
        }
    } catch {
        $errorCount++
        $errMsg = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ERROR: $($file.FullName) -> $($_.Exception.Message)"
        $errMsg | Out-File -FilePath $ErrorLog -Append
        Write-Host "  FAILED: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Conversion finished." -ForegroundColor Green
Write-Host "Total processed: $($mdFiles.Count)"
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount (Check $ErrorLog for details)" -ForegroundColor Red
} else {
    Write-Host "Errors: $errorCount (Check $ErrorLog for details)" -ForegroundColor Green
}
