#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 19:05:33 2019

@author: vbokharaie

This module includes methods of fmri_dataset class used for plotting.

"""
from mitfat import _Lib
#from mitfat import flags

__methods__ = []
register_method = _Lib.register_method(__methods__)

#%% plotting data for one voxel
#
@register_method
def plot_voxel(self,
                data_type='normalised',
                voxel_num=1,
                list_voxel_num=None,
                figsize=(16, 10),
                dir_save=None,
                filename_pre='',
                ):

    """Plots the time-series corresponsing to each voxel.
    The plots are arranged in a layout which follows the mask.
    Each layer is saved in a separeta file.
    Parameters
    ----------
    data_type : {'normalised', 'raw', 'lin_reg'}
        'normalised' (default): plot normalised time-series.
        'raw': plot raw signal
        'lin_reg': plot linear regression of time-series
    figsize : set of float, (fig_w, fig_h)
            fig dimensions in inches
    voxel_num: int
            voxels number to be plotter. shoud be in (1, self.voxel_no) range

    Raises
    ------
    NameError
        If data is not normalised and user tries to plot normalised data.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from pathlib import Path

    from mitfat.bplots import save_fig, plot_line


    if not list_voxel_num:
        no_voxels = self.num_voxels
        if voxel_num > no_voxels:
            print('Voxel number should not be more than ', no_voxels)
            return

    # which kind of signal?
    if data_type == 'normalised':
        try:
            my_data = self.data_normalised
        except NameError:
            print('normalised version of data does not exist')
            return
        subfolder = '01_voxels_normalised'
        print('Plot basic plots for normalised signals ...')
    elif data_type == 'raw':
        my_data = self.data
        subfolder = '01_voxels_raw'
        print('Plot basic plots for raw signals ...')
    elif data_type == 'lin_reg':
        try:
            my_data = self.line_reg
            subfolder = '01_voxels_linear_regresseion'
            print('Plot basic plots for linear regressed signals ...')
        except:
            print('The RoiDataset object does not contain a linear regression version of the data.')
            print('Run lin_reg method first.')
            return

    # general variables
    no_voxels = self.num_voxels
#    no_time_steps = self.num_time_steps
    y_max = np.nanmax(my_data)

    # plot params


#    fig.tight_layout(rect=[0, 0.03, 1, 0.95], w_pad=0.02)
    if not list_voxel_num:
        data_ind = voxel_num - 1
        data_array = my_data[:, data_ind]
        title_str = filename_pre+'Voxel '+str(voxel_num).zfill(4)
        if voxel_num<1e5:
            voxel_str = str(voxel_num).zfill(4)
        else:
            voxel_str = str(voxel_num)
        filename = filename_pre + 'Voxel_' + voxel_str
    else:
        data_2D = np.array(my_data)[:, list_voxel_num]
        data_array = np.nanmean(data_2D, axis=1)

        title_str = filename_pre + '_Voxels '
        filename = filename_pre + '_Voxels'
        for vox in list_voxel_num:
            title_str = title_str + str(vox) + ','
            filename = filename + '_' + str(vox)
    time_array = self.time_steps
    label_str = self.signal_name
    color = 'black'

    if len(self.cutoff_times) > 2:
        vert_line_times = self.cutoff_times

    fig, ax = plot_line(data_array,
              time_array,
              figsize=(16, 10),
              title_str=title_str,
              label_str=label_str,
              vert_line_times=vert_line_times,
              color=color,)

    if not dir_save:
        # where to save?
        dir_save = Path(self.dir_save, subfolder)
    dir_save = Path(dir_save)
    dir_save.mkdir(parents=True, exist_ok=True)
    print('Plot will be saved in: \n', dir_save)
    save_fig(fig, dir_save, filename, figsize)

    fig.clf()

    plt.close('all')


#%% plotting a list of 2d arrays, each row being fmri time-series for each voxel
# function plots all time series in each voxel in a plot
@register_method
def plot_basics(self,
                data_type='normalised',
                figsize=None,
                ):

    """Plots the time-series corresponsing to each voxel.
    The plots are arranged in a layout which follows the mask.
    Each layer is saved in a separeta file.
    Parameters
    ----------
    data_type : {'normalised', 'raw', 'lin_reg'}
        'normalised' (default): plot normalised time-series.
        'raw': plot raw signal
        'lin_reg': plot linear regression of time-series
    figsize : set of float, (fig_w, fig_h)
            fig dimensions in inches

    Raises
    ------
    NameError
        If data is not normalised and user tries to plot normalised data.
    """

    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    from pathlib import Path

    from mitfat.bplots import save_fig

    # which kind of signal?
    if data_type == 'normalised':
        try:
            my_data = self.data_normalised
        except NameError:
            print('normalised version of data does not exist')
            return
        subfolder = '01_basics_normalised'
        print('Plot basic plots for normalised signals ...')
    elif data_type == 'raw':
        my_data = self.data
        subfolder = '01_basics_raw'
        print('Plot basic plots for raw signals ...')
    elif data_type == 'lin_reg':
        try:
            my_data = self.line_reg
            subfolder = '01_basics_linear_regresseion'
            print('Plot basic plots for linear regressed signals ...')
        except:
            print('The RoiDataset object does not contain a linear regression version of the data.')
            print('Run lin_reg method first.')
            return
    # where to save?
    dir_save = Path(self.dir_save, subfolder)
    print('Plot will be saved in: \n', dir_save)
    dir_save.mkdir(parents=True, exist_ok=True)
    # general variables
    no_voxels = self.num_voxels
