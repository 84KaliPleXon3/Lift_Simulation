#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import random
import string
import time
import locale

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()
class lift:
    def __init__(self,height):
        self.height = height
        self.now = 0    #当前楼层
        self.direction = 0   #运动方向 上为1 下为-1 停留为0
        self.button = [set(),set()]    #按键状态字典 记录每一层楼上下按钮是否被按下
        self.target ={k:[] for k in range(height)}     #记录电梯中乘客的目的楼层
        self.waiting_up = {k:[] for k in range(height)}     #每层楼等候区 []中为等候人员目标楼层
        self.waiting_down = {k:[] for k in range(height)}     #每层楼等候区 []中为等候人员目标楼层
        self.number = 0
        self.info = '(w)乘坐 (q)退出 (任意键)运行\n'
        self.pad = lambda s: s + ( 10- len(s)) * ' '

    def getin(self):
        if self.direction == 1:
            if self.now in self.button[1]:

                self.button[1].remove(self.now)     #移除上按钮
                for target in self.waiting_up[self.now]:
                    people = random.choice(string.ascii_uppercase)
                    self.target[target].append(people)   #加入目标字典 
                    self.info += '%s 走进电梯 按下目标楼层 %d 层' % (people, target) +'\n'
                    self.number += 1
                self.waiting_up[self.now] = []           #清空等待上楼的等待人
        else:
            if self.now in self.button[0]:

                self.button[0].remove(self.now)     #移除下按钮
                for target in self.waiting_down[self.now]:
                    people = random.choice(string.ascii_uppercase)
                    self.target[target].append(people)   #加入目标字典 
                    self.info += '%s 走进电梯 按下目标楼层 %d 层' % (people, target) +'\n'
                    self.number += 1
                self.waiting_down[self.now] = []           #清空等待上楼的等待人

    def out(self):
        passenger = self.target[self.now]
        if passenger: 
            for people in passenger:
                self.info += '%s 到达目标楼层 %d 层 走出电梯' % (people,self.now) + '\n'
                self.number -= 1
            self.target[self.now] = []

    def up_choice(self):
        for floor in range(self.now,self.height):
            if self.target[floor] or floor in self.button[0] or floor in self.button[1]:       #如果有乘客的要上去 或者上面有人按下上/下按钮
                return 1    #返回继续上升

        for floor in range(self.now):
            if self.target[floor] or floor in self.button[0] or floor in self.button[1]:       #如果有乘客的要上去 或者上面有人按下上/下按钮
                return -1    #返回下降
        return 0    #电梯停留不动

    def down_choice(self):
        for floor in range(self.now + 1):
            if self.target[floor] or floor in self.button[0] or floor in self.button[1]:       #如果有乘客的要下去 或者下面有人按下上/下按钮
                return -1    #返回继续下降

        for floor in range(self.now + 1, self.height):
            if self.target[floor] or floor in self.button[0] or floor in self.button[1]:       #如果有乘客的要上去 或者上面有人按下上/下按钮
                return 1    #返回上升
        return 0    #电梯停留不动


    def addpassenger(self, since, go):
        if since == go or since not in range(self.height) or go not in range(self.height):
            self.info += 'orz 你可能想跳楼\n'
            pass
        else:
            if since < go:
                self.button[1].add(since)            #上升按钮被按下
                self.waiting_up[since].append(go)    #加入此层楼上升等候区

            else:
                self.button[0].add(since)            #下降按钮被按下
                self.waiting_down[since].append(go)    #加入此层楼下降等候区

    def run(self):
        self.now += self.direction
        if self.direction == 1:
            self.info += '电梯上升中\n'
            self.out()
            self.direction = self.up_choice()        #方向抉择
            self.getin()
            pass
        if self.direction == -1:
            self.info += '电梯下降中\n'
            self.out()
            self.direction = self.down_choice()    #方向抉择
            self.getin()
            pass
        if self.direction == 0:
            self.info += '电梯停留在 %d 层\n' % self.now
            self.direction = self.up_choice()   #停留状态调用上升抉择
            self.getin()
            pass

    def gui(self,stdscr):
        curses.use_default_colors()
        while 1:
            self.run()
            self.draw(stdscr)
            #stdscr.nodelay(6)
            char = stdscr.getch()
            if char == ord('q'):
                break
            if char == ord('w'):
                curses.echo()
                stdscr.addstr('请输入起始楼层\n')
                since = stdscr.getstr()
                stdscr.addstr('请输入目标楼层\n')
                go = stdscr.getstr()
                try:
                    self.info += '有人乘坐电梯 %s -> %s\n'%(since , go)
                    self.addpassenger(int(since),int(go))
                except:
                    self.info += '小朋友不要乱按电梯\n'
                curses.noecho()      

    def draw(self,screen):
        def cast(string):
            screen.addstr(string + '\n')
        def draw_hor_separator():
            line = '+----------+'+str(self.now)
            cast(line)
        def draw_row(row):
            floor = self.height - row-1
            if row == self.height - self.now-1:
                cast('|  -  -  -  |' +'\n|  '+ self.pad('*' * self.number) + '*' * (len(self.waiting_down[floor]) + len(self.waiting_up[floor])) + '\n|  -  -  -  |')
            else:
                cast('|           |' +'\n|           |' + '*' * (len(self.waiting_down[floor]) + len(self.waiting_up[floor])) + '\n|           |')

        screen.clear()
        for row in range(self.height):
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        cast(self.info)
        self.info = '(w)乘坐 (q)退出 (任意键)运行\n'

    def main(self):
        curses.wrapper(self.gui)

new_lift = lift(10)

new_lift.addpassenger(3,5)
new_lift.addpassenger(3,5)
new_lift.addpassenger(3,8)
new_lift.addpassenger(6,0)
new_lift.addpassenger(4,1)
new_lift.addpassenger(4,6)
new_lift.addpassenger(5,8)
new_lift.main()


