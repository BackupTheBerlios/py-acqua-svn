#! /usr/bin/env python
#
# python simple Oscilloscope 
#
# (C)2006 Patrick Nomblot <pyScope@nomblot.org>
# this is distributed under a free software license, see license.txt


import sys
import Tkinter


class Chanel:
    def __init__(self, scope, name, offsetY, xScale=5, yScale=30, color='white'):
        self.canvas = scope.canvas
        self.offsetY =  offsetY
        self.xScale = xScale
        self.yScale = yScale
        self.name = name
        self.color = color
        self.reset()

    def draw(self, val, color='white'):
        if self.y==None:
            self.y = val
        self.canvas.create_line(self.x*self.xScale, self.offsetY-(self.y*self.yScale), (self.x+1)*self.xScale, self.offsetY-(self.y*self.yScale), width=1, fill=color)
        oldy = self.y
        self.y = val
        self.x += 1
        self.canvas.create_line(self.x*self.xScale, self.offsetY-(oldy*self.yScale), self.x*self.xScale, self.offsetY - (self.y*self.yScale), width=1, fill=color)
        self.canvas.create_line(self.x*self.xScale, self.offsetY-(self.y*self.yScale), (self.x+1)*self.xScale, self.offsetY-(self.y*self.yScale), width=1, fill=color)

    def reset(self):
        self.x = self.xScale
        self.y = None
        self.canvas.create_text(15, self.offsetY-(self.yScale/2), text=self.name, fill=self.color)


class Scope:
    def __init__(self, name, width=8000, height=140):
        self.root = Tkinter.Tk()
        self.root.title(name)

        self.width = width
        self.height = height

        self.xscroll = Tkinter.Scrollbar(self.root, orient=Tkinter.HORIZONTAL)
        self.xscroll.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)
        self.yscroll = Tkinter.Scrollbar(self.root, orient=Tkinter.VERTICAL)
        if height>400:
            self.yscroll.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)

        self.canvas = Tkinter.Canvas(self.root, width=700, height=height, bg = 'black',
                                     xscrollcommand=self.xscroll.set,
                                     yscrollcommand=self.yscroll.set)

        self.xscroll.config(command=self.canvas.xview)
        self.yscroll.config(command=self.canvas.yview)
        self.canvas.pack(fill=Tkinter.BOTH)
        self.canvas.config(scrollregion=(0,0,width,height))
        Tkinter.Button(self.root, text='Quit', command=self.root.quit).pack(side=Tkinter.LEFT)
    
    def show(self):
        self.root.mainloop()

    def reset(self):
        self.canvas.create_rectangle(0,0,self.width,self.height, fill='black')
               
        

class multiChanelScope:
    def __init__(self, title):
        self.scope = Scope(title)
        self.addAction('Reset Scope', self.reset)
        self.result = Tkinter.Label(self.scope.root, text=' ? ')
        self.result.pack(side=Tkinter.RIGHT)

    def connect(self, object, functionName, chanels, colors=None):
        self.oldFunction = getattr(object, functionName)
        setattr(object, functionName, self.scopeWrapper)
        self.chanels = {}
        for i, chanel in enumerate(chanels):
            self.chanels[chanel] = Chanel(self.scope, chanel, offsetY=60*(i+1))
        self.colors = colors

    def reset(self):
        self.scope.reset()
        for chanel in self.chanels.values():
            chanel.reset()
       
    def addAction(self, name, function):
        Tkinter.Button(self.scope.root, text=name, command=function).pack(side=Tkinter.LEFT)

    def show(self):
        self.scope.show()


    def scopeWrapper(self, **values):
        caller = sys._getframe(1).f_code.co_name
        if self.colors and caller in self.colors:
            color = self.colors[caller]
        else:
            color = 'white'
        for chanel, value in values.items():
            self.chanels[chanel].draw(value,color)
        return self.oldFunction(**values)





