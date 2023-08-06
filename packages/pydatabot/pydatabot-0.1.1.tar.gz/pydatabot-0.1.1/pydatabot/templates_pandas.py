import pandas as pd 
import numpy as np 


# data load & initial part: Import / Create / Load operations

# data query & detect part: Query Operations + Sort Operations + Group Operations

# data pre-process & clean part: Edit Operations + Time series Operations

# data feature enginering & statistical analysis part: correlation / various feature selection 

# data modelling part: model construction (regression / classification / cluster)

# data visualization part. 


'''Create / Load Operations'''
def import_packages(import_packages):
    '''
    This function will import all necessary packages for data analytics
    '''
    if import_packages:
        tem = import_packages.split(',')
        res = [i.strip() for i in tem]
        template = ""
        if 'pandas' in res:
            template += "import pandas as pd\n"
        if 'numpy' in res:
            template += "import numpy as np\n"
        if 'matplotlib' in res:
            template += "import matplotlib.pyplot as plt\n"
        if 'os' in res:
            template += "import os\n"
        if 'sys' in res:
            template += "import sys\n"
    else:
        template = "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport os\nimport sys\n\n"
           
    return template


def load_data(file_path, dataframe_name, file_type):
    '''
    This function will load the dataset from file_path
    '''
    if file_type == 'csv':
        template = "df = pd.read_csv('file_path', header, index_col=0, sep)\n".replace('file_path', file_path) if file_path else "df = pd.read_csv('file_path', header, index_col=0, sep)\n"
    elif file_type == 'text':
        template = "df = pd.read_table('file_path', header, index_col=0, sep)\n".replace('file_path', file_path) if file_path else "df = pd.read_table('file_path', header, index_col=0, sep)\n"
    elif file_type == 'json':
        template = "df = pd.read_json('file_path', orient)\n".replace('file_path', file_path) if file_path else "df = pd.read_json('file_path', orient)\n"
    elif file_type == 'excel':
        template = "df = pd.read_excel('file_path', header, index_col=0)\n".replace('file_path', file_path) if file_path else "df = pd.read_excel('file_path', header, index_col=0)\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def save_data(file_path, dataframe_name, file_type):
    '''
    This function will save the dataset to file_path
    '''
    if file_type == 'csv':
        template = "df = pd.to_csv('file_path', header, index_col=0, sep)\n".replace('file_path', file_path) if file_path else "df = pd.to_csv('file_path', header, index_col=0, sep)\n"
    elif file_type == 'text':
        template = "df = pd.to_table('file_path', header, index_col=0, sep)\n".replace('file_path', file_path) if file_path else "df = pd.to_table('file_path', header, index_col=0, sep)\n"
    elif file_type == 'json':
        template = "df = pd.to_json('file_path', orient)\n".replace('file_path', file_path) if file_path else "df = pd.to_json('file_path', orient)\n"
    elif file_type == 'excel':
        template = "df = pd.to_excel('file_path', header, index_col=0)\n".replace('file_path', file_path) if file_path else "df = pd.to_excel('file_path', header, index_col=0)\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def create_dataframe(specific_column_name, dataframe_name):
    '''
    This function will create new dataframe
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = pd.DataFrame(columns=[{}])\n".format(str(res).strip('[]')) 
    else: 
        template = "df = pd.DataFrame()  # Option: add 'columns=[column_names]'\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Query Operations'''
