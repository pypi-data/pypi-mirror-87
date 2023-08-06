#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:58:00 2019

@author: vbokharaie

Thie mosule includes functions which will operate on a list of fmri_datasets,
    such as calcultating the average of a list of datasets.
"""
from mitfat.fmri_dataset import fmri_dataset

def calc_mean_dataset(list_of_fmri_datasets):
    """Reads a list of fmri_datasets,
    returns an fmri_dataset which contains the average of the data in all of them.

    :param list_of_fmri_datasets: list of fmri_datastes to be avegred
    :type time_steps: list of elemnts of :'fmri_dataset' type
    :param first_trial_time: the beginning time of the first trial, default 0.0
    :raises: Happiness level, and checks if input is a list and a list of fmri_dataset

    :return: fmri_dataset, average of input list data
    :rtype: 'fmri_dataset' type
    """

    import numpy as np
    assert isinstance(list_of_fmri_datasets, list), \
            'The Wizard says: Input argument should be a list!'
    for x in list_of_fmri_datasets:
        assert isinstance(x, fmri_dataset), \
            'The Wizard says: Each elemnt of the list should be an fmri_dataset!'
    len_list = len(list_of_fmri_datasets)
    for idx, ds in enumerate(list_of_fmri_datasets):
        if idx==0:
            data_sum = np.zeros(ds.data.shape)
        data_trial = ds.data
        assert data_sum.shape == data_trial.shape, \
            'The Wizard says: shape of data in trial %d different than others' % (idx+1)

        data_sum = data_sum + data_trial

    data_mean = data_sum/len_list
    ds1 = list_of_fmri_datasets[0]
    import os
    dir_save_1_up = os.path.dirname(ds1.dir_save)
    dir_save_mean = os.path.join(dir_save_1_up, 'MEAN')
    fmri_object_mean = fmri_dataset(
                            data_mean,
                            ds1.mask,
                            ds1.time_steps,
                            ds1.signal_name,
                            ds1.indices_cutoff,
                            ds1.experiment_name,
                            ds1.dataset_no,
                            ds1.mol_name,
                            ds1.dir_source,
                            dir_save_mean,
                            ds1.description+' --- AVERAGE DATA',
                            ds1.first_trial_time,
                            ds1.trial_length,
                            trial_no = 0,
                            )
    return fmri_object_mean