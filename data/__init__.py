def schools():
    return pd.read_csv('school_master.csv',encoding='utf-8')

def fortune_500():
    return pd.read_csv('fortune_master.csv',encoding='utf-8')