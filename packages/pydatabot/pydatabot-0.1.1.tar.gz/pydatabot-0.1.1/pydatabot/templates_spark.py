import pandas as pd 
import numpy as np 

# data load & initial part: Import / Create / Load operations

# data query & detect part: Query Operations + Sort Operations + Group Operations

# data pre-process & clean part: Edit Operations + Time series Operations

# data feature enginering & statistical analysis part: correlation / various feature selection 

# data modelling part: model construction (regression / classification / cluster)

# data visualization part. 

'''initial spark / load / create / save Operations'''
def spark_initial(specific_column_name):
    '''
    This function will initial pyspark environment for data analytics
    '''
    template = "import pyspark \n\
from pyspark import SparkContext as sc \n\
from pyspark import SparkConf \n\
from pyspark.sql import SparkSession \n\
from pyspark.sql import SQLContext \n\
from pyspark.sql import DataFrame \n\
from pyspark.sql import Row \n\
 \n\
sparkconf = SparkConf().setAppName('appName').setMaster('local[*]') \n\
spark = SparkSession.builder.config(conf=sparkconf).getOrCreate() \n\
sc = spark.sparkContext"

    if specific_column_name:
        template = template.replace('appName', specific_column_name) 
           
    return template


def spark_load_data(file_path, dataframe_name, file_type):
    '''
    This function will load the dataset from file_path
    '''
    if file_type == 'csv':
        template = "df = spark.read.csv('file_path', header) \n".replace('file_path', file_path) if file_path else "df = spark.read.csv('file_path', header) \n"
    elif file_type == 'text':
        template = "df = spark.read.text('file_path', header) \n".replace('file_path', file_path) if file_path else "df = spark.read.text('file_path', header) \n"
    elif file_type == 'json':
        template = "df = spark.read.json('file_path', header) \n".replace('file_path', file_path) if file_path else "df = spark.read.json('file_path', header) \n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def spark_pd_to_sp(dataframe_name):
    '''
    This function will load the dataset from file_path
    '''
    template = "df_spark = spark.createDataFrame(df_pd)"

    template = template.replace('df_pd', dataframe_name) if dataframe_name else template

    return template


def spark_sp_to_pd(dataframe_name):
    '''
    This function 
    '''
    template = "df_pd = df_spark.toPandas()"
    template = template.replace('df_spark', dataframe_name) if dataframe_name else template
    
    return template


def spark_save_data(file_path, dataframe_name, file_type):
    '''
    This function will save the dataset to file_path
    '''
    if file_type == 'csv':
        template = "df.write.csv(path='file_path', header=True, sep=',', mode='overwrite')\n".replace('file_path', file_path) if file_path else "df.write.csv(path='file_path', header=True, sep=',', mode='overwrite')\n"
    elif file_type == 'text':
        template = "df.write.format('text').save('file_path') \n".replace('file_path', file_path) if file_path else "df.write.format('text').save('file_path') \n"
    elif file_type == 'json':
        template = "df.write.format('json').save('file_path') \n".replace('file_path', file_path) if file_path else "df.write.format('json').save('file_path') \n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template


def spark_create_dataframe(specific_column_name, dataframe_name):
    '''
    This function will create new dataframe
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = pd.DataFrame(columns=[{}]) \n\
df_spark = spark.createDataFrame(df)".format(str(res).strip('[]')) 
    else: 
        template = "df = pd.DataFrame()  # Hints: add 'columns=[column_names]'\n\
df_spark = spark.createDataFrame(df)"

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Query Operations'''
"""
def index_info():
    '''
    This function will return all index to user
    '''
    template = 'index = df.index\n'

    return template
"""


def spark_column_name_all(dataframe_name):
    '''
    This function will return name of all columns in dataset
    '''
    template = 'columns = df.columns\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


def spark_dataset_length(dataframe_name):
    '''
    This function will return length of dataset.
    '''
    template = 'df_length = df.count()\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


def spark_dataset_shape(dataframe_name):
    '''
    This function will return shape of dataset.
    '''
    template = 'df_shape = (df.count(), len(df.columns))\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


def spark_dataset_dtype(dataframe_name):
    '''
    This function will return type of dataset.
    '''
    template = 'df_type = df.dtypes\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


def spark_dataset_describe(dataframe_name):
    '''
    This function will return statistical metrics of dataset.
    '''
    template = 'df_describe = df.describe()\n'

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


