#!/usr/bin/env python
"""The openpiv.tools module is a collection of utilities and tools.
"""

__licence__ = """
Copyright (C) 2011  www.openpiv.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import glob
import sys
import os.path
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt
# from builtins import range
from imageio import imread as _imread, imsave as _imsave


def display_vector_field(filename, on_img=False, image_name='None', 
                         window_size=32, scaling_factor=1, widim=False, 
                         negative_img=True, ax=None, **kw):
    """ Displays quiver plot of the data stored in the file 
    
    
    Parameters
    ----------
    filename :  string
        the absolute path of the text file

    on_img : Bool, optional
        if True, display the vector field on top of the image provided by 
        image_name

    image_name : string, optional
        path to the image to plot the vector field onto when on_img is True

    window_size : int, optional
        when on_img is True, provide the interrogation window size to fit the 
        background image to the vector field

    scaling_factor : float, optional
        when on_img is True, provide the scaling factor to scale the background
        image to the vector field
    
    widim : bool, optional, default is False
        when widim == True, the y values are flipped, i.e. y = y.max() - y

    negative_img : bool, optional, default is True
        when True, the negative of the image is showed in the background for better readability
        
    Key arguments   : (additional parameters, optional)
        *scale*: [None | float]
        *width*: [None | float]
    
    
    See also:
    ---------
    matplotlib.pyplot.quiver
    
        
    Examples
    --------
    --- only vector field
    >>> openpiv.tools.display_vector_field('./exp1_0000.txt',scale=100, 
                                           width=0.0025) 

    --- vector field on top of image
    >>> openpiv.tools.display_vector_field('./exp1_0000.txt', on_img=True, 
                                          image_name='exp1_001_a.bmp', 
                                          window_size=32, scaling_factor=70, 
                                          scale=100, width=0.0025)
    
    """
    #(Pouya) header line is skipped
    a = np.loadtxt(filename, skiprows=1)
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    if on_img is True:  # plot a background image
        im = imread(image_name)
        #im = negative(im)  # plot negative of the image for more clarity
        # (Pouya) lets provide the option to use original image
        if negative_img is True:
            im = negative(im)
        # imsave('neg.tif', im)
        # im = imread('neg.tif')
        xmax = np.amax(a[:, 0])+window_size/(2*scaling_factor)
        ymax = np.amax(a[:, 1])+window_size/(2*scaling_factor)
        ax.imshow(im, origin='lower', cmap="Greys_r", 
                  extent=[0., xmax, 0., ymax])
        plt.draw()
    
    if widim is True:
        a[:, 1] = a[:, 1].max() - a[:, 1]
        
    invalid = a[:, 4].astype('bool')  # mask
    # (Pouya) Let's show the number of bad vectors on the window title
    fig.canvas.set_window_title(f'Velocity field, {np.count_nonzero(invalid)} bad vectors out of {np.size(invalid)}')
    valid = ~invalid
    ax.quiver(a[invalid, 0], a[invalid, 1], a[invalid, 2], a[invalid, 3],
              color='r', **kw)
    ax.quiver(a[valid, 0], a[valid, 1], a[valid, 2], a[valid, 3], color='b',
              **kw)
#     if on_img is False:
    #ax.invert_yaxis()
    # (Pouya) y axis inversion is done in the pyprocess module no need to do it here

    plt.show()

    return fig, ax


def imread(filename, flatten=0):
    """Read an image file into a numpy array
    using imageio.imread
    
    Parameters
    ----------
    filename :  string
        the absolute path of the image file
    flatten :   bool
        True if the image is RGB color or False (default) if greyscale
        
    Returns
    -------
    frame : np.ndarray
        a numpy array with grey levels
        
        
    Examples
    --------
    
    >>> image = openpiv.tools.imread( 'image.bmp' )
    >>> print image.shape 
        (1280, 1024)
    
    
    """
    im = _imread(filename)
    if np.ndim(im) > 2:
        im = rgb2gray(im)

    return im


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def imsave( filename, arr ):
    """Write an image file from a numpy array
    using imageio.imread
    
    Parameters
    ----------
    filename :  string
        the absolute path of the image file that will be created
    arr : 2d np.ndarray
        a 2d numpy array with grey levels
        
    Example
    --------
    
    >>> image = openpiv.tools.imread( 'image.bmp' )
    >>> image2 = openpiv.tools.negative(image)
    >>> imsave( 'negative-image.tif', image2)
    
    """

    if np.ndim(arr) > 2:
        arr = rgb2gray(arr)

    if np.amin(arr) < 0:
        arr -= arr.min()

    if np.amax(arr) > 255:
        arr /= arr.max()
        arr *= 255

    if filename.endswith('tif'):
        _imsave(filename, arr, format='TIFF')
    else:
        _imsave(filename, arr)


def convert16bitsTIF( filename, save_name):
    img = imread(filename)
    img2 = np.zeros([img.shape[0], img.shape[1]], dtype=np.int32)
    for I in range(img.shape[0]):
        for J in range(img.shape[1]):
            img2[I, J] = img[I, J, 0]
    
    imsave(save_name, img2)


def mark_background(threshold, list_img, filename):
    list_frame = []
    for I in range(len(list_img)):
        list_frame.append(imread(list_img[I]))
    mark = np.zeros(list_frame[0].shape, dtype=np.int32)
    background = np.zeros(list_frame[0].shape, dtype=np.int32)
    for I in range(mark.shape[0]):
        print((" row ", I , " / " , mark.shape[0]))
        for J in range(mark.shape[1]):
            sum1 = 0
            for K in range(len(list_frame)):
                sum1 = sum1 + list_frame[K][I, J]
            if sum1 < threshold*len(list_img):
                mark[I, J] = 0
            else:
                mark[I, J] = 1
            background[I, J] = mark[I, J]*255
    imsave(filename, background)
    print("done with background")
    return background



def mark_background2(list_img, filename):
    list_frame = []
    for I in range(len(list_img)):
        list_frame.append(imread(list_img[I]))
    background = np.zeros(list_frame[0].shape, dtype=np.int32)
    for I in range(background.shape[0]):
        print((" row ", I , " / " , background.shape[0]))
        for J in range(background.shape[1]):
            min_1 = 255
            for K in range(len(list_frame)):
                if min_1 > list_frame[K][I,J]:
                    min_1 = list_frame[K][I,J]
            background[I,J]=min_1
    imsave(filename, background)
    print("done with background")
    return background

def edges(list_img, filename):
    back = mark_background(30, list_img, filename)
    edges = filter.canny(back, sigma=3)
    imsave(filename, edges)

def find_reflexions(list_img, filename):
    background = mark_background2(list_img, filename)
    reflexion = np.zeros(background.shape, dtype=np.int32)
    for I in range(background.shape[0]):
        print((" row ", I, " / ", background.shape[0]))
        for J in range(background.shape[1]):
            if background[I, J] > 253:
                reflexion[I, J] = 255
    imsave(filename, reflexion)
    print("done with reflexions")
    return reflexion
            

def find_boundaries(threshold, list_img1, list_img2, filename, picname):
    f = open(filename, 'w')
    print("mark1..")
    mark1 = mark_background(threshold, list_img1, "mark1.bmp")
    print("[DONE]")
    print((mark1.shape))
    print("mark2..")
    mark2 = mark_background(threshold, list_img2, "mark2.bmp")
    print("[DONE]")
    print("computing boundary")
    print((mark2.shape))
    list_bound = np.zeros(mark1.shape, dtype=np.int32)
    for I in range(list_bound.shape[0]):
        print(( "bound row ", I , " / " , mark1.shape[0]))
        for J in range(list_bound.shape[1]):
            list_bound[I,J]=0
            if mark1[I,J]==0:
                list_bound[I,J]=125
            if I>1 and J>1 and I<list_bound.shape[0]-2 and J< list_bound.shape[1]-2:
                for K in range(5):
                    for L in range(5):
                        if mark1[I-2+K,J-2+L] != mark2[I-2+K,J-2+L]:
                            list_bound[I,J]=255
            else:
                list_bound[I,J]=255
            f.write(str(I)+'\t'+str(J)+'\t'+str(list_bound[I,J])+'\n')
    print('[DONE]')
    f.close()
    imsave(picname, list_bound)
    return list_bound








def save( x, y, u=None, v=None, mask=None, filename=None, variables=None, header='"x", "y", "U", "V", "S2N"', fmt='%8.4f', delimiter='\t' ):
    """Save flow field to an ascii file.
    
    Parameters
    ----------
    x : 2d np.ndarray
        a two dimensional array containing the x coordinates of the 
        interrogation window centers
        
    y : 2d np.ndarray
        a two dimensional array containing the y coordinates of the 
        interrogation window centers
        
    u : 2d np.ndarray
        a two dimensional array containing the u velocity components
        
    v : 2d np.ndarray
        a two dimensional array containing the v velocity components
        
    mask : 2d np.ndarray
        a two dimensional boolen array where elements corresponding to
        invalid vectors are True
        
    filename : string
        the path of the file where to save the flow field

    variables : list of 2d np.ndarray
        a list of variables to be written to the file. default is None
        in which case the default variables: u, v, and mask will be used.
        If specified, the given variabes replace the defaults and a 
        suitable header needs to be given.

    header: string
        a string specifying the variable names for each column in the output.
        
    fmt : string
        a format string. See documentation of numpy.savetxt
        for more details.
    
    delimiter : string
        character separating columns
        
    Examples
    --------
    
    >>> openpiv.tools.save( x, y, u, v, 'field_001.txt', fmt='%6.3f', delimiter='\t')
    
    """
    if variables is None:
        v = [x, y, u, v, mask]
    else:
        v = [x, y]
        for var in variables:
            v.append(var)
    
    # build output array
    out = np.vstack( [m.ravel() for m in v ] )
            
    # save data to file.
    #(Pouya) added a header line for direct import to Tecplot
    headerline=f'VARIABLES = {header}, ZONE I={x.shape[1]}, J={x.shape[0]}'
    np.savetxt( filename, out.T, fmt=fmt, delimiter=delimiter, header=headerline, comments='' )

def display( message ):
    """Display a message to standard output.
    
    Parameters
    ----------
    message : string
        a message to be printed
    
    """
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()

class Multiprocesser():
    def __init__ ( self, data_dir, pattern_a, pattern_b = None  ):
        """A class to handle and process large sets of images.

        This class is responsible of loading image datasets
        and processing them. It has parallelization facilities
        to speed up the computation on multicore machines.
        
        It currently support only image pair obtained from 
        conventional double pulse piv acquisition. Support 
        for continuos time resolved piv acquistion is in the 
        future.
        
        
        Parameters
        ----------
        data_dir : str
            the path where image files are located 
            
        pattern_a : str
            a shell glob patter to match the first 
            frames.
            
        pattern_b : str
            a shell glob patter to match the second
            frames. if None, then the list is sequential, 001.tif, 002.tif 

        Examples
        --------
        >>> multi = openpiv.tools.Multiprocesser( '/home/user/images', 'image_*_a.bmp', 'image_*_b.bmp')
    
        """
        # load lists of images
        self.files_a = sorted( glob.glob( os.path.join( os.path.abspath(data_dir), pattern_a ) ) )
        
        if pattern_b is None:
            self.files_b = self.files_a[1:]
            self.files_a = self.files_a[:-1]
        else:    
            self.files_b = sorted( glob.glob( os.path.join( os.path.abspath(data_dir), pattern_b ) ) )
        
        # number of images
        self.n_files = len(self.files_a)
        
        # check if everything was fine
        if not len(self.files_a) == len(self.files_b):
            raise ValueError('Something failed loading the image file. There should be an equal number of "a" and "b" files.')
            
        if not len(self.files_a):
            raise ValueError('Something failed loading the image file. No images were found. Please check directory and image template name.')

    def run( self, func, n_cpus=1 ):
        """Start to process images.
        
        Parameters
        ----------
        
        func : python function which will be executed for each 
            image pair. See tutorial for more details.
        
        n_cpus : int
            the number of processes to launch in parallel.
            For debugging purposes use n_cpus=1
        
        """

        # create a list of tasks to be executed.
        image_pairs = [ (file_a, file_b, i ) for file_a, file_b, i in zip( self.files_a, self.files_b, range(self.n_files) ) ]
        
        # for debugging purposes always use n_cpus = 1,
        # since it is difficult to debug multiprocessing stuff.
        if n_cpus > 1:
            pool = multiprocessing.Pool( processes = n_cpus )
            res = pool.map( func, image_pairs)
        else:
            for image_pair in image_pairs:
                func( image_pair )
        return res
        
    # (Pouya) calculate background image using multiprocessing
    def find_background( self, n_files, chunk_size, n_cpus):
        """Finds the background of a and b set of images utilizing
        multiprocessing."""

        print('finding background image...')
        file_a = [self.files_a[i:i+chunk_size] for i in range(0,n_files,chunk_size)]
        file_b = [self.files_b[i:i+chunk_size] for i in range(0,n_files,chunk_size)]
        pool = multiprocessing.Pool( processes = n_cpus )
        res = pool.map( find_bg, file_a)
        background_a = find_bg(list_img=res)
        print('- done finding background for image set A')
        res = pool.map( find_bg, file_b)
        background_b = find_bg(list_img=res)
        print('- done finding background for image set B')
        #print(f'number of sets: {len(res)}')
        #print(f'n of images in the last set: {len(file_b[-1])}')

        return background_a, background_b

    # vectorized find_background (better and faster method)
    def find_background2(self, n_files):
        """Finds the background of a and b set of images"""

        print('finding background image...')
        background_a = find_bg2(self.files_a[0:n_files])
        print('- done finding background for image set A')
        background_b = find_bg2(self.files_b[0:n_files])
        print('- done finding background for image set B')

        return background_a, background_b

                

def negative( image):
    """ Return the negative of an image
    
    Parameter
    ----------
    image : 2d np.ndarray of grey levels

    Returns
    -------
    (255-image) : 2d np.ndarray of grey levels

    """
    return (255-image)


def display_windows_sampling( x, y, window_size, skip=0,  method='standard'):
    """ Displays a map of the interrogation points and windows
    
    
    Parameters
    ----------
    x : 2d np.ndarray
        a two dimensional array containing the x coordinates of the 
        interrogation window centers, in pixels.
        
    y : 2d np.ndarray
        a two dimensional array containing the y coordinates of the 
        interrogation window centers, in pixels.

    window_size : the interrogation window size, in pixels
    
    skip : the number of windows to skip on a row during display. 
           Recommended value is 0 or 1 for standard method, can be more for random method
           -1 to not show any window

    method : can be only <standard> (uniform sampling and constant window size)
                         <random> (pick randomly some windows)
    
    Examples
    --------
    
    >>> openpiv.tools.display_windows_sampling(x, y, window_size=32, skip=0, method='standard')

    
    """
    
    fig=plt.figure()
    if skip < 0 or skip +1 > len(x[0])*len(y):
        fig.canvas.set_window_title('interrogation points map')
        plt.scatter(x, y, color='g') #plot interrogation locations
    else:
        nb_windows = len(x[0])*len(y)/(skip+1)
        #standard method --> display uniformly picked windows
        if method == 'standard':
            plt.scatter(x, y, color='g')#plot interrogation locations (green dots)
            fig.canvas.set_window_title('interrogation window map')
            #plot the windows as red squares
            for i in range(len(x[0])):
                for j in range(len(y)):
                    if j%2 == 0:
                        if i%(skip+1) == 0:
                            x1 = x[0][i] - window_size/2
                            y1 = y[j][0] - window_size/2
                            plt.gca().add_patch(pt.Rectangle((x1, y1), window_size, window_size, facecolor='r', alpha=0.5))
                    else:
                        if i%(skip+1) == 1 or skip==0:
                            x1 = x[0][i] - window_size/2
                            y1 = y[j][0] - window_size/2
                            plt.gca().add_patch(pt.Rectangle((x1, y1), window_size, window_size, facecolor='r', alpha=0.5))
        #random method --> display randomly picked windows
        elif method == 'random':
            plt.scatter(x, y, color='g')#plot interrogation locations
            fig.canvas.set_window_title('interrogation window map, showing randomly '+str(nb_windows)+' windows')
            for i in range(nb_windows):
                k=np.random.randint(len(x[0])) #pick a row and column index
                l=np.random.randint(len(y))
                x1 = x[0][k] - window_size/2
                y1 = y[l][0] - window_size/2
                plt.gca().add_patch(pt.Rectangle((x1, y1), window_size, window_size, facecolor='r', alpha=0.5))
        else:
            raise ValueError('method not valid: choose between standard and random')
    plt.draw()
    plt.show()

# (Pouya) added all the functions from this line down
#--------------------------------------------------------------

def read_data(filename, Ncolumn=5):
    """function to read the saved data file and reconstruct the 2D field data
    
    Parameters
    ----------
    filename :  string, path to the file

    Returns
    --------
    x, y, u, v, mask : 2D numpy arrays containing the position and field data
    """
    a = np.loadtxt(filename, skiprows=1)
    nx = int(round((a[-1,0]-a[0,0])/(a[1,0]-a[0,0]) + 1))
    ny = a.shape[0]//nx 
    m = np.zeros((ny, nx, Ncolumn))
    for j in range(Ncolumn):
        for i in range(ny):
            m[i,:,j] = a[i*nx:(i+1)*nx,j].T
    
    return [m[:,:,n] for n in range(Ncolumn)]


def manipulate_field ( x, y, u, v, mask, mode ):
    """tool to flip/rotate flow field according to the mode parameter:
        'flipLR', 'flipUD', 'rotateCW', 'rotateCCW'
    """
    if mode == 'flipUD':
        v = -v
        y = np.flipud(y)
    elif mode == 'flipLR':
        u = -u
        x = np.fliplr(x)
    elif mode == 'rotateCW':
        u, v = v.T, -u.T
        x, y = y.T, np.flipud(x.T)
        mask = mask.T
    elif mode == 'rotateCCW':
        u, v = -v.T, u.T
        x, y = np.fliplr(y.T), x.T
        mask = mask.T
    else:
        raise ValueError('mode value not recognized, choose from available modes: flipLR, flipUD, rotateCW, rotateCCW')

    return x, y, u, v, mask


def create_path(file_name, folders=['Analysis']):
    """creates the file path to the given run counter"""

    name = os.path.basename(file_name)
    name, *_ = name.split('.')
    file_path = os.path.dirname(os.path.dirname(file_name))
    for fold in folders:
        file_path = os.path.join(file_path, fold)

    return os.path.join(file_path, name+'.dat')


def create_directory(directory ,folder='Analysis'):
    """creates the required directories and returns its' path"""

    Folder_path = os.path.join(directory, folder)
    if os.path.isdir(Folder_path)==False:
        os.mkdir(Folder_path)
    return Folder_path

def find_bg(list_file=None, list_img=None):
    """finds the background for image list or file list, similar to mark_background2 function but
    with minor differences in handling the images and image intensities"""
    
    if list_img == None:
        list_img = []
        for imgf in list_file:
            list_img.append(imread(imgf))
    
    background = np.zeros(list_img[0].shape, dtype=np.int32)
    for I in range(background.shape[0]):
        for J in range(background.shape[1]):
            min_1 = list_img[0][I,J]
            for img in list_img:
                if min_1 > img[I,J]:
                    min_1 = img[I,J]
            background[I,J] = min_1
    return background


# vectorized find_bg:
def find_bg2(file_list):
    """finds the background for file list, similar to mark_background2 function but
    vectorized and thus, much faster"""
    
    sample_img = imread(file_list[0])
    IMG = np.zeros((sample_img.shape[0],sample_img.shape[1],len(file_list)), dtype=np.int32)
    for i, fl in enumerate(file_list):
        IMG[:,:,i] = imread(fl)

    return IMG.min(axis=2)