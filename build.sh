echo Source wheel
rm -rf build dist MANIFEST.in pyzbar.egg-info
cp MANIFEST.in.all MANIFEST.in
./setup.py bdist_wheel

echo Windows 32-bit wheel
rm -rf build pyzbar.egg-info
cat MANIFEST.in.all MANIFEST.in.win32 > MANIFEST.in
./setup.py bdist_wheel --plat-name=win32

echo Windows 32-bit wheel
# Remove these dirs to prevent win32 DLLs from being included in win64 build
rm -rf build pyzbar.egg-info
cat MANIFEST.in.all MANIFEST.in.win64 > MANIFEST.in
./setup.py bdist_wheel --plat-name=win_amd64

echo Clean
rm -rf build MANIFEST.in pyzbar.egg-info
