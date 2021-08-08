$explorerAdvancedKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
Set-ItemProperty $explorerAdvancedKey HideFileExt 0
Set-ItemProperty $explorerAdvancedKey ShowSuperHidden 1
Set-ItemProperty $explorerAdvancedKey Hidden 1
Set-ItemProperty $explorerAdvancedKey TaskbarGlomLevel 2
Set-ItemProperty $explorerAdvancedKey PersistBrowsers 1

$osPath = "$env:mold/home/windows/path"

scoop bucket add extras
scoop bucket add jetbrains
scoop bucket add nerd-fonts

scoop install main/gsudo

scoop install main/dotnet-sdk
scoop install extras/anydesk
scoop install extras/fork
scoop install extras/synctrayzor
scoop install extras/vscode-insiders-portable
scoop install jetbrains/rider-portable

C:\Users\root\scoop\apps\vscode-insiders-portable\current\vscode-install-context.reg

# git clone https://github.com/fc1943s/rss.git $env:userprofile/home/fs/repos/rss


echo "let env=""idea""`r`nsource $env:mold\vimfiles\core.vim" > $env:userprofile/.ideavimrc
echo "let env=""sh""`r`nsource $env:mold\vimfiles\core.vim" > $env:userprofile/.vimrc

if(![System.IO.File]::Exists("./mold-install-windows-sudo.ps1")) {
    curl.exe -LO fc1943s.github.io/mold/mold-install-windows-sudo.ps1
}
sudo "$mold/src/windows/install-sudo.ps1"

$windowsRoot = "$scoop/buckets/mold/src/windows"
# . $windowsRoot/install-scoop-extras.ps1
# . $windowsRoot/install-dotnet.ps1
echo fsharp starting...
dotnet fsi $windowsRoot/install.fsx

Read-Host -Prompt "Script finished. Restart manually if needed. Press any key to close"
