# Set strict error handling
$ErrorActionPreference = "Stop"

Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]'7.2') {
    $PSNativeCommandUseErrorActionPreference = $true
}

Write-Host "🧹 Formatting all Bicep files..."

Get-ChildItem -Path . -Recurse -Filter *.bicep | ForEach-Object {
    Write-Host "⌛ Formatting $($_.FullName)"
    az bicep format -f "$($_.FullName)"
}

Write-Host "✅ All Bicep files have been formatted!"
