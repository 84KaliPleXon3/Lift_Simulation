#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import locale
import curses
from lift import *

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

class manage:
    def __init__(self,lift_num,height):
        self.lifts=[lift(height) for i in range(lift_num)]    #初始化电梯列表
        self.padrow = lambda s: s + (26- len(s)) * ' '
        self.info = '(w)乘坐 (q)退出 (任意键)运行\n'
        self.height = height

    def gui(self,stdscr):
        curses.use_default_colors()
        while 1:
            self.randompeople()
            for lift in self.lifts:
                lift.run()
                self.info += '----- 电梯分机信息 -----:\n'+lift.info
                lift.info = ''
            self.draw(stdscr)
            #stdscr.nodelay(6)
            char = stdscr.getch()
            if char == ord('q'):
                break
            if char == ord('w'):
                self.ride(stdscr)

    def addchoose(self,since,go):
        direction = 1 if go > since else -1    #方向
        prioritys = []
        for lift in self.lifts:
            prioritys.append(lift.priority(since,go,direction))
        self.lifts[prioritys.index(min(prioritys))].addpassenger(int(since),int(go)) #分配优先值最小的电梯给乘客

    def randompeople(self):
        for i in range(random.randint(0,3)):
            self.addchoose(random.randint(0,self.height-1),random.randint(0,self.height-1))
            
    def ride(self,stdscr):
        curses.echo()
        try:
            stdscr.addstr('请输入起始楼层\n')
            since = int(stdscr.getstr())
            stdscr.addstr('请输入目标楼层\n')
            go = int(stdscr.getstr())
            self.info += '有人乘坐电梯 %d -> %d\n'%(since , go)
            self.addchoose(since,go)
        except:
            self.info += '小朋友不要乱按电梯\n'
        curses.noecho()

    def draw(self,screen):
        def cast(string):
            screen.addstr(string + '\n')
        def draw_hor_separator():
            line = '+-----------+             ' * len(self.lifts)
            cast(line)
        def draw_row(row):
            rowline = ''
            for lift in self.lifts:
                rowline += self.padrow(lift.draw(row))
            cast(rowline)

        screen.clear()
        for row in range(self.height):
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        cast(self.info)
        self.info = '(w)乘坐 (q)退出 (任意键)运行\n'

    def main(self):
        curses.wrapper(self.gui)


manages = manage(4,15)
manages.main()
