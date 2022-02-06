#!/bin/bash
PYTHON_SITES=$(python3 -c 'import site; print(site.getsitepackages())') 
python3 -m PyInstaller  -F --paths="$PYTHON_SITES" --onefile tagger.py
mv dist/tagger dist/Linux64_2.6.32/