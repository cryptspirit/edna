#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#       hotkeys.py
#       
#       Copyright 2011 CryptSpirit <cryptspirit@gmail.com>
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
import re


def get_key_info(key_box):
    st = re.search(r'keyval=\S+>', key_box.string).group()[7:-1]
    k = key_box.keyval
    return st, k
    
    
def main():
    
    return 0

if __name__ == '__main__':
    main()

