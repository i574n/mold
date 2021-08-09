Write-Output 'Installing mold...'

$env:scoop = "$env:userprofile/scoop"
$env:mold = "$env:scoop/buckets/mold"

if(!$(gcm scoop)) {
    Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

    scoop install main/7zip
    scoop install main/git

    scoop config SCOOP_REPO 'https://github.com/Ash258/Scoop-Core'

    scoop bucket add mold https://github.com/fc1943s/mold.git

    scoop update

    [Environment]::SetEnvironmentVariable('SCOOP', $env:scoop, 'User')
    [Environment]::SetEnvironmentVariable('MOLD', $env:mold, 'User')

    [Environment]::SetEnvironmentVariable('PATH', "$env:PATH;" +
        "$env:mold/home/windows/path;" +
        "$env:scoop\persist\rustup\.cargo\bin;" +
        "$env:scoop\apps\nvm\current\nodejs\nodejs;" +
        "$env:scoop\apps\cygwin\current\root\bin"
    , 'User')

}

. "$env:mold/src/windows/install.ps1"
