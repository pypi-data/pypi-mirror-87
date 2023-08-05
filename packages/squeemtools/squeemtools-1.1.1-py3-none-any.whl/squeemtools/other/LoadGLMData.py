import numpy as np
import xarray as xr
import os
import shutil
import pandas as pd
from glmtools.io.glm import GLMDataset

def LoadRecords(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            key, val = line.split(":")
            key = pd.to_datetime(key)
            d[key] = val
    return d

def FindData(date,records):
    date = pd.to_datetime(date)
    try:
        baseFolder = pd.to_datetime(f'{date.year}/{date.month}/{date.day}')
        folder = records[baseFolder]
        file = os.listdir(f'./NCPython/NCPython/{folder}/{date.hour}')[int((date.minute * 60 + date.second) / 20) - 1]
        return f'./NCPython/NCPython/{folder}/{date.hour}/{file}'
    except KeyError:
        print("Wasn't found in records, might have to download")

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def ConvToCSV(input,output=None):
    '''input is the netdcf4 file you would like to turn into a csv
       output is the filename you would like to give it (without .csv)
       if output is none, it will use the date of the netcdf4 file
       returns the name of the file'''
    glm = GLMDataset(input)
    df = pd.DataFrame([glm.dataset.event_id.values,glm.dataset.event_time_offset.values,glm.dataset.event_lat.values,glm.dataset.event_lon.values,glm.dataset.event_energy.values]).T
    if output == None:
        output = str(glm.dataset.product_time.values).replace(':','-').replace('.','-')
    df.columns = ['EventID','EventTime','Lat','Lon','Energy']
    grp = pd.DataFrame([glm.dataset.group_id.values, glm.dataset.group_time_offset.values, glm.dataset.group_lat.values, glm.dataset.group_lat.values, glm.dataset.group_energy.values, glm.dataset.group_area.values]).T
    grp.columns = ['GroupID','GroupTime','Lat','Lon','Energy','GroupArea']
    ds = glm.dataset.flash_time_offset_of_last_event.values - glm.dataset.flash_time_offset_of_first_event.values
    flsh = pd.DataFrame([glm.dataset.flash_id.values, glm.dataset.flash_time_offset_of_first_event.values,glm.dataset.flash_lat.values,glm.dataset.flash_lon.values,glm.dataset.flash_energy.values,glm.dataset.flash_area.values, ds.astype(int)]).T
    flsh.columns = ['FlashID','FlashTime','Lat','Lon','Energy','FlashArea','Duration_ns']
    f1 = './temp1.csv'
    f2 = './temp2.csv'
    f3 = './temp3.csv'
    files = [f1,f2,f3]
    df.to_csv(f1)
    grp.to_csv(f2)
    flsh.to_csv(f3)

    with open('{}.csv'.format(output),'wb') as wfd:
        for f in files:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    line_prepender('{}.csv'.format(output), '{},{},{}'.format(int(glm.dataset.event_count.values),int(glm.dataset.group_count.values),int(glm.dataset.flash_count.values)))
    for f in files:
        os.remove(f)
    return output + '.csv'

def CSVtoDFs(filename):
    '''Reads in a .csv created by CONVToCSV and returns 3 dataframes; events, groups, flashes'''
    # Get the number of rows per group
    file = open(filename,'r')
    lst = file.readline().rstrip().split(',')
    numEvnts, numGrps, numFlshs = np.array(lst).astype(int)[0], np.array(lst).astype(int)[1], np.array(lst).astype(int)[2]
    file.close()

    ents = pd.read_csv(filename,skiprows=0,nrows=numEvnts,header=1,index_col=0,low_memory=False)
    grps = pd.read_csv(filename,skiprows=numEvnts + 1,nrows=numGrps,header=1,index_col=0,low_memory=False)
    flshs = pd.read_csv(filename,skiprows=numEvnts + numGrps + 2,nrows=numFlshs,header=1,index_col=0,low_memory=False)
    return ents,grps,flshs

def FolderToCSV(path,output=None):
    '''Takes a folder and converts the contents (netcd4 GLM data) into a csv that can be read with CSVtoDFS.
       output is a filename you want to give it, otherwise it will generate a filename.'''
    flshs = pd.DataFrame()
    grps = pd.DataFrame()
    evnts = pd.DataFrame()
    for file in os.listdir(path):
        glm = GLMDataset('{}/{}'.format(path,file)).dataset

        if output == None:
            output = str(glm.product_time.values).replace(':','-').replace('.','-')

        ds = glm.flash_time_offset_of_last_event.values - glm.flash_time_offset_of_first_event.values
        flsh = pd.DataFrame([glm.flash_id.values, glm.flash_time_offset_of_first_event.values,glm.flash_lat.values,glm.flash_lon.values,glm.flash_energy.values,glm.flash_area.values, ds.astype(int)]).T
        flsh.columns = ['FlashID','FlashTime','Lat','Lon','Energy','FlashArea','Duration_ns']

        grp = pd.DataFrame([glm.group_id.values, glm.group_time_offset.values, glm.group_lat.values, glm.group_lat.values, glm.group_energy.values, glm.group_area.values]).T
        grp.columns = ['GroupID','GroupTime','Lat','Lon','Energy','GroupArea']

        evnt = pd.DataFrame([glm.event_id.values,glm.event_time_offset.values,glm.event_lat.values,glm.event_lon.values,glm.event_energy.values]).T
        evnt.columns = ['EventID','EventTime','Lat','Lon','Energy']

        flshs = flshs.append(flsh)
        grps = grps.append(grp)
        evnts = evnts.append(evnt)

    f1 = path + 'temp1.csv'
    f2 = path + 'temp2.csv'
    f3 = path + 'temp3.csv'
    files = [f1,f2,f3]
    evnts.to_csv(f1)
    grps.to_csv(f2)
    flshs.to_csv(f3)

    with open(path + '../{}.csv'.format(output),'wb') as wfd:
        for f in files:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    line_prepender('../{}.csv'.format(output), '{},{},{}'.format(int(len(evnts)),int(len(grps)),int(len(flshs))))
    for f in files:
        os.remove(f)
    return output + '.csv'
