def loop_merge(inputdir,on_df,on_list):
    """Loops through inputdir, merging each csv file with on_df"""
    result = []
    csv_list = [f for f in os.listdir(inputdir) if f.endswith(".csv")]
    # For error handling if a Series object is passed instead of a dataframe
    if type(on_df)==type(Series()):
        on_df = DataFrame(on_df)
        on_df.columns = on_list
    
    for (i, csvfile) in enumerate(csv_list):
        print('Looping through',i,'of',len(csv_list))
        df = pd.read_csv(inputdir+csvfile, header=None,encoding='utf-8')
        try:
            df.columns = [u'degree', u'end-date', u'field-of-study', u'first-name', u'last-name', u'public-profile-url', u'school-name', u'start-date']
        except:
            df.columns = [u'company-name', u'end-date',u'first-name', u'industry', u'is-current', u'last-name', u'location', u'num-connections', u'public-profile-url', u'start-date', u'summary', u'title']
        filtered = pd.merge(df, on_df, on=on_list, how='inner')
        result.append(filtered)
    result = pd.concat(result)
    return result