def index_info():
    '''
    This function will return all index to user
    '''
    template = 'index = df.index\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def column_name_all(dataframe_name):
    '''
    This function will return name of all columns in dataset
    '''
    template = 'columns = df.columns\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def dataset_length(dataframe_name):
    '''
    This function will return length of dataset.
    '''
    template = 'df_length = len(data)\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def dataset_shape(dataframe_name):
    '''
    This function will return shape of dataset.
    '''
    template = 'df_shape = df.shape\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def dataset_dtype(dataframe_name):
    '''
    This function will return type of dataset.
    '''
    template = 'df_type = df.dtypes\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def dataset_describe(dataframe_name):
    '''
    This function will return statistical metrics of dataset.
    '''
    template = 'df_describe = df.describe()\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def extract_specific_column_by_name(specific_column_name, dataframe_name):
    '''
    This function will return one or some specific columns in dataset
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_columns = data.loc[:,[specified_column_name]]\n".replace('specified_column_name', str(res).strip('[]')) 
    else: 
        template = "df_columns = data.loc[:,['specified_column_name']]\n"

    if dataframe_name:
        template = template.replace('data', dataframe_name) 

    return template


def extract_specific_row_by_index(number, dataframe_name):
    '''
    This function will return one or some specific rows in dataset
    '''
    template = "df_rows = df.iloc[number]\n".replace("number", number) if number else "df_rows = df.iloc[index]\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def head_overview(number, dataframe_name):
    '''
    This function will return first numb_of_rows of dataframe.
    ''' 
    template = "df.head(number)\n".replace("number", number) if number else "df.head()\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def tail_overview(number, dataframe_name):
    '''
    This function will return last numb_of_rows of dataframe.
    ''' 
    template = "df.tail(number)\n".replace("number", number) if number else "df.tail()\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def nan_matrix(dataframe_name):
    '''
    This function will return nan matrix of original dataframe.
    ''' 
    template = "df.isna() # or we can use df.isnull()\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def where_nan(dataframe_name):
    '''
    This function will return concrete position of NaN value in original dataframe.
    ''' 
    template = "np.where(df.isna()) \n# df.index[np.where(df.isna())[0]] # This function can tell us in which rows existing NaN\n# df.columns[np.where(df.isna())[1]] # This function can tell us in which columns existing NaN\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template
    

def where_specified_element(specific_element, dataframe_name):
    '''
    This function will return position of this specified_element in original dataframe.
    ''' 
    if specific_element:
        tem = specific_element.split(',')
        res = [i.strip() for i in tem]
        template = "np.where(df == specified_element)\n".replace('specified_element', str(res).strip('[]')) 
    else: 
        template = "np.where(df == specified_element)\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def unique_value_in_specific_column(specific_column_name, dataframe_name):
    '''
    This function will return unique value of this specified cloumn in original dataframe.
    ''' 
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df[specific_column_name].unique()\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df[specific_column_name].unique()\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Sort Operations'''
def reset_index(dataframe_name):
    '''
    This function will reset original index.
    '''
    template = 'df.reset_index(drop=True)\n\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def set_index_by_specified_column(specific_column_name, dataframe_name):
    '''
    This function will set specified column as new index.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.set_index(specific_column_name)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.set_index(specific_column_name)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


def sort_index(dataframe_name):
    '''
    This function will set index based on axis 0 or 1.
    '''
    template = 'df.sort_index(axis=)\n\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


def sort_value_by_column(specific_column_name, dataframe_name):
    '''
    This function will sort value by specified column.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.sort_values(specific_column_name, axis=0)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.sort_index(axis=0)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Group Operations'''
def group_by_column(specific_column_name, dataframe_name):  # (.first / .size / .count / .sum / .mean , etc.)
    '''
    This function will group data by specified columns.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_group = df.groupby([specific_column_name])\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df_group = df.groupby(['specific_column_name'])\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Time series Operations'''
def change_to_datetime(specific_column_name, dataframe_name):
    '''
    This function will set specified column type tp datetime.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "pd.to_datetime(df[[specific_column_name]])\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "pd.to_datetime(df)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def find_missing_date(dataframe_name):
    '''
    This function will find missing date in one datatime column.
    '''
    template = 'date_range = pd.DataFrame(index=pd.data_range(strat="start_time", end="end_time")\ndate_missing = pd.merge(df, date_range, right_index=True, how="outer")\n\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Edit Operations'''
