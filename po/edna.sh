#!/bin/bash
xgettext Edna.py gui_class_main.py gui_class_rc.py -o edna.pot
#msgmerge edna-ru.po edna.pot -o edna-ru.po
msginit -l ru -i edna.pot -o edna-ru.po
