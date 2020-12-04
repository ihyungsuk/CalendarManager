from tkinter import *
from random import randint

# Return a random color string in the form of #RRGGBB
def getRandomColor():
    color = "#"
    for j in range(6):
        color += toHexChar(randint(0, 15)) # Add a random digit
    return color

# Convert an integer to a single hex digit in a character
def toHexChar(hexValue):
    if 0 <= hexValue <= 9:
        return chr(hexValue + ord('0'))
    else: # 10 <= hexValue <= 15
        return chr(hexValue - 10 + ord('A'))

# Define a Ball class
class Ball:
    def __init__(self):
        self.x = 0 # Starting center position
        self.y = 0
        self.dx = 2 # Move right by default
        self.dy  = 2 # Move down by default
        self.radius = 3
        self.color = getRandomColor()

class BounceBalls:
    def __init__(self):
        self.ballList = [] # Create a list for balls

        window = Tk()
        window.title("Bouncing Balls")

        ### Create Canvas ###
        self.width = 350
        self.height = 150
        self.canvas = Canvas(window, bg = "white", width = self.width, height = self.height)
        self.canvas.pack()


        ### Create Buttons ###
        frame = Frame(window)
        frame.pack()

        btStop = Button(frame, text = "Stop", command = self.stop)
        btStop.pack(side = LEFT)

        btResume = Button(frame, text = "Resume", command = self.resume)
        btResume.pack(side = LEFT)

        btAdd = Button(frame, text = "Add", command = self.add)
        btAdd.pack(side = LEFT)

        btRemove = Button(frame, text = "Remove", command = self.remove)
        btRemove.pack(side = LEFT)

        self.sleepTime = 20
        self.isStopped = False
        self.animate()

        window.mainloop()

    def stop(self): # Stop animation
        self.isStopped = True

    def resume(self):
        self.isStopped = False
        self.animate()

    def add(self): # Add a new ball
        self.ballList.append(Ball())

    def remove(self):
        self.ballList.pop()

    def animate(self):
        while not self.isStopped:
            self.canvas.after(self.sleepTime)
            self.canvas.update()
            self.canvas.delete("ball")

            for ball in self.ballList:
                self.redisplayBall(ball)

    def redisplayBall(self, ball):
        if ball.x > self.width or ball.x < 0:
            ball.dx = -ball.dx

        if ball.y > self.height or ball.y < 0:
            ball.dy = -ball.dy

        ball.x += ball.dx
        ball.y += ball.dy
        self.canvas.create_oval(ball.x - ball.radius, ball.y - ball.radius, \
                                ball.x + ball.radius, ball.y + ball.radius, \
                                fill = ball.color, tags = "ball")

BounceBalls()