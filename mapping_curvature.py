import numpy as np
import math
def rad_from_points(x1, y1, x2, y2, x3, y3):

    ma = (y2 - y1)/(x2 - x1)
    mb = (y3 - y2)/(x3 - x2)

    xc = (ma*mb*(y1 - y3) + mb*(x1 + x2) - ma*(x2 + x3))/(2*(mb - ma))
    yc = -1/ma*(xc - (x1 + x2)/2) + (y1 + y2)/2

    if ma == mb:
        r = float(np.inf)

    else:
        r = float(np.hypot(xc - x1, yc - y1))

    return(r, xc, yc)


def radius_of_curvature(x_path, y_path,scale):

    r = []
    xcs = []
    ycs = []
    DegreeOfCurv = []

    num_points = len(x_path)
    for i in range(int(scale),int(num_points-scale)):
        # points
        x1 = x_path[i-int(scale)]
        y1 = y_path[i-int(scale)]
        x2 = x_path[i]
        y2 = y_path[i]
        x3 = x_path[i+int(scale)]
        y3 = y_path[i+int(scale)]

        # fit circle
        rad, xc, yc = rad_from_points(x1, y1, x2, y2, x3, y3)

        # get vector normal to path for sign of curvature
        nv1 = np.cross(np.array([x2 - x1, y2 - y1, 0]), np.array([0 ,0, 1]))
        nv2 = np.cross(np.array([x3 - x2, y3 - y2, 0]), np.array([0 ,0, 1]))

        nv = np.average([nv1, nv2], axis = 0)

        # get sign of dot product (and flip for convention that positive curvature is inward)
        align = np.sign(np.dot(nv[0:2], np.array([x2 - xc, y2 - yc])))

        if rad == 0:
            r.append(np.nan)
        else:
            r.append(align * 1./rad)
            
        xcs.append(xc)
        ycs.append(yc)

        # AO_dot_OB = ((x1-xc)*(xc-x3))+((y1-yc)*(yc-y3))
        # AO_mag = np.sqrt((x1-xc)**2+(y1-yc)**2)
        # OB_mag = np.sqrt((xc-x3)**2+(yc-y3)**2)
        # theta = np.arccos(AO_dot_OB/(AO_mag*OB_mag))
        # arcL = 2*np.pi*rad*(theta/360)
        # D_r = np.degrees((180*arcL)/(np.pi*rad))
        # if D_r>180:
        #     D_r = D_r-180

        # DegreeOfCurv.append(align * D_r)

    return(r, xcs, ycs) # DegreeOfCurv)
