import matplotlib
matplotlib.use('qt5agg')
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
plt.switch_backend('agg') # For remote servers



SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title




for i in range(2):
    fig = plt.figure(figsize=(6, 3.2))
    
    ax = fig.add_subplot(341)
    ax.set_title(r'$t$')
    plt.imshow(np.array(historics)[i,0,:,:])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    
    ax = fig.add_subplot(345)
    ax.set_title(r'$x_t$')
    plt.imshow(np.array(abs_states)[i,:,:,0])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    ax = fig.add_subplot(349)
    ax.set_title(r'$x_t$')
    plt.imshow(np.array(abs_states)[i,:,:,1])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    
    ax = fig.add_subplot(344)
    ax.set_title(r'$t+1$')
    plt.imshow(np.array(historics)[i+1,0,:,:])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    
    ax = fig.add_subplot(348)
    ax.set_title(r'$x_t$')
    plt.imshow(np.array(abs_states)[i+1,:,:,0])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    ax = fig.add_subplot(3,4,12)
    ax.set_title(r'$x_t$')
    plt.imshow(np.array(abs_states)[i+1,:,:,1])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    
    ax = fig.add_subplot(346)
    ax.set_title(r'$x_t+\tau_1(x_t)$')
    plt.imshow(np.array(tr1[i])[:,:,0])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    ax = fig.add_subplot(3,4,10)
     ax.set_title('colorMap')
    plt.imshow(np.array(tr1[i])[:,:,1])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    ax = fig.add_subplot(347)
    ax.set_title(r'$x_t+\tau_2(x_t, a_t)$')
    plt.imshow(np.array(tr2[i])[:,:,0])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    ax = fig.add_subplot(3,4,11)
     ax.set_title('colorMap')
    plt.imshow(np.array(tr2[i])[:,:,1])
    plt.gca().invert_yaxis()
    ax.set_aspect('equal')
    
    plt.colorbar(orientation='vertical')
    
    
    plt.subplots_adjust(wspace=0.38, hspace=0.38)
    plt.show()
    plt.savefig('test'+str(i)+'.pdf')
