## TODO: add documentation
## TODO: manage dependencies

import datetime
import math as math
import numpy as np
from numbers import Number
import pandas as pd

def has_time(v):
    #"""Returns True if a datetime has a time - i.e. is not 00:00:00#"""
    if isinstance(v, datetime.date):
        strtime = v.strftime("%H:%M:%S")
        if strtime == "00:00:00":
            return False
        else:
            return True
    else:
        raise TypeError("Date type required")

def get_numstr(x):
    #"""Returns digits from a string - e.g. for extracting phone numbers from comments.#"""
    return str(''.join(ele for ele in x if ele.isdigit() or ele == '.'))

def is_phone_number(v):
    #"""Returns 'valid' if the digits within a string pass a basic format test for UK phone numbers, 'invalid' otherwise.#"""
    numstr = get_numstr(str(v))
    numValid = 'valid'
    lennum = len(numstr)
    if lennum > 13 or lennum < 10:
        numValid = 'invalid'
    distinctdigits = list(set(numstr))
    if(len(distinctdigits) < 3):
        numValid = 'invalid'
    return numValid

def as_percent(v, precision='0.2'):
    #"""Convert number to percentage string.#"""
    if isinstance(v, Number):
        return "{{:{}%}}".format(precision).format(v)
    else:
        raise TypeError("Numeric type required")


def as_quarter(v):
    #"""Convert calendar month to calendar quarter - e.g. 9 becomes 'q3'#"""
    if isinstance(v, Number):
        return 'q' + str( 1 + math.floor((v-1)/3))
    else:
        raise TypeError("Numeric type required")

def as_year(v):
    #"""Returns a year from a given datetime - e.g. 2019 q1#"""
    if isinstance(v, datetime.date):
        return v.year
    else:
        raise TypeError("Date type required")

def as_hour_of_day(v):
    #"""Returns hour of day from a given datetime#"""
    if isinstance(v, datetime.date):
        return v.hour
    else:
        raise TypeError("Date type required")

def as_day_of_week(v):
    #"""Returns day of week (Monday = 1) from datetime#"""
    if isinstance(v, datetime.date):
        return v.weekday()
    else:
        raise TypeError("Date type required")

def as_year_quarter(v):
    #"""Returns a combined year and quarter from a given datetime - e.g. 2019 q1#"""
    if isinstance(v, datetime.date):
        month = v.month
        year = v.year
        return str(year) + ' ' + as_quarter(month)
    else:
        raise TypeError("Date type required")

def date_is_not_null(v):
    if isinstance(v, datetime.date):
        return True
    else:
        return False

def as_minutes(v):
    #"""Returns float minutes from a timedelta#"""
    if isinstance(v, datetime.timedelta):
        return float(v.total_seconds() / 60)
    else:
        return None

def as_hours(v):
    #"""Returns float hours from a timedelta#"""
    if isinstance(v, datetime.timedelta):
        return float(v.total_seconds() / 3600)
    else:
        return None

def as_days(v):
    #"""Returns integer days from a timedelta#"""
    if isinstance(v, datetime.timedelta):
        return float(v.total_seconds() / 86400)
    else:
        return None


def describe_data(df):
    #''' Takes in a df and returns a summary of its data types, null values and counts#'''
    stats = ['field','count','unique','top','freq']
    data = df
    data_types = data.dtypes.rename_axis('field').reset_index().rename(columns={0:'data_type'})
    nulls = data.isnull().sum().rename_axis('field').reset_index().rename(columns={0:'number_null'})
    data_copy = data.copy()
    for col in data_copy.columns:
        data_copy[col] = data_copy[col].astype('str')
    describe = data_copy.describe(include='all').transpose().rename_axis('field').reset_index()
    schema = data_types.merge(nulls,how='inner',on='field').merge(describe[stats],how='inner',on='field')
    schema.insert(loc=3,column='prop_null',value=schema['number_null'] / (schema['number_null'] + schema['count']) )
    schema['prop_null'] = schema['prop_null'].mul(100).astype(int).round(1).astype(str)+'%'
    return schema

