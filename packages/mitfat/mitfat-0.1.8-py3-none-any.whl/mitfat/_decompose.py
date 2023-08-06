#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 12:25:43 2019

@author: vbokharaie
"""

from mitfat import _Lib
__methods__ = [] # self is a DataStore
register_method = _Lib.register_method(__methods__)

# %%
@register_method
def pca(self, num_pca=5):
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.decomposition import PCA
    from pathlib import Path
    
    # to calculate
    X_train = self.data  # just to unfiy notation
    pca = PCA(num_pca).fit(X_train)
    components = pca.transform(X_train)
    filtered = pca.inverse_transform(components)
    X_pca = pca.fit_transform(X_train)

    # %% plot of explaned variance
    dir_save_subfolder = Path(self.dir_save,
                                      '04_decompositions', '04_a_PCA',
                                      str(num_pca).zfill(2)+'_principal_components')

    dir_save_subfolder.mkdir(parents=True, exist_ok=True)
    print('--------------------------------------------------')
    print('Saving PCA plots in:')
    print(dir_save_subfolder)
    my_colours = plt.cm.Set1.colors

    fig_W = 20
    fig_H = 16
    fig = plt.figure(figsize=(fig_W, fig_H))
    ax = fig.add_subplot(111)

    ax.bar(np.arange(num_pca)+1, np.cumsum(pca.explained_variance_ratio_))
    ax.set_xlabel('number of components')
    ax.set_ylabel('cumulative explained variance')
    ax.set_ylim(0, 1.0)
    labels = [str(np.int8(label*100))+'%' for
              label in list(np.cumsum(pca.explained_variance_ratio_))]
    ax.set_xticks(np.arange(num_pca)+1, labels)

    ax.set_title('Exlpained variance of Princiapl Components, PCA')
    fig.savefig(Path(dir_save_subfolder, 'cumsum_PCA_variance.png'))
    plt.close(fig)

    # %% plot principal componenets vs original selected Signals
    # my_colours = ['r','b','g', 'y', 'm', 'c']
    # my_colours = plt.cm.Set1.colors

    indices_cutoff = self.indices_cutoff
    my_times = self.time_steps
    # fig2  = plt.figure(figsize=(fig_W, fig_H))
    # ax2 = fig2.add_subplot(111)
    fig, ax = plt.subplots(figsize=(fig_W, fig_H))
    if_save_csv = True
    if if_save_csv:
        import pandas as pd
        column_names = ['Time']
        for cc in np.arange(num_pca):
            column_names.append('Principal_Component_'+str(cc+1))
        my_index = np.arange(len(my_times))
        df_centroids = pd.DataFrame(columns=column_names, index=my_index)
        df_centroids.loc[:, 'Time'] = my_times

    for cc in np.arange(num_pca):
        my_alpha = (num_pca-cc)/(num_pca+1)
        ax.plot(my_times, components[:, cc],
                label='c'+str(cc+1), alpha=my_alpha,
                linewidth=3, color=my_colours[cc])
        if if_save_csv:
            df_centroids.iloc[:, cc+1] = components[:,cc]

    #ax.legend(loc = 1)
    ax.set_title('PCA Princinplal Compoenents')
    ax.set_xlabel('component')
    ax.set_ylabel('time')

    for cc_t in np.arange(len(indices_cutoff)):
        ax.axvline(x=my_times[indices_cutoff[cc_t]], color='k',\
                  linestyle='--', linewidth=1) # vertical lines
    ax.set_xticks(my_times[indices_cutoff])
    fig.savefig(Path(dir_save_subfolder,'pca_components.png'))

    num_voxels = self.num_voxels
    for cc in np.arange(num_voxels):
        ax.plot(my_times, self.data[cc,:], alpha = .5, color = 'xkcd:grey', linestyle = 'dotted')
    if if_save_csv:
        filename_csv = Path(dir_save_subfolder,'Principal_Components.xlsx')
        df_centroids.to_excel(filename_csv, index=False)

    fig.savefig(Path(dir_save_subfolder, 'pca_components_and_Signal.png'))
    plt.close(fig)
    plt.close('all')

    # %% subplots of different PCA components plotted seperately
    (fig_W1, fig_H1) = (16, 27)
    #fig  = plt.figure(figsize=(fig_W1, fig_H1))
    fig, ax = plt.subplots(figsize=(fig_W1, fig_H1))
#        ax = fig.add_subplot(111)
#        fig, ax = plt.subplots(num_pca,1, figsize = (fig_W1, fig_H1))

    fig.subplots_adjust(hspace=.3)
    Y_max = np.max(components)
    Y_min = np.min(components)
    for cc1 in np.arange(num_pca):
        ax = fig.add_subplot(num_pca, 1, cc1+1)
        ax.plot(my_times, components[:, cc1])
        ax.set(ylim=(Y_min, Y_max),
               title='PC'+str(cc1+1)+' -- Explained Variance =' +
               str(int(pca.explained_variance_ratio_[cc1]*100))+'%')
        ax.set_xticks(my_times[indices_cutoff])
    fig.savefig(Path(dir_save_subfolder, 'principal_components.png'))
    plt.close(fig)
    plt.close('all')

    # %% bbox plot of different components saved seperately for each component
    mask_bbox = self.bbox_mask
    for cc1 in np.arange(num_pca):
        X_decom = pca.components_[cc1, :]
        subfolder_name = 'PCA_mode_'+str(cc1+1)+'_of_'+str(num_pca)
        dir_save_bb_mean = Path(dir_save_subfolder, subfolder_name)

        dir_save_bb_mean.mkdir(parents=True, exist_ok=True)

        plot_and_save_bbox_continuous(X_decom, mask_bbox,dir_save_bb_mean,subfolder_name, VMIN = np.min(X_decom), VMAX = np.max(X_decom))
        plot_and_save_bbox_map(mask_bbox,dir_save_bb_mean)

        #fig  = plt.figure(figsize=(fig_W, fig_H))
        #ax = fig.add_subplot(111)
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (fig_W, fig_H))

        ax.plot(my_times, X_pca[:,cc1], 'brown', label = 'c'+str(cc1+1), linewidth = 3)

        ax.set_title('PCA Princinplal Compoenents')
        ax.set_xlabel('component')
        ax.set_ylabel('time')

        for cc_t in np.arange(len(indices_cutoff)):
            ax.axvline(x=my_times[indices_cutoff[cc_t]], color='k',\
                      linestyle='--', linewidth=1) # vertical lines
        ax.set_xticks(my_times[indices_cutoff])
        fig.savefig(Path(dir_save_bb_mean,'pca_components.png'))

        num_voxels = my_dataset.Signal.shape[0]
        for cc in np.arange(num_voxels):
            ax.plot(my_times, my_dataset.SignalNormalised[cc,:], alpha = .2, color = 'k', linestyle = 'dotted')
        fig.savefig(Path(dir_save_bb_mean,'pca_components_and_Signal.png'))
        plt.close(fig)

    plt.close('all')

    # %% plotting PCA-filtered Signals for different num_pca saved in subsequent folders
    if_save_large_plots = False
    if if_save_large_plots:
        N_data  = X_train.shape[1]
        num_pca_MAX = no_PCA_components
        for num_pca in np.arange(1,1+num_pca_MAX):
            subfolder_name = 'PCA_mode_'+str(num_pca)+'_of_'+str(num_pca_MAX)
            dir_save_bb_mean = Path(dir_save_subfolder, subfolder_name)

            dir_save_bb_mean.mkdir(parents=True, exist_ok=True)
            pca = PCA(num_pca).fit(X_train)
            components = pca.transform(X_train)
            filtered = pca.inverse_transform(components)

            (N_row, N_col) = (10, 5)
            (fig_W2, fig_H2) = (40,60)
            dir_save_PCA_filtered = dir_save_bb_mean

            dir_save_PCA_filtered.mkdir(parents=True, exist_ok=True)
            page_no = np.int(np.floor(N_data/(N_col*N_row)+1))

            cc_row = 0
            cc_col = 0
            fig  = plt.figure(figsize=(fig_W2, fig_H2))
            #ax = fig.add_subplot(nrows = N_row, ncols = N_col)
            #fig, ax = plt.subplots(nrows = N_row, ncols = N_col, figsize = (fig_W2, fig_H2))

            fig.suptitle('PCA-filtered Signal with '+str(num_pca)+' principal components')
            fig.subplots_adjust(hspace = .4)
            cc_p = 0
            cc_subplot = 1
            for cc2 in np.arange(N_data):
                #print(cc2)
                if (np.mod(cc2, N_col*N_row)==0) and (not cc2==0):
                    #print(cc2)
                    cc_subplot = 1

                    cc_p = cc_p +1
                    filename = 'PCA_filtered_with_'+str(num_pca)+'_components_PAGE_'+str(cc_p).zfill(2)+'_of_'+str(page_no).zfill(2)+'.png'
                    fig.savefig(Path(dir_save_PCA_filtered, filename))
                    plt.close(fig)

                    fig  = plt.figure(figsize=(fig_W2, fig_H2))
                    #ax = fig.add_subplot(nrows = N_row, ncols = N_col)
                    #fig, ax = plt.subplots(nrows = N_row, ncols = N_col, figsize = (fig_W2, fig_H2))

                    #fig, ax = plt.subplots(nrows = N_row, ncols = N_col, figsize = (fig_W2,fig_H2))
                    cc_row = 0
                    cc_col = 0
                #ax1 = ax[cc_row, cc_col]
                ax1 = fig.add_subplot(N_row, N_col, cc_subplot)
                cc_subplot = cc_subplot+1
                cc_col = cc_col+1

                if cc_col>=N_col:
                    cc_row = cc_row+1
                    cc_col = 0
                ax1.plot(my_times, X_train[:,cc2], ':', alpha = 0.9)
                ax1.plot(my_times, filtered[:,cc2], lw = 3)
                ax1.set_title('Voxel '+str(cc2+1))
                ax1.set_xticks(np.int16(my_times[indices_cutoff]))
            cc_p = cc_p +1
            filename = 'PCA_filtered_with_'+str(num_pca)+'_components_PAGE_'+str(cc_p).zfill(2)+'_of_'+str(page_no).zfill(2)+'.png'

            filename = Path(dir_save_PCA_filtered, filename)

            fig.savefig(filename)

            plt.close(fig)
    print('FINITO PCA')
    #plt.close('all')

    #print('FINITO All')
    import gc
    gc.collect()
    plt.close('all')
