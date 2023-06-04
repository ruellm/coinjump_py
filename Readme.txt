pip install pygame
pip install opencv-python
pip install mediapipe

dont forget to create venv
python3 -m venv ./venv

at initial run do this:
install all 3 dependencies and execute the command bellow to generate exe
pyinstaller --onefile --hidden-import mediapipe --hidden-import opencv-python --hidden-import pygame --add-data "images/*.png;images/" main.py

Edit the spec like this:
https://stackoverflow.com/questions/67887088/issues-compiling-mediapipe-with-pyinstaller-on-macos

finally build the exe
pyinstaller main.spec