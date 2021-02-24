import numpy as np
import matplotlib.pyplot as plt

class JuliaSet:
    def __init__(self, c, colored):
        self.c = c
        self.colored = colored

    def iter_at_divergence(self, p0, val_bound, iter_bound):
        '''
            z=z^2+c until divergence or not condition
            c fixed
        '''
        z = p0 #Succession start at complex specified
        i=0 #Iteration

        while i<iter_bound and abs(z) < val_bound:
            z = z**2 + self.c
            i+=1

        return i

    def plot(self, sampling_num, val_bound, iter_bound, start_x, end_x, start_y, end_y):
        img = np.full((sampling_num, sampling_num),0)
        x_samples = np.linspace(start_x, end_x, sampling_num)
        y_samples = np.linspace(start_y, end_y, sampling_num)

        for i in range(sampling_num):
            for j in range(sampling_num):
                img[j][i] = self.iter_at_divergence(complex(x_samples[i], y_samples[j]),
                                                    val_bound,
                                                    iter_bound)

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])

        if self.colored:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        else:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y], cmap='gray')

        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('julia_set.png')

class MandelbrotSet:
    def __init__(self, colored):
        self.colored = colored 

    def iter_at_divergence(self, c, val_bound, iter_bound):
        '''
        Return the iteration in which diverges
        z=z^2+c until divergence or maximum iterations reached
        '''
        z = c #Succession start
        i=0 #Iteration

        while i<iter_bound and abs(z) < val_bound:
            z = z**2 + c
            i+=1

        return i

    def plot(self, sampling_num, val_bound, iter_bound, start_x, end_x, start_y, end_y):
        img = np.full((sampling_num, sampling_num),0)
        x_samples = np.linspace(start_x, end_x, sampling_num)
        y_samples = np.linspace(start_y, end_y, sampling_num)

        for i in range(sampling_num):
            for j in range(sampling_num):
                img[j][i] = self.iter_at_divergence(complex(x_samples[i], y_samples[j]), 
                                                    val_bound,
                                                    iter_bound)

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])

        if self.colored:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        else:
            plt.imshow(img, extent=[start_x,end_x,start_y,end_y], cmap='gray')

        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('mandelbrot_set.png')


if __name__=='__main__':
    colored = True
    
    m = MandelbrotSet(colored)
    m.plot(2000, 2, 30, -2.1, 0.6, -1.4, 1.4)
    j = JuliaSet(complex(0.2,0.6), colored)
    j.plot(2000, 4, 30, -2, 2, -2, 2)