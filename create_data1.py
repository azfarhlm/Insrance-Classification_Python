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

# %% [markdown]
# Read data file
# %%
nan = ['.', 'NaN', 'N/A', ' ']
# df = pd.read_csv('/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project/adhd.csv', encoding = 'iso-8859-1', na_values = nan)   # small dataset
df = pd.read_csv('/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project/add1120.csv', encoding = 'iso-8859-1', na_values = nan, low_memory = False)  # full dataset

# %% [markdown]
# Fill rows for person level variables
# %%
# Specify the columns to forward fill
columns_to_fill = ['rectype',   'year',   'serial',   'pernum',   'duid',   'pid',   'mepsid',   'panel',   'psuann',   'stratann',   'psupld',   'stratapld',   'panelyr',   'relyr',   'perweight',   'saqweight',   'diabweight',   'age',   'agelast',   'sex',   'marstat',   'birthmo',   'birthyr',   'regionmeps',   'relate',   'famsize',   'racea',   'usborn',   'educ',   'student',   'ftotinccps',   'ftotincmeps',   'inctot',   'cpi2009',   'ftotval',   'incwage',   'incbus',   'incunemp',   'incwkcom',   'incint',   'incdivid',   'incprop',   'incretir',   'incss',   'inctrst',   'incvet',   'incira',   'incalim',   'incchld',   'inccash',   'incssi',   'incwelfr',   'incoth',   'foodstyn',   'povcat',   'povlev',   'hinotcov',   'hiprivate',   'hichampany',   'himachip',   'himcare',   'covertype',   'covtypeage',   'addev',   'addage',   'aeffort',   'ahopeless',   'anervous',   'arestless',   'asad',   'aworthless',   'phqintr',   'phqdep',   'rxexptot',   'rxexpsrc',   'probmom',   'probdad',   'probsad',   'probscbhv',   'probfun',   'probadlts',   'probnrvs',   'probsibs',   'probkids',   'probactvty',   'probscwrk',   'probhmbhv',   'probtrbl',   'admals',   'admwlm',   'adsoca',   'k6sum',   'phq2']
# Forward fill missing values in the specified columns
df[columns_to_fill] = df.groupby(['serial', 'pernum'])[columns_to_fill].ffill()

# %% [markdown]
# Save pre-processed data
df.to_csv('add1120_prep1.csv',index = False)