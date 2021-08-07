Write-Output 'Installing mold...'

$osPath = "$env:scoop/buckets/mold/home/path/windows"

if(!$(gcm scoop)) {
	Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

	scoop install main/7zip
	scoop install main/git

	scoop bucket add mold https://github.com/fc1943s/mold.git
	
	[Environment]::SetEnvironmentVariable('scoop', "$env:userprofile/scoop", 'User')
	
	[Environment]::SetEnvironmentVariable('Path', "$env:Path;" + 
	    $osPath + ";" +
		"$scoop\persist\rustup\.cargo\bin;" +
		"$scoop\apps\nvm\current\nodejs\nodejs;" +
		"$scoop\apps\cygwin\current\root\bin"
	, 'User')
}

$windowsRoot = "$env:scoop/buckets/mold/src/windows"

. $windowsRoot/install-dotnet.ps1

dotnet fsi $windowsRoot/install.fsx

. $windowsRoot/install-scoop-extras.ps1

scoop bucket add extras

Read-Host -Prompt "Script finished. Restart manually if needed. Press any key to close"
