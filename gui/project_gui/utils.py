import csv
import pandas as pd

path='gui_data.csv'

class Utils:
    
    @staticmethod
    def read_data(path):
        Utils.data=pd.read_csv(path)

    @staticmethod
    def sort_data(col_name,desc):
        Utils.read_data(path)
        if desc:
            df=Utils.data.sort_values(by=col_name,ascending=False)
        else:
            df=Utils.data.sort_values(by=col_name)
        return df

