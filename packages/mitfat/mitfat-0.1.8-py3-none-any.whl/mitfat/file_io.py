#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:55:19 2018

@author: vbokharaie

This module includes methods of fmri_dataset class used for I/O operations.

"""
# pylint: disable=line-too-long
# pylint: disable=wrong-import-position
from mitfat import _Lib

__methods__ = []  # self is a DataStore
register_method = _Lib.register_method(__methods__)

#%%
@register_method
def save_clusters(self, X_train, data_label, cluster_labels, cluster_centroids,
                  subfolder_c = ''):
    """
    Save cluster to excel file.

    Parameters
    ----------
    X_train : Numpy array.
        Data to cluster. N_clustered_data can be N_time_steps, 1, or N_segments.
        Shape is (N_clustered_data, N_voxels)
    data_label : str
        used in establishing save folders
    cluster_labels : list of int
        labels for clusters.
    cluster_centroids : Numpy array
        centroids.
    subfolder_c : str, optional
        adding an optional subfolder. The default is ''.

    Returns
    -------
    None.

    """
    import pandas as pd
    import numpy as np
    from pathlib import Path

    no_clusters = np.unique(cluster_labels).shape[0]
    dir_save_subfolder = Path(
        self.dir_save, subfolder_c, data_label + "_clusters_" + str(no_clusters)
    )
    dir_save_subfolder.mkdir(parents=True, exist_ok=True)
    centroid_length = np.shape(cluster_centroids)[1]

    column_names = []
    my_index = np.arange(centroid_length)
    df_centroids = pd.DataFrame(columns=column_names, index=my_index)

    if centroid_length == self.num_time_steps:
        df_centroids["Time"] = self.time_steps
    elif centroid_length == 1:
        df_centroids["Index"] = 1
    else:
        my_indices = np.arange(centroid_length) + 1
        df_centroids["Segments"] = my_indices

    for cc_ in np.arange(no_clusters):
        df_centroids["Cluster_" + str(cc_ + 1)] = cluster_centroids[cc_, :]

    filename_csv = Path(dir_save_subfolder, "Cluster_centres.xlsx")
    df_centroids.to_excel(filename_csv, index=False)


# %% just print a template for info files
def print_info(filename_info=None):
    """
    Print info text.

    Parameters
    ----------
    filename_info : str or pathlib Path, optional
        If given, info is written to file otherwise to standard output. The default is None.

    Returns
    -------
    None.

    """
    text_info = """
## This is a template for input files for the MiTfAT library,
#  				a pyhton-based fMRI analysis tool.
# In which line you write the info is irrelevant.
# every line not starting with a valid keyword is ignored.
# There should be at least one blank space between the keyword and the following input values.
# The only obligatory keywords are the DATA_FILE and MASK_FILE.
# The rest will be assigned default values or just ignored if not defined.

# REQUIRED keywords are:
# 'DATA_FILE:' -> (REQUIRED) name of the nifty data files
# 'MASK_FILE:' -> (REQUIRED) nifty file including the mask file.
                   0 elements in this file means ignore the voxel, non-zero means read the voxel.

# OPTIONAL Keywords:
# 'TIME_FILE:' -> file including time points for each data point.
                  If left blank, indices of data points are used as time-steps, starting from 1.
# 'EVENT_TIMES' -> can be any events of interest.
                    should be numbers (float or integer), comma separated.
                    They'd be irrelevant if TIME_FILE does not exist.
                    They do not need to match exact values of time steps.
# 'DIR_SOURCE:' -> Absolute or relative path to source directory.
                   default is 'datasets' subfolder inside the folder in which this file exists.
# 'DIR_SAVE:' -> Absolute or relative path to directory used to save the outputs.
                default is used: 'output' subfolder inside the current python folder,
		(not necessarily folder containing this file).
# 'MOL_NAME:' -> Molecule name. Used in molecular fMRI experiments.
                 If not left blank will be used to establish DIR_SAVE name.
# 'EXP_NAME:' -> Experiment name.
                 If not left blank will be used to establish DIR_SAVE name.
