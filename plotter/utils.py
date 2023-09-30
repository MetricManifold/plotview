import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.contrib.staticfiles import finders
from django.apps import apps


from .models import  Folder

def get_current_app_name():
    # Get the app's configuration for the current module
    current_app_config = apps.get_containing_app_config(__name__)
    
    # Get the app's name from the configuration
    app_name = current_app_config.name
    
    return app_name

def get_data_file_name(folder):
    data_name = "data_0.txt"
    file_name = os.path.join(folder.directory.path, folder.name, "data", data_name)
    return file_name

def contains_data_file(folder):
    return os.path.exists(get_data_file_name(folder))

def read_data(folder):
    
    file_name = get_data_file_name(folder)
    data_raw = np.loadtxt(file_name)
    frame_starts, = np.where(data_raw[:,0] == 0)

    if (len(frame_starts) > 1):
        delta = frame_starts[1] - frame_starts[0]
    else:
        delta = len(data_raw)
    frames = frame_starts.size

    x = data_raw[0, 1:]
    y = data_raw[1:delta, 0]
    #X, Y = np.meshgrid(x, y)

    picked_frame = frames - 1
    data = data_raw[(picked_frame) * delta + 1:(picked_frame + 1) * delta, 1:]
    return (x, y, data)

def plot_data(folder):
    
    if (contains_data_file(folder)):
        x, y, data = read_data(folder)
        X, Y = np.meshgrid(x, y)

        fig, ax = plt.subplots(figsize=(4,4))
        ax.set_xlim([x[0], x[-1]])
        ax.set_ylim([y[0], y[-1]])
        #problem in cell 127 of 03.15

        cell_color = "#7dabf5"
        levels=[0.25, 2]
        extent=[x[0], x[-1], y[0], y[-1]]

        im0 = ax.contourf(data, extent=extent, colors=[cell_color], levels=levels)
        im1 = ax.contour(data, extent=extent, colors=["black"], levels=levels)
        ax.axis('off')

        #for p in points[55:56]:
        #    xp, yp = zip(*p)
        #    #ax.scatter(xp[0:1] % delta, yp[0:1] % delta)
        #        #np.max([x0 for x0 in [xp[picked_frame]]]) % 1600, \
        #        #np.max([y0 for y0 in [yp[picked_frame]]]) % 1600)

        #fig.savefig('plot_cells.svg', format='svg', bbox_inches='tight')
        
        app_name = get_current_app_name()
        static_dir = finders.find(app_name)
        picture_name = folder.name + '.png'
        picture_path = picture_path = os.path.join(static_dir, "images", picture_name)
        fig.savefig(picture_path, format='png', bbox_inches='tight')
        folder.picture = os.path.join(app_name, "images", picture_name)
        folder.save()
