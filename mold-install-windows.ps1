Write-Output 'Installing mold...'

Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression
scoop bucket add mold https://github.com/fc1943s/mold.git

Read-Host -Prompt "Script finished. Restart manually if needed. Press any key to close"
