$outDir = "c:\Users\gan\medpatent\doc\downloaded_patents"
if (-Not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }
$data = Get-Content search_results.json | ConvertFrom-Json
foreach ($item in $data.results) {
    $patentNum = $item.metadata.bibliographic_data.patent_number
    if (-not $patentNum) { $patentNum = $item.title -replace '[^a-zA-Z0-9_\-]', '_' }
    $file = Join-Path $outDir "$patentNum.md"
    $content = "# $($item.title)`r`n`r`n**Patent Number:** $patentNum`r`n**URL:** $($item.url)`r`n`r`n## Content / Abstract`r`n`r`n$($item.content)"
    $content | Out-File -FilePath $file -Encoding utf8
}
Write-Host "Patents extracted successfully to $outDir"
