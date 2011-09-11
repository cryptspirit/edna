# -*- coding: utf-8 -*-


import os
import re

import time
import subprocess
import gtk
import edna_gui
import stat
import gettext
import gio
import gobject
import glib
import getpass

gettext.install('edna', unicode=True)
###############################################################################
betc = {'row_fg':3,
        'row_bg':2,
        'flag':1,
        'name':0,}

hotkeys_function_name = {'key_1': _('Copy'),
                        'key_2': _('Remove'),
                        'key_3': _('Properties'),
                        'key_4': _('Rename'),
                        'key_5': _('Make directory'),
                        'key_6': _('Open terminal'),
                        'key_7': _('View'),
                        'key_8': _('Show hide files')}

md = ['Y', 
    'M', 
    'D', 
    'h', 
    'm', 
    's']


type_ico_load = gtk.ICON_LOOKUP_USE_BUILTIN
dic_icon = {}
get_theme = gtk.icon_theme_get_default()
get_theme_gnome = gtk.IconTheme()
get_theme_gnome.set_custom_theme('gnome')

def icon_load_try(name, size):
    '''
    Безопасная процедура загрузки иконок
    '''
    try:
        return get_theme.load_icon(name, size, type_ico_load)
    except glib.GError:
        return get_theme_gnome.load_icon(name, size, type_ico_load)

dic_icon['application/octet-stream'] = icon_load_try('inode-directory', int(rc_dict['style']['icon_size']))
dic_icon['empty'] = icon_load_try('empty', int(rc_dict['style']['icon_size']))

#dic_icon['empty'] = get_theme.load_icon('empty', int(rc_dict['style']['icon_size']), type_ico_load)
########################## edna function (begin) ##############################

        
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
    return f[int(rc_dict['style']['cell_atr_format'])]
    
def get_file_date(path, cm):
    '''
    Получение даты создания или даты последней модификации файла 
    '''
    b = rc_dict['style'][cm]
    ss = ''
    if cm == 'cell_datec_format':
        nm = 8
    else:
        nm = 9
    if len(b) > 0:
        s = time.localtime(os.lstat(path)[nm])
        
        for i in xrange(len(b)):
            if b[i] in md:
                t = str(s[md.index(b[i])])
                if len(t) == 1: t = '0' + t
                ss += t
            else:
                ss += b[i] 
    return ss
    
def get_file_uid(path):
    '''
    Получение индификатора владельца файла
    '''
    return get_username(str(os.lstat(path)[4]))

def get_file_gid(path):
    '''
    Получение индификатора группы владельца файла
    '''
    return get_groupname(str(os.lstat(path)[5]))

def get_username(uidd):
    '''
    Сравнение индефикатора с сушествующим списком имен пользователей
    '''
    try: dickt_nameusers.keys().index(uidd)
    except: return uidd
    else: return dickt_nameusers[uidd][0]

def get_groupname(gidd):
    '''
    Сравнение индефикатора с сушествующим списком имен групп
    '''
    try: dickt_namegroups.keys().index(gidd)
    except: return gidd
    else: return dickt_namegroups[gidd][0]

def get_file_size(path):
    '''
    Получение размера файла в байтах
    '''
    try: t = os.path.getsize(path)
    except: t = 0
    return get_in_format_size(t)

def get_mime(path_i, is_fil):
    '''
    Получение mimetype
    '''
    if is_fil:
        try:
            f = open(path_i)
            r = f.read(200)
            f.close()
        except: temp = 'empty'
        else: temp = str(gio.content_type_guess(None, r, True)[0])
    else:
        temp = 'application/octet-stream'
    if temp:
        pass
    else:
        temp = 'empty'
    return temp
    
def get_ico(s, size_ico=True):
    '''
    Получение иконки по типу и если такой тип уже есть в словаре иконок то используеться
    словарь если нет то в словарь добавляеться новая иконка
    '''
    global dic_icon
    p = gio.content_type_get_icon(s)
    pm = p.get_names()
    if size_ico:
        try:
            dic_icon.keys().index(s)
        except:
            for i in pm:
                try:
                    b = icon_load_try(i, int(rc_dict['style']['icon_size']))
                except:
                    pass
                else:
                    dic_icon[s] = b
                    return dic_icon[s]
            if s != 'None': print s
            return dic_icon['empty']
        else:
            return dic_icon[s]
    else:
        for i in pm:
            print i
            try:
                b = icon_load_try(i, 24)
            except:
                pass
            else:
                return b
        return icon_load_try('empty', 24)

def get_full_size(path, no_list=False):
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
    
def get_full_size_in_thread(path, text_object):
    '''
    Определение размера каталога в фоновом режиме
    '''
    summ = 0
    os_path_join = os.path.join
    os_path_getsize = os.path.getsize
    for root, dirs, files in os.walk(path):
        for name in files:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            else:
                gtk.gdk.threads_enter()
                text_object.set_text(get_in_format_size(summ))
                gtk.gdk.threads_leave()
        for name in dirs:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            else:
                gtk.gdk.threads_enter()
                text_object.set_text(get_in_format_size(summ))
                gtk.gdk.threads_leave()   
    gtk.gdk.threads_enter()
    text_object.set_text(get_in_format_size(summ))
    gtk.gdk.threads_leave()  

