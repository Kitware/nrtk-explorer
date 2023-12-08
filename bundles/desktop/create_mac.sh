#!/bin/bash

python -m PyInstaller \
    --clean --noconfirm \
    --windowed \
    --hidden-import pkgutil \
    --collect-data trame_vuetify \
    --collect-data trame_vtk \
    --collect-data trame_client \
    --collect-data nrtk_explorer \
    ./run.py
