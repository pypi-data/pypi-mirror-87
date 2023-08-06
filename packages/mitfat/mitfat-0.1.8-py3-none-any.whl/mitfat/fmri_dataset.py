#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 10:55:19 2018

@author: vbokharaie
"""
# pylint: disable=line-too-long
# pylint: disable=C0103, E1101, W0212
# %% defintion of fMRI dataset class
# This _Lib module is just a trick to distribute methods of the class over
# several modules.
from mitfat import _Lib
from mitfat import _basics
from mitfat import _plotting
from mitfat import _private
from mitfat import _detrending
from mitfat import file_io
#from mitfat import _decompose
@_Lib.add_methods_from(_basics)
@_Lib.add_methods_from(_plotting)
@_Lib.add_methods_from(_private)
@_Lib.add_methods_from(_detrending)
@_Lib.add_methods_from(file_io)
#@_Lib.add_methods_from(_decompose)

class fmri_dataset:
    """
    A class as a container for all relvant data of an fMRI recording.

    class method are distributed in different modules whose names start with '_'

    """

    #  a variable to keep track of all created objects
    total_created_objects = 0
    """ keeps track of total number of objects"""

    ###
    def __init__(self,
                 data_masked,
                 mask_numpy,
                 time_steps,
                 signal_name,
                 indices_cutoff,
                 experiment_name,
                 dataset_no,
                 mol_name,
                 dir_source,
                 dir_save,
                 description,
                 first_trial_time,
                 trial_length,
                 trial_no=0,
                 ):
        """
        Intilise the class and defin properties.

        Parameters
        ----------
        data_masked: 'numpy.ndarray', (N_time_steps, N_voxels)
        mask_numpy: 'numpy.ndarray', (d1, d2, d3)
        time_steps: 'list' of 'float'
        signal_name: 'str'
        indices_cuttoff: 'list' if 'int'
        experiment_name: 'str'
        dataset_no: 'int'
        mol_name: 'str'
        dir_source: 'str'
        dir_save: 'str'
        description: 'str'
        first_trial_time: float
        trial_length: float, default None, in which case would be set to time_steps
        time_steps_relative: list of floats, time steps in each trial realtive to start of trial
        trial_no: int, when dataset is split in trials, shows the number of trial, default = 0,
                        meaning no trials defined
        """
        import numpy as np
        from mitfat._shapes import bbox_3d, bbox_mean, bbox_3d_seq
        from mitfat import flags

        # main variables
        self.data_raw = data_masked
        """raw data, always"""
        self.data = self.data_raw  # default: raw. Can also be normalised.
        """normalised, unless flags.if_normalise=False"""
        self.data_mean = np.nanmean(self.data, axis=0)
        """mean of each voxels"""
        self.mask = mask_numpy
        """3d mask"""
        self.time_steps = time_steps
        """flow list"""
        self.num_voxels = self.data.shape[1]
        """inti"""
        self.num_time_steps = self.data.shape[0]
        """int"""
        assert self.num_voxels == np.sum(self.mask),\
            'mask size not equal to number of voxels in data file'
        assert self.num_time_steps == len(self.time_steps),\
            'number of time-steps in data file does not match that of time file'
        # now other variables
        self.signal_name = signal_name

        self.indices_cutoff = indices_cutoff

        self.cutoff_times = [0.0]*len(indices_cutoff)
        for idx, elem in enumerate(indices_cutoff):
            self.cutoff_times[idx] = self.time_steps[elem]

        self.calc_mean_segments()

        self.experiment_name = experiment_name

        self.dataset_no = dataset_no

        self.mol_name = mol_name

        self.dir_source = dir_source

        self.dir_save = dir_save

        self.description = description

        self.first_trial_time = first_trial_time

        self.trial_length = trial_length

        self.trial_no = trial_no



        #####################################################################
        # defining new properties
        #####################################################################

        # normalised to overall maximum and to mean per voxel
        # self.data would be set to be self.data_normalised

        self.data_normalised = None
        self.data_normalised_per_voxel = None

        # linear regression
        self.line_reg = None

        self.line_reg_slopes = None

        self.line_reg_biases = None

        # bbox
        self.bbox_mask = bbox_3d(self.mask)

        self.bbox_data_mean = bbox_mean(self.bbox_mask, self.data)

        self.bbox_mask_seq = bbox_3d_seq(self.bbox_mask)

        # possible hiearachial clustering
        self.data_hierarchical = None

        self.bbox_mask_hierarchical = None

        #
        fmri_dataset.total_created_objects = fmri_dataset.total_created_objects + 1

        # fix anamolies, impute, normlaise
        if flags.if_fix_anomolies:
            self.fix_anomolies()

        if flags.if_impute:
            self.impute()

        if flags.if_normalised:
            self.normalise()

        self.calc_lin_reg()


