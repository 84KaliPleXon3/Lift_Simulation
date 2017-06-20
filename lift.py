#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import random
import string
import time
class lift:
    def __init__(self,height):
        self.height = height
        self.now = 0    #当前楼层
        self.direction = 0   #运动方向 上为1 下为-1 停留为0
        self.button = [set(),set()]    #按键状态字典 记录每一层楼上下按钮是否被按下
        self.target ={k:[] for k in range(height)}     #记录电梯中乘客的目的楼层
        self.waiting_up = {k:[] for k in range(height)}     #每层楼等候区 []中为等候人员目标楼层
        self.waiting_down = {k:[] for k in range(height)}     #每层楼等候区 []中为等候人员目标楼层

    def getin(self):
        if self.direction == 1:
            if self.now in self.button[1]:
                print '电梯门打开'
                self.button[1].remove(self.now)     #移除上按钮
                for target in self.waiting_up[self.now]:
                    people = random.choice(string.ascii_uppercase)
                    self.target[target].append(people)   #加入目标字典 
                    print '%s 走进电梯 按下目标楼层 %d 层' % (people, target)
                self.waiting_up[self.now] = []           #清空等待上楼的等待人
        else:
            if self.now in self.button[0]:
                print '电梯门打开'
                self.button[0].remove(self.now)     #移除下按钮
                for target in self.waiting_down[self.now]:
                    people = random.choice(string.ascii_uppercase)
                    self.target[target].append(people)   #加入目标字典 
                    print '%s 走进电梯 按下目标楼层 %d 层' % (people, target)
                self.waiting_down[self.now] = []           #清空等待上楼的等待人

    def out(self):
        passenger = self.target[self.now]
        if passenger: 
            for people in passenger:
                print people,'到达目标楼层 %d 层 走出电梯' % self.now
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
            print '错误指令 %d ->  %s'%(since,go)
            pass
        else:
            if since < go:
                self.button[1].add(since)            #上升按钮被按下
                self.waiting_up[since].append(go)    #加入此层楼上升等候区
                print '%d楼上升楼层被按下' % since
            else:
                self.button[0].add(since)            #下降按钮被按下
                self.waiting_down[since].append(go)    #加入此层楼下降等候区
                print '%d楼下降楼层被按下' % since
        

    def run(self):
        print '电梯运行中 楼高:%d 当前楼层:%d 上下方向:%d' % (self.height ,self.now,self.direction)
        while 1:
            if self.direction == 1:
                print '电梯上升到 %s 层' % self.now
                self.out()
                self.direction = self.up_choice()        #方向抉择
                self.getin()
                pass
            if self.direction == -1:
                print '电梯下降到 %s 层' % self.now
                self.out()
                self.direction = self.down_choice()    #方向抉择
                self.getin()
                pass
            if self.direction == 0:
                self.direction = self.up_choice()   #停留状态调用上升抉择
                self.getin()
                pass
            time.sleep(1)
            self.now += self.direction
