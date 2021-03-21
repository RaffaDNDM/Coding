import turtle
import sys
import math
from termcolor import cprint
sys.setrecursionlimit(10000)
from random import randint

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
        self.cursor = turtle.Turtle(visible=False)
        self.screen = turtle.Screen()
        self.screen.screensize(600, 600)
        self.size = abs(self.TOP_RIGHT[0] - self.TOP_LEFT[0]) // 2
        self.step = self.size // self.AXIS_NUM_SAMPLES
        self.cursor.pencolor('blue')

    def color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self):
        '''
        Draw process
        '''
        choice = -1

        while(choice < 0 or choice > 11):
            cprint('Select the type of image you want to draw', 'blue')
            cprint('_________________________________________', 'blue')
            cprint('0) Lines drawing', 'blue')
            cprint('1) Illusion 1', 'blue')
            cprint('2) Illusion 2', 'blue')
            cprint('3) Vertical tangent circles', 'blue')
            cprint('4) Horizontal tangent circles', 'blue')
            cprint('5) Diagonal tangent circles 1', 'blue')
            cprint('6) Diagonal tangent circles 2', 'blue')
            cprint('7) Concentric circles', 'blue')
            cprint('8) Spiral', 'blue')
            cprint('9) Intersection of circles', 'blue')
            cprint('10) Circles donut', 'blue')
            cprint('_________________________________________', 'blue')

            try:
                choice = int(input())
                if choice == 0:
                    self.lines_figure()
                elif choice == 1:
                    self.illusion()
                elif choice == 2:
                    self.illusion2()
                elif choice == 3:
                    self.vertical_tangent_circles()
                elif choice == 4:
                    self.horizontal_tangent_circles()
                elif choice == 5:
                    self.diagonal_tangent_circles1()
                elif choice == 6:
                    self.diagonal_tangent_circles2()
                elif choice == 7:
                    self.concentric_circles()
                elif choice == 8:
                    self.spiral()
                elif choice == 9:
                    self.intersection_circles()
                elif choice == 10:
                    self.circles_donut()
                elif choice == 11:
                    exit(0)
            except TypeError:
                pass

        #Exit clicking on the window
        self.screen.exitonclick()

    def illusion(self):
        SIZE = 240
        STEP_SIZE = 10

        self.cursor.fillcolor('black')
        self.cursor.pencolor('black')

        #Outer borders
        self.cursor.penup()
        self.cursor.goto(-SIZE, SIZE)
        self.cursor.pendown()
        self.cursor.goto(SIZE, SIZE)
        self.cursor.goto(SIZE, -SIZE)
        self.cursor.goto(-SIZE, -SIZE)
        self.cursor.goto(-SIZE, SIZE)

        #Inner borders
        self.cursor.penup()
        self.cursor.goto(0, -SIZE)
        self.cursor.pendown()
        self.cursor.goto(SIZE, 0)
        self.cursor.goto(0, SIZE)
        self.cursor.goto(-SIZE, 0)
        self.cursor.goto(0, -SIZE)

        #Outer triangles
        self.outer_square(SIZE, STEP_SIZE)

        #Inner triangles
        self.inner_square(SIZE, STEP_SIZE)

    def illusion2(self):
        MIN_RADIUS = 20
        MAX_RADIUS = 240
        STEP_RADIUS = 20
        THETA = 22.5
        NUM_ANGLES = int(360.0 / 22.5)

        self.cursor.fillcolor('black')
        self.cursor.pencolor('black')

        count = 0

        for i in range(count%2, NUM_ANGLES, 2):
            self.cursor.penup()
            self.cursor.setheading(i*THETA)
            self.cursor.pendown()

            self.cursor.begin_fill()

            self.cursor.forward(MIN_RADIUS)
            self.cursor.left(90)
            self.cursor.circle(MIN_RADIUS, THETA)
            self.cursor.left(90)
            self.cursor.forward(MIN_RADIUS)

            self.cursor.end_fill()

        count += 1

        for r in range(MIN_RADIUS, MAX_RADIUS, STEP_RADIUS):

            for i in range(count%2, NUM_ANGLES, 2):
                self.cursor.penup()
                self.cursor.goto(int(r*math.cos(2*math.pi*i*THETA/360.0)),int(r*math.sin(2*math.pi*i*THETA/360.0)))
                self.cursor.setheading(i*THETA)
                self.cursor.pendown()

                self.cursor.begin_fill()

                self.cursor.forward(STEP_RADIUS)
                self.cursor.left(90)
                self.cursor.circle(r+STEP_RADIUS, THETA)
                self.cursor.left(90)
                self.cursor.forward(STEP_RADIUS)
                self.cursor.right(90)
                self.cursor.circle(r, -THETA)

                self.cursor.end_fill()

            count += 1

        self.cursor.penup()
        self.cursor.goto(MAX_RADIUS, 0)
        self.cursor.setheading(90)
        self.cursor.pendown()

        self.cursor.circle(MAX_RADIUS)

    def outer_square(self, size, step_size):
        num_steps = int(size/step_size)

        #Top left
        for i in range(0,num_steps,2):
            self.cursor.penup()
            self.cursor.goto(-i*step_size, size-(i*step_size))
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(-135)
            
            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            self.cursor.right(180-45-90+abs(math.degrees(math.atan((y_to)/(size-x_to)))))
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))
            
            self.cursor.end_fill()

        #Bottom left
        for i in range(0,num_steps,2):

            self.cursor.penup()
            self.cursor.goto(-size+i*step_size, -i*step_size)
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(-45)
            
            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            self.cursor.right(180-45-90+abs(math.degrees(math.atan((y_to)/(size-x_to)))))
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))
            
            self.cursor.end_fill()       

        #Bottom right
        for i in range(0,num_steps,2):

            self.cursor.penup()
            self.cursor.goto(i*step_size, -size+(i*step_size))
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(45)
            
            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            self.cursor.right(180-45-90+abs(math.degrees(math.atan((y_to)/(size-x_to)))))
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))
            
            self.cursor.end_fill()

        #Top right
        for i in range(0,num_steps,2):

            self.cursor.penup()
            self.cursor.goto(size-i*step_size, i*step_size)
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(135)
            
            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            self.cursor.right(180-45-90+abs(math.degrees(math.atan((y_to)/(size-x_to)))))
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))
            
            self.cursor.end_fill()

    def inner_square(self, size, step_size):
        num_steps = int(size/step_size)

        for i in range(1,num_steps + 1,2):

            self.cursor.penup()
            self.cursor.goto(-i*step_size, size-(i*step_size))
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(-135)
            
            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            
            angle = 0
            if x_to != size:
                angle = 90-abs(math.degrees(math.atan((y_to)/(size-x_to))))

            self.cursor.left(180-45-angle)
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))
            
            self.cursor.end_fill()

        for i in range(1,num_steps + 1,2):

            self.cursor.penup()
            self.cursor.goto(-size+i*step_size, -i*step_size)
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(-45)

            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            
            angle = 0
            if x_to != size:
                angle = 90-abs(math.degrees(math.atan((y_to)/(size-x_to))))

            self.cursor.left(180-45-angle)
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))

            self.cursor.end_fill()

        for i in range(1,num_steps + 1,2):

            self.cursor.penup()
            self.cursor.goto(i*step_size, -size+i*step_size)
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(45)

            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            
            angle = 0
            if x_to != size:
                angle = 90-abs(math.degrees(math.atan((y_to)/(size-x_to))))

            self.cursor.left(180-45-angle)
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))

            self.cursor.end_fill()

        for i in range(1,num_steps + 1,2):

            self.cursor.penup()
            self.cursor.goto(size-i*step_size, i*step_size)
            self.cursor.pendown()
        
            self.cursor.begin_fill()
            self.cursor.setheading(135)

            x_from, y_from = i*step_size, i*step_size
            x_to, y_to = (i+1)*step_size, (i+1)*step_size
            self.cursor.forward(int(math.sqrt((x_to-x_from)**2 + (y_to-y_from)**2)))
            
            angle = 0
            if x_to != size:
                angle = 90-abs(math.degrees(math.atan((y_to)/(size-x_to))))

            self.cursor.left(180-45-angle)            
            self.cursor.forward(int(math.sqrt(y_to**2 + (size-x_to)**2)))

            self.cursor.end_fill()

    def vertical_tangent_circles(self):
        MAX_RADIUS = 150
        STEP_RADIUS = 4
        turtle.colormode(255)

        #Draw on the TOP side
        for i in range(0, MAX_RADIUS, STEP_RADIUS):
            self.cursor.pencolor(self.color())
            self.cursor.circle(MAX_RADIUS-i)
            self.cursor.circle(-(MAX_RADIUS-i))

    def horizontal_tangent_circles(self):
        MAX_RADIUS = 150
        STEP_RADIUS = 4
        turtle.colormode(255)

        self.cursor.setheading(90)

        #Draw on the LEFT side
        for i in range(0, MAX_RADIUS, STEP_RADIUS):
            self.cursor.pencolor(self.color())
            self.cursor.circle(MAX_RADIUS-i)
            self.cursor.circle(-(MAX_RADIUS-i))

    def diagonal_tangent_circles1(self):
        MAX_RADIUS = 150
        STEP_RADIUS = 4
        turtle.colormode(255)

        self.cursor.setheading(45)

        #Draw on the LEFT side
        for i in range(0, MAX_RADIUS, STEP_RADIUS):
            self.cursor.pencolor(self.color())
            self.cursor.circle(MAX_RADIUS-i)
            self.cursor.circle(-(MAX_RADIUS-i))

    def diagonal_tangent_circles2(self):
        MAX_RADIUS = 150
        STEP_RADIUS = 4
        turtle.colormode(255)

        self.cursor.setheading(-45)

        #Draw on the LEFT side
        for i in range(0, MAX_RADIUS, STEP_RADIUS):
            self.cursor.pencolor(self.color())
            self.cursor.circle(MAX_RADIUS-i)
            self.cursor.circle(-(MAX_RADIUS-i))
            
    def concentric_circles(self):
        MAX_RADIUS = 300
        STEP_RADIUS = 4
        turtle.colormode(255)

        #Draw on the LEFT side
        for r in range(0, MAX_RADIUS, STEP_RADIUS):
            self.cursor.pencolor(self.color())
            self.cursor.penup()
            self.cursor.goto(0, -r)
            self.cursor.pendown()
            self.cursor.circle(r)

    def spiral(self):
        MIN_RADIUS = 4        
        MAX_RADIUS = 300
        
        self.cursor.penup()
        self.cursor.goto(0, -MIN_RADIUS)
        self.cursor.pendown()

        #Draw on the LEFT side
        for r in range(MIN_RADIUS, MAX_RADIUS):
            self.cursor.circle(r, 90)

    def intersection_circles(self):
        RADIUS = 100
        MIN_ANGLE = 0
        MAX_ANGLE = 360
        STEP_ANGLE = 5
        turtle.colormode(255)

        #Draw on the LEFT side
        for angle in range(MIN_ANGLE, MAX_ANGLE, STEP_ANGLE):
            self.cursor.pencolor(self.color())
            self.cursor.setheading(angle)
            self.cursor.circle(RADIUS)

    def circles_donut(self):
        RADIUS_CIRCLE = 80
        RADIUS_HOLE = 50
        MIN_ANGLE = 0
        MAX_ANGLE = 360
        STEP_ANGLE = 5

        #Draw on the LEFT side
        for angle in range(MIN_ANGLE, MAX_ANGLE, STEP_ANGLE):
            self.cursor.penup()
            rad_angle = angle*2*math.pi/360.0
            self.cursor.goto(int(RADIUS_HOLE*math.cos(rad_angle)), int(RADIUS_HOLE*math.sin(rad_angle)))
            self.cursor.pendown()
            self.cursor.setheading(90+angle)
            self.cursor.circle(-RADIUS_CIRCLE)

    def lines_figure(self):
        #Draw in the TOP LEFT subwindow
        self.lines_subfigure((self.TOP_LEFT[0], self.TOP_LEFT[1]), 
                             (self.TOP_LEFT[0], self.TOP_LEFT[1]-self.size),
                             (self.TOP_LEFT[0]+self.size, self.TOP_LEFT[1]-self.size),
                             (self.TOP_LEFT[0]+self.size, self.TOP_LEFT[1]))
        
        #Draw in the BOTTOM LEFT subwindow
        self.lines_subfigure((self.BOTTOM_LEFT[0], self.BOTTOM_LEFT[1]+self.size), 
                             (self.BOTTOM_LEFT[0], self.BOTTOM_LEFT[1]),
                             (self.BOTTOM_LEFT[0]+self.size, self.BOTTOM_LEFT[1]),
                             (self.BOTTOM_LEFT[0]+self.size, self.BOTTOM_LEFT[1]+self.size))

        #Draw in the TOP RIGHT subwindow
        self.lines_subfigure((self.BOTTOM_RIGHT[0]-self.size, self.BOTTOM_RIGHT[1]+self.size), 
                             (self.BOTTOM_RIGHT[0]-self.size, self.BOTTOM_RIGHT[1]),
                             (self.BOTTOM_RIGHT[0], self.BOTTOM_RIGHT[1]),
                             (self.BOTTOM_RIGHT[0], self.BOTTOM_RIGHT[1]+self.size))

        #Draw in the TOP RIGHT subwindow
        self.lines_subfigure((self.TOP_RIGHT[0]-self.size, self.TOP_RIGHT[1]), 
                             (self.TOP_RIGHT[0]-self.size, self.TOP_RIGHT[1]-self.size),
                             (self.TOP_RIGHT[0], self.TOP_RIGHT[1]-self.size),
                             (self.TOP_RIGHT[0], self.TOP_RIGHT[1]))

    def lines_subfigure(self, top_left, bottom_left, bottom_right, top_right):
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