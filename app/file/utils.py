import glob
import pandas as pd
from typing import List, Union
import os

def read_csv_directory(directory: str, columns: List[str] = None, filelimit: int = None) -> pd.DataFrame:
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
    files = glob.glob(directory + '/*.csv')
    data_frames = []
    filecount = 0

    for filename in files:
        df = pd.read_csv(filename, index_col = None, header = 0)
        include_df = True

        if columns is not None:
            for column in columns:
                if column not in df.columns:
                    include_df = False
                    break
        
        if include_df:
            df = pd.read_csv(filename, index_col = None, header = 0)
            data_frames.append(df[columns])
            filecount += 1
        
        if filelimit is not None and filecount >= filelimit:
            break

    return pd.concat(data_frames, axis = 0, ignore_index = True)

def get_absolute_path(path: str):
    if not path.startswith(os.path.sep):
        path = os.getcwd() + os.path.sep + path

    return path