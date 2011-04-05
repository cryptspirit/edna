#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       edna_function.py
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
import os
import re
import rc_modul
import time
import subprocess
import gtk
#import gio
import mimetypes
import gui_class_main
import threading
import stat


betc = {'row_fg':3,
        'row_bg':2,
        'flag':1,
        'name':0,}

type_ico_load = gtk.ICON_LOOKUP_USE_BUILTIN

dic_icon = {}

get_theme = gtk.icon_theme_get_default()

dic_icon['application-x-directory'] = get_theme.load_icon('gtk-directory', int(rc_modul.rc_dict['style']['icon_size']), type_ico_load)
dic_icon['empty'] = get_theme.load_icon('empty', int(rc_modul.rc_dict['style']['icon_size']), type_ico_load)

#def get_key_info(key_box):
#    st = re.search(r'keyval=\S+>', key_box.string).group()[7:-1]
#    k = key_box.keyval
#    return st, k

def buf_def(c):
    global answer
    answer = c
    
def tread_window(path):
    gtk.gdk.threads_enter()
    h = gui_class_main.miss_window(path)
    h.butt_miss.connect('clicked', lambda *y: buf_def(1))
    h.butt_again.connect('clicked', lambda *y: buf_def(2))
    h.butt_miss_all.connect('clicked', lambda *y: buf_def(3))
    h.butt_cancel.connect('clicked', lambda *y: buf_def(4))
    h.show_all()
    gtk.gdk.threads_leave()
    
def save_open(path, flg, miss):
    global answer
    answer = 0
    try: f = open(path, flg)
    except:
        f = None
        if miss:
            pass
        else:
            t = threading.Timer(1, lambda *y: tread_window(path))
            t.start()
            t.join()
            print answer
    return f, answer

def deleting_files_folders(path, flag):
    if os.path.islink(path):
        os.remove(path)
    else:
        if flag:
            #try:
            os.remove(path)
            #except:
            #    print 'галяк', path
        else:
            #try:
            os.rmdir(path)
            #except:
            #    print 'галяк', path
            
def get_normal_flag_name(flag):
    '''
    Преобразование Флагов клавиш в человеческий вид
    '''
    try:
        f = flag.value_names[0]
    except:
        return None
    else:
        if f == 'GDK_SHIFT_MASK':
            return 'Shift'
        elif f == 'GDK_CONTROL_MASK':
            return 'Ctrl'
        elif f == 'GDK_MOD1_MASK':
            return 'Alt'
        else:
            return None
        
        
def get_key_info(key_box):
    k = gtk.gdk.keyval_name(key_box.keyval)
    s = get_normal_flag_name(key_box.state)
    if s:
        k = s + ' ' + k
    return k

def get_full_size(path, list=False):
    '''
    оттавизм на удаление
    '''
    #np = os.path.dirname(path)
    #return full_size(np, path, 0, [])
    return full_size_new(path, list)

def full_size_new(path, no_list):
    '''
    Определение размера каталога
    '''
    summ = 0
    os_path_join = os.path.join
    os_path_getsize = os.path.getsize
    if no_list:
        list = []
        list_append = list.append
        list_dirs = []
        list_dirs_append = list_dirs.append
    for root, dirs, files in os.walk(path):
        for name in files:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            if no_list: list_append([p, True])
        for name in dirs:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            if no_list: list_dirs_append([p, False])
    if no_list:
        return summ, list_dirs + list
    else:                        
        return summ                     

def get_launch(path):
    temp = mimetypes.guess_type(path)[0]
    print temp
    if temp != None:
        ret = subprocess.Popen(['xdg-mime', 'query', 'default', temp],
                                        stdout=subprocess.PIPE).communicate()[0]
        if len(ret[:-1]):
            f = open('/usr/share/applications/' + ret[:-1], 'r')
            red = re.search(r'Exec=.*', f.read()).group()[5:]
            f.close()
            red = re.search(r'\S+', red).group()
            if red:
                return red
            else:
                return None

def get_file_size(path):
    '''
    Получение размера файла в байтах
    '''
    try: t = os.path.getsize(path)
    except: t = 0
    return get_in_format_size(t)
    