def spark_extract_specific_column_by_name(specific_column_name, dataframe_name):
    '''
    This function will return one or some specific columns in dataset
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_columns = data.select(specified_column_name)  # can add .show()\n".replace('specified_column_name', str(res).strip('[]')) 
    else: 
        template = "df_columns = data.select('specified_column_name') # can add .show()\n"

    if dataframe_name:
        template = template.replace('data', dataframe_name) 

    return template


"""
def extract_specific_row_by_index(number):
    '''
    This function will return one or some specific rows in dataset
    '''
    template = "df_rows = df.iloc[number]\n".replace("number", number) if number else "df_rows = df.iloc[index]\n"

    return template
"""


def spark_head_overview(number, dataframe_name):
    '''
    This function will return first numb_of_rows of dataframe.
    ''' 
    template = "df.show(number)\n".replace("number", number) if number else "df.show()\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template


"""
def tail_overview(number):
    '''
    This function will return last numb_of_rows of dataframe.
    ''' 
    template = "df.tail(number)\n".replace("number", number) if number else "df.tail()\n"

    return template
"""


"""
def nan_matrix():
    '''
    This function will return nan matrix of original dataframe.
    ''' 
    template = "df.isna() # or we can use df.isnull()\n"

    return template
"""


def spark_where_nan(dataframe_name):
    '''
    This function will return concrete position of NaN value in original dataframe.
    ''' 
    template = "from pyspark.sql.functions import isnan, when, count, col \n\
 \n\
df.select([count(when(isnan(col), col)).alias(col) for col in df.columns]).show() \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template
    

"""
def where_specified_element(specific_element):
    '''
    This function will return position of this specified_element in original dataframe.
    ''' 
    if specific_element:
        tem = specific_element.split(',')
        res = [i.strip() for i in tem]
        template = "np.where(df == specified_element) \n".replace('specified_element', str(res).strip('[]')) 
    else: 
        template = "np.where(df == specified_element) \n"

    return template 
"""


def spark_unique_value_in_specific_column(specific_column_name, dataframe_name):
    '''
    This function will return unique value of this specified cloumn in original dataframe.
    ''' 
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df.select(specific_column_name).distinct().show() \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df.select('specific_column_name').distinct().show() \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Sort Operations'''
"""
def reset_index():
    '''
    This function will reset original index.
    '''
    template = 'df.reset_index(drop=True)\n\n'

    return template
"""


"""
def set_index_by_specified_column(specific_column_name):
    '''
    This function will set specified column as new index.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.set_index(specific_column_name)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.set_index(specific_column_name)\n\n"

    return template 
"""


"""
def sort_index():
    '''
    This function will set index based on axis 0 or 1.
    '''
    template = 'df.sort_index(axis=)\n\n'

    return template
"""


def spark_sort_value_by_column(specific_column_name, dataframe_name):
    '''
    This function will sort value by specified column.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.sort(specific_column_name, ascending=False) \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.sort('specific_column_name', ascending=False) \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Group Operations'''
def spark_group_by_column(specific_column_name, dataframe_name):  # (.first / .size / .count / .sum / .mean , etc.)
    '''
    This function will group data by specified columns.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_group = df.groupby(specific_column_name) \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df_group = df.groupby('specific_column_name') \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

"""
'''Time series Operations'''
def change_to_datetime(specific_column_name):
    '''
    This function will set specified column type tp datetime.
    '''
    template = 'pd.to_datetime(specific_column_name)\n\n'

    return template
"""


"""
def find_missing_date():
    '''
    This function will find missing date in one datatime column.
    '''
    template = 'fakedf = pd.DataFrame(index = pd.data_range(strat='', end='', freq='')\npd.merge(data, fakedf, right_index=True, how="outer")\n\n'

    return template
"""

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Edit Operations'''
def spark_rename_column(specific_column_name, rename_new_name, dataframe_name):
    '''
    This function will change name of specified columns.
    '''
    if specific_column_name and rename_new_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_rename = rename_new_name.split(',')
        res_rename = [i.strip() for i in tem_rename]
        strs = ''
        for i in range(len(tem)):
            strs += "'" + str(tem[i]) + "'" + "," + "'" + str(tem_rename[i]) + "'"
        template = "df = df.withColumnRenamed(strs) \n".replace('strs', strs.strip(','))
    elif specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        for i in range(len(tem)):
            strs += "'" + str(tem[i]) + "'" + "," + 'new_name'
        template = "df = df.withColumnRenamed(strs) \n".replace('strs', strs.strip(','))
    elif rename_new_name:
        tem_rename = rename_new_name.split(',')
        res_rename = [i.strip() for i in tem_rename]
        for i in range(len(res_rename)):
            strs += 'original_name' + "," + "'" + str(tem_rename[i]) + "'"
        template = "df = df.withColumnRenamed(strs) \n".replace('strs', strs.strip(','))
    else:
        template = "df = df.withColumnRenamed('original_name', 'new_name') \n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
    
    return template 


