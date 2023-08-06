__all__ = [
    "stripe_removal",
    "stripe_del",
    "xRemoveSpriesHorizontal",
    "image_flattening",
    "gaussian_flattening",
    "poly_flattening",
    "analyse_morphologique",
    "read_image",
    "Otsu_tresholding",
    "read_plu_topography",
    "fill_gap"
]



def stripe_removal(ima, **kwargs):

    """
    Stripes removal from an image.

    Arguments :
        ima (nparray): image to process
        **kwargs: kwargs["method"] = "wavelet" or "epandage" (default "wavelet")
                  kwargs["mode"] = "mean", "median", "mode", "poly" (default "median")
                  kwargs["order"]  order orde of the smoothing polynomial
                  kwargs["wname"] wname of the wavelet (default db15)
                  kwargs["decNum_h"] order of decimation
                  kwargs["sigma_wl_h"] sigma_wl_h
    Returns:
        iama: corrected image
    """

    if "method" in list(kwargs.keys()):
        method_type = kwargs["method"]
    else:
        method_type = "wavelet"

    if method_type == "epandage":
        try:
            mode = kwargs["mode"]
        except:
            mode = "median"

        if mode == 'poly':
            try:
                order = kwargs["order"]
            except:
                order = 3
            ima = stripe_del(ima, mode, order)
        else:
            ima = stripe_del(ima, mode)

    elif method_type == "wavelet":
        try:
            wname = kwargs["wname"]
        except:
            wname = "db15"

        try:
            decNum_h = kwargs["decNum_h"]
        except:
            decNum_h = 7

        try:
            sigma_wl_h = kwargs["sigma_wl_h"]
        except:
            sigma_wl_h = 3

        ima = xRemoveSpriesHorizontal(ima,decNum_h,wname,sigma_wl_h)

    else:
        raise Exception(f"unknown method:{method_type}")

    return ima




def stripe_del(ima, mode, order=3):
    '''Supress stripe by aligning row using different method
    median: for each row, subtract the row median value from that row
    mean: for each row, subtract the row mean value from that row
    mode: for each row, subtract the mode value from that row
    polynomial: for each row, subtract least square smoothing polynomial from that row

    Arguments
        ima (nparray): image to process
        mode (string): algorith to apply (mean, median, mode, polynomial)
        order (integer): order of the smoothing polynomial
    Returns
        ima (nparray): corrected image
    '''
    # 3rd party import
    import numpy as np
    from scipy import stats
    import pandas as pd

    if mode=='median':
        epandage = np.median(ima,axis=1).reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode=='mean':
        epandage = np.mean(ima,axis=1).reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode == 'mode':
        epandage = stats.mode(ima,axis=1)[0].flatten().reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode == 'poly':
        df = pd.DataFrame(ima)
        imb = []
        for row in df.iterrows():
            coeff = np.polyfit(np.array(row[1].index), np.array(row[1].values), order)
            imb.append(np.array(row[1].values) - np.polyval(coeff, np.array(row[1].index)))
        ima = np.array(imb).reshape(np.shape(ima))

    return ima

def xRemoveSpriesHorizontal(ima,decNum,wname,sigma):

    '''
    Horizontal stripes supression using the folowing algorithm
    [1] https://www.osapublishing.org/oe/abstract.cfm?uri=oe-17-10-8567

    Arguments:
        ima (ndarray) : image to process
        decNum (integer) : decimation number
        wname (string) : wavelet type
        sigma (float): damping factor (see [1])
    Returns:
        imc (ndarray) : filtered image

    '''
    # 3rd party import
    import numpy.matlib
    import numpy as np
    import pywt

    # wavelet decomposition
    coeffs = pywt.wavedec2(ima, wname, level=decNum)
    ima=coeffs[0]
    cH=[coeffs[I][0] for I in range(1,decNum+1)]
    cV=[coeffs[I][1] for I in range(1,decNum+1)]
    cD=[coeffs[I][2] for I in range(1,decNum+1)]

    # FFT transform of horizontal frequency bands
    cHf=[]
    for cH_ in cH:
        fcH=np.fft.fftshift(np.fft.fft(cH_))
        [my,mx]=np.shape(fcH)

        # damping of vertical strips information
        m=mx
        damp=1-np.exp(-np.arange(np.floor(-m/2),np.floor(-m/2)+m)*np.arange(np.floor(-m/2),np.floor(-m/2)+m)/(2*np.power(sigma,2)))
        fcH=fcH*(np.matlib.repmat(damp,my,1))
        # inverse FFT
        cHf.append(np.fft.ifft(np.fft.ifftshift(fcH)))


    coefft=[ima]
    for ii in range(decNum):
        coefft.append((cHf[ii],cV[ii],cD[ii]))

    imc=pywt.waverec2(coefft, wname)
    imc = np.real(imc)
    imc = imc - imc.min()
    return imc