def rename_column(specific_column_name, rename_new_name, dataframe_name):
    '''
    This function will change name of specified columns.
    '''
    if specific_column_name and rename_new_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_rename = rename_new_name.split(',')
        res_rename = [i.strip() for i in tem_rename]
        
        strs = "columns={"
        for i in range(len(tem)):
            strs += "'" + str(tem[i]) + "'" + ":" + "'" + str(tem_rename[i]) + "'" + ","
        template = "df = df.rename(strs}, inplace=False) \n# df = df.rename(index={'original_name':'new_name'}, inplace=False)\n\n".replace('strs', strs.strip(','))

    elif specific_column_name: 
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]

        strs = "columns={"
        for i in range(len(tem)):
            strs += "'" + str(tem[i]) + "'" + ":" + "'new_name'" + ","
        template = "df = df.rename(strs}, inplace=False) \n# df = df.rename(index={'original_name':'new_name'}, inplace=False)\n\n".replace('strs', strs.strip(',')) 

    elif rename_new_name: 
        tem_rename = rename_new_name.split(',')
        res_rename = [i.strip() for i in tem_rename]
        template = "df.columns = [{}]\n\n".format(str(res_rename).strip('[]'))

    else:
        template = "df.rename(columns={'original_name':'new_name'}, inplace=False) \n# df = df.rename(index={'original_name':'new_name'}, inplace=False)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def change_specified_column_type(specific_column_name, dataframe_name):
    '''
    This function will remove specified columns or rows.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df[[{}] = df[[{}]].astype(new_type)".format(str(res).strip('[]'), str(res).strip('[]'))#replace('specific_column_name', str(res).strip('[]'))
    else: 
        template = "df[[specific_column_name]] = df[[specific_column_name]].astype(new_type)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def delete_by_column_row(specific_column_name, dataframe_name):
    '''
    This function will remove specified columns or rows.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.drop(columns=[specific_column_name], inplace=False) \n# data = df.drop(index=[rows_index], inplace=False) # we can also use drop to delete rows\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.drop(columns=[specific_column_name], inplace=False) \n# df = df.drop(index=[rows_index], inplace=False) # we can also use drop to delete rows\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def drop_na(specific_column_name, dataframe_name):
    '''
    This function will drop NaN.
    '''
    template = "df.dropna(axis=0)"
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.dropna(subset=[specific_column_name])\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.dropna(axis)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 
    

def drop_duplicates(specific_column_name, dataframe_name):
    '''
    This function will remove all duplicated rows on specified columns.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.drop_duplicates(subset=[specific_column_name], keep=, inplace=False)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.drop_duplicates(keep=, inplace=False)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def extract_duplicates(specific_column_name, dataframe_name):
    '''
    This function will return all duplicated elements (on specified columns).
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df1 = df.drop_duplicates(subset=[specific_column_name], keep=False, inplace=False) \ndf2 = df.drop_duplicates(subset=[specific_column_name], keep='first', inplace=False) \ndf_all_duplicates = df1.append(df2).drop_duplicates(subset=[specific_column_name], keep=False, inplace=False)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df1 = df.drop_duplicates(keep=False, inplace=False) \ndf2 = df.drop_duplicates(keep='first', inplace=False) \ndf_all_duplicates = df1.append(df2).drop_duplicates(keep=False, inplace=False)\n\n" 

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def fill_na(dataframe_name, specific_column_name, fill_value):
    '''
    This function will fill in NaN with fill_value in specific columns.
    '''
    if specific_column_name and fill_value and dataframe_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_value = fill_value.strip('with').strip()
        df_name = dataframe_name.strip()

        template = "df = df[[specific_column_name]].fillna(value='fill_value', method=None, axis=None, limit=None, inplace=False)\n\n".replace('fill_value', str(tem_value)).replace('specific_column_name', str(res).strip('[]')).replace('df', str(df_name).strip())
    elif specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df[[specific_column_name]].fillna('value', method, axis=None, limit=None, inplace=False)\n\n".replace('specific_column_name', str(res).strip('[]'))
    elif fill_value:
        tem_value = fill_value.strip('with')
        template = "df = df.fillna(value='fill_value', method=None, axis=None, limit=None, inplace=False)\n\n".replace('fill_value', tem_value)
    elif dataframe_name:
        df_name = dataframe_name.strip()
        template = "df = df.fillna(value='fill_value', method=None, axis=None, limit=None, inplace=False)\n\n".replace('df', str(df_name).strip())
    else:
        template = "df = df.fillna(value, method, axis=None, limit=None, inplace=False)\n\n"

    return template