def spark_change_specified_column_type(specific_column_name, dataframe_name):
    '''
    This function will remove specified columns or rows.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.withColumn({},col({}).cast('new_type')) \n".format(str(res).strip('[]'), str(res).strip('[]'))#replace('specific_column_name', str(res).strip('[]'))
    else: 
        template = "df = df.withColumn('specific_column_name', col('specific_column_name').cast('new_type')) \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template  


def spark_delete_by_column_row(specific_column_name, dataframe_name):
    '''
    This function will remove specified columns or rows.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.drop([specific_column_name]) \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.drop(['specific_column_name']) \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template  


def spark_drop_na(specific_column_name, dataframe_name):
    '''
    This function will drop NaN.
    '''
    template = "df.dropna(axis=0)"
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.dropna(subset=(specific_column_name)) \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.dropna()\n\n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template   
    

def spark_drop_duplicates(specific_column_name, dataframe_name):
    '''
    This function will remove all duplicated rows on specified columns.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.dropDuplicates([specific_column_name]) \n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df = df.dropDuplicates() \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template  


"""
def extract_duplicates(specific_column_name):
    '''
    This function will return all duplicated elements (on specified columns).
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df1 = df.drop_duplicates(subset=[specific_column_name], keep=False, inplace=False) \ndf2 = df.drop_duplicates(subset=[specific_column_name], keep='first', inplace=False) \ndf_all_duplicates = df1.append(df2).drop_duplicates(subset=[specific_column_name], keep=False, inplace=False)\n\n".replace('specific_column_name', str(res).strip('[]')) 
    else: 
        template = "df1 = df.drop_duplicates(keep=False, inplace=False) \ndf2 = df.drop_duplicates(keep='first', inplace=False) \ndf_all_duplicates = df1.append(df2).drop_duplicates(keep=False, inplace=False)\n\n" 

    return template 