def image_flattening(ima, **kwargs):

    """
    Stripes removal from an image.

    Arguments :
        ima (nparray): image to process
        **kwargs: kwargs["method_flat"]
                  kwargs["sigma"]
                  kwargs["kx"]
                  kwargs["ky"]


    Returns:
        ima (nparray): corrected image
    """
    if "method_flat" in list(kwargs.keys()):
        method_type = kwargs["method_flat"]
    else:
        method_type = "gauss"

    if method_type == "gauss":
        try:
            sigma = kwargs["sigma"]
        except:
            sigma = 3
        ima = gaussian_flattening(ima, sigma)

    elif method_type == "poly":
        try:
            kx = kwargs["kx"]
        except:
            sigma = 2

        try:
            ky = kwargs["ky"]
        except:
            ky = 2
        ima = poly_flattening(ima, kx, ky, order=None)

    else:
        raise Exception(f"unknown method:{method_type}")

    return ima



def gaussian_flattening(im, sigma):

    '''
    Image flattening
    '''
    # 3rd party imports
    from scipy.ndimage import gaussian_filter

    im_flat = im/gaussian_filter(im, sigma=sigma)
    return im_flat

def poly_flattening(im, kx, ky, order=None):

    # 3rd party imports
    import numpy as np

    ny,nx = np.shape(im)
    x = np.arange(0,nx,1)/nx
    y = np.arange(0,ny,1)/ny

    coeff = polyfit2d(x,y, im, kx=kx, ky=ky, order = order)
    im_background = poly2Dreco(x,y,coeff)
    im_flatten = im - im_background

    return im_flatten

def polyfit2d(x, y, z, kx, ky, order):

    '''
    Two dimensional polynomial fitting by least squares.
    Fits the functional form f(x,y) = z.
    credit : https://stackoverflow.com/questions/33964913/equivalent-of-polyfit-for-a-2d-polynomial-in-python


    Arguments
        x, y (array-like, 1d) : x and y coordinates.
        z (np.ndarray, 2d) : Surface to fit.
        kx, ky (int, default is 3) : Polynomial order in x and y, respectively.
        order (int or None, default is None) :
            If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
            If int, coefficients up to a maximum of kx+ky <= order are considered.

    Returns
        coeff (np.ndarray, 2d): polynomial coefficients c(i,j) y**i x**j

    '''

    # 3rd party imports
    import numpy as np

    x, y = np.meshgrid(x, y)
    coeffs = np.ones((kx+1, ky+1))
    a = np.zeros((coeffs.size, x.size))

    for index, (i,j) in enumerate(np.ndindex(coeffs.shape)):
        # do not include powers greater than order
        if order is not None and i + j > order:
            arr = np.zeros_like(x)
        else:
            arr = coeffs[i, j] * x**i * y**j
        a[index] = arr.ravel()

    coeff, _, _, _ = np.linalg.lstsq(a.T, np.ravel(z), rcond=None)
    return coeff.reshape(kx+1,ky+1)

def poly2Dreco(x,y, c):
    import numpy as np
    return np.polynomial.polynomial.polygrid2d(x,y,c).T


def analyse_morphologique(img):

    '''
    find the features in the image
    Arguments:
        img (ndarray): image to analyze
        path (string): absolute path of the excel file containing the dataframe df (see returns)
                       optional (default=None no storage)
    Returns:
        df (dataframe): index|'x'|'long_x'| 'y'|'long_y'| 'size'
    '''

    import numpy as np
    from scipy.ndimage.measurements import label
    import pandas as pd

    labeled_array, num_features = label(img,[[0,1,0], [1,1,1], [0,1,0]])

    morpho = {}

    for i in range(1,np.max(labeled_array)+1):
        x,y = np.where(labeled_array==i)
        morpho[i] = [ int(np.mean(x)), max(x)-min(x)+1, int(np.mean(y)), max(y)-min(y)+1, np.sum(labeled_array==i)]

    df = pd.DataFrame.from_dict(morpho, orient='index',
                           columns=['x','long_x', 'y','long_y', 'size'])

    return df

