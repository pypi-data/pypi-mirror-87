set PATH=C:\Program Files\Python37;C:\Program Files\Python37\Scripts;C:\Program Files\CMake\bin;%PATH%
virtualenv -p "C:\Program Files\Python37\python.exe" .
call .\Scripts\activate
python setup.py bdist_wheel --dist-dir dist3
