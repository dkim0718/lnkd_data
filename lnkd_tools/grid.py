#!/usr/bin/env python
"""
Collection of functions for working on the grid
"""
import pandas as pd
import numpy as numpy
from pandas import DataFrame, Series
import os 

def loop_merge(inputdir,on_df,on,keep=None,resultname='loop_df.csv',split=False):
    """Loops through inputdir, merging each csv file with on_df"""
    result = []

    # If user passes a string instead of a list
    if type(on) == type('string'):
        on = [on]


    # Shorthand notation for directories
    if (inputdir=='educ') | (inputdir=='education'):
        inputdir = '/export/home/doctoral/dokim/Linkedin/Education/'
    elif (inputdir=='prof') | (inputdir=='profile'):
        inputdir = '/export/home/doctoral/dokim/Linkedin/Output/'
    csv_list = [f for f in os.listdir(inputdir) if f.endswith(".csv")]


    # For error handling if a Series object is passed instead of a dataframe
    if type(on_df)==type(Series()):
        on_df = DataFrame(on_df)
        on_df.columns = on_list


    # To display summaries when finished
    totlen = 0
    totsum = 0


    # Loop each directory and mere
    for (i, csvfile) in enumerate(csv_list):
        print('Looping through',i,'of',len(csv_list))
        df = pd.read_csv(inputdir+csvfile, header=None,encoding='utf-8')
        try:
            df.columns = [u'degree', u'end-date', u'field-of-study', u'first-name', u'last-name', u'public-profile-url', u'school-name', u'start-date']
        except:
            df.columns = [u'company-name', u'end-date',u'first-name', u'industry', u'is-current', u'last-name', u'location', u'num-connections', u'public-profile-url', u'start-date', u'summary', u'title']
        filtered = pd.merge(df, on_df, on=on_list, how='inner')


        # Keep only relevant columns
        if keep==None:
            pass
        else:
            filtered = filtered.ix[:,keep].drop_duplicates()


        # Split the result into multiple files?
        if split==False:
            if i == 0:
                filtered.to_csv(resultname,encoding='utf-8')
            else:
                filtered.to_csv(resultname,encoding='utf-8',mode='a',header=False)
        else:
            filtered.to_csv(resultname+'_'+str(i)+'.csv',encoding='utf-8')


        # How many people do we have?
        totlen += len(filtered)
        totsum += len(filtered['public-profile-url'].unique())
        # result.append(filtered)

    # result = pd.concat(result)
    print "Final dataframe is %s rows long containing %s unique individuals." % (totlen, totsum)
    return result