def Otsu_tresholding(im,Ostu_corr=1):
    '''
    Image thresholding using the Otsu's method
    https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4310076
    Arguments:
        im (ndarray) : image
        Ostu_corr (float) : division of the Otsu threshold by Otsu_corr

    Returns:
        im_bin (ndarray) : binarized image
    '''

    from skimage import filters
    import numpy as np

    thresh_otsu = filters.threshold_otsu(convert(im)) # détermination du seuil optimum selon Otsu
    im_bin = np.where((convert(im) < thresh_otsu/Ostu_corr), 1, 0)
    return im_bin

def top_hat_flattening(im,struct_elmt_size):
    ''' mise à plat de l image en appliquant une transformation top hat à chacune des lignes de l image im'''
    from scipy.ndimage import white_tophat
    (mx,my)=np.shape(im)
    Ip=[]
    for ii in range(mx):
        Ip.append(white_tophat(im[ii,:], None, np.repeat([1], struct_elmt_size)))
    Ip=np.array(Ip).reshape((mx,my))
    Ip=255*Ip/np.max(np.max(Ip))

    return Ip


def effective_erea(df,n_row, n_col):
    surf = lambda size_min: 100*df.query("size > @size_min")["size"].sum()/(n_row* n_col)
    eff_erea = [surf(size_min) for size_min in range(max(df["size"])+1)]
    return eff_erea

def convert(data):
    import numpy as np
    data = data / data.max() #normalizes data in range 0 - 255
    data = 255 * data
    return data.astype(np.uint8)

def read_image(file):
    import numpy as np
    import matplotlib.pyplot as plt

    img = plt.imread(file, 1)
    im_brute=img[:,:,0]
    n_row, n_col,_ = np.shape(img)
    return im_brute,n_row, n_col

def read_plu_topography(file):
    '''
    https://sensofar.app.box.com/s/k3k9pboznc0shhjgzr5f7s4uzmeeessy

    Arguments:
        file (string): path+name of the .plu file
    Returns:
        N (integer): number of rows
        M (integer): number of columns
        confocal_img (NxM nparray of floats): confocal image z in µm
        rgb (NxMx3 array of int) : rgb image of the plain view image

    '''
    import struct
    import numpy as np

    data = open(file, "rb").read()

    # Area 1
    fmt = "500c"
    date = struct.unpack(fmt, data[:struct.calcsize(fmt)] )

    # Area 2
    pos = struct.calcsize(fmt)
    fmt = "2i"
    (N,M) = struct.unpack(fmt, data[pos:pos+ struct.calcsize(fmt)] )

    pos += struct.calcsize(fmt)
    fmt = str(M*N)+'f'
    confocal_img = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])
    confocal_img = np.array(confocal_img)
    confocal_img = confocal_img.reshape((N,M))

    pos += struct.calcsize(fmt)
    fmt = '2f'
    (a,b) = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])

    pos += struct.calcsize(fmt)
    fmt = str(M*N)+'B'
    y = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])
    B = np.array(y) .reshape((N,M))

    pos += struct.calcsize(fmt)
    fmt = str(M*N)+'B'
    y = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])
    G = np.array(y) .reshape((N,M))

    pos += struct.calcsize(fmt)
    fmt = str(M*N)+'B'
    y = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])
    R = np.array(y) .reshape((N,M))
    rgb=np.array(list(zip(R.flatten(),G.flatten(),B.flatten()))).reshape((N,M,3))

    # Area 3 not used
    pos += struct.calcsize(fmt)
    print(pos,len(data))
    fmt = 'i'
    offset = struct.unpack(fmt, data[pos:pos+struct.calcsize(fmt)])

    pos += offset[0]

    # area 4 work in progress (missing information)
    return N, M, confocal_img, rgb, date

def fill_gap(data):
    '''
    fill the missing value (1000001) of the confocal image using a linear interpolation method

    Arguments:
        data (2D nparray of floats): confocal image with missing values
    Returns:
        data (2D nparray of floats): confocal image with interpolated values
    '''
    import numpy as np
    shape = data.shape
    data = data.flatten()
    mask = np.array([True if x==1000001 else False for x in data ])
    data[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), data[~mask])
    return data.reshape(shape)

