import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

class JuliaSet:
    '''
    Plot of Julia set.

    Args:
        step (float): Maximum size of the step on both the axis
                      in the complex plane 
        
        val_bound (float): Maximum value until divergence
        
        iter_bound (int): Maximum number of iteration until divergence
        
        c (complex): Complex factor in succession
        
        colored (bool): True for colored plot, False for grayscale plot 

    Attributes:
        step (float): Maximum size of the step on both the axis
                      in the complex plane 
        
        val_bound (float): Maximum value until divergence
        
        iter_bound (int): Maximum number of iteration until divergence
        
        c (complex): Complex factor in succession
        
        colored (bool): True for colored plot, False for grayscale plot 

        RGB_COLORS (list): List of random RGB colors, one for each possible
                           iteration in which the succession diverges for
                           colored plot

        GRAY_COLORS (list): List of random RGB colors (with equal components)
                            one for each possible iteration in which the 
                            succession diverges for colored plot

    '''
    
    def __init__(self, step, val_bound, iter_bound, c, colored=True):
        self.step = step
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.c = c
        self.colored = colored
        self.RGB_COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]
        self.GRAY_COLORS = [np.array([x,x,x]) for x in np.random.choice(range(256), size=self.iter_bound+1)]

    def iter_at_divergence(self, p0):
        '''
        Compute z=z^2+c until divergence of point p0 of the complex plane 
        or maximum number of iteration is reached without divergency (fixed c).
        Then return the color related to that iteration.

        Args:
            p0 (complex): Initial complex point

        Returns:
            color (tuple): Color related to the iteration in which
                           the succession diverges for p0

        '''

        z = p0 #Succession start at complex specified
        i=0 #Iteration

        while i<self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + self.c
            i+=1

        if self.colored:
            return self.RGB_COLORS[i]
        else:
            return self.GRAY_COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        '''
        Plot all the points w of the complex plane with Real in [start_x, end_x]
        and Im(w) in [start_y, end_y].
        (The number of points is ((end_x-start_x)//step)*((end_y-start_y)//step)

        Args:
            start_x (float): First value of the Real axis to be analysed

            end_x (float): Last value of the Real axis to be analysed

            start_y (float): First value of the Imaginary axis to be analysed

            end_y (float): Last value of the Imaginary axis to be analysed

        '''

        #Find the iteration of divergence for each sample in space 
        #with specified step
        x_samples = np.arange(start_x, end_x, self.step)
        y_samples = np.arange(start_y, end_y, self.step)
        img = np.full((len(y_samples), len(x_samples), 3),0)

        for i in range(len(y_samples)):
            for j in range(len(x_samples)):
                #Color related to the iteration of divergence
                img[i][j] = self.iter_at_divergence(complex(x_samples[j], y_samples[i]))

        #Plot the result image of Julia set
        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])
        plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('julia_set.png')

class MandelbrotSet:
    '''
    Plot of Mandelbrot set.

    Args:
        step (float): Maximum size of the step on both the axis
                      in the complex plane 
        
        val_bound (float): Maximum value until divergence
        
        iter_bound (int): Maximum number of iteration until divergence
        
        colored (bool): True for colored plot, False for grayscale plot 

    Attributes:
        step (float): Maximum size of the step on both the axis
                      in the complex plane 
        
        val_bound (float): Maximum value until divergence
        
        iter_bound (int): Maximum number of iteration until divergence
        
        colored (bool): True for colored plot, False for grayscale plot 

        RGB_COLORS (list): List of random RGB colors, one for each possible
                           iteration in which the succession diverges for
                           colored plot

        GRAY_COLORS (list): List of random RGB colors (with equal components)
                            one for each possible iteration in which the 
                            succession diverges for colored plot

    '''

    def __init__(self, step, val_bound, iter_bound, colored=True):
        self.step = step
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.colored = colored
        self.RGB_COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]
        self.GRAY_COLORS = [np.array([x,x,x]) for x in np.random.choice(range(256), size=self.iter_bound+1)]

    def iter_at_divergence(self, c):
        '''
        Compute z=z^2+c until divergence of point p0 of the complex plane 
        or maximum number of iteration is reached without divergency.
        Then return the color related to that iteration.

        Args:
            c (complex): Initial complex point and constant in succession

        Returns:
            color (tuple): Color related to the iteration in which
                           the succession diverges for c

        '''
        z = c #Succession start
        i=0 #Iteration

        while i < self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + c
            i+=1

        if self.colored:
            return self.RGB_COLORS[i]
        else:
            return self.GRAY_COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        '''
        Plot all the points w of the complex plane with Real in [start_x, end_x]
        and Im(w) in [start_y, end_y].
        (The number of points is ((end_x-start_x)//step)*((end_y-start_y)//step)

        Args:
            start_x (float): First value of the Real axis to be analysed

            end_x (float): Last value of the Real axis to be analysed

            start_y (float): First value of the Imaginary axis to be analysed

            end_y (float): Last value of the Imaginary axis to be analysed

        '''
        
        #Find the iteration of divergence for each sample in space 
        #with specified step
        x_samples = np.arange(start_x, end_x, self.step)
        y_samples = np.arange(start_y, end_y, self.step)
        img = np.full((len(y_samples), len(x_samples), 3),0)

        for i in range(len(y_samples)):
            for j in range(len(x_samples)):
                #Color related to the iteration of divergence
                img[i][j] = self.iter_at_divergence(complex(x_samples[j], y_samples[i]))

        #Plot the result image of Julia set
        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])
        plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('mandelbrot_set.png')


def main():
    colored = True
    
    m = MandelbrotSet(1e-3, 3, 40, colored)
    m.plot(-2.1, 0.6, -1.4, 1.4)
    #m.plot(-1.48, -1.42, -0.02, 0.02)
    j = JuliaSet(1e-3, 3, 30, complex(0.2,0.6), colored)
    j.plot(-2, 2, -2, 2)

if __name__=='__main__':
    main()