conda activate base

Set-Location .\src
pyinstaller `
	--onefile `
	--noconsole `
	--hiddenimport http.server `
	--paths='O:\_dev\venvs\sptm\conda-meta\' `
	--paths='O:\_dev\venvs\sptm\Library\bin' `
	--paths='O:\_dev\venvs\sptm\Lib\site-packages' `
	--icon=img/icon.ico `
	--name=SpotiMini `
	spotimini.py

Set-Location ..

# --paths='C:\Users\dogac\_dev\anaconda3' `
# --paths='C:\Users\dogac\_dev\anaconda3\pkgs' `
# --paths='C:\Users\dogac\_dev\anaconda3\Library\ssl' `
# --hiddenimport spotipy `
# --hiddenimport urllib3 `