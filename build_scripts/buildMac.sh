cd src

pyinstaller \
	--onefile \
	--noconsole \
	--distpath ../build/MacOS \
	--icon=img/icon.icns \
	--name=SpotiMini \
	spotimini.py

cp -R img ../build/MacOS/img
cd ..