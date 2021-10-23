## Development

```
python -m venv venv
source ./venv/bin/activate
pip install -U pip==20.3.4
pip install -r requirements.txt

python -m pytest --verbose --cov=pyzbar --cov-report=term-missing --cov-report=html pyzbar
python -m pyzbar.scripts.read_zbar pyzbar/tests/code128.png
```

### Test matrix of supported Python versions

Run tox

```
rm -rf .tox && tox
```

### Windows

Save the 32-bit and 64-bit `zbar.dll` files, and their dependencies,
to `libzbar-32.dll` and `libzbar-64.dll` respectively, in the `pyzbar` directory.
The `load_zbar` function in `wrapper.py` looks for the appropriate `DLL`s.
The appropriate `DLL`s are packaged up into the wheel build and is installed
alongside the package source. This strategy allows the same method to be used
when `pyzbar` is run from source, as an installed package and when included in a
frozen binary.

## Releasing

1. Build
    Create source and wheel builds. The `win32` and `win_amd64` wheels will
    contain the appropriate `zbar.dll` and its dependencies.

    ```
    rm -rf build dist MANIFEST.in pyzbar.egg-info
    cp MANIFEST.in.all MANIFEST.in
    ./setup.py bdist_wheel

    cat MANIFEST.in.all MANIFEST.in.win32 > MANIFEST.in
    ./setup.py bdist_wheel --plat-name=win32

    # Remove these dirs to prevent win32 DLLs from being included in win64 build
    rm -rf build pyzbar.egg-info
    cat MANIFEST.in.all MANIFEST.in.win64 > MANIFEST.in
    ./setup.py bdist_wheel --plat-name=win_amd64

    rm -rf build MANIFEST.in pyzbar.egg-info
    ```

2. Release to TestPyPI (see https://packaging.python.org/guides/using-testpypi/)

    ```
    twine upload -r testpypi dist/*
    ```

3. Test the release to TestPyPI

    * Check https://test.pypi.org/project/pyzbar/

    * If you are on Windows

    ```
    c:\python27\python.exe -m venv test1
    test1\scripts\activate
    ```

    * Install dependencies that are not on testpypi.python.org.
    If you are on Python 2.x, these are mandatory

    ```
    pip install enum34 pathlib
    ```

    * Pillow for tests and command-line programs. We can't use the
    `pip install pyzbar[scripts]` form here because `Pillow` will not be
    on testpypi.python.org

    ```
    pip install Pillow
    ```

    * Install the package itself

    ```
    pip install --index https://testpypi.python.org/simple pyzbar
    ```

    * Test

    ```
    read_zbar --help
    read_zbar <path-to-image-with-barcode.png>
    ```

4. If all is well, release to PyPI

    ```
    twine upload dist/*
    ```

    * Check https://pypi.python.org/pypi/pyzbar/

    * Install!

    ```
    pip install pyzbar[scripts]
    ```
