#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:38:15 2020

@author: vbokharaie
"""


#%%
def plot_trial_cluster_seq(centroid_to_plot,
                           labels_to_plot,
                           my_title,
                           dir_save='./clusters_one_trial',
                           Cluster_num=2,):
    """
    Plot a heatmap of cluster labels for each trial in a sequence of trials.

    Parameters
    ----------
    centroid_to_plot : NumPy array.
        centroids.
    labels_to_plot : int
        numeral lables for each centroid.
    my_title : str
        plot title.
    dir_save : str or pathlib.Path, optional
        where to save the plots. The default is './clusters_one_trial'.
    Cluster_num : int, optional
        Number of clusters. The default is 2.

    Returns
    -------
    None.

    """
    from pathlib import Path
    import matplotlib.pyplot as plt
    import seaborn as sns
    dir_save = Path(dir_save)
    dir_save.mkdir(exist_ok=True)
    cmap = sns.color_palette("Paired", Cluster_num)
    plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.Paired.colors)
    fig, ax = plt.subplots()
    ax.plot(centroid_to_plot)
    ax.set_title(my_title)
    fig.savefig(Path(dir_save, my_title+'_line_plot.png'))
    fig, ax = plt.subplots(figsize=(40, Cluster_num))
    labels_to_plot = labels_to_plot.reshape([labels_to_plot.shape[0],1]).T
    ax = sns.heatmap(labels_to_plot, cmap=cmap)
    # modify colorbar:
    colorbar = ax.collections[0].colorbar
#    r = colorbar.vmax - colorbar.vmin
    colorbar.set_ticks([i+1 for i in range(Cluster_num)])
    ax.set_title(my_title)
    fig.savefig(Path(dir_save, my_title+'_labels.png'))

    plt.close('all')

#%% line plot for things like a single voxel data
def plot_line(data_array,
              time_array,
              figsize=(16, 10),
              title_str='',
              label_str='',
              vert_line_times=[],
              color='black',):
    """
    Plot line-plot for centroids.

    Parameters
    ----------
    data_array : NumPy array.
        original data.
    time_array : NumPy array.
        time-stamps for each entry of data_array.
    figsize : set of (int, int), optional
        Figure size. The default is (16, 10).
    title_str : str, optional
        plot title. The default is ''.
    label_str : str, optional
        Label. The default is ''.
    vert_line_times : list of float, optional
        Times to be marked with a vertical red line. The default is [].
    color : valid matplotlib color, optional
        color in plot. The default is 'black'.

    Returns
    -------
    fig : matplotlib Figure
        matplotlib Figure.
    my_ax : matplotlib axes
        matplotlib axes.

    """
    import matplotlib.pyplot as plt
    import numpy as np
    plt.style.use('seaborn-whitegrid')
    fig, my_ax = plt.subplots(nrows=1, ncols=1,
                                 sharey=False, figsize=figsize)
    my_ax.set(title=title_str)
    my_ax.plot(time_array, data_array,
                           label=label_str,
                           color=color)
    if len(vert_line_times) > 2:
        my_ax.set_xticks(vert_line_times)
        my_ax.tick_params(axis='both', which='major', labelsize=7)
        from matplotlib.ticker import FormatStrFormatter
        my_ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        my_ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        for cc_t in np.arange(len(vert_line_times)):
            my_ax.axvline(x=vert_line_times[cc_t],
                          color='k', linestyle='--', linewidth=1) # vertical lines
    return fig, my_ax
#%%
def save_fig(fig,
             dir_save,
             filename_in,
             figsize=(16,12),):
    """
    Save the matplotlib Figure.

    Parameters
    ----------
    fig : matplotlib Figure
        Figure to be saved to disk.
    dir_save : str or pathlib.Path
        where to save..
    filename_in : str or pathlib.Path
        filename.
    figsize : set of (int, int), optional
        OBSOLETE, becasue it has gone obsolete in matplotlib.

    Returns
    -------
    None.

    """
    from mitfat import flags
    from pathlib import Path
    filename_in = Path(filename_in)

    if flags.if_save_eps:
        filename = filename_in.with_suffix('.eps')
        filename = Path(dir_save, filename)
        fig.savefig(filename, format='eps', transparent=False)

    if flags.if_save_png:
        filename = filename_in.with_suffix('.png')
        filename = Path(dir_save, filename)
        fig.savefig(filename, format='png')



# %%
def plot_and_save_bbox_discrete(my_bbox, dir_save_bb,
                                 sup_title=[], limits=[], colours=[]):
    """
    Plot the continuous bbox.

    when elemnts are continuous values (such as mean)
    default color pallete is default (virdis), 0 will be navy and 1 will be yellow.

    Parameters
    ----------
    my_bbox : numpy.ndarray
        Those voxels that we want to plot.
    dir_save_bb : str or pathlib.Path
        where to save.
    sup_title : str, optional
        main title. The default is [].
    limits : list of floats, optional
        y-axis limits. The default is [].
    colours : list of matplotlib colors, optional
        colours for the plot. The default is [].

    Returns
    -------
    None.

    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import numpy as np
    my_bbox = my_bbox - 1  # I used to have label numbers starting from 0,
                           # but chnages it to starting from 1
                           # to make the code work well, need to
                           # set them back to starting from 0

    [aa_d, bb_d, cc_d] = np.shape(my_bbox)