def get_dtypes(df):
    #''' Takes in a df with col: type mapping and returns a dtypes dict'''#
    dtypes = df.set_index('original_field_name').to_dict()['type']
    return dtypes

def get_dates(df):
    #''' Takes in a df with a dates col and returns this is a list'''#
    dates_list = df['dates'].to_list()
    cleaned_dates_list = [x for x in dates_list if str(x) != 'nan']
    return cleaned_dates_list

def get_new_cols(df):
    #''' Takes in a df with original col and new col name and returns as dict for rename'''#
    columns = df.set_index('original_field_name').to_dict()['new_field_name']
    return columns

def col_val_distr(df,col):
    #''' Takes in a df and a col and prints the distribution and proportion of the values in that col'''#
    s = df[col]
    counts = s.value_counts()
    percent100 = s.value_counts(normalize=True).mul(100).round(1).astype(str)+'%'
    distr = pd.DataFrame({'count':counts,'percentage':percent100})
    distr.rename_axis(str(col+'_values'),inplace=True)
    distr.reset_index(inplace=True)
    return distr

def filteronnulls(df,col):
    #'''Takes in a df and a col and returns the df filtered where cols are null'''#
    df = df[df[col].isnull()]
    return df

def filteronnotnull(df,col):
    #''' Takes in a df and a col and returns the df filtered where cols aren't null#'
    df = df[df[col].isnull()]
    return df

def convert_cols_string(df):
    #''' Takes in a df and converts all the columns to string data type'''#
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df

def printmd(string):
    #''' Takes in a string and prints it bold'''#
    display(Markdown(string))

def pretty_value_counts(df,col):
    #''' Takes in a df and col and gives value counts with clean headers'''#
    df = df[col].value_counts().rename_axis(str(col)).reset_index(name='count')
    df['proportion'] = df['count'] / df['count'].sum()
    df['prop_cumul_sum'] = df['proportion'].cumsum()
    df['proportion'] = FormatAsPercentage(df,'proportion')
    df['prop_cumul_sum'] = FormatAsPercentage(df,'prop_cumul_sum')
    return df

def lower_cols(df):
    #''' Takes in a df and lower cases the column names'''#
    for col in list(df.columns):
        df.rename(columns={col:col.lower()},inplace=True)
    return df

def add_proportion_distr(df,col):
    ''' Takes in a df and a count col and adds the proportion this represents'''#
    df['proportion'] = round(df[col] / df[col].sum() * 100, 2)
    return df

def camel_case_cols(df):
    df.columns = [x.title() for x in df.columns]
    df.columns = [x.replace("_"," ") for x in df.columns]

def display_all(df):
    ''' Takes in a df and prints all columns and rows'''#
    with pd.option_context("display.max_rows",1000,"display.max_columns",1000):
        display(df)

def percentile(n):
    ''' Use this in dataframe aggregation to get the percentile value for a col'''#
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

def add_mil_col(df,col):
    df[col +' mil'] = df[col]/1000000
    return df



def show_all_col(df):
    with pd.option_context('display.max_colwidth', 1000):
        display(df)

def display_and_show_all(df):
    ''' Takes in a df and prints all columns and rows, max col size '''#
    with pd.option_context("display.max_rows",1000,"display.max_columns",1000,'display.max_colwidth', 1000):
        display(df)

def put_last_col_to_front(df):
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df

def getDirFilePath(str_file):
    return os.path.join(datdir, str_file)

def output_csv(df, filename):
    filepath = os.path.join(datdir, filename)
    df.to_csv(filepath)

def output_excel(df, filename):
    filepath = os.path.join(datdir, filename)
    df.to_excel(filepath)

def output_pickle(df, filename):
    filepath = os.path.join(datdir, filename)
    df.to_pickle(filepath)

def display_more(df):
    with pd.option_context("display.max_rows", 1000): display(df)

def FormatAsPercentage(df, field):
    return pd.Series(["{0:.2f}%".format(val * 100) for val in df[field]], index = df.index)

def FormatAsMoney(df, field):
    return pd.Series(["£{0:,.0f}".format(val) for val in df[field]], index = df.index)
