import numpy as np
import matplotlib.pyplot as plt

def until_divergence(c, val_bound, iter_bound):
    '''
    z=z^2+c until divergence or not condition
    '''
    z = c #Succession start
    i=0 #Iteration

    while i<iter_bound and abs(z) < val_bound:
        z = z**2 + c
        i+=1

    return i

def plot_fractal(sampling_num, val_bound, iter_bound, start_x, end_x, start_y, end_y):
    img = np.full((sampling_num, sampling_num),0)
    x_samples = np.linspace(start_x, end_x, sampling_num)
    y_samples = np.linspace(start_y, end_y, sampling_num)

    for i in range(sampling_num):
        for j in range(sampling_num):
            img[j][i] = until_divergence(complex(x_samples[i], y_samples[j]), 
                                         val_bound,
                                         iter_bound)

    fig = plt.figure('Mandelbrot fractal', figsize=[8,8])
    plt.imshow(img, extent=[-3,1,-2,2])
    plt.title('Complex plane')
    plt.xlabel('Real')
    plt.ylabel('Img')
    plt.show()
    fig.savefig('fractal.png')


if __name__=='__main__':
    plot_fractal(1000, 5, 30, -3, 1, -2, 2)