#    no_time_steps = self.num_time_steps
    bbox_seq = self.bbox_mask_seq
    bbox_mean = self.bbox_data_mean
    [n_row, n_col, no_figures] = bbox_seq.shape
    y_max = np.nanmax(my_data)

    # plot params
    plt.style.use('classic')
    cmap = matplotlib.cm.get_cmap('viridis')
    if not figsize:
        fig_w = 2*n_col
        fig_h = 2*n_row
        figsize =(fig_w, fig_h)

    # %% let's count
    idx = 0
    for cc1 in np.arange(no_figures):
        print('Saving layer', cc1+1, 'of ', no_figures, ' ...')
        fig, my_ax_all = plt.subplots(nrows=n_row, ncols=n_col,
                                      sharey=False, figsize=figsize)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95], w_pad=0.02)

        for cc_r in np.arange(n_row):
            is_new_row = True
            if data_type == 'lin_reg':
                is_new_row == False  # no need for y-axis ticks for lin_reg data.
            for cc_c in np.arange(n_col):
                my_ax = my_ax_all[cc_r, cc_c]
                my_ax.grid()
                my_ax.set_ylim(0, y_max)

                if bbox_seq[cc_r, cc_c, cc1] != 0:
                    data_ind = bbox_seq[cc_r, cc_c, cc1]-1
                    my_ax.set(title='Voxel '+str(idx+1).zfill(4))
                    my_ax.plot(self.time_steps, my_data[:, data_ind],
                               label=self.signal_name,
                               color='black')

                    if len(self.cutoff_times) > 2:
                        my_ax.set_xticks(self.cutoff_times)
                        my_ax.tick_params(axis='both', which='major', labelsize=7)
                        from matplotlib.ticker import FormatStrFormatter
                        my_ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
                        my_ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
                        for cc_t in np.arange(len(self.cutoff_times)):
                            my_ax.axvline(x=self.cutoff_times[cc_t],
                                          color='k', linestyle='--', linewidth=1) # vertical lines
                    color_face = cmap(bbox_mean[cc_r, cc_c, cc1])
                    my_ax.set_facecolor(color_face)
                    # y label ticks only shown in the first subplot in each row
                    if not is_new_row:
                        my_ax.set_yticklabels([])
                    else:
                        is_new_row = False

                    idx = idx+1
                else:
                    my_ax.axis('off')  #subplots outside the mask are suppressed

        voxel_start = str(cc1*(n_row*n_col)).zfill(4)
        voxel_end = str(np.min([(cc1+1)*n_row*n_col, no_voxels])).zfill(4)
        filename = 'Voxels_'+voxel_start+'_to_'+voxel_end
        figsize = (fig_w, fig_h)
        save_fig(fig, dir_save, filename, figsize)

#        if flags.if_save_eps:
#            filename = Path(dir_save, filename + '.eps')
#            fig.savefig(filename, dpi=100, figsize=(fig_w, fig_h), format='eps')
#        if flags.if_save_png:
#            filename = Path(dir_save, filename + '.png')
#            fig.savefig(filename, dpi=100, figsize=(fig_w, fig_h), format='png')

        fig.clf()

    plt.close('all')


