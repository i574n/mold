
# Get-TimeZone -ListAvailable
Set-TimeZone ($env:MOLD_TIMEZONE, "E. South America Standard Time" | Select -First 1) # -3

Set-WinUserLanguageList -LanguageList ($env:MOLD_KEYBOARD, "pt-BR" | Select -First 1) -Force

$explorerAdvancedKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
Set-ItemProperty $explorerAdvancedKey HideFileExt 0
Set-ItemProperty $explorerAdvancedKey ShowSuperHidden 1
Set-ItemProperty $explorerAdvancedKey Hidden 1
Set-ItemProperty $explorerAdvancedKey TaskbarGlomLevel 2
Set-ItemProperty $explorerAdvancedKey TaskbarSmallIcons 2
Set-ItemProperty $explorerAdvancedKey PersistBrowsers 1
Set-ItemProperty $explorerAdvancedKey NavPaneExpandToCurrentFolder 1

shovel install main/aria2

shovel install main/dark
shovel install main/lessmsi
shovel install main/innounp
shovel install main/gsudo

shovel bucket add extras
shovel bucket add games
shovel bucket add java
shovel bucket add jetbrains
shovel bucket add nerd-fonts
shovel bucket add nonportable
shovel bucket add versions

shovel bucket add Ash258 https://github.com/Ash258/Scoop-Ash258.git
shovel bucket add dorado https://github.com/chawyehsu/dorado
shovel bucket add emulators https://github.com/hermanjustnu/scoop-emulators.git
shovel bucket add rasa https://github.com/rasa/scoops.git
shovel bucket add retools https://github.com/TheCjw/scoop-retools.git
shovel bucket add scoop-clojure https://github.com/littleli/scoop-clojure
shovel bucket add scoopet https://github.com/ivaquero/scoopet


shovel install main/cygwin
shovel install main/dotnet-sdk
shovel install main/pwsh
shovel install main/neovim
shovel install main/rclone
shovel install java/graalvm-nightly-jdk17
shovel install extras/discord
shovel install extras/electrum
shovel install extras/everything
shovel install extras/fork
shovel install extras/notepadplusplus
shovel install extras/obs-studio
shovel install extras/processhacker
shovel install extras/scoop-completion
shovel install extras/sumatrapdf
shovel install extras/sysinternals
shovel install extras/telegram
shovel install extras/treesize-free
shovel install extras/vivaldi
shovel install extras/vscode
shovel install extras/windirstat
shovel install extras/winmerge
shovel install extras/yed
shovel install scoop-clojure/clj-deps

winget install "microsoft powertoys"
