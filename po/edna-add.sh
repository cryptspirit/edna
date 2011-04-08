#!/bin/bash
cd ..
echo $PWD
xgettext Edna.py gui_class_main.py edna_function.py -o po/edna.pot
msgmerge po/edna-ru.po po/edna.pot -o po/edna-ru.po
