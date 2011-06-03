# -*- coding: utf-8 -*-
#
#       observer.py
#       
#       Copyright 2011 Sevka <sevka@ukr.net>
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
'''
Интерфейсы для реализации паттерна Наблюдатель (Observer)
'''
class Event(object):
    '''
    Интерфейс события наблюдаемого объекта
    '''
    pass

class Observable(object):
    '''
    Интерфейс наблюдаемого объекта
    '''
    def __init__(self):
        '''
        Конструктор
        '''
        self.callbacks = []
        
    def subscribe(self, callback):
        '''
        Подключить наблюдателя
        :param callback: Метод-коллбек наблюдателя
        :type callback: function
        '''
        self.callbacks.append(callback)
        
    def notify_observers(self, event):
        '''
        Уведомить наблюдателей о событии
        '''
        #event.source = self
        for callback in self.callbacks:
            callback(event)
