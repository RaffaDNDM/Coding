import turtle
import sys
sys.setrecursionlimit(10000)

TURTLE_SIZE = 20
turtle.hideturtle()

class GeometryDraw:
    '''
    Gemotric draw
    
    Args:
        axis_num_samples (int): Number of samples in every axis

        size (tuple): Size of the window
    
    Attributes:
        AXIS_NUM_SAMPLES (int): Number of samples in every axis
        
        cursor (turtle.Turtle): Turle cursor for drawing
        
        screen (turtle.Screen): Window of the turtle
        
        size (int): Size of an axis of every subwindow
        
        step (int): Size of the step of every subwindow 

    '''
    
    MAX_AXIS_VALUE = 300
    TOP_LEFT = (-MAX_AXIS_VALUE, MAX_AXIS_VALUE)
    BOTTOM_LEFT = (-MAX_AXIS_VALUE, -MAX_AXIS_VALUE)
    TOP_RIGHT = (MAX_AXIS_VALUE, MAX_AXIS_VALUE)
    BOTTOM_RIGHT = (MAX_AXIS_VALUE, -MAX_AXIS_VALUE)

    def __init__(self, axis_num_samples, size=(300, 300)):
        self.AXIS_NUM_SAMPLES = axis_num_samples
        turtle.speed(10)
        self.cursor = turtle.Turtle()
        self.screen = turtle.Screen()
        self.screen.screensize(600, 600)
        self.size = abs(self.TOP_RIGHT[0] - self.TOP_LEFT[0]) // 2
        self.step = self.size // self.AXIS_NUM_SAMPLES
        
    def draw(self):
        '''
        Draw process
        '''

        #Draw in the TOP LEFT subwindow
        self.draw_subfigure((self.TOP_LEFT[0], self.TOP_LEFT[1]), 
                            (self.TOP_LEFT[0], self.TOP_LEFT[1]-self.size),
                            (self.TOP_LEFT[0]+self.size, self.TOP_LEFT[1]-self.size),
                            (self.TOP_LEFT[0]+self.size, self.TOP_LEFT[1]))
        
        #Draw in the BOTTOM LEFT subwindow
        self.draw_subfigure((self.BOTTOM_LEFT[0], self.BOTTOM_LEFT[1]+self.size), 
                            (self.BOTTOM_LEFT[0], self.BOTTOM_LEFT[1]),
                            (self.BOTTOM_LEFT[0]+self.size, self.BOTTOM_LEFT[1]),
                            (self.BOTTOM_LEFT[0]+self.size, self.BOTTOM_LEFT[1]+self.size))

        #Draw in the TOP RIGHT subwindow
        self.draw_subfigure((self.BOTTOM_RIGHT[0]-self.size, self.BOTTOM_RIGHT[1]+self.size), 
                            (self.BOTTOM_RIGHT[0]-self.size, self.BOTTOM_RIGHT[1]),
                            (self.BOTTOM_RIGHT[0], self.BOTTOM_RIGHT[1]),
                            (self.BOTTOM_RIGHT[0], self.BOTTOM_RIGHT[1]+self.size))

        #Draw in the TOP RIGHT subwindow
        self.draw_subfigure((self.TOP_RIGHT[0]-self.size, self.TOP_RIGHT[1]), 
                            (self.TOP_RIGHT[0]-self.size, self.TOP_RIGHT[1]-self.size),
                            (self.TOP_RIGHT[0], self.TOP_RIGHT[1]-self.size),
                            (self.TOP_RIGHT[0], self.TOP_RIGHT[1]))

        #Exit clicking on the window
        self.screen.exitonclick()

    def draw_subfigure(self, top_left, bottom_left, bottom_right, top_right):
        #Draw external square
        self.cursor.penup()
        self.cursor.goto(top_left[0], top_left[1])
        self.cursor.pendown()
        self.cursor.goto(bottom_left[0], bottom_left[1])
        self.cursor.goto(bottom_right[0], bottom_right[1])
        self.cursor.goto(top_right[0], top_right[1])
        self.cursor.goto(top_left[0], top_left[1])

        #Geometric draw from left axis
        for i in range(1, self.AXIS_NUM_SAMPLES+1):
            self.cursor.penup()
            self.cursor.goto(top_left[0], top_left[1]-(i-1)*self.step)
            self.cursor.pendown()
            self.cursor.goto(bottom_left[0]+i*self.step, bottom_left[1])

        #Geometric draw from bottom axis
        for i in range(1, self.AXIS_NUM_SAMPLES+1):
            self.cursor.penup()
            self.cursor.goto(bottom_left[0]+(i-1)*self.step, bottom_left[1])
            self.cursor.pendown()
            self.cursor.goto(bottom_right[0], bottom_right[1]+i*self.step)            

        #Geometric draw from right axis
        for i in range(1, self.AXIS_NUM_SAMPLES+1):
            self.cursor.penup()
            self.cursor.goto(bottom_right[0], bottom_right[1]+(i-1)*self.step)
            self.cursor.pendown()
            self.cursor.goto(top_right[0]-i*self.step, top_right[1])

        #Geometric draw from top axis
        for i in range(1, self.AXIS_NUM_SAMPLES+1):
            self.cursor.penup()
            self.cursor.goto(top_right[0]-(i-1)*self.step, top_right[1])
            self.cursor.pendown()
            self.cursor.goto(top_left[0], top_left[1]-i*self.step)


def main():
    g = GeometryDraw(30)
    g.draw()

if __name__=='__main__':
    main()