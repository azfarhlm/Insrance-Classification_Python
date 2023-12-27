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
# import functions
import os                                                                       # work with absolute directory path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import missingno as msno                                                        # visualize missing data
from statsmodels.stats.outliers_influence import variance_inflation_factor      # compute VIF

# set display and graphics
pd.set_option('display.max_columns', None)  
sns.set(style = "whitegrid")                                                    # set the style for the plot
sns.set_context("paper")

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"                                 # display output for all lines within a cell

# define working directory path
path_workdir = '/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project'
path_fig = '/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project/Paper/figure'

# %%
# Load data file
df = pd.read_csv('/Users/azfar/Documents/Python/Health Data Analytics Using Python/Project/add1120_prep2.csv', na_values=['nan', 'NaN'])

# %% [markdown]
# Drop cases that don't use ADD rx and irrelevant elements

# %%
#df = df[df['addrx'] == 1]                                  # limit to cases that use addrx
#df = df.drop(['rxrecid', 'mepsrxrecid'], axis = 1)         # drop elements
columns_keep = ['age', 'sex', 'marstat', 
    'famsize', 'racea', 'usborn', 'educ', 
    'student', 'ftotincmeps', 
    'inctot', 	'ftotval', 'incwage', 'foodstyn', 
    'povcat','povlev', 'hinotcov', 'mepsid']
"""
columns_keep = ['age', 'sex', 'marstat', 
    'famsize', 'racea', 'usborn', 'educ', 
    'student', 'ftotincmeps', 
    'inctot', 	'ftotval', 'incwage', 'foodstyn', 
    'povcat','povlev', 'addev', 'addage', 
    'aeffort', 'ahopeless', 'anervous', 'arestless', 
    'asad', 'aworthless', 'phqintr', 'phqdep', 'probmom', 	
    'probdad', 'probsad',  'probscbhv', 'probfun', 
    'probadlts', 'probnrvs', 'probsibs', 'probkids', 
    'probactvty', 'probscwrk', 'probhmbhv', 
    'probtrbl', 'admals', 'admwlm', 'adsoca', 
    'k6sum', 'phq2', 'icd9code', 'icd10code', 
    'addrx', 'hinotcov', 'addrxbrd', 'addev', 'addage',
    'addrxfexpday']
"""
dfa = df[columns_keep]                                       # keep elements for analysis

# %%
"""
totalnull=df.isnull().sum()                                 # compute total missing observations
null=100*(df.isnull().sum())/(df.shape[0])                  # compute percentage missing observations
df_null=pd.DataFrame({'percentage':null})                   # create dataframe for missing observations
df_null                                                     # display percentage of missing observations for each element

df_high=df_null[df_null['percentage']>90]                   # identify elements with more than some percentage missing of observations
getindexlist=list(df_high.index)                            # get an index of elements with high missing observations
len(getindexlist)                                           # number of elements in the index
df.drop(list(df_high.index),axis = 1, inplace = True)       # drop these elements
"""

# %% [markdown]
# Clean data

# %%
# received warnings mixed type variables:
# dfa['icd9code'] = str(dfa['icd9code'])
# dfa['icd10code'] = str(dfa['icd10code'])

# Replace values
dfa['hinotcov'] = dfa['hinotcov'].replace({'No, has coverage':'No', 'Yes, has no coverage':'Yes'})

# Dummy variables for the 'category' column
category = ['hinotcov']
for i in category:
    dummy_dfa = pd.get_dummies(dfa[i], prefix = i, drop_first = True)
    
# Concatenate the dummy variables with the original DataFrame
dfa = pd.concat([dfa, dummy_dfa], axis=1)
dfa = dfa.drop('hinotcov', axis=1)

# Variable labels
var_labels = {'addrx': 'ADD Medication', 'addrxnam': 'ADD Medication Name', 'addrxbrd': 'Brand Name ADD Medication'}

# %% [markdown]
# Density plots

# %%
# Create a kernel density plot for 'addrxfexpday'
plt.figure(figsize=(8, 6))
sns.kdeplot(df['addrxfexpday'], fill = True, color = "b")
# Customize the plot with labels and title
plt.xlabel('Normalized Expenditure (per Day Supply) from All Sources')
plt.ylabel('Density')
# Save the plot
plt.savefig(os.path.join(path_fig, 'kerneldensity_addrxfexpday.png'))
# Show the plot
plt.show()

# %%
# Create a kernel density plot for 'addrxfexpday' and color by 'addrxbrd'
plt.figure(figsize=(8,4))
f = sns.kdeplot(data=df, x='addrxfexpday', hue='addrxbrd', fill = True)
# Custom axis title
f.set_xlabel("Normalized Expenditure (per Day Supply) from All Sources")
# Custom legend
legend_labels = ["Brand", "Non-Brand"]                                  # hue label
f.legend(title = "Brand-Name ADD Medication", labels = legend_labels)   # legend title
# Save the plot
plt.savefig(os.path.join(path_fig, 'kerneldensity_addrxfexpday_bybrand.png'))
# Show the plot
plt.show()

# %%
"""
# Create a kernel density plot for 'addrxfexpday' and color by 'hinotcov_Yes'
plt.figure(figsize=(8,4))
f = sns.kdeplot(data=df, x='addrxfexpday', hue='hinotcov_Yes', fill = True)
# Custom axis title
f.set_xlabel("Normalized Expenditure (per Day Supply) from All Sources")
# Custom legend
legend_labels = ["Without Coverage", "With Coverage"]                                  # hue label
f.legend(title = "Insurance Coverage", labels = legend_labels)                         # legend title
# Save the plot
plt.savefig(os.path.join(path_fig, 'kerneldensity_addrxfexpday_byinscov.png'))
# Show the plot
plt.show()
"""

# %% [markdown]
# Save datafile

# %%
dfa.to_csv("add1120_prep3.csv", index = False)


