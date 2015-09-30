"""
A set of functions to help getting data on the movement of individuals.
"""

def get_movement_individual(profile_df,idx_cols=None,track=None):
    """ Create a dataframe of movements """
    # Check if cols is in the set of columns
    if type(idx_cols) == type('string'):
        idx_cols = [idx_cols]
    if idx_cols != None:
        missing = set(idx_cols) - set(profile_df.columns) # User specified but missing in df
        check_cols = len(missing) == 0 
    else:
        check_cols = True
    if check_cols == False:
        print "Missing columns: "
        print missing
        raise KeyError("Columns in 'idx_cols' need to be in 'profile_df'! Try adding those back in. ")
    
    # Reset index 
    profile_df = profile_df.reset_index(drop=True)

    # Is it a row vector, hence no movement?
    if type(profile_df) == type(Series()):
        profile_df = DataFrame(profile_df).T.reset_index()
    else:
        profile_df = profile_df.reset_index()
    
    # Which columns are fixed?
#     col_no_info = profile_df.columns[profile_df.apply(lambda x: len(x.unique()))==1]
    col_no_info = idx_cols
    add_later = profile_df[col_no_info].reset_index().iloc[0]
    profile_df = profile_df.drop(col_no_info,axis=1)
    
    # If the number of columns is just one, need to reset index.
    if len(profile_df.columns) == 1:
        profile_df['filler'] = 0
    else:
        pass
#     if cols == None:
#         pass
#     elif len(cols)>1:
#         profile_df = profile_df[list(cols)]
#     else:
#         profile_df = profile_df[list(cols)].reset_index(drop=True)
    
    # Create left and right dataframes
    left_df = profile_df.copy()
    left_df.loc[-1]='START'
    left_df = left_df.sort().ix[:,1:]
    result_cols = [cname+'_from' for cname in left_df.columns]
    
    right_df = profile_df.copy()
    right_df.loc[len(right_df)+1]='END'
    right_df = right_df.sort().ix[:,1:]
    result_cols = result_cols + [cname+'_to' for cname in right_df.columns]
    
    # Merge left and right dataframes
    result = pd.concat([left_df.reset_index().ix[:,1:],right_df.reset_index().ix[:,1:]],axis=1,ignore_index=True)
    result.columns = result_cols
    
    # Add identifying information
    for i,colname in enumerate(col_no_info):
        result[colname] = add_later[i+1]
        
    # Add columns for movement, stationary, and endpoints
    if track == None:
        pass
    else:
        endpoints = (result.index == result.index[0]) | (result.index==result.index[len(result)-1])
        promotion = result[track+'_from'] == result[track+'_to']
        result['movement'] = True
        result.loc[endpoints,'movement'] = False
        result.loc[promotion,'movement'] = False
        result['endpoints'] = endpoints
    return result[sorted(result.columns)]

def count_jumps(input_df,jumploc,desire='bool'):
    """ Create boolean variable for job mobility patterns of the form X->Y->X """
    found_idx = input_df.loc[input_df.state_final.notnull()].reset_index()
    found_idx = found_idx.loc[found_idx.state_final == jumploc].index.tolist()
    # Issue: Currently doing this is really slow because I didn't want the code to get messy and long, but should nest the if/else clauses
    if len(found_idx)<=1:
        result = (False,0,0,0)
    else:
        dist = []
        for i in range(len(found_idx)-1):
            temp_dist = found_idx[i+1]-found_idx[i]
            if temp_dist >= 2:
                dist.append(temp_dist)
        # How many greater than one jumps?
        if len(dist) > 0:
            result = (True,np.mean(dist),len(dist),max(dist))
        else:
            result = (False,0,0,0)
    if desire == 'bool':
        return result[0]
    elif desire == 'mean':
        return result[1]
    elif desire == 'count':
        return result[2]
    elif desire == 'max':
        return result[3]
    else:
        return result[0]
    
# Indicator for whether the person spent time in CA, then another place, then back to CA
def get_jumps(input_df,state,id_col='index'):
    """ Return a Series object of statistics related to job location patterns of the form X->Y->X """
    means = input_df.groupby(id_col).apply(lambda x: count_jumps(x,state,'mean'))
    bools = input_df.groupby(id_col).apply(lambda x: count_jumps(x,state,'bool'))
#     cts = df.groupby('index').apply(lambda x: count_jumps(x,state,'count'))
#     maxs = df.groupby('index').apply(lambda x: count_jumps(x,state,'max'))
#     result = pd.concat([bools,cts,means,maxs],axis=1)
    result = pd.concat([bools,means],axis=1)
    result.columns = ['jump_'+state,'time_'+state]
    return result