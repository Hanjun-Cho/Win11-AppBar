## Setup 
****
> [!Important]
> Due to the code using user32.dll and shell32.dll, this project can only run if the code base is in a windows directory (editing the code with wsl is fine, but you'll need to use the windows python executable to run the code instead of the linux version)

### Windows
****
```
python -m venv venv
venv\Scripts\activate.bat
cd src
pip install -r requirements.txt
python main.py
```

### WSL
****
```
alias winpy="/mnt/c/Users/<username>/AppData/Local/Programs/Python/<pythonVersion>/python.exe"
winpy -m venv venv
./venv/Scripts/activate
cd src
./venv/Scripts/pip.exe install -r requirements.txt
winpy main.py
```
It's worth storing the 'winpy' alias inside ~/.bashrc so the alias stays in a new WSL instance later