# %% bbox the clusters and time-series plots
@register_method
def plot_clusters(self, original_data, data_label,
                   cluster_labels, cluster_centroids,
                   if_slopes=False, if_hierarchical=False,
                   subfolder_c='',
                   ):
    """Plots the cluster, saves cntroid values.
    Including bbox plots, centroid plots.
    centroids are saved in .xlsx file in the same folder as plots.

    The plots are arranged in a layout which follows the mask.
    Each layer is saved in a separeta file.

    Parameters
    ----------

    original_data: 'numpy.ndarray', (N_clustered_data, N_voxels)
                    N_clustered_data can be N_time_steps, 1, or N_segments
    data_label: 'str'
                used in establishing save folders
    cluster_labels: 'numpy.ndarray', (N_voxels, 1)
    cluster_centroids: 'numpy.ndarray', (N_clusters, N_clustered_data)
    subfolder_c: str,
                    name of subfolder inside main dir_save to save the plots

    Raises
    ------

    NameError
        If data is not normalised and user tries to plot normalised data.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    from pathlib import Path
    from mitfat.bplots import plot_and_save_bbox_discrete
    from mitfat.bplots import save_fig


    plt.style.use('seaborn-whitegrid')

    no_clusters = np.unique(cluster_labels).shape[0]
    centroid_length = np.shape(cluster_centroids)[1]
    if if_hierarchical:
        original_data = self.data_hierarchical
        mask_bbox = self.bbox_mask_hierarchical
        dir_save_subfolder = Path(self.dir_save,
                                  subfolder_c,
                                  data_label+'_clusters_'+str(no_clusters))
    else:
        mask_bbox = self.bbox_mask
        dir_save_subfolder = Path(self.dir_save,
                                  subfolder_c,
                                  data_label+'_clusters_'+str(no_clusters))

    dir_save_subfolder.mkdir(parents=True, exist_ok=True)
#    original_data = self.data_normalised
    y_max = np.nanmax(original_data)
    colours_for_cat = ['#f43605', '#fcc006', '#89a203',
                       '#047495', '#030764', '#c071fe',
                       '#db5856', '#0cdc73', '#fbdd7e', '#e78ea5']
    colours_for_cat = colours_for_cat + colours_for_cat
    colours_for_cat = colours_for_cat[0:no_clusters]
    colours_for_cat_colorbar = ['#000000']+colours_for_cat
    cat_labels = ['Cluster '+str(idx+1) for idx in np.arange(no_clusters)]
    bbox_cat = np.int8(np.zeros(np.shape(mask_bbox)))-1
    bbox_cat[mask_bbox == 1] = cluster_labels
    plot_and_save_bbox_discrete(bbox_cat, dir_save_subfolder,
                                sup_title='kmeans with '+str(no_clusters)+' clusters',
                                colours=colours_for_cat_colorbar)
    fig, my_ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(12, 8))

    if (self.num_time_steps == centroid_length) and centroid_length > 1:
        for cc2 in np.arange(no_clusters):
#            sns.set_style("white", {'axes.grid': True})
            plt.style.use('seaborn-whitegrid')
            my_ax.plot(self.time_steps, cluster_centroids[cc2, :],
                       label=cat_labels[cc2], color=colours_for_cat[cc2], lw=5)
            fig.suptitle(str(len(list(set(cluster_labels)))) + ' clusters')
            for cc_t in np.arange(len(self.indices_cutoff)):
                my_ax.axvline(x=self.cutoff_times[cc_t], color='k',
                              linestyle='--', linewidth=1)  # vertical lines
        my_ax.set_xticks(self.cutoff_times)
        my_ax.grid(True)
        my_ax.set_ylim(0, y_max)
        for item in ([my_ax.xaxis.label, my_ax.yaxis.label] +
                     my_ax.get_xticklabels() + my_ax.get_yticklabels()):
            item.set_fontsize(20)
            item.set_fontweight('bold')
        handles, labels = my_ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
        figsize=(16.0, 10.0)
        save_fig(fig, dir_save_subfolder,
                 'Cluster_centres.eps',
                 figsize)
#        if flags.if_save_eps:
#            filename_bb_wo_raw = Path(dir_save_subfolder, 'Cluster_centres.eps')
#            fig.savefig(filename_bb_wo_raw, transparent=False, dpi=100,
#                        figsize=(16.0, 10.0), format='eps')
#
#        if flags.if_save_png:
#            filename_bb_wo_raw = Path(dir_save_subfolder, 'Cluster_centres.png')
#            fig.savefig(filename_bb_wo_raw, transparent=False, dpi=100,
#                        figsize=(16.0, 10.0), format='eps')
#
        for cc3 in np.arange(original_data.shape[1]):
            my_cluster_label = cluster_labels[cc3]
            my_ax.plot(self.time_steps, original_data[:, cc3],
                       color=colours_for_cat[my_cluster_label-1],
                       alpha=0.2, linestyle='dotted')

        filename_bb_alpha = Path('Cluster_centres_with_OriginalData.png')
        figsize=(16.0, 10.0)

        if False:  # enable if you want to have hiearachical cnetroid for all trials in one folder
            if self.trial_no:
                dir_save2 = dir_save_subfolder.parent.parent.parent
                filename_pre = 'TRIAL_' + str(self.trial_no).zfill(3)
                filename = Path(filename_pre + '_Cluster_centres_with_OriginalData.png')
                save_fig(fig, dir_save2, filename, figsize)
            else:
                save_fig(fig, dir_save_subfolder,
                     filename_bb_alpha,
                     figsize)
#        if flags.if_save_eps:
#            filename_bb_alpha = Path(dir_save_subfolder, 'Cluster_centres_with_OriginalData.eps')
#            fig.savefig(filename_bb_alpha, transparent=False, dpi=100,
#                        figsize=(16.0, 10.0), format='eps')
#
#        if flags.if_save_png:
#            filename_bb_alpha = Path(dir_save_subfolder, 'Cluster_centres_with_OriginalData.png')
#            fig.savefig(filename_bb_alpha, dpi=100, figsize=(16.0, 10.0), format='png')

    else:
        if centroid_length == 1 and not if_slopes:
            ind = (np.arange(np.shape(cluster_centroids)[0])+1)
            my_ax.bar(ind, cluster_centroids.flatten(), color=colours_for_cat)
            fig.suptitle('Cluster Centres')

        elif centroid_length == 1 and if_slopes:
            for cc2 in np.arange(no_clusters):
                time_steps = self.time_steps
                temp_line = np.zeros(np.shape(time_steps))
                indices_cutoff = self.indices_cutoff
                for cc3 in np.arange(centroid_length):
                    x_temp = time_steps[indices_cutoff[cc3]:indices_cutoff[cc3+1]+1]\
                                - time_steps[indices_cutoff[cc3]]
                    if cc3 > 0:
                        y_temp = x_temp*cluster_centroids[cc2, cc3] + \
                                temp_line[indices_cutoff[cc3]]
                    else:
                        y_temp = x_temp*cluster_centroids[cc2, cc3]
                    temp_line[indices_cutoff[cc3]:indices_cutoff[cc3+1]+1] = y_temp

                my_ax.plot(time_steps, temp_line[:],\
                    label=cat_labels[cc2], color=colours_for_cat[cc2])

                fig.suptitle('Cluster Centres'+\
                             '\n lines represent slopes, not actuall signal values')
                for cc_t in np.arange(len(indices_cutoff)):
                    my_ax.axvline(x=time_steps[indices_cutoff[cc_t]], color='k',\
                                      linestyle='--', linewidth=1) # vertical lines

        elif centroid_length < self.num_time_steps and centroid_length > 1 and not if_slopes:
            for cc2 in np.arange(no_clusters):
                my_ax.plot(np.arange(centroid_length)+1,\
                            cluster_centroids[cc2, :], label=cat_labels[cc2],\
                            color=colours_for_cat[cc2], marker='H', linestyle=':')
            from matplotlib.ticker import MaxNLocator
            my_ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # x ticks be integer
            fig.suptitle('Cluster Centres')

        elif centroid_length < self.num_time_steps and centroid_length > 1 and if_slopes:
            for cc2 in np.arange(no_clusters):
                time_steps = self.time_steps
                temp_line = np.zeros(np.shape(time_steps))
                indices_cutoff = self.indices_cutoff
                for cc3 in np.arange(centroid_length):
                    x_temp = time_steps[indices_cutoff[cc3]:indices_cutoff[cc3+1]+1] - \
                             time_steps[indices_cutoff[cc3]]
                    if cc3 > 0:
                        y_temp = x_temp*cluster_centroids[cc2, cc3] + \
                                        temp_line[indices_cutoff[cc3]]
                    else:
                        y_temp = x_temp*cluster_centroids[cc2, cc3]
                    temp_line[indices_cutoff[cc3]:indices_cutoff[cc3+1]+1] = y_temp

                my_ax.plot(time_steps, temp_line[:],
                           label=cat_labels[cc2], color=colours_for_cat[cc2])
                fig.suptitle('Cluster Centres' +
                             '\n lines represent slopes, not actuall signal values')
                for cc_t in np.arange(len(indices_cutoff)):
                    my_ax.axvline(x=time_steps[indices_cutoff[cc_t]], color='k',
                                  linestyle='--', linewidth=1)  # vertical lines

        my_ax.grid(True)
        handles, labels = my_ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
        figsize=(16.0, 10.0)
        save_fig(fig, dir_save_subfolder, 'Cluster_centres.png', figsize)
#        if flags.if_save_png:
#            filename_bb = Path(dir_save_subfolder, 'Cluster_centres.png')
#            fig.savefig(filename_bb, dpi=100, figsize=(16.0, 10.0), format='png')
#        if flags.if_save_eps:
#            filename_bb = Path(dir_save_subfolder, 'Cluster_centres.eps')
#            fig.savefig(filename_bb, transparent=False,
#                        dpi=100, figsize=(16.0, 10.0), format='eps')

    plt.close('all')


