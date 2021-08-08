Write-Output 'Installing mold...'

$scoop = "$env:userprofile/scoop"
$mold = "$scoop/buckets/mold"
$osPath = "$mold/home/windows/path"

if(!$(gcm scoop)) {
	$explorerAdvancedKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
	Set-ItemProperty $explorerAdvancedKey HideFileExt 0
	Set-ItemProperty $explorerAdvancedKey ShowSuperHidden 1
	Set-ItemProperty $explorerAdvancedKey Hidden 1
	Set-ItemProperty $explorerAdvancedKey TaskbarGlomLevel 2
	Set-ItemProperty $explorerAdvancedKey PersistBrowsers 1

	Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

	scoop install main/7zip
	scoop install main/git

	scoop bucket add mold https://github.com/fc1943s/mold.git
	
	[Environment]::SetEnvironmentVariable('SCOOP', $scoop, 'User')
	[Environment]::SetEnvironmentVariable('MOLD', $mold, 'User')
	
	[Environment]::SetEnvironmentVariable('PATH', "$env:PATH;" + 
	    "$mold/home/path/windows;" +
		"$scoop\persist\rustup\.cargo\bin;" +
		"$scoop\apps\nvm\current\nodejs\nodejs;" +
		"$scoop\apps\cygwin\current\root\bin"
	, 'User')
}

scoop config SCOOP_REPO 'https://github.com/Ash258/Scoop-Core'

scoop update

scoop bucket add extras
scoop bucket add jetbrains

scoop install main/gsudo

scoop install main/dotnet-sdk
scoop install extras/anydesk
scoop install extras/fork
scoop install extras/synctrayzor
scoop install jetbrains/rider-portable

# git clone https://github.com/fc1943s/rss.git $env:userprofile/home/fs/repos/rss


echo "let env=""idea""`r`nsource $env:mold/vimfiles/core.vim" > $env:userprofile/.ideavimrc
echo "let env=""sh""`r`nsource $env:mold/vimfiles/core.vim" > $env:userprofile/.vimrc

sudo ./mold-install-windows-sudo.ps1


$windowsRoot = "$scoop/buckets/mold/src/windows"
# . $windowsRoot/install-scoop-extras.ps1
# . $windowsRoot/install-dotnet.ps1
echo fsharp starting...
dotnet fsi $windowsRoot/install.fsx

Read-Host -Prompt "Script finished. Restart manually if needed. Press any key to close"
