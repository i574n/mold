Write-Output 'Installing mold...'

Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

if ($( gcm scoop ))
{
	scoop update
}

Read-Host -Prompt "Script finished. Please restart manually. Press any key to close"
