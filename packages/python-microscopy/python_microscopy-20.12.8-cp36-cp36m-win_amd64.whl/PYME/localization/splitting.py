import numpy as np
from PYME.IO.MetaDataHandler import get_camera_roi_origin


def _bdsClip(x, w, x0, iw):
    x -= x0
    if (x < 0):
        w += x
        x = 0
    if ((x + w) > iw):
        w -= (x + w) - iw
    
    return x, w

def get_splitter_rois(md, data_shape):
    x0, y0 = get_camera_roi_origin(md)
    
    if 'Splitter.Channel0ROI' in md.getEntryNames():
        xg, yg, wg, hg = md['Splitter.Channel0ROI']
        xr, yr, wr, hr = md['Splitter.Channel1ROI']
        #print 'Have splitter ROIs'
    else:
        xg = 0
        yg = 0
        wg = data_shape[0]
        hg = data_shape[1] / 2
        
        xr = 0
        yr = hg
        wr = data_shape[0]
        hr = data_shape[1] / 2
     
    #print yr, hr
    
    xg, wg = _bdsClip(xg, wg, x0, data_shape[0])
    xr, wr = _bdsClip(xr, wr, x0, data_shape[0])
    yg, hg = _bdsClip(yg, hg, y0, data_shape[1])
    yr, hr = _bdsClip(yr, hr, y0, data_shape[1])
    
    w = min(wg, wr)
    h = min(hg, hr)
    
    #print yg, hg, yr, hr
    
    if ('Splitter.Flip' in md.getEntryNames() and not md.getEntry('Splitter.Flip')):
        step = 1
        return (slice(xg, xg + w, 1), slice(xr, xr + w, 1), slice(yg, yg + h, 1), slice(yr, yr + h, step))
    else:
        step = -1
        return (slice(xg, xg + w, 1), slice(xr, xr + w, 1), slice(yg + hg-h, yg + hg, 1), slice(yr + h, yr - 1, step))

def map_splitter_coords(md, data_shape, x, y):
    vx, vy, _ = md.voxelsize_nm

    x0, y0 = get_camera_roi_origin(md)

    if False: #'Splitter.Channel0ROI' in md.getEntryNames():
        xg, yg, wg, hg = md['Splitter.Channel0ROI']
        xr, yr, wr, hr = md['Splitter.Channel1ROI']
    
        #w2 = w - x0
        #h2 = h - y0
    else:
        xg, yg, wg, hg = 0, 0, data_shape[0], data_shape[1]
        xr, yr, wr, hr = wg, hg, wg, hg

    #xg, wg = _bdsClip(xg, wg, x0, data_shape[0])
    #xr, wr = _bdsClip(xr, wr, x0, data_shape[0])
    #yg, hg = _bdsClip(yg, hg, y0, data_shape[1])
    #yr, hr = _bdsClip(yr, hr, y0, data_shape[1])

    w = min(wg, wr)
    h = min(hg, hr)

    ch1 = (x >= xr) & (y >= yr)

    xn = x - ch1 * xr
    yn = y - ch1 * yr

    if md.get('Splitter.Flip', True): #not (('Splitter.Flip' in md.getEntryNames() and not md.getEntry('Splitter.Flip'))):
        #yn = y - ch1*yr
        yn += ch1 * (h - 2 * yn)

    #chromatic shift
    if 'chroma.dx' in md.getEntryNames():
        dx = md['chroma.dx'].ev((xn + x0) * vx, (yn + y0) * vy) / vx
        dy = md['chroma.dy'].ev((xn + x0) * vy, (yn + y0) * vy) / vy
    
        xn += dx * ch1
        yn += dy * ch1

    return np.clip(xn, 0, w - 1), np.clip(yn, 0, h - 1)

def map_splitter_coords_(x, y, xslices, yslices, flip=True):
    xo = np.zeros_like(x)
    yo = np.zeros_like(y)
    for i in range(len(xslices)):
        x0 = min(xslices[i].start, xslices[i].stop)
        x1 = max(xslices[i].start, xslices[i].stop)
        y0 = min(yslices[i].start, yslices[i].stop)
        y1 = max(yslices[i].start, yslices[i].stop)
        
        msk = (x > x0) & (x < x1) & (y > y0) & (y < y1)
        
        xo += msk*(x-x0)
        
        if flip and (i > 0):
            yo += msk*(y1 - y)
        else:
            yo += msk * (y - y0)
            
    return xo, yo


def remap_splitter_coords_(x, y, xslices, yslices, quadrant = 1, flip=True):
    #xo = np.zeros_like(x)
    #yo = np.zeros_like(y)
    i = quadrant
    x0 = min(xslices[i].start, xslices[i].stop)
    #x1 = max(xslices[i].start, xslices[i].end)
    y0 = min(yslices[i].start, yslices[i].stop)
    y1 = max(yslices[i].start, yslices[i].stop)
        
    xo = (x + x0)
        
    if flip and (i > 0):
        yo = (y1 - y)
    else:
        yo = y + y0
    
    return xo, yo

def remap_splitter_coords(md, data_shape, x, y):
    vx, vy, _ = md.voxelsize_nm

    x0, y0 = get_camera_roi_origin(md)

    if False: #'Splitter.Channel0ROI' in md.getEntryNames():
        xg, yg, w, h = md['Splitter.Channel0ROI']
        xr, yr, w, h = md['Splitter.Channel1ROI']
    else:
        xg, yg, w, h = 0, 0, data_shape[0], data_shape[1]
        xr, yr = w, h

    xn = x + (xr - xg)
    yn = y + (yr - yg)

    if md.get('Splitter.Flip', True):#not (('Splitter.Flip' in md.getEntryNames() and not md.getEntry('Splitter.Flip'))):
        yn = (h - y0 - y) + yr - yg

    #chromatic shift
    if 'chroma.dx' in md.getEntryNames():
        dx = md['chroma.dx'].ev((x + x0) * vx, (y + y0) * vy) / vx
        dy = md['chroma.dy'].ev((x + x0) * vx, (y + y0) * vy) / vy
    
        xn -= dx
        yn -= dy

    return xn, yn

def split_image(md, img):
    xgs, xrs, ygs, yrs = get_splitter_rois(md, img.shape)
    g = img[xgs, ygs]
    r = img[xrs, yrs]

    # print xgs, xrs, ygs, yrs, g.shape, r.shape

    return np.concatenate((g.reshape(g.shape[0], -1, 1), r.reshape(g.shape[0], -1, 1)), 2)

def get_shifts(md, data_shape, x, y):
    x = round(x)
    y = round(y)

    # pixel size in nm
    vx, vy, _ = md.voxelsize_nm

    # position in nm from camera origin
    roi_x0, roi_y0 = get_camera_roi_origin(md)
    x_ = (x + roi_x0) * vx
    y_ = (y + roi_y0) * vy

    # look up shifts
    if not md.getOrDefault('Analysis.FitShifts', False):
        DeltaX = md.chroma.dx.ev(x_, y_)
        DeltaY = md.chroma.dy.ev(x_, y_)
    else:
        DeltaX = 0
        DeltaY = 0

    # find shift in whole pixels
    dxp = int(DeltaX / vx)
    dyp = int(DeltaY / vy)

    return DeltaX, DeltaY, dxp, dxy