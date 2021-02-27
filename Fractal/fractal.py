import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

class JuliaSet:
    def __init__(self, c, sampling_num, val_bound, iter_bound, colored):
        self.sampling_num = sampling_num
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.c = c
        self.colored = colored
        self.COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]

    def iter_at_divergence(self, p0):
        '''
            z=z^2+c until divergence or not condition
            c fixed
        '''
        z = p0 #Succession start at complex specified
        i=0 #Iteration

        while i<self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + self.c
            i+=1

        return self.COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        img = np.full((self.sampling_num, self.sampling_num, 3),0)
        x_samples = np.linspace(start_x, end_x, self.sampling_num)
        y_samples = np.linspace(start_y, end_y, self.sampling_num)

        for i in range(self.sampling_num):
            for j in range(self.sampling_num):
                img[j][i] = self.iter_at_divergence(complex(x_samples[i], y_samples[j]))

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])

        if self.colored:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        else:
            plt.imshow(img[:,:,1], 
                       cmap='gray', 
                       interpolation='none', 
                       extent=[start_x,end_x,start_y,end_y])
        
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('julia_set.png')

class MandelbrotSet:
    def __init__(self, sampling_num, val_bound, iter_bound, colored=True):
        self.sampling_num = sampling_num
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.colored = colored
        self.COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]

    def iter_at_divergence(self, c):
        '''
        Return the iteration in which diverges
        z=z^2+c until divergence or maximum iterations reached
        '''
        z = c #Succession start
        i=0 #Iteration

        while i < self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + c
            i+=1

        return self.COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        img = np.full((self.sampling_num, self.sampling_num, 3),0)
        x_samples = np.linspace(start_x, end_x, self.sampling_num)
        y_samples = np.linspace(start_y, end_y, self.sampling_num)

        for i in range(self.sampling_num):
            for j in range(self.sampling_num):
                img[j][i] = self.iter_at_divergence(complex(x_samples[i], y_samples[j]))

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])

        if self.colored:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        else:
            plt.imshow(img[:,:,1], 
                       cmap='gray', 
                       interpolation='none', 
                       extent=[start_x,end_x,start_y,end_y])
        
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('mandelbrot_set.png')


if __name__=='__main__':
    colored = False
    
    m = MandelbrotSet(2000, 3, 40, colored)
    m.plot(-2.1, 0.6, -1.4, 1.4)
    #m.plot(-1.48, -1.42, -0.02, 0.02)
    j = JuliaSet(complex(0.2,0.6), 2000, 3, 30, colored)
    j.plot(-2, 2, -2, 2)