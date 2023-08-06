"""Miscellaneous tools.

"""
import os
import csv

from scipy.io import loadmat
import pandas as pd

def num_to_ith(num):
    """Converts an integer to a string containing an ordinal number (1st, 2nd, 3rd, ect.)
    
    Parameters
    ----------
    num : int
        Number
    
    Returns
    -------
    str
        Ordinal number

    """    
    if num == -1:
        return 'last'
    elif num < -1:    
        value = str(num+1).replace('-', '')
    else:
        value = str(num)
    
    last_digit = value[-1]

    if len(value) > 1 and value[-2] == '1':
        suffix = 'th'
    elif last_digit == '1':
        suffix = 'st'
    elif last_digit == '2':
        suffix = 'nd'
    elif last_digit == '3':
        suffix = 'rd'
    else:
        suffix = 'th'

    if num < -1:
        suffix += ' to last'

    return  value + suffix

def read_data_string(text, delimiter=',', newline='\n', has_headerline=True):
    """Reads a delimited string into a list of dictionaries.  Functions very similar to :meth:`numpy.genfromtxt`, but for strings instead of text files.
    
    Parameters
    ----------
    text : str
        String of row/column data with delimiters and new line indicators given in `delimiter` and `newline`.
    delimiter : str, optional
        Delimiter used in `text`, by default ','
    newline : str, optional
        New line indicator used in `text`, by default '\n'
    has_headerline : bool, optional
        If True, treats the first line of `text` as headers. If False, treats the first line of `text` as data and makes generic headers, by default True
    
    Returns
    -------
    :obj:`list` of :obj:`dict`
        A list of dictionaries containing the data from `text`

    """
    lines = text.split(newline)
    
    # Generate headers
    if has_headerline:
        # If the text has headerlines, get them
        headers = lines.pop(0).split(delimiter)

    else:
        # If the text doesn't have headerlines, make generic ones
        headers = [str(i+1) for i in range(len(lines[0].split(delimiter)))]
    
    data = []
    for line in lines:
        # For each line, check if data is missing
                
        if len(line.split(delimiter)) == len(headers):
            # If there is no missing data on this line, initialize a dictionary for the line data
            line_data = {}       
            
            for header, value in zip(headers, line.split(delimiter)):
                # For each column in the line, add to the line_data dict (header as key and value as value)
                line_data[header] = value
            
            # Append the line_data dict to the data list
            data.append(line_data)

    return data

def convert_path(filepath):
    """Converts the slashes in `filepath` to whatever is appropriate for the current OS.
    
    Parameters
    ----------
    filepath : str
        Filepath to be converted
    
    Returns
    -------
    str
        Converted filepath

    """
    return os.path.normpath(filepath.replace('\\', os.sep).replace('/', os.sep))

def mat_to_pd(filename, data_start=None, data_end=None):
    """Creates a pandas dataframe from a .mat file
    
    Parameters
    ----------
    filename : str
        Filename of a .mat file
    
    Returns
    -------
    dataframe
        Pandas datafrom of data in `filename`

    """
    mat = loadmat(filename)  # load mat-file
    
    dataframes = []
    
    for variable in [var for var in mat if var not in ['__header__', '__globals__', '__version__']]:        
        
        if mat[variable].shape[1] == 1:
            array = mat[variable]
        elif mat[variable].shape[0] == 1:
            array = mat[variable].transpose()
        else:
            raise ValueError(f'{filename} does not contain the expected data!')
        
        # Figure out data start and end indices if given
        if data_start is None:            
            data_start = 0            
        if data_end is None:
            data_end = len(array)

        dataframes.append(pd.DataFrame(array[data_start:data_end], columns=[variable]))

    dataframe = pd.concat(dataframes, axis=1)

    return dataframe

def dict_to_csv(data, filename):
    """Writes data in `dict` to a csv file with the keys as headers and the values as columns.
    
    Parameters
    ----------
    data : dict
        Dictionary of data
    filename : str
        Name of file to write data to. (include extension)

    """
    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))
