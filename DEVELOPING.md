## Development

```
mkvirtualenv pyzbar
pip install -U pip
pip install -r requirements.pip

nosetests
python -m pyzbar.scripts.read_zbar pyzbar/tests/code128.png
```

### Testing python versions

Make a virtual env and install `tox`

```
mkvirtualenv tox
pip install tox
```

If you use non-standard locations for your Python builds, make the interpreters available on the `PATH` before running `tox`.

```
PATH=~/local/python-2.7.12/bin:~/local/python-3.4.5/bin:~/local/python-3.5.2/bin:$PATH
tox
```

### Windows

Save the 32-bit and 64-bit `zbar.dll` files, and their dependencies,
to `zbar-32.dll` and `zbar-64.dll` respectively, in the directories `dlls-32`
and dlls-64/ respectively.
The `load_zbar` function in `wrapper.py` looks for the appropriate `DLL`
on `sys.path`. The appropriate `DLL` is packaged up into the wheel build,
then installed to the root of the virtual env. This strategy allows
the same method to be used when `pyzbar` is run from source, as an installed
package and when included in a frozen binary.

## Releasing

1. Install tools.

```
pip install wheel
brew install pandoc
```

2. Build
    Generate the `reStructuredText README.rst` from `README.md` and create
    source and wheel builds. The `win32` and `win_amd64` will contain the
    appropriate `zbar.dll` and its dependencies.

    ```
    pandoc --from=markdown --to=rst README.md -o README.rst
    rm -rf build dist
    ./setup.py bdist_wheel
    ./setup.py bdist_wheel --plat-name=win32
    ./setup.py bdist_wheel --plat-name=win_amd64
    ```

3. Release to pypitest (see https://wiki.python.org/moin/TestPyPI for details)

    ```
    mkvirtualenv pypi
    pip install twine
    twine register -r pypitest dist/pyzbar-0.1.1-py2.py3-none-any.whl
    twine upload -r pypitest dist/*
    ```

4. Test the release to pypitest

    * Check https://testpypi.python.org/pypi/pyzbar/

    * If you are on Windows

    ```
    set PATH=%PATH%;c:\python35\;c:\python35\scripts
    \Python35\Scripts\mkvirtualenv.bat --python=c:\python27\python.exe test1
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

5. If all is well, release to PyPI

    ```
    twine register dist/pyzbar-0.1.1-py2.py3-none-any.whl
    twine upload dist/*
    ```

    * Check https://pypi.python.org/pypi/pyzbar/

    * Install!

    ```
    pip install pyzbar[scripts]
    ```
