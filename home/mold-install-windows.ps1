Write-Output 'Installing mold...'

$scoop = "$env:userprofile/scoop"
$mold = "$scoop/buckets/mold"

if(!$(gcm scoop)) {
    Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

    scoop install main/7zip
    scoop install main/git

    scoop config SCOOP_REPO 'https://github.com/Ash258/Scoop-Core'

    scoop bucket add mold https://github.com/fc1943s/mold.git

    scoop update

    [Environment]::SetEnvironmentVariable('SCOOP', $scoop, 'User')
    [Environment]::SetEnvironmentVariable('MOLD', $mold, 'User')

    [Environment]::SetEnvironmentVariable('PATH', "$env:PATH;" +
        "$mold/home/path/windows;" +
        "$scoop\persist\rustup\.cargo\bin;" +
        "$scoop\apps\nvm\current\nodejs\nodejs;" +
        "$scoop\apps\cygwin\current\root\bin"
    , 'User')

}

. "$mold/src/windows/install.ps1"
