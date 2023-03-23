import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from flow_vis import flow_to_color

# Create the optical flow color encoding legend
def flow_with_legend(of):
    h,w = of.shape[0:2]
    wsize = np.array([2*max(h,w)+1, 2*max(h,w)+1], dtype=int)
    wheel = np.zeros(wsize, dtype=np.float32)

    xpos = np.array([np.arange(wsize[1]),]*wsize[0], dtype=np.float32)   - wsize[1]/2
    ypos = np.array([np.arange(wsize[0]),]*wsize[1], dtype=np.float32).T - wsize[0]/2

    mvects = np.stack([xpos,-ypos], axis=2)
    modulus = np.sqrt(xpos*xpos + ypos*ypos)
    modulus = modulus / modulus[0,wsize[0]//2]

    mask_wheel = np.zeros(wsize, dtype=np.float32)
    mask_wheel[modulus <=1] = 1
    mask_wheel = np.stack([mask_wheel,mask_wheel],axis=2)

    # Generate the legend image
    of_legend = flow_to_color(mvects*mask_wheel, convert_to_bgr=True)

    # Encode the flow using the color representation
    cc = flow_to_color(of, convert_to_bgr=True)


    plt.figure(figsize=(6, 4))
    G = gridspec.GridSpec(2, 3)
    axes_1 = plt.subplot(G[:, 0:2])
    axes_1.imshow(cc)
    axes_1.set_title('Optical Flow')

    axes_2 = plt.subplot(G[:, 2])
    axes_2.imshow(of_legend, extent=[-wsize[0]/2, wsize[0]/2, wsize[0]/2, -wsize[0]/2])
    axes_2.set_title ('Color code')

    plt.tight_layout()

    plt.show()
