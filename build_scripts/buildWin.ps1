Set-Location .\src
pyinstaller `
	--onefile `
	--noconsole `
	--icon=img/icon.ico `
	--distpath ../build/Windows `
	--name=SpotiMini `
	spotimini.py
	
Copy-Item -Path "img\" -Destination "..\build\Windows\img" -Recurse
Set-Location ..