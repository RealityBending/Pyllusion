import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PIL
import neurokit as nk

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )

    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a np array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return PIL.Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )



def merge_images(img1, img2):

    img_final = img1.copy()
    for i in range(img1.size[0]):
      for j in range(img1.size[1]):

        p1 = img1.getpixel((j,i))
        p2 = img2.getpixel((j,i))
        p = (max(p1[0],p2[0]), max(p1[1],p2[1]), max(p1[2],p2[2]) )
        img_final.putpixel((j,i), p)

    return(img_final)






def create_image_blobs(figsize=(10, 10), n=2500, blobsize=1, blur_radius=2, background="black"):

    if background is "black":
        fig = plt.figure(figsize=figsize, facecolor="black", edgecolor="black")
    else:
        fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    plt.axis('off')
    plt.tight_layout()


    for i in range(n):
        x = np.random.uniform(0, 1)
        y = np.random.uniform(0, 1)
    #    size = np.random.uniform(0, 0.01)
        if background is "black":
            circle = plt.Circle((x, y), blobsize/100, color='white')
        else:
            circle = plt.Circle((x, y), blobsize/100, color='black')
        ax.add_artist(circle)

    img = fig2img ( fig )
    img = img.filter(PIL.ImageFilter.GaussianBlur(radius=blur_radius))
    img = img.convert("RGBA")
    return(img)







# Array

#img1_array = np.array(img1) # im2arr.shape: height x width x channel
#img2_array = np.array(img2) # im2arr.shape: height x width x channel
#
#img_array = img1_array * img2_array
#v_min = img_array.min(axis=(0, 1, 2), keepdims=True)
#v_max = img_array.max(axis=(0, 1, 2), keepdims=True)
#img_array = (img_array - v_min)/(v_max - v_min)
#img = PIL.Image.fromarray(img_array)
#
#img.show()

