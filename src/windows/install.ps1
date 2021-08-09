$moldWindowsRoot = "$env:mold/src/windows"

. "$moldWindowsRoot/install-core.ps1"
. "$moldWindowsRoot/install-extras.ps1"

sudo "$moldWindowsRoot/install-sudo.ps1"
sudo "$moldWindowsRoot/install-extras-sudo.ps1"

dotnet fsi $moldWindowsRoot/install.fsx
dotnet fsi $moldWindowsRoot/install-extras.fsx

Read-Host -Prompt "Script finished. Restart manually if needed. Press any key to close"

