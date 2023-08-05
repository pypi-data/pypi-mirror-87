import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import datetime
import os
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.image as mpimg
from glmtools.io.glm import GLMDataset

def GetRadius(area):
    return np.sqrt(area/np.pi) / 110

def MakeBigGraph(dataset,buffer=0,areaofInterest=None):
    '''Dataset is an xarray that contains GLM data
       Buffer is how much extra area around the data do you want to show
       Area of interest will draw a rectangle around it on the big map, as well as draw a smaller map after zoomed into that section'''
    # Shown as yellow circles
    y0 = dataset.flash_lat.values
    x0 = dataset.flash_lon.values
    a0 = dataset.flash_energy.values
    a0 = (a0 - np.min(a0))/np.ptp(a0)
    a0 *= .35

    # Shown as orange circles
    y1 = dataset.event_lat.values
    x1 = dataset.event_lon.values

    # Shown as blue dots
    y2 = dataset.group_lat.values
    x2 = dataset.group_lon.values
    
    img = np.asarray(mpimg.imread('./yel.png'))
    minLong_, minLat_, maxLong_, maxLat_ = min(x0), min(y0), max(x0), max(y0)
    fig, ax = plt.subplots(figsize=(30,15))

    # Map with scaled size
    m = Basemap(llcrnrlon=minLong_-buffer, llcrnrlat=minLat_-buffer,urcrnrlon=maxLong_+buffer,urcrnrlat=maxLat_+buffer,lon_0=0,lat_0=0)

    #Map with full size
    #m = Basemap(llcrnrlon=-180, llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,lon_0=0,lat_0=0)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
    m.drawcoastlines(linewidth=0.1, color="white")

    for x in range(len(a0)):
        #m.scatter(x0[x],y0[x],zorder=3,c='blue',marker='D')
        radius = GetRadius(dataset.flash_area.values[x])
        #ax.add_artist(Circle((x0[x],y0[x]),radius/5,alpha=a0[x],color='yellow'))
        extent=[x0[x] - radius, x0[x] + radius, y0[x] - radius, y0[x] + radius]
        aimg = img.copy()
        # Change back to alpha=a0[x]
        plt.imshow(aimg,extent=extent,zorder=4,alpha=1)

    plt.xticks(np.arange(minLong_-buffer,maxLong_+buffer,step=5))
    plt.yticks(np.arange(minLat_-buffer,maxLat_+buffer,step=5))
    m.scatter(x1,y1,zorder=5,s=10)
    m.scatter(x2,y2,zorder=5,s=3)
    
    if(areaofInterest != None):
        Left = areaofInterest[0]
        Right = areaofInterest[1]
        Top = areaofInterest[2]
        Bot = areaofInterest[3]
        width = np.abs(Right - Left)
        height = np.abs(Top - Bot)
        rectangle = patches.Rectangle((Left,Bot ),width,height,linewidth=1,edgecolor='r',facecolor='none')
        rectangle.zorder = 5
        ax.add_patch(rectangle)
    plt.title(label=str(dataset.product_time.values))
    plt.show()
    
    if(areaofInterest != None):
        maxLong_ = Right
        minLong_ = Left
        minLat_ = Bot
        maxLat_ = Top
        fig, ax = plt.subplots(figsize=(30,15))

        # Map with scaled size
        m = Basemap(llcrnrlon=minLong_, llcrnrlat=minLat_,urcrnrlon=maxLong_,urcrnrlat=maxLat_,lon_0=0,lat_0=0)

        #Map with full size
        #m = Basemap(llcrnrlon=-180, llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,lon_0=0,lat_0=0)
        m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
        m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
        m.drawcoastlines(linewidth=0.1, color="white")

        for x in range(len(a0)):
            #m.scatter(x0[x],y0[x],zorder=3,c='blue',marker='D')
            radius = GetRadius(dataset.flash_area.values[x])
            #ax.add_artist(Circle((x0[x],y0[x]),radius/5,alpha=a0[x],color='yellow'))
            extent=[x0[x] - radius, x0[x] + radius, y0[x] - radius, y0[x] + radius]
            aimg = img.copy()
            plt.imshow(aimg,extent=extent,zorder=4,alpha=a0[x])

        plt.xticks(np.arange(minLong_,maxLong_,step=5))
        plt.yticks(np.arange(minLat_,maxLat_,step=5))
        m.scatter(x1,y1,zorder=5,s=10)
        m.scatter(x2,y2,zorder=5,s=3)
        plt.title(label=str(dataset.product_time.values))
        plt.show()