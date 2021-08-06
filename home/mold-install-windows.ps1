Write-Output 'Installing mold...'

if ($true -or !$( which scoop ))
{
	if (!$( which scoop ))
	{
		Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression
	}
	
	Read-Host -Prompt "Script finished. Please restart manually. Press any key to close"
}
else
{
	scoop update
}
