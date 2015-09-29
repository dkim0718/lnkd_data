import pandas as pd 
from pandas import DataFrame, Series

def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')

def tempdf():
    return Series([0,1,2,3,4,5,6,7,8,9,10]).mean()