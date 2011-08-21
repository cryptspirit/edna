#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#       edna.py
#       
#       Copyright 2011 Podlesnyj Maxim <edna.filebrowser@yandex.ua>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import edna_filemanager
import pygtk
from edna_filemanager import root_window


pygtk.require('2.0')

def main():
    edna_filemanager.main()
    return 0

if __name__ == '__main__':
    main()

