from tkinter import Tk, Canvas, Label
from time import sleep
from random import choice, randint


class Apple:
    def __init__(self, x, y, canv):
        self.canv = canv
        self.coords = {'x': x, 'y': y}
        self.body = self.canv.create_rectangle(self.coords['x'], 
                                               self.coords['y'], 
                                               self.coords['x'] + 10, 
                                               self.coords['y'] + 10, 
                                               fill='red', 
                                               width=0)
    
    def new_pos(self):
        self.coords['x'] = randint(1, 48) * 10
        self.coords['y'] = randint(1, 48) * 10
        self.canv.coords(self.body, self.coords['x'], self.coords['y'], self.coords['x'] + 10, self.coords['y'] + 10)


class Snake:
    def __init__(self, root, canv, apple):
        self.root = root
        self.apple = apple
        self.COLORS = ['yellow', 'blue', 'purple', 'orange', 'pink', 'brown', 'skyblue']
        self.canv = canv
        self.body = [self.canv.create_rectangle(90, 100, 100, 110, fill='white', width=0), 
                     self.canv.create_rectangle(100, 100, 110, 110, fill=choice(self.COLORS), width=0)]
        self.coords = {'x': 90, 'y': 100}
        self.direction = 'Right'
        self.root.bind('<KeyPress>', self.key_press)
        self.next_dead = True
        self.turned = True
        self.living = True
        self.score = 0

    def key_press(self, event):
        if event.keysym in ['Right', 'Left', 'Up', 'Down', 'q']:
            accept = True
            match self.direction:
                case 'Right':
                    if event.keysym == 'Left':
                        accept = False
                
                case 'Left':
                    if event.keysym == 'Right':
                        accept = False
                
                case 'Up':
                    if event.keysym == 'Down':
                        accept = False
                
                case 'Down':
                    if event.keysym == 'Up':
                        accept = False

                case 'q':
                    self.root.destroy()                
            
            if accept and self.turned:
                self.direction = event.keysym
                self.turned = False

    def update(self):
        all_coords = []
        if self.coords == self.apple.coords:
            self.apple.new_pos()
            self.next_dead = True
            self.body.append(self.canv.create_rectangle(*self.canv.coords(self.body[-1]), fill=choice(self.COLORS), width=0))
            self.score += 1
        for i in range(len(self.body) - 1, 0, -1):
            all_coords.append(' '.join(list(map(str, self.canv.coords(self.body[i])))))
            self.canv.coords(self.body[i], self.canv.coords(self.body[i - 1]))
        match self.direction:
            case 'Right':
                self.canv.move(self.body[0], 10, 0)
                self.coords['x'] += 10
            case 'Left':
                self.canv.move(self.body[0], -10, 0)
                self.coords['x'] -= 10
            case 'Up':
                self.canv.move(self.body[0], 0, -10)
                self.coords['y'] -= 10
            case 'Down':
                self.canv.move(self.body[0], 0, 10)
                self.coords['y'] += 10
            case 'q':
                self.root.destroy()
        
        all_coords.append(' '.join(list(map(str, self.canv.coords(self.body[0])))))
        if len(set(all_coords)) < len(all_coords):
            if self.next_dead:
                self.next_dead = False
            else:
                self.living = False
        
        if not 0 <= self.coords['x'] < 500 or not 0 <= self.coords['y'] < 500:
            self.living = False
        self.turned = True
        self.score += 0.001
        

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        self.root.title('Snake')
        self.canv = Canvas(self.root, width=500, height=500, bg='green')
        self.canv.pack()
        self.apple = Apple(randint(1, 48) * 10, randint(1, 48) * 10, self.canv)
        self.snake = Snake(self.root, self.canv, self.apple)
        self.mainloop()

    def mainloop(self):
        while self.snake.living:
            self.snake.update()
            self.root.update()
            sleep(0.1)
        self.end_title = Label(self.root, text=f'Game over\nYour score was {int(self.snake.score)}', font='Arial 30', fg='red', bg='green')
        self.end_title.place(anchor='center', x=250, y=250)
        self.root.mainloop()


if __name__ == '__main__':
    try:
        app = App()
    except:
        pass