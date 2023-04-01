scoop install scoopet/vmware-workstation-pro

if (!$(Get-Command choco)) {
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}


# C:/ProgramData/chocolatey/bin/choco.exe install dotnet-6.0-sdk -y --pre
# C:/ProgramData/chocolatey/bin/choco.exe install dotnet-5.0-sdk -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install dotnetcore-sdk -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install dotnet-6.0-sdk -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install protonvpn -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install LinkShellExtension -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install p4merge -y --pre
C:/ProgramData/chocolatey/bin/choco.exe install nanum-gothic-coding-font -y --pre
