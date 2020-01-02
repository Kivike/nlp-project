import glob
import pandas as pd
from typing import List, Union
import os

def read_csv_directory(
    directory: str,
    columns: List[str] = None,
    filelimit: int = None,
    filetype: str = 'csv'
    ) -> pd.DataFrame:
    """Read csv files from a directory and combine into one single DataFrame. The
    limit can be set in order to prevent awkward memory issues.
    
    Arguments:

        directory {str} -- The directory path
    
    Keyword Arguments:

        columns {List[str]} -- The columns to include into the combined data (default: {None})

        filelimit {int} -- The limit of files to read (default: {None})
    
    Returns:

        DataFrame -- The data combined into a single DataFrame
    """
    assert filetype in ['csv', 'xlsx'], 'File type must be csv or xlsx'

    files = glob.glob(directory + '/*.' + filetype)
    data_frames = []
    filecount = 0

    for filename in files:
        if filetype == 'csv':
            df = pd.read_csv(filename, index_col = None, header = 0)
        else:
            df = pd.read_excel(filename, index_col = None, header = 0)

        include_df = True

        if columns is not None:
            for column in columns:
                if column not in df.columns:
                    include_df = False
                    break
        
        if include_df:
            if columns is not None:
                data_frames.append(df[columns])
            else:
                data_frames.append(df)
            filecount += 1
        
        if filelimit is not None and filecount >= filelimit:
            break

    return pd.concat(data_frames, axis = 0, ignore_index = True, sort = False)

def get_absolute_path(path: str):
    """
    Convert relative path of caller to absolute path,
    or simply returns the path if it is already absolute
    """
    if not path.startswith(os.path.sep):
        path = os.getcwd() + os.path.sep + path

    return path
