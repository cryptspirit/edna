#!/usr/bin/python
# -*- coding: utf-8 -*-

# Необходимо поставить пакеты для сборки deb файла install python-distutils-extra и python-stdeb
# сборка пакета python setup.py --command-packages=stdeb.command bdist_deb
# установка в псевдокорень для проверки python setup.py install --prefix=/tmp


from distutils.core import setup
from DistUtilsExtra.command import *
import os, sys
import glob

if sys.prefix == '/usr': share_folder = 'share/'
else: share_folder = 'usr/share/'

def build_mo():
    mo_files = []
    os.system('rm -rf locale')
    for i in glob.glob('po/*.po'):
        local_name = i.split('/')[1][:-3]
        try: os.makedirs('locale/%s' % local_name)
        except IOError: pass
        os.system('msgfmt -o locale/%s/edna.mo %s' % (local_name, i))
        mo_files.append((share_folder + 'locale/%s/LC_MESSAGES' % local_name, ['locale/%s/edna.mo' % local_name]))
    return mo_files

def main():
    setup(name='edna',
    version='0.0.1a',
    description='two panel file manager',
    author='Maxim Podlesnyj',
    author_email='cryptspirit@gmail.com',
    url='https://github.com/cryptspirit/edna',
    license='GPL v2',
    packages=['edna_filemanager', 'edna_filemanager/search'],
    package_dir={'edna_filemanager': 'edna_filemanager', 'search': 'edna_filemanager/search'},
    data_files=[
                (share_folder + 'applications', ['edna.desktop']),
                (share_folder + 'pixmaps', glob.glob('icon/*'))
                ] + build_mo(),
    scripts=['edna'],
    classifiers=['Development Status :: 1 - Planning', 'Intended Audience :: End Users/Desktop', 'License :: OSI Approved :: GNU General Public License (GPL)', 'Operating System :: POSIX :: Linux'],
    long_description='This two-panel file manager written in Python programming language version 2.6 and above, using the framework Gtk 2 for unix-like operating systems.')
    
if __name__ == '__main__':
    main()  