def get_in_format_size(t):
    '''
    Преобразование размера файла в байтах в формат указаный в настройках
    '''
    s = ''
    if rc_modul.rc_dict['style']['cell_size_format'] == '0':
        t = str(t)
        if len(t) > 3:
            l = len(t)
            for i in xrange(l):
                s += t[i]
                if (l - i - 1) % 3 == 0 and i != l - 1:
                    s += ' '
        else:
            s = t

    elif rc_modul.rc_dict['style']['cell_size_format'] == '1':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        else:
            s = str(round(t / 1048576., 2)) + ' MB'
            
    elif rc_modul.rc_dict['style']['cell_size_format'] == '2':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        elif t >= 1048576 and t <= 1073741824:
            s = str(round(t / 1048576., 2)) + ' MB'
        else:
            s = str(round(t / 1073741824., 2)) + ' GB'
    return s

def get_file_attr(file):
    '''
    Получение атрибутов файла
    '''
    s = ''
    s1 = ''
    kl = {'R':4, 'W':2, 'X':1}
    jb = os.lstat(file)[stat.ST_MODE]
    mode = stat.S_IMODE(jb)
    if stat.S_ISDIR(jb):
        s += 'd'
    else:
        s += '-'
    for i in 'USR', 'GRP', 'OTH':
        u = 0
        for j in 'R', 'W', 'X':
            if mode & getattr(stat, 'S_I%s%s' % (j, i)):
                s += j.lower()
                u += kl[j]
            else:
                s += '-'
        s1 += str(u)
    f = [s, s1]
    return f[int(rc_modul.rc_dict['style']['cell_atr_format'])]

def get_file_date(path, cm):
    b = rc_modul.rc_dict['style'][cm]
    ss = ''
    if cm == 'cell_datec_format':
        nm = 8
    else:
        nm = 9
    if len(b) > 0:
        s = time.localtime(os.lstat(path)[nm])
        
        for i in xrange(len(b)):
            if b[i] in rc_modul.md:
                t = str(s[rc_modul.md.index(b[i])])
                if len(t) == 1: t = '0' + t
                ss += t
            else:
                ss += b[i] 
    return ss
    
def get_file_uid(path):
    return get_username(str(os.lstat(path)[4]))
    
def get_file_gid(path):
    return get_groupname(str(os.lstat(path)[5]))

def get_username(uidd):
    try: dickt_nameusers.keys().index(uidd)
    except: return uidd
    else: return dickt_nameusers[uidd][0]
    
def get_groupname(gidd):
    try: dickt_namegroups.keys().index(gidd)
    except: return gidd
    else: return dickt_namegroups[gidd][0]
    
def get_dickt_nameusers():
    global dickt_nameusers
    f = open('/etc/passwd','r')
    r = f.readlines()
    f.close()
    dickt_nameusers = {}
    for i in r:
        y = i.split(':')
        dickt_nameusers[y[2]] = y
        
def get_dickt_namegroups():
    global dickt_namegroups
    f = open('/etc/group','r')
    r = f.readlines()
    f.close()
    dickt_namegroups = {}
    for i in r:
        y = i.split(':')
        dickt_namegroups[y[2]] = y
        
        
def get_typ(n):
    type = n.rfind('.', 1)
    if type != 0 and type != -1:
        return n[:type], n[type + 1:]
    else:
        return n, ''
            
def mime_name_ico(s):
    return s.replace('/', '-')

def get_mime(path_i, is_fil):
    '''
    Получение mimetype
    '''
    if is_fil:
        temp = mimetypes.guess_type(path_i)[0]
    else:
        temp = 'application-x-directory'
    if temp:
        pass
    else:
        temp = 'empty'
    return temp