# 'DESC:'-> A free style text with info about the dataset.
# 'DS_NO:' -> An integer number assigned to identify the dataset.
             If not left blank will be used to establish DIR_SAVE name.
# 'SIGNAL_NAME:' -> can be T1w, FISP, T2* or any arbitrary string.

## Here is a sample info file:
# obligatiry info:
DATA_FILE: sample_data_T1w.nii.gz
MASK_FILE: sample_data_mask.nii.gz

# optional time file, and event times
TIME_FILE: sample_data_time_T1w.txt
EVENT_TIMES: 123,181

# other optional info
MOL_NAME: SCA
SIGNAL_NAME: T1w
DS_NO: 1
EXP_NAME: Exp1
DESC: Just a sample dataset.
"""
    if not filename_info:
        print(text_info)
    else:
        with open(filename_info, "w") as file:
            file.write(text_info)
        from pathlib import Path

        print("info file template saved in:", Path(filename_info).resolve())
        print(Path(__file__).resolve())


# %% just print a template for info files
def test_script(filename=None):
    """
    Return back the name of test script.

    Parameters
    ----------
    filename : str or pathlib.Path, optional
        Either a user-defined test file, or the default that already exists in mitfat.
        The default is None.

    Returns
    -------
    None.

    """
    from pathlib import Path
    from shutil import copyfile

    file_io_path = Path(__file__).parent
    src = Path(file_io_path, "test_script.py")
    if not filename:
        filename = "MiTfAT_test_script.py"
    dst = Path(Path.cwd(), filename)
    copyfile(src, dst)

# %%
def make_list_of_trial_times(time_steps, first_trial_time=0.0, trial_length=None):
    """
    Read time-steps, first trial time and trial length.

    calculates ands returns the indices and time-steps of consecutive trials

    :param time_steps: time-steps of the fMRI recording
    :type time_steps: list of floats
    :param first_trial_time: the beginning time of the first trial, default 0.0
    :type first_trial_time: float, optional
    :param first_trial_time: length of each trial, default None (wouold be set to max(time_steps))
    :type first_trial_time: float, optional

    :return: list_of_trial_times, list_of_trial_times_indices
    :rtype: list of floats, list of integers
    """
    time_steps_corrected = [x for x in time_steps if x >= first_trial_time]
    if len(time_steps_corrected) == 0:
        raise 'FFS!'
    list_of_trial_times = []
    list_of_trial_times_indices = []
    cc1 = 0
    while True:  #  oh my!
        t0 = cc1 * trial_length
        tf = (cc1+1) * trial_length
        if tf > max(time_steps_corrected):
            break
        list_times = [x for x in time_steps_corrected if (x >= t0 and x < tf)]
        list_indices = [idx for idx, x in enumerate(time_steps_corrected) if (x >= t0 and x < tf)]
        list_of_trial_times.append(list_times)
        list_of_trial_times_indices.append(list_indices)
        cc1 = cc1 + 1
    return list_of_trial_times, list_of_trial_times_indices

# %%
def read_data(info_file_name):
    """
    Read the input dataset info from a file.

    returns a fmri_dataset object including all those files.

    Parameters
    ----------
    info_file_name:     str
        an os.path filename object

    Returns
    -------
    fmri_dataset: obj

    """
    from mitfat.file_io import main_get_data
    from mitfat.fmri_dataset import fmri_dataset
    import numpy as np
    from pathlib import Path
    # read the data from file
    data_masked, mask_numpy, time_steps, signal_name, cutoff_times, \
            experiment_name, dataset_no, mol_name, \
            dir_source, dir_save, description, \
            first_trial_time, trial_length = main_get_data(info_file_name)

    print("Data dimensions (n_time x n_voxels): ", data_masked.shape)
    print("Mask size: ", np.sum(mask_numpy))
    if trial_length > 0:
        print('dataset is going to be split into subsets of time-length', trial_length)
    print("----------------------------------------")

    #%% WARNINIG: This is going to be a majot chnage in the code, and might come back to bite us
    #   in the arse. So far, the concept of trial did not exist, and all the recording data
    #   goes into a single dataset. But with trials, there are two options:
    #           1. chnage fmri_dataset object
    #           2. define a new fmri_dataset for each trial
    #  we go with option (2), since it seems to need less changes in the code.
    #  So, this funciton now returns a list of fmri_dataset objects.
    #  Maybe, we add a condition that if the length of the list is 1, just return the 1st element.

#    if trial_length > 0:

#        for my_times in np.arange(first_trial_time, time_steps[-1], time_steps[1]-time_steps[0]):


    # establish the fmri_dataset object
    list_fmri_objects = []
    if trial_length == 0:
        if cutoff_times == '':
            indices_cutoff = [0, data_masked.shape[0] - 1]
        else:
            indices_cutoff = convert_real_time_to_index(time_steps, cutoff_times)

        fmri_object = fmri_dataset(
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
            )
        list_fmri_objects.append(fmri_object)
    elif trial_length > 0:
        list_of_times, list_of_trial_times_indices = make_list_of_trial_times(
            time_steps,
            first_trial_time,
            trial_length
            )
        print('-----------', (list_of_times[-1]), len(list_of_times))
        number_of_trials = len(list_of_times)
        if number_of_trials == 0:
            raise 'FFS!'

        for trial_no in np.arange(number_of_trials):
            print('creating dataset for trial ', trial_no+1)
            time_segment = list_of_times[trial_no]
            time_steps_relative = time_segment - time_segment[0]
            my_indices = list_of_trial_times_indices[trial_no]
            data_masked_subset = data_masked[my_indices, :]

            if cutoff_times == '':
                indices_cutoff = [0, data_masked_subset.shape[0] - 1]
            else:
                indices_cutoff = convert_real_time_to_index(time_steps_relative, cutoff_times)

            dir_save_trial = Path(dir_save.as_posix()+'_TRIAL_'+str(trial_no+1).zfill(3))
            fmri_object = fmri_dataset(
                data_masked_subset,
                mask_numpy,
                time_steps_relative,
                signal_name,
                indices_cutoff,
                experiment_name,
                dataset_no,
                mol_name,
                dir_source,
                dir_save_trial,
                description,
                first_trial_time,
                trial_length,
                trial_no+1,
                )
            list_fmri_objects.append(fmri_object)
    else:
        raise 'trial_length is negative or not a number. Fix it!'
    return list_fmri_objects


#%%
def convert_real_time_to_index(time_steps, cutoff_times_to_convert):
    """
    Return index values for first time steps bigger than input time-values.

    Parameters
    ----------
    times_files: 'str'
                path to file including values of time-steps
    cutoff_times_to_convert: 'list' of 'float'

    Returns
    -------
    output_list: 'list' if 'int'
                indices for time values

    """
#    text_file = open(times_files, "r")
#    time_steps = text_file.read().strip().split("\n")
    n_last = len(time_steps) - 1
    n_0 = 0
#    times_all = np.zeros(len(time_steps))
#    for cc23, one_line in enumerate(time_steps):
#        times_all[cc23] = np.float(one_line)
#    output_list = []
#    for idx, my_time in enumerate(cutoff_times_to_convert):
#        bb_d = [i for i, v in enumerate(times_all) if v > my_time]
#        output_list.append(bb_d[0])
    output_list = []
    for tt in cutoff_times_to_convert:
        my_ind_temp = [idx for idx, x in enumerate(time_steps) if x >= tt][0]
        output_list.append(my_ind_temp)
    output_list.insert(0, n_0)
    output_list.append(n_last)
    return output_list


#%% read info file
def read_info_file(info_file_name):
    """
    Read the config file.

    assigns default values to fmri_dataset object if not defined in config file.
    A 'sample_info_file.txt' accompanying the library includes standrard format.

    Parameters
    ----------
    info_file_name: 'str' or pathlib.Path
        path to config file

    Returns
    -------
    data_file_name: 'str' or pathlib.Path
        data_file_name
    mask_file_name: 'str' or pathlib.Path
        mask_file_name
    time_file_name: 'str' or pathlib.Path
        time_file_name
    dir_source: 'str' or pathlib.Path
        dir_source
    dir_save: 'str' or pathlib.Path
        dir_save
    mol_name: 'str'
        molecule name
    exp_name: 'str'
        Experiment name
    dataset_no: 'int'
        number assigned to dataset.
    cutoff_times: 'list' of 'float'
        Times in which experimental conditions changed.
    description: 'str'
        general descriptions.
    signal_name: 'str'
        name of signal. 'T1', 'T2, 'T1*', 'FISP, etc.
    """
    from  pathlib import Path

    print(info_file_name)

    try:
        with open(info_file_name) as f:
            info_file_content = f.readlines()
    except FileNotFoundError:
        raise Exception('Where is the info file???')

    dir_current = Path.cwd()
    print("---------------------------------------")
    print("Config file:", info_file_name)
    print("Current directory:", dir_current)

    # %%
    info_file_content = [x.strip() for x in info_file_content]  # remove '\n'
    info_file_content = [
        x.lstrip() for x in info_file_content
    ]  # remove leading white space
    flag_data_file = False
    flag_mask_file = False
    flag_time_file = False
    flag_dir_source = False
    flag_dir_save = False
    flag_mol_name = False
    flag_exp_name = False
    flag_dataset_no = False
    flag_description = False
    flag_cutoff_times = False
    flag_signal_name = False
    flag_first_trial_time = False
    flag_trial_length = False
    flag_time_step = False

    for line in info_file_content:
        ### DATA_FILE:
        if line[:9].lower() == "DATA_FILE".lower():
            data_file_name = line[10:].strip()
            flag_data_file = True
        ### MASK_FILE:
        elif line[:9].lower() == "MASK_FILE".lower():
            mask_file_name = line[10:].strip()
            flag_mask_file = True
        ### TIME_FILE:
        elif line[:9].lower() == "TIME_FILE".lower():
            time_file_name = line[10:].strip()
            flag_time_file = True

        ### DIR_SOURCE:
        elif line[:10].lower() == "DIR_SOURCE".lower():
            dir_source = line[11:].strip()

            dir_source = Path(dir_source)
            if not dir_source.is_absolute():
                dir_source = Path(dir_current, dir_source)
            flag_dir_source = True

        ### DIR_SAVE:
        elif line[:8].lower() == "DIR_SAVE".lower():
            dir_save = line[9:].strip()
            dir_save = Path(dir_save)
            if not dir_save.is_absolute():
                dir_save = Path(dir_current, dir_save)
                # dir_save = dir_save.resolve()
            flag_dir_save = True
        ### MOL_NAME:
        elif line[:8].lower() == "MOL_NAME".lower():
            mol_name = line[9:].strip()
            flag_mol_name = True
        ### EXP_NAME:
        elif line[:8].lower() == "EXP_NAME".lower():
            exp_name = line[9:].strip()
            flag_exp_name = True
        ### DS_NO:
        elif line[:5].lower() == "DS_NO".lower():
            dataset_no = line[6:].strip()
            try:
                dataset_no = int(dataset_no)
            except ValueError:
                raise TypeError(
                    "Only integers are allowed for DS_NO in " + info_file_name
                )
        ### FIRST_TRIAL_TIME:
        elif line[:16].lower() == "FIRST_TRIAL_TIME".lower():
            first_trial_time = line[17:].strip()
            try:
                first_trial_time = float(first_trial_time)
            except ValueError:
                raise TypeError(
                    "Only float is allowed for FIRST_TRIAL_TIME in " \
                        + info_file_name
                )
            flag_first_trial_time = True
        ### TRIAL_LENGTH:
        elif line[:12].lower() == "TRIAL_LENGTH".lower():
            trial_length = line[13:].strip()
            try:
                trial_length = float(trial_length)
            except ValueError:
                raise TypeError(
                    "Only float is allowed for TRIAL_LENGTH in " \
                        + info_file_name
                )
            flag_trial_length = True
        ### TIME_STEP:
        elif line[:9].lower() == "TIME_STEP".lower():
            time_step = line[10:].strip()
            try:
                time_step = float(time_step)
            except ValueError:
                raise TypeError(
                    "Only float is allowed for TRIAL_LENGTH in " \
                        + info_file_name
                )
            flag_time_step = True
        ### DESC:
        elif line[:4].lower() == "DESC".lower():
            description = line[5:].strip()
            flag_description = True
        ### SIGNAL_NAME
        elif line[:11].lower() == "SIGNAL_NAME".lower():
            signal_name = line[12:].strip()
            flag_signal_name = True
        ### EVENT_TIMES
        elif line[:11].lower() == "EVENT_TIMES".lower():
            cutoff_times_raw = line[12:].strip()
            if cutoff_times_raw == "":
                pass
            else:
                cutoff_times_raw = cutoff_times_raw.split(",")
                cutoff_times = []
                for el in cutoff_times_raw:
                    current_time = float(el.strip())
                    cutoff_times.append(current_time)
            flag_cutoff_times = True
        ### Whatever there was to read, it is read now.
        ### ---------------------------------------------------------
        ### handling missing data:
        ### ---------------------------------------------------------
    ###
    if not flag_dir_source:
        dir_source = Path(dir_current, "datasets")

    if not dir_source.exists():
        print('Source folder you have given me:\n', dir_source)
        import sys
        sys.exit('Source folder DOES NOT exist! :/')
    ###
    if not flag_dir_save:
        dir_save = Path(dir_current, "output")

    ###
    if not flag_data_file:
        raise "Data file name is missing in info file"
    else:
        data_file_name = Path(dir_source, data_file_name)

    ###
    if not flag_mask_file:
        raise "Mask file name is missing in info file"
    else:
        mask_file_name = Path(dir_source, mask_file_name)

    ###
    if not flag_time_file:
        time_file_name = ""
    else:
        time_file_name = Path(dir_source, time_file_name)
    ###
    if not flag_dataset_no:
        dataset_no = ""
        dir_save_ds = ""
    else:
        dir_save_ds = "DS_" + str(dataset_no) +'_'
    ###
    if not flag_exp_name:
        exp_name = "noname"
    dir_save_ds = dir_save_ds + "Exp_" + exp_name + '_'
    ###
    if not flag_mol_name:
        mol_name = ""
    else:
        dir_save_ds = dir_save_ds + "Mol_" + mol_name
    ###
    if not flag_signal_name:
        signal_name = "unknown_signal"
    dir_save = Path(dir_save, dir_save_ds, signal_name)
    ###
    if not flag_description:
        description = ""
    ###
    if not flag_cutoff_times:
        cutoff_times = ""
    ###
    if not flag_first_trial_time:
        first_trial_time = 0
    ###
    if not flag_trial_length:
        trial_length = 0
    ###
    if not flag_time_step:
        time_step = 0

    if trial_length == 0 and first_trial_time > 0:
        print("You have defined FIRST_TRIAL_TIME but not TRIAL_LENGTH or it is 0")
        raise 'Make up your mind!'


    if trial_length > 0 and (time_file_name == "" and time_step == 0):
        print("You have defined TRIAL_LENGTH but no time file or time_step.")
        raise 'Make up your mind!'

    ################################
    return (
        data_file_name,
        mask_file_name,
        time_file_name,
        dir_source,
        dir_save,
        mol_name,
        exp_name,
        dataset_no,
        cutoff_times,
        description,
        signal_name,
        first_trial_time,
        trial_length,
        time_step
    )


#%%
def main_get_data(info_file_name):
    """
    Read actual data based on info_file_name.

    uses read_info_file to read the config file and then loads the data.
    A 'sample_info_file.txt' accompanying the library includes standrard format.
    Run mitfat.file_io.print_info() to see how config files should be organised.


    Parameters
    ----------
    info_file_name : 'str' or pathlib.Path
        config file.

    Returns
    -------
    data_nii_masked: 'numpy.ndarray',
        (N_time_steps, N_voxels)
    mask_roi_numpy: 'numpy.ndarray',
        (d1, d2, d3)
    time_steps: 'list' of 'float'
        time steps
    signal_name: 'str'
        signal name
    indices_cuttoff: 'list' if 'int'
        times in which experimental condtions changed.
    experiment_name: 'str'
        name
    dataset_no: 'int'
        dtaaset number
    mol_name: 'str'
        name of moecule
    dir_source:
        source folder
    dir_save: 'str' or pathlib.Path
        where to save
    mask_roi_numpy: Numpy.ndarray
        maks for voxels to consider
    description: 'str'
        descriptions for dataset
    """
    import numpy as np
    import nibabel

#    from mitfat import flags

    mask_roi = []
    mask_roi_numpy = []

    data_file_name, mask_file_name, time_file_name, dir_source, \
            dir_save, mol_name, experiment_name, dataset_no, \
            cutoff_times, description, signal_name, \
            first_trial_time, trial_length,\
            time_step = read_info_file(info_file_name)

    print("----------------------------------------")
    print("reading data from: ", dir_source)
    print("outputs will be saved in: ", dir_save)
    print("----------------------------------------")

    data_roi = nibabel.load(data_file_name)
    mask_roi = nibabel.load(mask_file_name)
    mask_roi_numpy = mask_roi.get_data()
    # following line added in case mask values are not set at 1.
    mask_roi_numpy[mask_roi_numpy != 0] = 1
    ## applying the mask and storing data in 2D format in a list
    from nilearn.masking import apply_mask

    data_nii_masked = apply_mask(data_roi, mask_roi)
#    if flags.if_debug:
#        from mitfat.func_tests import check_how_nilearn_apply_mask_works
#        check_how_nilearn_apply_mask_works(data_nii_masked, data_roi)

    data_nii_masked = np.abs(
        data_nii_masked
    )  # in case data is recorded as negative values

    (d1, d2) = data_nii_masked.shape
    mask_size = np.sum(mask_roi_numpy)
    if d1 == mask_size:
        data_nii_masked = np.transpose(data_nii_masked)
    elif d2 == mask_size:
        pass
    else:
        print("mask size does not match data dimesnion ---------")
        print("Data dimensions: ", data_nii_masked.shape)
        print("Mask size: ", np.sum(mask_roi_numpy))


    if not time_file_name == "":
        text_file = open(time_file_name, "r")
        time_steps_raw = text_file.read().strip().split("\n")
        time_steps = np.zeros(len(time_steps_raw))
        for cc23, one_line in enumerate(time_steps_raw):
            time_steps[cc23] = np.float(one_line)
        text_file.close()
    else:
        if time_step > 0:
            time_steps = np.arange(data_nii_masked.shape[0]) * time_step
        else:
            time_steps = np.arange(data_nii_masked.shape[0]) + 1

#    if not (time_file_name == "" and cutoff_times == ""):
#        time_steps_min = np.min(time_steps)
#        time_steps_max = np.max(time_steps)
#        for el in cutoff_times:
#            if el < time_steps_min or el > time_steps_max:
#                raise ValueError(
#                    "EVENT_TIMES exceed time step values in TIME_FILE in "
#                    + info_file_name
#                )
#        indices_cuttoff = convert_real_time_to_index(time_steps, cutoff_times)
#    else:
#        indices_cuttoff = [0, data_nii_masked.shape[0] - 1]

    time_steps_min = np.min(time_steps)
    time_steps_max = np.max(time_steps)
    for el in cutoff_times:
        if el < time_steps_min or el > time_steps_max:
            raise ValueError(
                "EVENT_TIMES exceed time step values in TIME_FILE in "
                + info_file_name
            )

    return (
        data_nii_masked,
        mask_roi_numpy,
        time_steps,
        signal_name,
        cutoff_times,
        experiment_name,
        dataset_no,
        mol_name,
        dir_source,
        dir_save,
        description,
        first_trial_time,
        trial_length,
    )
