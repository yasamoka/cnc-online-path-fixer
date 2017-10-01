pyinstaller -w --icon=Icon_5.ico cnc-online-path-fixer.py
cp Icon_5.ico dist/cnc-online-path-fixer/Icon_5.ico
cd dist
rename cnc-online-path-fixer "C&C Online Path Fixer"
cd ..