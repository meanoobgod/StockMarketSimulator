"""
What this program is suppose to do?

this program will take to dataset of time sereas data (csv) and a list of token names,
then it will take the time-frame they are working in, 
now this program will return a list containing (suppose a timeframe 15m, and 1m)
a[0] = the first row from the larger timeframe (15m row),
a[1] .. a[n-1] = the underlying 1 min data rows
lastly
a[n] = next row of larger data.  
for any given open time, close time.

"""

import os
from functools import cache
import numpy as np
import pandas as pd

class LoadData():
    @cache
    def __init__(self, path_of_higher_timeframe: str, path_of_lower_timeframe:str, suffix:str, index_col: str = None, parent_token:str = None, header = None)  -> None:
        """
            path_of_higher_timeframe: str = path to the nearest folder, of the folder containg the higher timeframe dataset
            path_of_lower_timeframe: str = path to the nearest folder, of the folder containg the higher timeframe dataset
        """
        assert type(path_of_higher_timeframe) == type(path_of_lower_timeframe) == type(suffix) == str#!!!checks if the path is string or not
        assert os.path.exists(path_of_higher_timeframe) and os.path.exists(path_of_lower_timeframe)#!!! if the given path exists
        if parent_token == None: raise ValueError("Need a parent_token!!") #!!! parent_token is important!!
        
        self.parent_token = parent_token
        self.Higher_path = path_of_higher_timeframe
        self.Lower_path = path_of_lower_timeframe
        self.suffix = suffix
        self.index_col = index_col
        self.header  = header
        self.higher_timeframe_dataset = None
        self.lower_timeframe_dataset = None
    
    def GetTokenName(self) -> list:
        higher_file = set([_ for _ in os.listdir(self.Higher_path) if _[-4:] == self.suffix])
        lower_file = set([_ for _ in os.listdir(self.Higher_path) if _[-4:] == self.suffix])
        return list(higher_file.intersection(lower_file))

    @cache
    def ImportTokens(self) -> list:
        token = self.GetTokenName()

        higher_dataset = {}
        lower_dataset = {}

        if len(token) == 0:
            raise "Their is no token to work with!" 
        
        for _ in token:
            higher_dataset[_] = pd.read_csv(f"{self.Higher_path}//{_}" , index_col= self.index_col, header=self.header)
            lower_dataset[_] = pd.read_csv(f"{self.Lower_path}//{_}", index_col= self.index_col, header= self.header)
        
        self.higher_timeframe_dataset = higher_dataset 
        self.lower_timeframe_dataset = lower_dataset

    @cache
    def GettingIndex(self) -> list:
        parent_dataframe = pd.read_csv(f"{self.Higher_path}//{_}", header= self.header)
        child_dataframe = pd.read_csv(f"{self.Lower_path}//{_}", header= self.header)
        _ = parent_dataframe.open_time.values
        a_0 = _[0]
        n = len(_)
        d = _[1] - a_0
        a_n = a_0 + (n - 1) * d
        parent_open_time_range = range(a_0, a_n + d, d)

        _ = child_dataframe.open_time.values
        a_0 = _[0]
        n = len(_)
        d = _[1] - a_0
        a_n = a_0 + (n - 1) * d
        child_open_time_range = range(a_0, a_n + d, d)
        return [parent_dataframe, child_dataframe]

    @cache
    def StreamingData(self, token:str, i, j) -> list:
        #importing Data
        if self.higher_timeframe_dataset == None or self.lower_timeframe_dataset == None:
            raise ValueError("Please run `ImportTokens` first!!")
        return [self.higher_timeframe_dataset[token].loc[[i]], lower_timeframe_dataset[token].loc[i: j]]

