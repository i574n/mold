echo "install-sudo.ps1 ()"

function WindowsFeature {
    [CmdletBinding()]
    param(
        [Parameter(Position=0,Mandatory=$true)] [string]$FeatureName
    )
    if(!$((Get-WindowsOptionalFeature -FeatureName $FeatureName -Online).State -eq "Enabled")) {
        Enable-WindowsOptionalFeature -Online -FeatureName $FeatureName -All -Verbose # asks for restart
    } else {
        echo "$FeatureName already installed"
    }
}

Set-MpPreference -DisableRealtimeMonitoring $true
Add-MpPreference -ExclusionPath "$env:scoop"
Add-MpPreference -ExclusionPath 'C:/ProgramData/scoop'

WindowsFeature -FeatureName Microsoft-Hyper-V
WindowsFeature -FeatureName Microsoft-Windows-Subsystem-Linux
WindowsFeature -FeatureName Containers

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

$policiesSystemKey = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'
Set-ItemProperty $policiesSystemKey "Segoe UI (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Bold (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Bold Italic (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Italic (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Black (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Light (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Semilight (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Semibold (TrueType)" ""
Set-ItemProperty $policiesSystemKey "Segoe UI Symbol (TrueType)" ""

$policiesSystemKey = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes'
Set-ItemProperty $policiesSystemKey "Segoe UI" "Roboto Condensed Light"

Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layout' `
    -Name "Scancode Map" `
    -Value ([byte[]](0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00,     `
            0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x3a, 0x00, 0x00, 0x00, 0x00, 00))

Get-ChildItem "$env:mold/fonts" | ForEach-Object {
    if(![System.IO.File]::Exists("$env:windir/Fonts/$_")){
        New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts' -Name $_.Name.Replace($_.Extension, ' (TrueType)') -Value $_.Name -Force | Out-Null
        Copy-Item $_.FullName -destination $env:windir/Fonts/
        echo "$env:windir/Fonts/$_ copied"
    } else {
        echo "$env:windir/Fonts/$_ already exists"
    }
}

reg import "$env:scoop/apps/vscode/current/install-context.reg"

if(![System.IO.File]::Exists("$env:userprofile/.ideavimrc")){
    New-Item -Path "$env:userprofile/.ideavimrc" -ItemType SymbolicLink -Value $env:mold/vimfiles/.ideavimrc
}

if(![System.IO.File]::Exists("$env:userprofile/.vimrc")){
    New-Item -Path "$env:userprofile/.vimrc" -ItemType SymbolicLink -Value $env:mold/vimfiles/.vimrc
}

if(![System.IO.File]::Exists("$env:LOCALAPPDATA/Microsoft/PowerToys")){
    New-Item -Path "$env:LOCALAPPDATA/Microsoft/PowerToys/FancyZones" -ItemType SymbolicLink -Value $env:mold/dist/appdata/FancyZones
}


# mkdir $env:scoop/persist/rider-portable/profile/config/settingsRepository
# New-Item -Path "$env:scoop/persist/rider-portable/profile/config/settingsRepository/repository" -ItemType SymbolicLink -Value $env:mold/dist/appdata/rider
# "$env:mold/dist/appdata/rider"

if(![System.IO.Directory]::Exists("$env:mold/dist/appdata/rider/.git")){
    pushd
    echo "initializing rider repo"
    cd "$env:mold/dist/appdata/rider"
    git init
    git add .
    git commit -m '.'
    popd
}

scoop install extras/vcredist2019
scoop install extras/vcredist2015
scoop install extras/vcredist2013
scoop install extras/vcredist2005

scoop install main/nvm
nvm install latest
nvm use $( nvm list )

scoop install -g nerd-fonts/FiraCode
scoop install nonportable/asio4all-np

scoop install rasa/wfc
