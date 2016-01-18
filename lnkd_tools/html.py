#!/usr/bin/env python
""" 
Collection of functions for working with HTML data 

"""
import lxml.html
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import mechanize
import cookielib
import random
from time import sleep

"""
Create mechanize browser that is difficult to catch

"""
# List of headers that I can use.
headerslist = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'), ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'),('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:39.0) Gecko/20100101 Firefox/39.0'),('User-agent','Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'), ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16'), ('User-agent','Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'),('User-agent','Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'),('User-agent','Mozilla/5.0 (X11; U; Linux i686; fr-fr) AppleWebKit/525.1+ (KHTML, like Gecko, Safari/525.1+) midori/1.19'),('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'),('User-agent','Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'),('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')]

def initialize_browser(inputurl=""):
    ''' Return mechanize browser object with appropriate headers and cookie handling.
    '''
    print('Initializing browser...')
    #Handles all the browser details 
    br = mechanize.Browser()
    
    br.addheaders = [random.choice(headerslist)]

    #Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    return br

"""
HTML to CSV

"""

def from_text(input_str,url=''):
    """ If input_str is a LinkedIn profile source, returns two dataframes: one for education, one for work experience """
    tree = lxml.html.fromstring(input_str)
    # Try getting url of page if url not specified
    # if url == '':
    #     try:
    #         url = tree.xpath('//div[@class="public-profile"]//a/@href')
    #         print url
    #         if url == []:
    #             url = ''
    #     except:
    #         pass
    # else:
    #     pass

    # Get Name
    try:
        name = tree.xpath('//span[@class="full-name"]/text()')[0]
    except:
        print('No name for',url,', skipping.')
        positions = DataFrame({'company-name':'NaN','company-location':'NaN','end-date':'NaN','id':url,'industry':'NaN','industry':'NaN','location':'NaN','name':'NaN','name':'NaN','num-connections':'NaN','start-date':'NaN','summary':'NaN','summary':'NaN','title':'NaN'},index=[0])
        educations = DataFrame({'degree':'NaN','id':url,'industry':'NaN','location':'NaN','major':'NaN','name':'NaN','num-connections':'NaN','school-end-date':'NaN','school-name':'NaN','school-start-date':'NaN'},index=[0])
        return (positions,educations)
    try:
        location = tree.xpath('//span[@class="locality"][1]/text()')[0]
    except:
        location = ''
    try:
        connections = tree.xpath('//div[@class="member-connections"][1]/strong/text()')[0]
    except:
        connections = ''
    try:
        industry = tree.xpath('//dd/text()')[0]
    except:
        industry = ''
    
    # Download work information
    positions = []
    site_positions = tree.xpath('//div[@id="background-experience"]/div')
    numpos=len(site_positions)
    for p in range(numpos):
        pdict={}
        try:
            pdict['title'] = tree.xpath('//div[@id="background-experience"]/div['+str(p+1)+']//h4//text()')[0]
        except:
            pdict['title'] = 'NaN'
        try:
            pdict['company-name'] = tree.xpath('//div[@id="background-experience"]/div['+str(p+1)+']//h5//text()')[0]
        except:
            pdict['company-name'] = 'NaN'
        try:
            pdict['summary'] = tree.xpath('//div[@id="background-experience"]//p[@dir]['+str(p+1)+']/text()')[0]
        except:
            pdict['summary'] = 'NaN'
        try:
            pdict['company-location'] = tree.xpath('//div[@id="background-experience"]/div['+str(p+1)+']//span[@class="locality"]//text()')[0]
        except:
            pdict['company-location'] = 'NaN'
        try:
            pdict['start-date'] = tree.xpath('//div[@id="background-experience"]/div['+str(p+1)+']//time//text()')[0]
        except:
            pdict['start-date']='NaN'
        try:
            pdict['end-date'] = tree.xpath('//div[@id="background-experience"]/div['+str(p+1)+']//time//text()')[1]
        except:
            pdict['end-date']='NaN'
        positions.append(pdict)
    
    # Get education data
    educations = []
    site_educations = tree.xpath('//div[@id="background-education"]/div')
    numeduc = len(site_educations)
    for p in range(numeduc):
        edict={}
        try:
            edict['school-name'] = tree.xpath('//div[@id="background-education"]/div['+str(p+1)+']//h4//text()')[0]
        except:
            edict['school-name'] = 'NaN'
        try:
            edict['degree'] = tree.xpath('//div[@id="background-education"]/div['+str(p+1)+']//span[@class="degree"]//text()')[0]
        except:
            edict['degree'] = 'NaN'
        try:
            edict['major'] = tree.xpath('//div[@id="background-education"]/div['+str(p+1)+']//span[@class="major"]//text()')[0]
        except:
            edict['major'] = 'NaN'
        try:
            edict['school-start-date'] = tree.xpath('//div[@id="background-education"]/div['+str(p+1)+']//span[@class="education-date"]/time[1]/text()')[0]
        except:
            edict['school-start-date'] = 'NaN'
        try:
            edict['school-end-date'] = tree.xpath('//div[@id="background-education"]/div['+str(p+1)+']//span[@class="education-date"]/time[2]/text()')[0].replace(u'\u2013','').strip()
        except:
            edict['school-end-date'] = 'NaN'
        educations.append(edict)

    # Recommendations
    # Try getting the number of recommendations. If these don't show up, give up.
    try:
        recs_given = Series(tree.xpath('//li[@class="nav-given"]//text()')[0]).str.extract('([0-9]+)')[0]
    except:
        recs_given = np.nan

    # Finish and add id column etc
    positions = DataFrame(positions)
    positions['id'] = url
    positions['name'] = name 
    positions['industry'] = industry
    positions['num-connections'] = connections 
    positions['location'] = location
    positions['endorsements-given'] = recs_given

    educations = DataFrame(educations)
    educations['id'] = url
    educations['name'] = name 
    educations['industry'] = industry
    educations['num-connections'] = connections 
    educations['location'] = location
    return positions, educations