"""


def spark_fill_na(dataframe_name, specific_column_name, fill_value):
    '''
    This function will fill in NaN with fill_value in specific columns.
    '''
    template = "df = df.fillna() \n"

    if specific_column_name and fill_value:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_value = fill_value.strip('with').strip()
        template = "df = df.fillna({specific_column_name: 'fill_value'}) \n".replace('fill_value', str(tem_value)).replace('specific_column_name', str(res).strip('[]'))

    elif specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df = df.fillna({specific_column_name: 'fill_value'}) \n".replace('specific_column_name', str(res).strip('[]'))
    
    elif fill_value:
        tem_value = fill_value.strip('with')
        template = "df = df.fillna('fill_value') \n".replace('fill_value', tem_value)
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template  


def spark_add_new_row(dataframe_name):
    '''
    This function will insert new row in specified position.
    '''
    template = "newRow = spark.createDataFrame([lists_value]) \n\
df = df.union(newRow) \n"
 
    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template


def spark_insert_new_column(specific_column_name, fill_value, dataframe_name):
    '''
    This function will insert new column in specified position.
    '''
    if specific_column_name and fill_value:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        tem_value = fill_value.strip('with').strip()
        template = "from pyspark.sql import functions \n\
 \n\
df = df.withColumn(specific_column_name, functions.lit('fill_value')) \n".replace('specific_column_name', str(res).strip('[]')).replace('fill_value', tem_value) 
    
    elif specific_column_name: 
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "from pyspark.sql import functions \n\
 \n\
df = df.withColumn(specific_column_name, functions.lit(0)) \n".replace('specific_column_name', str(res).strip('[]'))
    elif fill_value:
        tem_value = fill_value.strip('with').strip()
        template = "from pyspark.sql import functions \n\
 \n\
df = df.withColumn('specific_column_name', functions.lit('fill_value')) \n".replace('fill_value', tem_value) 
    else:
        template = "from pyspark.sql import functions \n\
 \n\
df = df.withColumn('specific_column_name', functions.lit(0)) \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


def spark_merge_dataframe(dataframe_name, specific_column_name):
    '''
    This function will return concatenated dataframe.
    '''
    if dataframe_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_merge = df_left.join(df_right, on='key_column', how='inner') \n".replace('df_left', res[0]).replace('df_right', res[1])
    else: 
        template = "df_merge = df_left.join(df_right, on='key_column', how='inner') \n"

    template = template.replace('key_column', str(dataframe_name).strip("'")) if dataframe_name else template

    return template 


"""
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
"""


def spark_filter_by_conditions(filter_conditions, specific_column_name, dataframe_name):
    '''
    This function will return filtered dataframe based on specified conditions.
    '''
    if specific_column_name and filter_conditions:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "df_filtered = df.filter(df[specific_column_name] filter_conditions) \n".replace('specific_column_name', str(res).strip('[]')).replace('filter_conditions', str(filter_conditions).strip('[]')) 
    else: 
        template = "df_filtered = df.filter(df['specific_column_name'] 'filter_conditions')\n\n"
        
    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


def spark_set_operation(dataframe_name, specific_column_name, set_operation_type):
    '''
    This function will return filtered dataframe based on set operation.
    '''
    template = "df_new = df.select('specific_column_name_1').operation(df.select('specific_column_name_2')) \n" 

    if set_operation_type:
        template = template.replace('operation', set_operation_type)

    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = template.replace('specific_column_name_1', res[0]).replace('specific_column_name_2', res[1])

    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template


'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Preprocessing Operations'''
def spark_sampling(fraction, dataframe_name):
    '''
    This function will return random sampled sub-dataset.
    '''
    if fraction:
        template = "df = df.sample(withReplacement=False, fraction={}) \n".format(fraction)
    else:
        template = "df = df.sample(withReplacement=False, fraction=) \n"
    
    template = template.replace('df', dataframe_name) if dataframe_name else template
        
    return template 


def spark_train_test_split(fraction, dataframe_name):
    '''
    This function will return splited training / test sub-dataset.
    '''
    if fraction:
        template = "train_split, test_split = df.randomSplit(weights=[{}, {}]) \n".format(float(fraction), float(1)-float(fraction))
        
    else:
        template = "train_split, test_split = df.randomSplit(weights=[0.8, 0.2]) \n"

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template 


def spark_scaler(dataframe_name, specific_column_name):
    '''
    This function will return scaled data.
    '''
    template = "from pyspark.ml.feature import StandardScaler \n\
  \n\
scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures', withStd=True, withMean=False) \n\
scalerModel = scaler.fit(dataFrame) \n\
scaledData = scalerModel.transform(dataFrame) \n\
scaledData.show()"

    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = template.replace('features', res[0])
   
    template = template.replace('dataFrame', dataframe_name) if dataframe_name else template

    return template 


def spark_one_hot_encoding(dataframe_name, specific_column_name):
    '''
    This function will return scaled data.
    '''
    template = "from pyspark.ml.feature import OneHotEncoder, StringIndexer \n\
 \n\
stringIndexer = StringIndexer(inputCol='category', outputCol='categoryIndex') \n\
model = stringIndexer.fit(df) \n\
indexed = model.transform(df) \n\
  \n\
encoder = OneHotEncoder(inputCol='categoryIndex', outputCol='categoryVec') \n\
encoded = encoder.transform(indexed) \n\
encoded.show()"

    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = template.replace('category', res[0])
   
    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template 
    

'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Feature Enginering Operations'''
def spark_correlation_matrix(specific_column_name, dataframe_name):
    '''
    This function will return correlation matrix for original dataframe.
    '''
    if specific_column_name:
        tem = specific_column_name.split(',')
        res = [i.strip() for i in tem]
        template = "from pyspark.ml.stat import Correlation \n\
  \n\
cor_matrix = Correlation.corr(df, 'specific_column_name')".replace('specific_column_name', specific_column_name)
    else:
        template = "from pyspark.ml.stat import Correlation \n\
  \n\
cor_matrix = Correlation.corr(df, df.columns)"

    template = template.replace('df', dataframe_name) if dataframe_name else template

    return template 


def spark_feature_selection(dataframe_name, fs_type):
    '''
    This function will selected dataframe by different ways to filter features.
    '''
    template = '# Please specify the feature selection approach, like PCA, collinear, missing element, feature importance, etc.'

    if fs_type == 'collinear':
        template = "from feature_selector import FeatureSelector \n\
  \n\
df_pd = df_spark.toPandas() \n\
train_labels = df_pd['label'] \n\
train_features = df_pd.drop(columns='label') \n\
 \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_collinear(correlation_threshold=, one_hot=False) \n\
fs.ops['collinear'] \n\
fs.plot_collinear() \n\
df_x_filtered = fs.remove(methods = 'collinear', keep_one_hot=False) \n\n"

    elif fs_type == 'missing':
        template = "from feature_selector import FeatureSelector \n\
  \n\
df_pd = df_spark.toPandas() \n\
train_labels = df_pd['label'] \n\
train_features = df_pd.drop(columns='label') \n\
 \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_missing(missing_threshold=0.6) \n\
fs.ops['missing'] \n\
fs.plot_missing() \n\
df_x_filtered = fs.remove(methods = 'missing', keep_one_hot=False) \n\n"
    
    elif fs_type == 'low importance':
        template = "from feature_selector import FeatureSelector \n\
  \n\
df_pd = df_spark.toPandas() \n\
train_labels = df_pd['label'] \n\
train_features = df_pd.drop(columns='label') \n\
 \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_zero_importance(task='classification', eval_metric='auc', n_iteration=10, early_stopping=True) # fs.identify_low_importance(cumulative_importance=0.99) \n\
fs.ops['zero_importance']  # fs.ops['low_importance'] \n\
fs.plot_feature_importances(threshold=0.99, plot_n=12) \n\
df_x_filtered = fs.remove(methods = 'low_importance', keep_one_hot=False) \n\n"

    elif fs_type == 'single unique':
        template = "from feature_selector import FeatureSelector \n\
  \n\
df_pd = df_spark.toPandas() \n\
train_labels = df_pd['label'] \n\
train_features = df_pd.drop(columns='label') \n\
 \n\
fs = FeatureSelector(data=train_features, labels=train_labels) \n\
fs.identify_single_unique() \n\
fs.ops['single_unique'] \n\
fs.plot_unique() \n\
df_x_filtered = fs.remove(methods = 'single_unique', keep_one_hot=False) \n\n"

    elif fs_type == 'all' or fs_type is None:
        template = "from feature_selector import FeatureSelector \n\
  \n\
df_pd = df_spark.toPandas() \n\
train_labels = df_pd['label'] \n\
 \n\
train_features = df_pd.drop(columns='label') \n\
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
df_pd = df_spark.toPandas() \n\
 \n\
pca = PCA(n_components=None) \n\
df_pca_x = pca.fit_transform(df_pd) \n\
features_importance_pca = pca.explained_variance_ratio_ \n\
df_x_filtered = PCA(n_components).fit_transform(df_pd) \n\n"

    elif fs_type == 'low variance':
        template = "from sklearn.feature_selection import VarianceThreshold \n\
  \n\
df_pd = df_spark.toPandas() \n\
 \n\
fs = VarianceThreshold(threshold=(.8 * (1 - .8))) \n\
df_x_filtered = fs.fit_transform(df_pd) \n\n"

    template = template.replace('df_spark', dataframe_name) if dataframe_name else template
    
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
        template = "from sklearn.linear_model import LogisticRegression\n\
model = LogisticRegression(penalty='l2', random_state=0)\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores\n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"
    elif algorithm_type == 'knn':
        template = "from sklearn.neighbors import KNeighborsClassifier\n\
model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"
    elif algorithm_type == 'decision tree':
        template = "from sklearn.tree import DecisionTreeClassifier\n\
model = DecisionTreeClassifier()\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores\n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"
    elif algorithm_type == 'random forest':
        template = "from sklearn.ensemble import RandomForestClassifier\n\
model = RandomForestClassifier(criterion='entropy', n_estimators=10)\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"
    elif algorithm_type == 'svm':
        template = "from sklearn.svm import SVC\n\
model = SVC(kernel='rbf')\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores\n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"
    elif algorithm_type == 'bayes':
        template = "from sklearn.naive_bayes import MultinomialNB\n\
model = MultinomialNB()\n\
model.fit(x_train, y_train)\n\
model.predict_proba(x_test) # predict probability scores \n\
y_pred = model.predict(x_test)\n\
plt.scatter(x_test, y_test)\n\
plt.plot(x_test, y_pred)\n\n"

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