#    plt.close('all')
    my_vmax = np.max(np.unique(my_bbox))
#    colours_all = colours
#    colours_selected = colours_all[0:my_vmax+2]
    colours_selected = colours
    cmap = ListedColormap(colours_selected)

    for cc3 in np.arange(cc_d):
        fig, my_ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
        my_matrix = my_bbox[:, :, cc3]
        mat = my_ax.matshow(my_matrix, cmap=cmap, vmin=-1,
                            vmax=my_vmax, origin='upper', aspect='equal')
        if my_vmax == 0:
            cbar = fig.colorbar(mat, ticks=np.arange(0, my_vmax+2), shrink=0.4)
            labels = ['Representative Voxels']
        else:
            cbar = fig.colorbar(mat, ticks=np.arange(0, my_vmax+2), shrink=0.9)
            labels = list(np.arange(0, my_vmax+2))
            labels = ['Cluster'+str(x+1) for x in labels[0:-1]]
            labels = labels+[' ']

        cbar.ax.set_yticklabels(labels)
        xticks = [x - 0.5 for x in np.arange(my_matrix.shape[1])][1:]
        yticks = [y - 0.5 for y in np.arange(my_matrix.shape[0])][1:]
        my_ax.set_xticks(xticks)
        my_ax.set_yticks(yticks)
        my_ax.set_xticks(np.arange(my_matrix.shape[1]), minor=True)
        my_ax.set_yticks(np.arange(my_matrix.shape[0]), minor=True)

        my_ax.set_xticklabels(np.arange(my_matrix.shape[1])+1, minor=True)
        my_ax.set_yticklabels(np.arange(my_matrix.shape[0])+1, minor=True)
        my_ax.set_yticklabels([])
        my_ax.set_xticklabels([])
        my_ax.grid(color='w', linewidth=0.2)

        filename = 'Axis_3_Slice_'+str(cc3+1).zfill(3)

        # fig.suptitle(sup_title+'- > '+'Axis 3, Slice '+str(cc3+1).zfill(2) )
        figsize=(20.0, 15.0)
        save_fig(fig, dir_save_bb, filename, figsize)

#        if flags.if_save_eps:
#            filename = Path(dir_save_bb, filename + '.eps')
#            fig.savefig(filename, dpi=100, figsize=(20, 15), format='eps')
#        if flags.if_save_png:
#            filename = Path(dir_save_bb, filename + '.png')
#            fig.savefig(filename, dpi=100, figsize=(20.0, 15.0), format='png')

        fig.clf()

    plt.close('all')


# %%
def plot_and_save_bbox_continuous(my_bbox, dir_save_bb,
                                   sup_title=[], v_min=0.0, v_max=1.0):
    """
    Plot the continuous bbox.

    when elemnts are continuous values (such as mean)
    default color pallete is default (virdis), 0 will be navy and 1 will be yellow.

    Parameters
    ----------
    my_bbox : numpy.ndarray
        Those voxels that we want to plot..
    dir_save_bb : str or pathlib.Path
        where to save.
    sup_title : str, optional
        main title. The default is [].
    v_min : float, optional
        Minimum value for coloarbar. The default is 0.0.
    v_max : TYPE, optional
        Maximum value for coloarbar. The default is 1.0.

    Returns
    -------
    None.

    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm

    [aa_d, bb_d, cc_d] = np.shape(my_bbox)


    plt.close('all')
    for cc3 in np.arange(cc_d):
        fig, my_ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
        #fig.suptitle(sup_title+': Signal mean value - >  Axis 3, Slice '+str(cc3+1).zfill(2))
        h_ = my_ax.pcolor(my_bbox[:, :, cc3], vmin=v_min, vmax=v_max, cmap=cm.gist_gray)
        my_ax.set_aspect(1)
        fig.colorbar(h_)
        filename = 'Axis_3_Slice_'+str(cc3+1).zfill(3)

        figsize=(20.0, 15.0)
        save_fig(fig, dir_save_bb, filename, figsize)
#
#        if flags.if_save_eps:
#            filename = Path(dir_save_bb, filename + '.eps')
#            fig.savefig(filename, dpi=100, figsize=(20, 15), format='eps')
#        if flags.if_save_png:
#            filename = Path(dir_save_bb, filename + '.png')
#            fig.savefig(filename, dpi=100, figsize=(20.0, 15.0), format='png')

        fig.clf()
    plt.close('all')