def add_new_row(dataframe_name):
    '''
    This function will insert new row in specified position.
    '''
    template = "df_new = pd.DataFrame([lists_value]) # This is the new dataframe need to be added to original dataframe \ndf.append(df_new, ignore_index=True)\n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def insert_new_column(specific_column_name, fill_value, dataframe_name):
    '''
    This function will insert new column in specified position.
    '''
    if specific_column_name and fill_value:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_value = fill_value.strip('with').strip()
        template = "df = df.insert(loc=insert_index_of_new_column, column=specific_column_name, value=fill_value, allow_duplicates=False)\n\n".replace('specific_column_name', str(res).strip('[]')).replace('fill_value', tem_value) 
    elif specific_column_name: 
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.insert(loc=insert_index_of_new_column, column=specific_column_name, value=value_of_new_column, allow_duplicates=False)\n\n".replace('specific_column_name', str(res).strip('[]'))
    elif fill_value:
        tem_value = fill_value.strip('with').strip()
        template = "df = df.insert(loc=insert_index_of_new_column, column=specific_column_name, value=fill_value, allow_duplicates=False)\n\n".replace('fill_value', tem_value) 
    else:
        template = "df = df.insert(loc=insert_index_of_new_column, column=specific_column_name, value=value_of_new_column, allow_duplicates=False)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def merge_dataframe(specific_column_name):
    '''
    This function will return concatenated dataframe.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_merge = pd.merge(left={}, right={}, how)\n\n".format(res[0], res[1]) 
    else: 
        template = "df_merge = pd.merge(left='df_left', right='df_right', how)\n\n"
    
    return template


def concat_dataframe(specific_column_name):
    '''
    This function will return concatenated dataframe.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_concat = pd.concat([specified_column_name], axis)\n\n".replace('specified_column_name', str(res).strip('[]')) 
    else: 
        template = "df_concat = pd.concat(['specified_dataframe_name'], axis)\n\n"

    return template 


