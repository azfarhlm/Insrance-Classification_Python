# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %% [markdown]
# Import functions and specify options
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

pd.set_option('display.max_columns', None)  
sns.set(style = "whitegrid")  # set the style for the plot
sns.set_context("paper")

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" # display output for all lines within a cell

# %%
# Load data file
df = pd.read_csv('/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project/add1120_prep1.csv', low_memory = False)

# %% [markdown]
# Calibrate values
# %%
df['rxdaysup'] = df['rxdaysup'].fillna(0).replace(9999,0).astype(int)

# Convert object variables to categorical
list = ['probmom', 'probdad', 'probsad', 'probscbhv', 'probfun', 
        'probadlts', 'probnrvs', 'probsibs', 'probkids', 'probactvty', 
        'probscwrk', 'probhmbhv', 'probtrbl']
for i in list:
    df[i] = df[i].astype('category')

# %% [markdown]
# Create variables
# %%
# ADD Rx indicator
# Mapping function
def map_to_new_category(value):
    if value == 'AMPHETAMINE-DEXTROAMPHETAMINE':
        return 1
    elif value == 'DEXTROAMPHETAMINE':
        return 1
    elif value == 'METHYLPHENIDATE':
        return 1
    elif value == 'DEXMETHYLPHENIDATE':
        return 1
    elif value == 'LISDEXAMFETAMINE':
        return 1
    elif value == "AMPHETAMINE":
        return 1
    else:
        return 0
# Apply the mapping function to create the new variable
df['addrx'] = df['rxdrgnam'].apply(map_to_new_category)

# ADD Rx categorical
# Define a function to map original_indicator values to new categories
def map_to_new_category(value):
    if value == 'AMPHETAMINE-DEXTROAMPHETAMINE':
        return 'AMPHETAMINE-DEXTROAMPHETAMINE'
    elif value == 'DEXTROAMPHETAMINE':
        return 'DEXTROAMPHETAMINE'
    elif value == 'METHYLPHENIDATE':
        return 'METHYLPHENIDATE'
    elif value == 'DEXMETHYLPHENIDATE':
        return 'DEXMETHYLPHENIDATE'
    elif value == 'LISDEXAMFETAMINE':
        return 'LISDEXAMFETAMINE'
    else:
        return None
# Apply the mapping function to create the new category column
df['addrxnam'] = df['rxdrgnam'].apply(map_to_new_category)

# Rx expenditure per day supply
df['rxfexpday'] = df['rxfexptot'] / df['rxdaysup']
df['rxfexpday'] = df['rxfexpday'].where((df['rxfexptot'] != 0) & (df['rxdaysup'] != 0), None)     # only for non-zero values, otherwise the division will result in inf

# ADD Rx expenditure per day supply
df['addrxfexpday'] = df['rxfexpday'][df['addrx'] == 1]
df['addrxfexpday'] = df['addrxfexpday'].where((df['rxfexpday'] != 0) & (df['addrx'] != 0), None)  # only for non-zero values, otherwise the division will result in inf

# Brand name ADD Rx
# List of names to check against
name_list = ["RITALIN LA", "RITALIN", "QUILLIVANT", "QUILLIVANT XR", "FOCALIN", "APTENSIO XR", "COTEMPLA XR-ODT", "QUILLICHEW ER", "JORNAY PM", "DEXEDRINE", "FOCALIN XR", "CONCERTA", "METADATE", "DAYTRANA", "ADDERALL", "ADDERALL XR", "VYVANSE", "EVEKEO"]
# Create the 'addrxbrd' variable based on whether 'rxname' is in the list
#df['addrxbrd'] = df['rxname'].isin(name_list).astype(int)
df['addrxbrd'] = df.apply(lambda row: 1 if row['rxname'] in name_list else 0, axis = 1)

# Child indicator
df['chld'] = np.where((df['age'] >= 1) & (df['age'] <= 17), 1, 0)

# Child facing problem indicator variables
list = ['probmom', 'probdad', 'probsad', 'probscbhv', 'probfun', 
        'probadlts', 'probnrvs', 'probsibs', 'probkids', 'probactvty', 
        'probscwrk', 'probhmbhv', 'probtrbl']
for i in list:
    conditions = [
        df[i].isin(['A very big problem', 'Big problem']),
        df[i].isin(['Little problem', 'No problem', 'Some problem']),
        df[i].isin(['NIU', "Unknown-don't know", 'Unknown-not ascertained', 'Unknown-refused'])
    ] 
    choices = [1, 0, None]  # 1 for 'A very big problem' or 'Big problem', 0 for others, None for missing values
    df['xt' + i] = np.select(conditions, choices, default = None)


# %% [markdown]
# Save datafile
# %%
df.to_csv("add1120_prep2.csv", index = False)
