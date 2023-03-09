Write-Output 'mold ()'

$env:scoop = "$env:userprofile/scoop"
$env:mold = "$env:scoop/buckets/mold"

if (!$(Get-Command scoop)) {
    Invoke-RestMethod get.scoop.sh | Invoke-Expression

    [Environment]::SetEnvironmentVariable('SCOOP', $env:scoop, 'User')
    [Environment]::SetEnvironmentVariable('MOLD', $env:mold, 'User')

    [Environment]::SetEnvironmentVariable('PATH', "$env:PATH;" +
        "$env:mold/home/windows/path;" +
        "$env:scoop/persist/rustup/.cargo/bin;" +
        "$env:scoop/apps/nvm/current/nodejs/nodejs;" +
        "$env:scoop/apps/cygwin/current/root/bin"
        , 'User')

}

scoop install main/7zip
scoop install main/git

scoop config SCOOP_REPO 'https://github.com/i574n/Scoop-Core'

Get-ChildItem "$env:scoop/shims" -Filter 'scoop.*' | Copy-Item -Destination { Join-Path $_.Directory.FullName (($_.BaseName -replace 'scoop', 'shovel') + $_.Extension) }

shovel bucket add mold https://github.com/i574n/mold.git

shovel update
shovel status
shovel checkup

. "$env:mold/src/windows/install.ps1"
