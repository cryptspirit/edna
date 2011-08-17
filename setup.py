#!/usr/bin/env python
# -*- coding: utf-8 -*-




# Необходимо поставить пакеты для сборки deb файла install python-distutils-extra и python-stdeb
# сборка пакета python setup.py --command-packages=stdeb.command bdist_deb
# установка в псевдокорень для проверки python setup.py install --prefix=/tmp
#  /usr/lib/python2.7/Tools/i18n/msgfmt.py


from distutils.core import setup
#from DistUtilsExtra.command import *
import os, sys
import glob

def build_mo():
    mo_files = []
    os.system('rm -rf locale')
    for i in glob.glob('po/*.po'):
        local_name = i.split('/')[1][:-3]
        try: os.makedirs('locale/%s' % local_name)
        except IOError: pass
        os.system('msgfmt -o locale/%s/edna.mo %s' % (local_name, i))
        mo_files.append(('usr/share/locale/%s/LC_MESSAGES' % local_name, ['locale/%s/edna.mo' % local_name]))
        
    return mo_files


def main():
    
    print 
    
    setup(name='edna',
    version='0.0.1',
    description='a two panel file manager',
    author='Maxim Podlesnyj',
    author_email='cryptspirit@gmail.com',
    url='https://github.com/cryptspirit/edna',
    license='GPL v2',
    packages=['edna', 'edna/search'],
    package_dir={'edna': 'edna', 'search': 'edna/search'},
    data_files=[
                ('usr/share/applications', ['edna.desktop']),
                ('usr/share/pixmaps', glob.glob('icon/*'))
                ] + build_mo(),
    scripts=['edna.py'],
    #classifiers=['Development Status :: 5 - Production/Stable', 'Intended Audience :: End Users/Desktop', 'License :: OSI Approved :: GNU General Public License (GPL)', 'Operating System :: POSIX :: Linux'],
    long_description='notsdfsdfsdfad')
    
if __name__ == '__main__':
    main()  