def filter_by_conditions(filter_conditions, specific_column_name, dataframe_name):
    '''
    This function will return filtered dataframe based on specified conditions.
    '''
    if specific_column_name and filter_conditions:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_filtered = df[df[specific_column_name] filter_conditions]\n\n".replace('specific_column_name', str(res).strip('[]')).replace('filter_conditions', str(filter_conditions).strip('[]')) 
    else: 
        template = "df_filtered = df[df['specific_column_name'] filter_conditions]\n\n"
        
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Preprocessing Operations'''
def sampling(fraction, dataframe_name):
    '''
    This function will return random sampled sub-dataset.
    '''
    if fraction:
        template = "df = df.sample(frac={}, n=None, axis=0).reset_index(drop=True)\n\n".format(fraction)
    else:
        template = "df = df.sample(frac=fraction, n=None, axis=0).reset_index(drop=True)\n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def train_test_split(fraction, dataframe_name):
    '''
    This function will return splited training / test sub-dataset.
    '''
    if fraction:
        template = "from sklearn.model_selection import train_test_split \nx_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size={})\n\n".format(fraction)
    
    else:
        template = "from sklearn.model_selection import train_test_split \nx_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=fraction)\n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def scaler(dataframe_name):
    '''
    This function will return scaled data.
    '''
    template = "from sklearn.preprocessing import StandardScaler \nscaler = StandardScaler() \ndf_scaled = scaler.fit_transform(df)\n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


def one_hot_encoding(specific_column_name, dataframe_name):
    '''
    This function will return scaled data.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.join(pd.get_dummies(df." + (str(res).strip('[]').strip("'")) + "))\n\n"
    else:
        template = "df = df.join(pd.get_dummies(df)\n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  
    

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Feature Enginering Operations'''
def correlation_matrix(specific_column_name, dataframe_name):
    '''
    This function will return correlation matrix for original dataframe.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df[[specific_column_name]].corr(method='pearson', min_periods=1)\n\n".replace('specified_column_name', str(res).strip('[]')) 
    else:
        template = "df.corr(method='pearson', min_periods=1)\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template   


def feature_selection(fs_type, dataframe_name):
    '''
    This function will selected dataframe by different ways to filter features.
    '''
    template = '# Please specify the feature selection approach, like PCA, collinear, missing element, feature importance, etc.'

    if fs_type == 'collinear':
        template = "from feature_selector import FeatureSelector \n\
train_labels = df['label'] \n\
train_features = df.drop(columns='label') \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_collinear(correlation_threshold=, one_hot=False) \n\
fs.ops['collinear'] \n\
fs.plot_collinear() \n\
df_x_filtered = fs.remove(methods = 'collinear', keep_one_hot=False) \n\n"

    elif fs_type == 'missing':
        template = "from feature_selector import FeatureSelector \n\
train_labels = df['label'] \n\
train_features = df.drop(columns='label') \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_missing(missing_threshold=0.6) \n\
fs.ops['missing'] \n\
fs.plot_missing() \n\
df_x_filtered = fs.remove(methods = 'missing', keep_one_hot=False) \n\n"
    
    elif fs_type == 'low importance':
        template = "from feature_selector import FeatureSelector \n\
train_labels = df['label'] \n\
train_features = df.drop(columns='label') \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_zero_importance(task='classification', eval_metric='auc', n_iteration=10, early_stopping=True) # fs.identify_low_importance(cumulative_importance=0.99) \n\
fs.ops['zero_importance']  # fs.ops['low_importance'] \n\
fs.plot_feature_importances(threshold=0.99, plot_n=12) \n\
df_x_filtered = fs.remove(methods = 'low_importance', keep_one_hot=False) \n\n"

    elif fs_type == 'single unique':
        template = "from feature_selector import FeatureSelector \n\
train_labels = df['label'] \n\
train_features = df.drop(columns='label') \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_single_unique() \n\
fs.ops['single_unique'] \n\
fs.plot_unique() \n\
df_x_filtered = fs.remove(methods = 'single_unique', keep_one_hot=False) \n\n"

    elif fs_type == 'all' or fs_type is None:
        template = "from feature_selector import FeatureSelector \n\
train_labels = df['label'] \n\
train_features = df.drop(columns='label') \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_all(selection_params = {'missing_threshold': 0.6, \
                    'correlation_threshold': 0.98, \
                    'task': 'classification',  \
                    'eval_metric': 'auc',  \
                    'cumulative_importance': 0.99})  \
df_x_filtered = fs.remove(methods = 'all', keep_one_hot=False) \n\n"

    elif fs_type == 'pca':
        template = "from sklearn.decomposition import PCA \n\
 \n\
pca = PCA(n_components=None) \n\
df_pca_x = pca.fit_transform(df_x) \n\
features_importance_pca = pca.explained_variance_ratio_ \n\
df_x_filtered = PCA(n_components).fit_transform(df_x) \n\n"

    elif fs_type == 'low variance':
        template = "from sklearn.feature_selection import VarianceThreshold \n\
fs = VarianceThreshold(threshold=(.8 * (1 - .8))) \n\
df_x_filtered = fs.fit_transform(df_x) \n\n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template  


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Model Operations'''
def regression_model(algorithm_type):
    '''
    This function will return regression model by differecnt algorithm_type.
    '''
    template = '# Please specify the regression model, like logistic, linear, lasso, polynomial, svm, etc.'

    if algorithm_type == 'logistic':
        template = "from sklearn.linear_model import LogisticRegression \n\
model = LogisticRegression(penalty='l2', C=1, random_state=0) \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'linear':
        template = "from sklearn.linear_model import LinearRegression \n\
model = LinearRegression(fit_intercept=True) \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'lasso':
        template = "from sklearn.linear_model import Lasso \n\
model = Lasso(alpha=0.1) \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'polynomial':
        template = "from sklearn.linear_model import LinearRegression \n\
from sklearn.preprocessing import PolynomialFeatures \n\
quadratic_featurizer = PolynomialFeatures(degree=2) \n\
x_train_quadratic = quadratic_featurizer.fit_transform(x_train) \n\
x_test_quadratic = quadratic_featurizer.transform(x_test) \n\
model = LinearRegression() \n\
model.fit(x_train_quadratic, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_train_quadratic) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'svm':
        template = "from sklearn.svm import SVR \n\
model = SVR(kernel='rbf') \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'random forest':
        template = "from sklearn.ensemble import RandomForestRegressor \n\
model = RandomForestRegressor() \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'decision tree':
        template = "from sklearn.tree import DecisionTreeRegressor \n\
model = DecisionTreeRegressor() \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    #template = model
    return template 


def classification_model(algorithm_type):
    '''
    This function will return classification model by differecnt algorithm_type.
    '''
    template = '# Please specify the classification model, like logistic, knn, decision tree, random forest, svm, etc.'
    
    if algorithm_type == 'logistic':
        template = "from sklearn.linear_model import LogisticRegression \n\
model = LogisticRegression(penalty='l2', random_state=0) \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'knn':
        template = "from sklearn.neighbors import KNeighborsClassifier \n\
model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski') \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'decision tree':
        template = "from sklearn.tree import DecisionTreeClassifier \n\
model = DecisionTreeClassifier() \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'random forest':
        template = "from sklearn.ensemble import RandomForestClassifier \n\
model = RandomForestClassifier(criterion='entropy', n_estimators=10) \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'svm':
        template = "from sklearn.svm import SVC \n\
model = SVC(kernel='rbf') \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"
    elif algorithm_type == 'bayes':
        template = "from sklearn.naive_bayes import MultinomialNB \n\
model = MultinomialNB() \n\
model.fit(x_train, y_train) \n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test) \n\
plt.scatter(x_test, y_test) \n\
plt.plot(x_test, y_pred) \n\n"

    return template 


def clustering_model(algorithm_type, specific_column_name, dataframe_name, number):
    '''
    This function will return classification model by differecnt algorithm_type.
    ''' 
    template = '# Please specify the clustering model, like KMeans, SpectralClustering, AgglomerativeClustering, DBSCAN, etc.'

    if algorithm_type == 'kmeans':
        template = "from sklearn.cluster import KMeans \n\
X = df.as_matrix() \n\
cluster = KMeans(n_clusters=number, max_iter=600, algorithm = 'auto') \n\
cluster.fit(X)  \n\
label_clusters = cluster.fit_predict(x) \n\
print(label_clusters)"
    elif algorithm_type == 'SpectralClustering':
        template = "from sklearn.cluster import SpectralClustering \n\
X = df.as_matrix() \n\
cluster = SpectralClustering(n_clusters=number, max_iter=600, algorithm = 'auto') \n\
cluster.fit(X)  \n\
label_clusters = cluster.fit_predict(x) \n\
print(label_clusters)"
    elif algorithm_type == 'AgglomerativeClustering':
        template = "from sklearn.cluster import AgglomerativeClustering \n\
X = df.as_matrix() \n\
cluster = AgglomerativeClustering(n_clusters=number, max_iter=600, algorithm = 'auto') \n\
cluster.fit(X)  \n\
label_clusters = cluster.fit_predict(x) \n\
print(label_clusters)"
    elif algorithm_type == 'DBSCAN':
        template = "from sklearn.cluster import DBSCAN \n\
X = df.as_matrix() \n\
cluster = DBSCAN(eps=0.3, min_samples=10) \n\
cluster.fit(X)  \n\
label_clusters = cluster.fit_predict(x) \n\
print(label_clusters)"

    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        df_new = "df[['" + str(res).strip('[]').strip("'") + "']]"
        template = template.replace('df', df_new)

    if dataframe_name:
        template = template.replace('df', dataframe_name)

    if number:
        template = template.replace('number', number)

    return template 

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
'''Pipeline workflow Operations'''
def initial_pipeline():
    
    template = import_packages(import_packages=None) + load_data(file_path=None) + sort_index() + \
        index_info() + column_name_all() + dataset_shape() + \
        dataset_dtype() + dataset_describe() + unique_value_in_specific_column(specific_column_name=None) + head_overview(number=None)

    return template


def preprocessing_pipeline():
    
    template = group_by_column(specific_column_name=None) + drop_duplicates(specific_column_name=None) + extract_duplicates(specific_column_name=None) + \
        nan_matrix() + where_nan() + drop_na(specific_column_name=None) + fill_na(specific_column_name=None, fill_value=0) + one_hot_encoding(specific_column_name=None)

    return template


def feature_engineering_pipeline():
    
    template = scaler() + correlation_matrix() + feature_selection(fs_type='all')

    return template


def regression_model_pipeline(algorithm_type):

    if algorithm_type != '': 
        template = sampling(0.75) + train_test_split(0.2) + regression_model(algorithm_type)
    else:
        template = '# Please specify the regression model, like logistic, linear, lasso, polynomial, svm, etc.'
    return template


def classification_model_pipeline(algorithm_type):

    if algorithm_type != '': 
        template = sampling(0.75) + train_test_split(0.2) + classification_model(algorithm_type)
    else:
        template = '# Please specify the classification model, like logistic, knn, decision tree, random forest, svm, etc.'
    return template


def outlier(dataframe_name):
    
    template = where_nan() + nan_matrix() + fill_na(specific_column_name=None, fill_value='missing') + drop_na(specific_column_name=None) + drop_duplicates(specific_column_name=None)
    
    outliers_by_z_score = "# Remove outliers by z_score \n\
def detect_outliers(df,threshold=3): \n\
    mean_d = np.mean(df) \n\
    std_d = np.std(df) \n\
    outliers = [] \n\
    for y in df: \n\
        z_score= (y - mean_d) / std_d \n\
        if np.abs(z_score) > threshold: \n\
            outliers.append(y) \n\
    return outliers \n\
    "

    outliers_by_IQR = "# Remove outliers by Inter-Quartile Range \n\
def detect_outliers(df): \n\
    q1 = df.quantile(0.25) \n\
    q3 = df.quantile(0.75) \n\
    iqr = q3-q1 #Interquartile range \n\
    fence_low  = q1-1.5*iqr \n\
    fence_high = q3+1.5*iqr \n\
    outliers = df.loc[(df < fence_low) | (df > fence_high)] \n\
    return outliers \n\
    "
    
    template = template + outliers_by_z_score + outliers_by_IQR

    if dataframe_name:
        template = template.replace('df', dataframe_name) 

    return template


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Visualization Operations''' 
def distribution(dataframe_name, specific_column_name):
    template = "df.plot(subplots=True, layout=(2,3), figsize = (10,10), kind='kde')"
    if specific_column_name: 
        template = "df[['specific_column_name']].plot(subplots=True, layout=(2,3), figsize = (10,10), kind='kde')".replace('specific_column_name', specific_column_name) 
    if dataframe_name:
        template = template.replace('df', dataframe_name) 
    return template


def heatmap(dataframe_name, specific_column_name):
    template = 'import seaborn as sns \nsns.heatmap(df, annot=True)' 

    if specific_column_name: 
        template = "import seaborn as sns \nsns.heatmap(df[['specific_column_name']], annot=True)".replace('specific_column_name', specific_column_name) 
    if dataframe_name:
        template = template.replace('df', dataframe_name)
    return template


def plot(plot_type, dataframe_name, specific_column_name):
    template = "df.plot(subplots=False, figsize = (10,10), kind='plot_type', stacked=False)"
    if specific_column_name: 
        template = "df[['specific_column_name']].plot(subplots=False, figsize = (10,10), kind='plot_type', stacked=False)".replace('specific_column_name', specific_column_name) 
    if dataframe_name:
        template = template.replace('df', dataframe_name) 
    if plot_type:
        template = template.replace('plot_type', plot_type) 
    return template

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Recommendation'''
# recommendation based on user historical queries.
def recommendation(user_history_query):
    data_operations = {'initial': ['import_packages', 'sort_index', 'load_data', 'save_data', 'sort_index', 'index_info', 'column_name_all', 'dataset_shape', 'dataset_dtype', 'dataset_describe', 'head_overview'],
                    'preprocessing': ['group_by_column', 'nan_matrix', 'where_nan', 'drop_na', 'fill_na', 'drop_duplicates', 'extract_duplicates', 'one_hot_encoding'],
                    'feature engineering': ['scaler', 'correlation_matrix', 'feature_selection', 'feature_selection_collinear', 'feature_selection_pca', 'feature_selection_missing', 'feature_selection_importance', 'feature_selection_variance', 'feature_selection_single_unique'],
                    'model construction': ['sampling', 'train_test_split', 'regression_model', 'classification_model'],
                    'pipeline workflow': ['regression_model_pipeline', 'classification_model_pipeline']}
    step_hist, opera_rec_this_step, opera_rec_next_step = set(), [], []
    for i in user_history_query:
        for key, value in data_operations.items():
            if i in value:
                step_hist.add(key)
    
    steps_all, step_rec = list(data_operations.keys()), []
    for i in step_hist:
        if i in steps_all:
            steps_all.remove(i)

    step_rec = steps_all.pop(0)   # just one step next
    for i in list(step_hist):
        opera_rec_this_step.extend(data_operations[i])

    opera_rec_this_step = list(set(opera_rec_this_step) - set(user_history_query))
    opera_rec_next_step = data_operations[step_rec]
    #print(step_hist)
    #print(step_rec)
    #print(opera_rec_this_step)
    #print(opera_rec_next_step)

    template = '# The more relevant operations in existed pipeline: {}\n\n# The operations you could try in next pipeline "{}": {}'.format(opera_rec_this_step, step_rec, opera_rec_next_step)

    return template


# Quick statistics query result regarding to user dataset attributes.
# Columns, index, one column average/max/min value,  


if __name__=='__main__':
    
    code = str(intent)()

