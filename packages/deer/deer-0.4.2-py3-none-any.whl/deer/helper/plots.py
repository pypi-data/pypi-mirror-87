import numpy as np

import matplotlib
matplotlib.use('qt5agg')
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
plt.switch_backend('agg') # For remote servers


VSMALL_SIZE = 6
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=VSMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=VSMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


def plot_abstract_repr(historics,abs_states,tr1,tr2,tr3, height):

    historics=np.array(historics).astype('float32')
    abs_states=np.array(abs_states).astype('float32')
    tr1=np.array(tr1).astype('float32')
    tr2=np.array(tr2).astype('float32')
    
    for i in range(height-1):
        fig = plt.figure(figsize=(6, 3.2))
        
        print (np.array(historics).shape)
        print (np.array(historics))
        ax = fig.add_subplot(351)
        ax.set_title(r'$t$')
        plt.imshow(np.array(historics)[i,0,:,:], vmin=-1, vmax=1)
        print (np.array(historics).dtype)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        
        ax = fig.add_subplot(356)
        #ax.set_title(r'$x_t$')
        plt.imshow(np.array(abs_states)[i,:,:,0], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        ax = fig.add_subplot(3,5,11)
        #ax.set_title(r'$x_t$')
        plt.imshow(np.array(abs_states)[i,:,:,1], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        
        ax = fig.add_subplot(3,5,5)
        ax.set_title(r'$t+1$')
        plt.imshow(np.array(historics)[i+1,0,:,:], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        
        ax = fig.add_subplot(3,5,10)
        #ax.set_title(r'$x_t$')
        plt.imshow(np.array(abs_states)[i+1,:,:,0], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        ax = fig.add_subplot(3,5,15)
        #ax.set_title(r'$x_t$')
        plt.imshow(np.array(abs_states)[i+1,:,:,1], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        
        ax = fig.add_subplot(3,5,7)
        ax.set_title(r'$x_t+\tau_1(x_t)$')
        plt.imshow(np.array(tr1[i])[:,:,0], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        ax = fig.add_subplot(3,5,12)
        plt.imshow(np.array(tr1[i])[:,:,1], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        ax = fig.add_subplot(3,5,8)
        ax.set_title(r'$x_t+\tau_2(x_t, a_t)$')
        plt.imshow(np.array(tr2[i])[:,:,0], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')

        ax = fig.add_subplot(3,5,9)
        ax.set_title(r'$x_t+\tau_3(x_t, a_t)$')
        plt.imshow(np.array(tr3[i])[:,:,0], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')

        
        ax = fig.add_subplot(3,5,13)
        plt.imshow(np.array(tr2[i])[:,:,1], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')

        ax = fig.add_subplot(3,5,14)
        plt.imshow(np.array(tr3[i])[:,:,1], vmin=-1, vmax=1)
        ax.set_aspect('equal')
        
        plt.colorbar(orientation='vertical')
        
        
        plt.subplots_adjust(wspace=0.38, hspace=0.38)
        plt.show()
        plt.savefig('test'+str(i)+'.pdf')
