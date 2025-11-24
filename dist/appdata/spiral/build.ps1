param(
    $ScriptDir = $PSScriptRoot
)
Set-Location $ScriptDir
$ErrorActionPreference = "Stop"
. c:/home/git/polyglot/scripts/core.ps1


$projectName = "appdata"

# { . c:/home/git/polyglot/apps/spiral/dist/Supervisor$(_exe) --build-file "$projectName.spi" "$projectName.lua" --timeout 300000 } | Invoke-Block
{ . c:/home/git/polyglot/apps/spiral/dist/Supervisor$(_exe) --build-file "$projectName.spi" "$projectName.py" --timeout 300000 } | Invoke-Block

# $output = { . c:/home/git/spiral/workspace/target/release/spiral$(_exe) lua --lua-path "$ScriptDir/$projectName.lua" } | Invoke-Block
$output = { python "$projectName.py" } | Invoke-Block
Write-Output "`$output: $output"
$output > ".$projectName.toml.txt"