def get_launch_apps(path):
    '''
    Определяет по типу какими програмамми можно открывать файл
    '''
    mime_type = get_mime(path, True)
    print mime_type
    apps_list = gio.app_info_get_all_for_type(mime_type)
    ret_list = []
    for i in apps_list:
        name = i.get_name()
        if name: pass
        else: name = ''
        icon = i.get_icon()
        if icon: icon = icon.get_names()[0]
        else: icon = ''
        ret_list.append({'app_name':name, 'desktop':i.get_id(), 'icon':icon})
    return ret_list
    
def get_launch(gioFile):
    '''
    Определяет по типу какой программой открывать файл по умолчанию
    '''
    temp = get_mime(gioFile.get_path(), True)
    if temp != None:
        list_apps = gio.app_info_get_all_for_type(temp)
        return list_apps[0]
    else:
        return None

def get_typ(n):
    '''
    Получение расширения файла если оно есть
    '''
    type = n.rfind('.', 1)
    if type != 0 and type != -1:
        return n[:type], n[type + 1:]
    else:
        return n, ''
    
    
def deleting_files_folders(path, flag):
    '''
    Удаление папок
    '''
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
            return 'Control'
        elif f == 'GDK_MOD1_MASK':
            return 'Alt'
        else:
            return None
        
    
def get_key_info(key_box):
    '''
    Текстовое представление названий нажатых клавиш
    '''
    k = gtk.gdk.keyval_name(key_box.keyval)
    s = get_normal_flag_name(key_box.state)
    if s:
        k = '<%s>%s' % (s, k)
    return k
    
def get_in_format_size(t):
    '''
    Преобразование размера файла в байтах в формат указаный в настройках
    '''
    s = ''
    if rc_dict['style']['cell_size_format'] == '0':
        t = str(t)
        if len(t) > 3:
            l = len(t)
            for i in xrange(l):
                s += t[i]
                if (l - i - 1) % 3 == 0 and i != l - 1:
                    s += ' '
        else:
            s = t
    elif rc_dict['style']['cell_size_format'] == '1':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        else:
            s = str(round(t / 1048576., 2)) + ' MB'
    elif rc_dict['style']['cell_size_format'] == '2':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        elif t >= 1048576 and t <= 1073741824:
            s = str(round(t / 1048576., 2)) + ' MB'
        else:
            s = str(round(t / 1073741824., 2)) + ' GB'
    return s
    
def get_dickt_nameusers():
    '''
    Получение списка имен пользователей по их индефикатору
    '''
    global dickt_nameusers
    f = open('/etc/passwd','r')
    r = f.readlines()
    f.close()
    dickt_nameusers = {}
    for i in r:
        y = i.split(':')
        dickt_nameusers[y[2]] = y
        
def get_dickt_namegroups():
    '''
    Получение списка названий групп по их индефикатору
    '''
    global dickt_namegroups
    f = open('/etc/group','r')
    r = f.readlines()
    f.close()
    dickt_namegroups = {}
    for i in r:
        y = i.split(':')
        dickt_namegroups[y[2]] = y
    
def get_cell(gioFile, is_fil):
    '''
    Получение строки для списка файлов
    '''
    ret = []
    temp = get_mime(gioFile.get_path(), is_fil)
    ret.append(get_ico(temp))
    t = ''
    n = gioFile.get_basename()
    if is_fil:
        n, t = get_typ(gioFile.get_basename())
    for j in Sum_cell:
        if j == 'cell_name':
            if is_fil:
                ret.append(n)
            else:
                ret.append(gioFile.get_basename())
        elif j == 'cell_type':
            ret.append(t)
        elif j == 'cell_size':
            if is_fil:
                ret.append(get_file_size(gioFile.get_path()))
            else:
                ret.append('<DIR>')
        elif j == 'cell_datec':
                ret.append(get_file_date(gioFile.get_path(), 'cell_datec_format'))
        elif j == 'cell_datem':
                ret.append(get_file_date(gioFile.get_path(), 'cell_datem_format'))
        elif j == 'cell_user':
                ret.append(get_file_uid(gioFile.get_path()))
        elif j == 'cell_group':
                ret.append(get_file_gid(gioFile.get_path()))
        elif j == 'cell_atr':
                ret.append(get_file_attr(gioFile.get_path()))
    ret.append(gioFile.get_uri())
    basename = gioFile.get_basename()
    if basename[0] == '.':
        if is_fil:
            basename = '21' + basename[1:]
        else:
            basename = '10' + basename[1:]
    else:
        if is_fil:
            basename = '20' + basename[1:]
        else:
            basename = '11' + basename[1:]
        
    ret.append(basename)
    return ret

def get_user_shell():
    """Get the user's shell defined in /etc/passwd ."""
    data = None
    try:
        # Read out the data in /etc/passwd
        with open('/etc/passwd') as f:
            data = f.readlines()
    except e:
        print "Something unexpected happened!"
        raise e
    for i in data:
        tmp = i.split(":")
        # Check for the entry of the currently logged in user
        if tmp[0] == getpass.getuser(): 
            return i.split(":")[-1:][0].strip('\n')

########################### edna function (end) ###############################        

def main():
    path = '/home/mort'
    p = Get_gioFile_list(path)
    print p
    #OOF = Object_of_Files()
    #print OOF.add_path(path)

if __name__ == '__main__':
    main()

