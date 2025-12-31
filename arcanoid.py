from tkinter import Tk, Canvas, Label
from time import sleep
from random import randint, choice


class Block:
    def __init__(self, canv, x, y):
        self.canv = canv
        self.pos = {'x': x, 'y': y}
        self.work = True
        self.body = self.canv.create_rectangle(self.pos['x'] - 50, 
                                               self.pos['y'] - 15, 
                                               self.pos['x'] + 50, 
                                               self.pos['y'] + 15, 
                                               fill=choice(['red', 'white', 'green', 'brown', 'orange', 'purple']), 
                                               width=0)
    
    def crash(self):
        self.canv.delete(self.body)
        self.work = False


class Ball:
    def __init__(self, canv, rocket, x, y, blocks):
        self.canv = canv
        self.rocket = rocket
        self.pos = {'x': x, 'y': y}
        self.x_speed = choice([4, -4])
        self.y_speed = -4
        self.blocks = blocks
        self.blocks_num = 1
        self.body = self.canv.create_oval(self.pos['x'] - 7, self.pos['y'] - 7, self.pos['x'] + 7, self.pos['y'] + 7, fill='white', width=0)
        self.ok = True

    def update(self):
        self.pos['x'] += self.x_speed
        self.pos['y'] += self.y_speed
        self.canv.move(self.body, self.x_speed, self.y_speed)
        if abs(self.pos['x'] - self.rocket.x) <= 66 and self.pos['y'] >= 690:
            self.y_speed = -self.y_speed
            if self.y_speed > 0:
                self.y_speed = randint(3, 5)
            else:
                self.y_speed = randint(-5, -3)
    
        if not 7 < self.pos['x'] < 993:
            self.x_speed = -self.x_speed
        if not 7 < self.pos['y'] < 693:
            self.y_speed = -self.y_speed

        self.blocks_num = 0
        for block in self.blocks:
            if block.work:
                self.blocks_num += 1
                if abs(self.pos['x'] - block.pos['x']) <= 57 and abs(self.pos['y'] - block.pos['y']) <= 17:
                    self.y_speed = -self.y_speed
                    block.crash()

        if self.pos['y'] > 693:
            self.ok = False


class Rocket:
    def __init__(self, canv, root, x):
        self.x = x
        self.canv = canv
        self.root = root
        self.body = self.canv.create_rectangle(x - 60, 690, x + 60, 700, fill='white', width=0)
        self.root.bind('<KeyPress>', self.press)
        self.root.bind('<KeyRelease>', self.release)
        self.direction = 'Stay'
    def press(self, event):
        new_direction = None
        match event.keysym:
            case 'Left':
                new_direction = 'Left'
            case 'Right':
                new_direction = 'Right'
            case 'q':
                self.root.destroy()
            case _:
                new_direction = self.direction
        self.direction = new_direction
    
    def release(self, event):
        self.direction = 'Stay'

    def update(self):
        match self.direction:
            case 'Left':
                if self.x > 60:
                    self.x -= 7
                    self.canv.move(self.body, -7, 0)
            case 'Right':
                if self.x < 940:
                    self.x += 7
                    self.canv.move(self.body, 7, 0)


class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1000x700+0+0')
        self.root.resizable(False, False)
        self.canv = Canvas(self.root, width=1000, height=700, bg='darkblue')
        self.canv.pack()
        self.blocks = [Block(self.canv, x, y) for x in range(50, 951, 100) for y in range(50, 301, 30)]
        self.rocket = Rocket(self.canv, self.root, 500)
        self.ball = Ball(self.canv, self.rocket, randint(8, 992), randint(350, 650), self.blocks)
        self.mainloop()

    def mainloop(self):
        while self.ball.ok and self.ball.blocks_num > 0:
            self.root.update()
            self.rocket.update()
            self.ball.update()
            sleep(0.01) 
        if self.ball.blocks_num == 0:
            Label(self.root, text='You\'ve won', font='Arial 60', bg='darkblue', fg='green').place(x=500, y=300, anchor='center')
        else:
            Label(self.root, text='You\'ve lost', font='Arial 60', bg='red', fg='white').place(x=500, y=300, anchor='center')

        self.root.mainloop()

if __name__ == '__main__':
    app = App()