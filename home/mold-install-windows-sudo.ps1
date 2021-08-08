Write-Output "Installing mold (sudo)..."

Add-MpPreference -ExclusionPath "C:\Users\$env:UserName\scoop"
Add-MpPreference -ExclusionPath 'C:\ProgramData\scoop'
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All # asks for restart
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux # asks for restart

$policiesSystemKey = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
Set-ItemProperty $policiesSystemKey PersistBrowsers 1
Set-ItemProperty $policiesSystemKey ConsentPromptBehaviorAdmin 5
Set-ItemProperty $policiesSystemKey ConsentPromptBehaviorUser 3
Set-ItemProperty $policiesSystemKey EnableInstallerDetection 1
Set-ItemProperty $policiesSystemKey EnableLUA 1
Set-ItemProperty $policiesSystemKey EnableVirtualization 1
Set-ItemProperty $policiesSystemKey PromptOnSecureDesktop 0
Set-ItemProperty $policiesSystemKey ValidateAdminCodeSignatures 0
Set-ItemProperty $policiesSystemKey FilterAdministratorToken 0

Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layout' `
	-Name "Scancode Map" `
	-Value ([byte[]](0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00,     `
			0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x3a, 0x00, 0x00, 0x00, 0x00, 00))

Get-ChildItem "../fonts" | ForEach-Object {
    New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts' -Name $_.Name.Replace($_.Extension, ' (TrueType)') -Value $_.Name -Force | Out-Null
    Copy-Item $_.FullName -destination \"$env:windir\\Fonts\"
}

# mkdir $env:scoop/persist/rider-portable/profile/config/settingsRepository
# New-Item -Path "$env:scoop/persist/rider-portable/profile/config/settingsRepository/repository" -ItemType SymbolicLink -Value $env:mold/home/appdata/rider
# "$env:mold/home/appdata/rider"

if(![System.IO.File]::Exists("$env:mold/home/appdata/rider/.git")){
	pushd
	echo "initializing rider repo"
	cd "$env:mold/home/appdata/rider"
	git init
	git add .
	git commit -m '.'
	popd
}