def get_cell(path, i, is_fil, cellse):
    '''
    Получение строки для списка файлов
    '''
    path_i = path + i #В будующем заменить на функцию слияния из os.path
    ret = []
    temp = get_mime(path_i, is_fil)
    t = ''
    n = i
    if is_fil:
        n, t = get_typ(i)
    for j in cellse:
        if j == 'cell_name':
            if is_fil:
                ret.append(n)
            else:
                ret.append(i)
        elif j == 'cell_type':
            ret.append(t)
        elif j == 'cell_size':
            if is_fil:
                ret.append(get_file_size(path_i))
            else:
                ret.append('<DIR>')
        elif j == 'cell_datec':
                ret.append(get_file_date(path_i, 'cell_datec_format'))
        elif j == 'cell_datem':
                ret.append(get_file_date(path_i, 'cell_datem_format'))
        elif j == 'cell_user':
                ret.append(get_file_uid(path_i))
        elif j == 'cell_group':
                ret.append(get_file_gid(path_i))
        elif j == 'cell_atr':
                ret.append(get_file_attr(path_i))
    ret.append(path_i)
    ret.append(get_ico(mime_name_ico(temp)))
    return ret
    
def get_ico(s, size_ico=True):
    '''
    Получение иконки по типу и если такой тип уже есть в словаре иконок то используеться
    словарь если нет то в словарь добавляеться новая иконка
    '''
    global dic_icon
    if size_ico:
        try:
            dic_icon.keys().index(s)
        except:
            try:
                b = get_theme.load_icon(s, int(rc_modul.rc_dict['style']['icon_size']), type_ico_load)
            except:
                return dic_icon['empty']
            else:
                dic_icon[s] = b
                return dic_icon[s]
        else:
            return dic_icon[s]
    else:
        try:
            b = get_theme.load_icon(s, 30, type_ico_load)
        except:
            return get_theme.load_icon('empty', 30, type_ico_load)
        else:
            return b
       
def get_list_path(path, pattern_s, select_list):
    '''
    Получение списка файлов с описаными столбцами
    '''
    cellse = rc_modul.Sum_cell
    
    try: cellse.index('cell_user')
    except: pass
    else: get_dickt_nameusers()
    
    try: cellse.index('cell_group')
    except: pass
    else: get_dickt_namegroups()
    
    if path[len(path) -1] != '/': path += '/'
    list = os.listdir(path)
    return_dir = []
    return_fil = []
    if path != '/':
        ttt = []
        
        for j in cellse:
            if j == 'cell_name':
                ttt.append('..')
            elif j == 'cell_size':
                ttt.append('<DIR>')
            else:
                ttt.append('')
        ttt.append('..')
        ttt.append(dic_icon['application-x-directory'])
    path_probe = os.path.isdir
    return_dir_append = return_dir.append
    return_fil_append = return_fil.append
    for i in list:
        if path_probe(path + i):
            return_dir_append(get_cell(path, i, False, cellse))
        else:
            return_fil_append(get_cell(path, i, True, cellse))
    return_dir.sort()
    return_fil.sort()
    m = return_dir + return_fil
    if path != '/':
        m.insert(0, ttt)
    op = 0
    fg = {}
    for i in xrange(len(m)):
        fg[m[i][len(cellse)]] = i
        if select_list:
            try: select_list.index(m[i][len(cellse)])
            except:
                if i % 2 != 0:
                    color_fg = rc_modul.rc_dict['style']['odd_row_fg']
                    color_bg = rc_modul.rc_dict['style']['odd_row_bg']
                else:
                    color_fg = rc_modul.rc_dict['style']['even_row_fg']
                    color_bg = rc_modul.rc_dict['style']['even_row_bg']
                fgl = 'False'
            else:
                fgl = 'True'
                color_fg = rc_modul.rc_dict['style']['sel_row_fg']
                color_bg = rc_modul.rc_dict['style']['sel_row_bg']
        else:
            if i % 2 != 0:
                color_fg = rc_modul.rc_dict['style']['odd_row_fg']
                color_bg = rc_modul.rc_dict['style']['odd_row_bg']
            else:
                color_fg = rc_modul.rc_dict['style']['even_row_fg']
                color_bg = rc_modul.rc_dict['style']['even_row_bg']
            fgl = 'False'
        m[i].append(color_fg)
        m[i].append(color_bg)
        m[i].append(fgl)
    
        if m[i][len(cellse)].strip('\t\n') == pattern_s.strip('\t\n'):
            op = i
            #print 'i', i
    
    return m, op, fg
        
        
def main():
    k = get_list_path('/home/mort', rc_modul.read_rc())
    for i in k:
        print i
    return 0

if __name__ == '__main__':
    main()

