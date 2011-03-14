#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       rc_modul.py
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
import os

filerc = '.ednarc'

md = ['Y', 
'M', 
'D', 
'h', 
'm', 
's']

mc = ['Cell_Name', 
'Cell_Type', 
'Cell_Size', 
'Cell_DateC', 
'Cell_DateM', 
'Cell_User', 
'Cell_Group', 
'Cell_Atr']

defaultrc = {'Cell_Name':'1',  
            'Cell_Type':'1', 
            'Cell_Size':'1', 
            'Cell_DateC':'0', 
            'Cell_DateM':'0', 
            'Cell_User':'0', 
            'Cell_Group':'0', 
            'Cell_Atr':'0',
            'Cell_Sort':'01234567',
            'Panel_History0':'/',
            'Panel_History1':'/',
            'Cell_Name_Expand':'1',  
            'Cell_Type_Expand':'0', 
            'Cell_Size_Expand':'0', 
            'Cell_DateC_Expand':'0', 
            'Cell_DateM_Expand':'0', 
            'Cell_User_Expand':'0', 
            'Cell_Group_Expand':'0', 
            'Cell_Atr_Expand':'0',
            'Cell_Name_Alignment_H':'0.0',  
            'Cell_Type_Alignment_H':'0.0', 
            'Cell_Size_Alignment_H':'1.0', 
            'Cell_DateC_Alignment_H':'0.0', 
            'Cell_DateM_Alignment_H':'0.0', 
            'Cell_User_Alignment_H':'0.0', 
            'Cell_Group_Alignment_H':'1.0', 
            'Cell_Atr_Alignment_H':'1.0',
            'Cell_Name_Alignment_V':'0.5',  
            'Cell_Type_Alignment_V':'0.5', 
            'Cell_Size_Alignment_V':'0.5', 
            'Cell_DateC_Alignment_V':'0.5', 
            'Cell_DateM_Alignment_V':'0.5', 
            'Cell_User_Alignment_V':'0.5', 
            'Cell_Group_Alignment_V':'0.5', 
            'Cell_Atr_Alignment_V':'0.5',
            'Cell_Name_Size':'100',  
            'Cell_Type_Size':'70', 
            'Cell_Size_Size':'70', 
            'Cell_DateC_Size':'70', 
            'Cell_DateM_Size':'70', 
            'Cell_User_Size':'70', 
            'Cell_Group_Size':'70', 
            'Cell_Atr_Size':'70',
            'Cell_DateC_Format':'M.D.Y',
            'Cell_DateM_Format':'M.D.Y',
            'Cell_Size_Format':'0',
            'Cell_Date_Type':'0',
            'Cell_Atr_Format':'0',
            'Date_Format':'0',
            'Even_Row_FG':'#DFDDF0',
            'Even_Row_BG':'#454a56',
            'Odd_Row_FG':'#DFDDF0',
            'Odd_Row_BG':'#41517a',
            'Sel_Row_FG':'#474747',
            'Sel_Row_BG':'#599839',
            'Icon_Size':'16',
            'Font_Cell_Text':'Sans 10',
            'Hot_Key_1':'0',
            'Hot_Key_2':'0',
            'Hot_Key_3':'0',
            'Hot_Key_4':'0',
            'Hot_Key_5':'0',
            'Hot_Key_6':'0',
            'Hot_Key_7':'0'}


    
def Sum_cell(rc_dict):
    t = rc_dict['Cell_Sort']
    p = []
    for i in xrange(len(t)):
        if rc_dict[mc[int(t[i])]] == '1':
            p.append(mc[int(t[i])])
    return p

def read_rc():
    '''
    Функция чтения файла настроек
    '''
    if os.path.isfile(filerc):
        f = open(filerc, 'r')
        s = f.read()
        f.close()
        return correction_rc(parsa(s))
    else:
        return defaultrc
                
def save_rc(dict):
    '''
    Функция сохранения словаря настроек
    '''
    f = open(filerc, 'w')
    for k in dict.keys():
        f.write(k + '=' + dict[k] + '\n')
    f.close()

def parsa(s):
    '''
    Функция заполнения словаря настроек и локализации
    '''
    m = re.findall(r'\S+=.*', s)
    res_dict = {}
    for i in m:
        temp = re.search(r'\S+=', i).group()[:-1]
        temp1 = i[len(temp) + 1:]
        res_dict[temp] = temp1
    return res_dict

def locale_rc(path):
    '''
    Функция чтения файла локализации
    '''
    f = open(path, 'r')
    s = f.read()
    f.close()
    return parsa(s)

def correction_rc(rc_dict):
    '''
    Функция внисения недостающих настроек в файл настроек
    '''
    f = False
    for i in defaultrc.keys():
        try:
            rc_dict[i]
        except:
            rc_dict[i] = defaultrc[i]
            f = True
    if f:        
        save_rc(rc_dict)
    return rc_dict
    
locale = locale_rc('.local')
    
def main():
    read_rc()
    return 0

if __name__ == '__main__':
    main()

