# Winbar
An extensible module-based utility bar for Windows written in **Python** and **PySide6**

<img width="1919" height="59" alt="image" src="https://github.com/user-attachments/assets/38dad815-888d-43ce-9e7c-79e424affcc7" />

## Demo
https://github.com/user-attachments/assets/e3ca87f3-0f50-4354-bf26-357ca409e112

## Roadmap
- [ ] Default Configuration Components
    - [x] Clock
    - [x] Virtual Desktop Status / Changer
    - [ ] Application Quickstart
    - [ ] System Settings Control
        - [ ] Battery Display
        - [ ] Audio Control
        - [ ] Brightness Control
        - [ ] Wifi Select
        - [X] Language Control (switch IME states is not possible...)
- [ ] Custom QT Widgets
    - [X] Clickable Text Label
    - [X] Clickable Image Label
    - [x] Color Animated Clickable Label
    - [ ] Position Animated Clickable Label
- [ ] Customizability
    - [X] Global Font Default Size
    - [ ] Colors in config files for global color settings
- [ ] Fixes
    - [ ] Backchecking Existing Config File for Updated Setting Fields
- [ ] Major Refactors
    - [ ] Allow for multi-file dependencies for components

## Setup 
> [!Important]
> Due to the code using ``user32.dll`` and ``shell32.dll``, this project can only run if the code base is in a windows directory (editing the code with wsl is fine, but you'll need to use the windows python executable to run the code instead of the linux version)


### Windows
```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```


### WSL
```
alias winpy="/mnt/c/Users/<username>/AppData/Local/Programs/Python/<pythonVersion>/python.exe"
winpy -m venv venv
./venv/Scripts/activate
./venv/Scripts/pip.exe install -r requirements.txt
winpy main.py
```
It's worth storing the 'winpy' alias inside ``~/.bashrc`` so the alias stays in a new WSL instance later

## Customization
All customization configs / modules are stored within the ``C:\Users\<username>\Documents\Winbar folder.``

Below is the default configuration folder structure:
```
Winbar/
├── layout.json
├── components.json
├── components/
│   ├── clock.py
└── └── desktop_status.py
```
When creating a new module that you want to add into the Winbar, create a python file in ``components/``

Each component should be self-contained, no helper python files which are imported from the config folder - if you need a specific custom type of widget, adding that into ``<project files>/customQt`` and importing it with ``from customQt`` from the component module is possible

Each python file within the components folder **must** have the following method defined:
```
def get_widget(layout_config) -> QWidget:
```
How and what ``QWidget`` is returned has no requirement, just as long as ``get_widget(layout_config)`` can return a QWidget which can be added to a ``QHBoxLayout()``

### Layout.json
``Layout.json`` is used to control the size dimension and margin of the App Bar - along with global default font.
```
{
  "winbar_component_height": 40,
  "winbar_margins": {
    "left": 5,
    "right": 5,
    "top": 5,
    "bottom": 5
  },
  "global_font": "Roboto"
}
```
``Layout.json`` is automatically passed through as a dictionary when calling ``get_widget(layout_config)``. 

The following ``StrEnum`` exists in ``configs.layout_config`` to call fields within the ``layout_config`` dictionary
```
class LayoutFields(StrEnum):
    WINBAR_COMPONENT_HEIGHT = "winbar_component_height"
    WINBAR_MARGINS = "winbar_margins"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    GLOBAL_FONT = "global_font"
```

### Components.json
``Components.json`` holds information on how the components should be rendered and how they should be aligned
```
{
  "LEFT": [
    "desktop_status"
  ],
  "CENTER": [
    "clock"
  ],
  "RIGHT": [

  ]
}
```
Adding the name of the python file in the ``component/`` folder will tell the program where and the order in which components should render 