# The following is temporary code. 
def wrapper():
    """ Process scraped files and return a concatenated dataframe of all files """
    outputdir = "/Users/dokim/Documents/Projects/Movement/YelpTA/"
    base_dir = "/Users/dokim/Documents/Projects/Movement/"

    # Read urldf
    urldf = pd.read_csv(base_dir+'temp.csv',encoding='utf-8')
    urldf['source'] = ''
    urldf.loc[0:1086,'source'] = 'TripAdvisor'
    urldf.loc[1086:,'source'] = 'Yelp'

    # # Remove people that I don't want
    # urldf = urldf.loc[~urldf.url.str.contains('/dir/')]
    # urldf['fixedurl'] = urldf.url.str.split('?').str.get(0)
    # urldf = urldf.drop_duplicates('fixedurl')
    # urldf['counts'] = urldf.groupby('name')['url'].transform('count')

    # data_dir = '/Users/dokim/Documents/Projects/Movement/YelpTA/'
    # filelist = [n for n in urldf.name.tolist() if n != 'Megan Coger, PHR/SHRM-CP']
    # filelist = filelist + ['Megan Coger']
    # filelist = [f for f in filelist if (f.endswith('.txt')) & (f!='log.txt')]
    reference = urldf[['name','url']].set_index('name')
    p_all = []
    e_all = []
    exception_count = 0
    exception_list = []
    for f in filelist:
        try:
            with open(data_dir+f+'.txt','r') as raw:
                input_str = raw.read()
                url = reference.loc[f,'url']
                if type(url) == type(Series()):
                    url = reference.loc[f,'url'][-1]
                (p_df, e_df) = crt_df_from_string(input_str, url)
                # want to use this to get movement, but need to add 'first-name' and 'last-name' to the df columns
                p_df['first-name'] = f.split()[0]
                p_df['last-name'] = ' '.join(f.split()[1:])
                p_all.append(p_df)
                e_all.append(e_df)
        except:
            exception_count = exception_count + 1
            exception_list.append(f)
    print(exception_count,'errors stored in exception_list')
    if len(exception_list) < 10:
        print(exception_list)
    prof_df = pd.concat(p_all)
    prof_df = prof_df.rename(columns={'id':'public-profile-url'})
    educ_df = pd.concat(e_all)
    return (educ_df, prof_df, exception_list)