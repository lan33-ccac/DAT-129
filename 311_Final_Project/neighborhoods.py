# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:15:45 2019

@author: lnydi
"""

import pandas as pd

def main():
    process_df()
    
    
def process_df():
    df = pd.read_csv('311.csv', ',')
    
    df = df.loc[:, ['REQUEST_ID', 'NEIGHBORHOOD']]
    df.columns = ['Counts', 'Neighborhood']
    
    df = df.groupby(['Neighborhood'])
    df = df.count()
    print(df)
    
    df.to_csv('Neighborhood_311_Counts.csv')
    
    








###################################################################################################
if __name__=='__main__':
    main()