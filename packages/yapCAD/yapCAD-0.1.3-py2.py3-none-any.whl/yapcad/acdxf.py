## yapCAD support functions for working with Autodesk's DXF file format
## Created on Fri Oct  9 16:06:08 PDT 2020
## Copyright (c) 2020 Richard W. DeVaul
## Copyright (c) 2020 yapCAD contributors
## All rights reserved
## See licensing terms here: https://github.com/rdevaul/yapCAD/blob/master/LICENSE

from yapcad.geom import *
import math

## eqivalent to autoLISP polar function
## note this function works in radians
def polar(p,ang,r):
    x = math.cos(ang)*r
    y = math.sin(ang)*r
    return add(p,point(x,y))

## equivalent to autoLISP angle function
## note this function returns radians
def angle(p1,p2):
    if vclose(p1,p2):
        raise ValueError('coincident points')
    pp = sub(p2,p1)
    return atan2(pp[1],pp[0])

## utility functions for radian/degree conversions
def rad2deg(theta):
    return theta*360.0/pi2

def deg2rad(theta):
    return theta*pi2/360.0

## function to convert from DXF Polyline "bulge" representation to
## a yapCAD arc.
## Thanks to Lee Mac for autoLISP code examples
## http://www.lee-mac.com/bulgeconversion.html
def bulge2arc(p1,p2,b):
    a = 2.0 * math.atan(b)
    r = dist(p1,p2) / (math.sin(a)*2.0)
    c = polar(p1, ((math.pi/2.0 - a) + angle(p1, p2)),r)
    a1 = rad2deg(angle(c,p1))
    a2 = rad2deg(angle(c,p2))
    if b < 0.0:
        return arc(c,abs(r),a2,a1)
    else:
        return arc(c,abs(r),a1,a2)

## function to convert from a yapCAD arc to a DXF Polyline "bulge"
## representaiton.
## Thanks to Lee Mac for autoLISP code examples
def arc2bulge(ac):
    c = ac[0]
    r= ac[1][0]
    a1=deg2rad(ac[1][1])
    a2=deg2rad(ac[1][2])
    
    b = math.tan(((a2-a1)%pi2)/4.0)

    return [polar(c,a1,r),polar(c,a2,r),b]


## Function to convert a yapCAD poly (point list) to an internal DXF
## polyline representation
def yappoly2acpoly(plist):
    dxfpoly=[]
    for i in range(len(plist)-1):
        p=plist[i]
        dxfpoly.append([p[0],p[1],0,-2])
    p = plist[-1]
    dxfpoly.append([p[0],p[1],0,-2])
    return dxfpoly

## funtion to convert a yapCAD geometry list to a list of DXF
## polylines. Each contiguous sequence of yapCAD lines, arcs, and
## polys will be converted into a DXF polyline.

## If there are elements, such as circles, that aren't convertable to
## a DXF polyline representation, they will be added to a separate
## "nonconvertable" yapCAD geometry list.

## Return value ( dxfpolys , nonconvertable ), where dxfpolys is a
## list of contiguous dxf bulge polyline representations, and
## nonconvertable is a yapCAD geometry list of remainders

def yapgeom2acpoly(glist):
    ## internal function to take a non-zero-length geometry list and
    ## return one or more contiguous geometry lists
    def gl2contig(gl):
        nonconv=[]
        ggl=[]
        cl=[gl[0]]
        ep = sample(cl[0],1.0) # find endpoint of first element
        for i in range(1,len(gl)):
            g = gl[i]
            sp = sample(g,0.0) # find start of current element
            if vclose(sp,ep): # are they close?
                cl.append(g) # yep, append
            else:
                ggl.append(cl) #nope, finish out current list, start
                               #new one
                cl=g
            ep = sample(g,1.0)
        return ggl
    if not isgeomlist(glist):
        return False
    
    ypgls = gl2contig(glist)
    dxfgls = []
    dxfgl = []
    for ypgl in ypgls:
        dxfpoly=[]
        for i in range(1,len(ypgl)):
            if ispoint(gl):
                ## bogus, unfinished function
                return

        return


                
