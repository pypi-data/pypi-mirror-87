Prepare the (standard) python environment:
```
######## virtualenvwrapper recommended #######
sudo -H pip3 install  virtualenvwrapper # if not already present
# in bash
echo "echo i... setting virtualenvwrapper.sh" >> ~/.bashrc
echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "source `which virtualenvwrapper.sh`" >> ~/.bashrc
# in zsh
echo "echo i... setting virtualenvwrapper.sh" >> ~/.zshrc
echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.zshrc
echo "source `which virtualenvwrapper.sh`" >> ~/.zshrc
#
# new shell now ... e.g.
bash
mkvirtualenv nuphy 
```

Installation with python 
```
pip install --index-url https://test.pypi.org/simple/ nuphy
```

# Project: Nuphy 
 
## Module: nubase 
 The Nubase2016 evaluation of nuclear and decay properties appeared 
in Chinese Physics C, 2016, vol. 41 030001 

[http://amdc.in2p3.fr/web/nubase_en.html](http://amdc.in2p3.fr/web/nubase_en.html)




## Module: kinematics


## Module: srim

SRIM 2013 can be downloaded from  http://www.srim.org/SRIM/SRIM-2013-Pro.e

or better get a smaller version for multiple running copies http://www.srim.org/SRIM/SRIM-2013-Std.e

Exctract using autoextraction exe

Try to run with ``` wine SRIM.exe```

Upon errors:

IN ```~/.wine/drive_c/windows/system``` exctract MS libraries ```tar -xvzf libs2013.tgz```


