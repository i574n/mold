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

scoop install main/aria2

scoop install main/dark
scoop install main/lessmsi
scoop install main/innounp
scoop install main/gsudo

scoop bucket add extras
scoop bucket add games
scoop bucket add java
scoop bucket add jetbrains
scoop bucket add nerd-fonts
scoop bucket add nightlies
scoop bucket add nonportable
scoop bucket add versions

scoop bucket add Ash258 https://github.com/Ash258/Scoop-Ash258.git
scoop bucket add dorado https://github.com/chawyehsu/dorado
scoop bucket add emulators https://github.com/hermanjustnu/scoop-emulators.git
scoop bucket add everyx https://github.com/everyx/scoop-bucket
scoop bucket add rasa https://github.com/rasa/scoops.git
scoop bucket add retools https://github.com/TheCjw/scoop-retools.git
scoop bucket add scoop-clojure https://github.com/littleli/scoop-clojure
scoop bucket add scoopet https://github.com/integzz/scoopet
scoop bucket add spotify https://github.com/TheRandomLabs/Scoop-Spotify.git
# scoop bucket add sushi https://github.com/kidonng/sushi
scoop bucket add wsl https://git.irs.sh/KNOXDEV/wsl
scoop bucket add scoop-completion https://github.com/Moeologist/scoop-completion

scoop install main/dotnet-sdk
scoop install main/pwsh
scoop install extras/anydesk
scoop install extras/fork
scoop install extras/notepadplusplus
scoop install extras/processhacker
scoop install extras/synctrayzor
scoop install extras/vscode-insiders-portable
scoop install jetbrains/rider-portable

winget install powertoys
