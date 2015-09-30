import pandas as pd 
import pkg_resources, os 

resource_package = __name__  ## Could be any module/package name.

def get_data(input_arg):
    """ Return the dataframes for data collected online """ 
    if input_arg == "school":
        resource_path = os.path.join('lnkd_data/data', 'school_master.csv')
        
    elif input_arg == "fortune":
        resource_path = os.path.join('lnkd_data/data', 'fortune_master.csv')
    else:
        resource_path = ''
        print ("Specify a file name: 'school' or 'fortune'")
        raise NameError('Unknown file specified.')
    return pd.read_csv(resource_path,encoding='utf-8')