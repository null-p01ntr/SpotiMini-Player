Set-Location .\src
pyinstaller `
	--onefile `
	--noconsole `
	--icon=img/icon.ico `
	--distpath ../build/Windows `
	--name=SpotiMini `
	spotimini.py

Set-Location ..