'''This code uses 2014 colon cancer cases from the SEER dataset and aims to create variables
 to score cases on likelihood of receiving neoadjuvant care'''

#Importing and viewing various aspects of dataframe
#Importing pandas for data wrangling
from typing import Any, Union
import pandas as pd


# Importing the Neoadjuvant variables for colon cancer cases
from pandas import DataFrame
from pandas.io.parsers import TextFileReader

neocolon: Union[Union[TextFileReader, DataFrame], Any]= pd.read_csv('/Users/mbruno2/Documents/neo_colon.csv')

#Viewing head/tail  of the dataframe
neocolon.head()
neocolon.tail()

#Pulling description of dataframe
neocolon.describe()

#Creating list of variable names
for col in neocolon.columns:
    print(col)


#Counting number of observations
total_rows= neocolon.count()
    print(total_rows)

#Looking at participants <18 years old for special characteristics
neocolon.rename(columns={'Age recode with <1 year olds':'Age'}, inplace=True)
print(neocolon[neocolon['Age']<18])

print(neocolon['Immunotherapy'])











#Exploratory data analysis (EDA)
#Importing matplotlib for data visualization
import matplotlib.pyplot as plt

#Creating variables for outcome of interest
sys_surg_seq=neocolon['RX Summ--Systemic Surg Seq']
rad_surg_seq=neocolon['Radiation sequence with surgery']

#Histogram for Systemic-Surgery Sequence
plt.hist(sys_surg_seq, bins=8)
plt.xlabel('NAACCR code')
plt.ylabel('Number of observations')
plt.title('Distribution of cases for Systemic Surgery Sequence')
plt.show()

#Histogram for Radiation-Surgery Sequence
plt.hist(rad_surg_seq, bins=8)
plt.xlabel('NAACCR code')
plt.ylabel('Number of observations')
plt.title('Distribution of cases for Radiation Surgery Sequence')
plt.show()





'''In this next section we will be creating new neoadjuvant variables for future use in an algorithm
The following coding categories will be used for the new variables:
0= no neoadjuvant
1= unlikely neoadjuvant
2= possible neoadjuvant
3= likely neoadjuvant
4= unindicative of neoadjuvant
9= unknown'''




#Looking at the unique NAACCR codes for Chemotherapy
#Creating list from chemotherapy column
chemo_list=list(neocolon['Chemotherapy'])


def unique(list1):
    '''This function prints out the unique codes or values for list1'''
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    for x in unique_list:
        print(x)

print('The NAACCR codes for Chemotherapy are:')
unique(chemo_list)


#Creating new chemotherapy variable for use in algorithm
neocolon.loc[neocolon.Chemotherapy == 0,  'neo_chemotherapy'] = 0
neocolon.loc[neocolon.Chemotherapy == 1,  'neo_chemotherapy'] = 2
neocolon.loc[neocolon.Chemotherapy == 2,  'neo_chemotherapy'] = 2
neocolon.loc[neocolon.Chemotherapy == 3,  'neo_chemotherapy'] = 1
neocolon.loc[neocolon.Chemotherapy == 82, 'neo_chemotherapy'] = 1
neocolon.loc[neocolon.Chemotherapy == 85, 'neo_chemotherapy'] = 3
neocolon.loc[neocolon.Chemotherapy == 86, 'neo_chemotherapy'] = 4
neocolon.loc[neocolon.Chemotherapy == 87, 'neo_chemotherapy'] = 4
neocolon.loc[neocolon.Chemotherapy == 88, 'neo_chemotherapy'] = 2
neocolon.loc[neocolon.Chemotherapy == 99, 'neo_chemotherapy'] = 9

print(neocolon[['Chemotherapy','neo_chemotherapy']])
neo_chemotherapy=neocolon['neo_chemotherapy']


#Creating histogram of new neo_chemotherapy variable categories
x_ticks=[0, 1, 2, 3, 4, 9]
x_labs= ['no', 'unl', 'pos', 'lik', 'uni', 'unk']

plt.hist(neo_chemotherapy, bins=8)
plt.xlabel('Neoadjuvant category')
plt.ylabel('Number of observations')
plt.xticks(x_ticks,x_labs)
plt.title('Distribution of cases for neoadjuvant chemotherapy categories')
plt.show()








#Looking at the unique NAACCR codes for Immunotherapy
immuno_list=list(neocolon['Immunotherapy'])

print('The NAACCR codes for Immunotherapy are:')
unique()

#Creating new immunotherapy variable for use in algorithm
neocolon.loc[neocolon.Immunotherapy == 0,  'neo_immunotherapy'] = 0
neocolon.loc[neocolon.Immunotherapy == 1,  'neo_immunotherapy'] = 2
neocolon.loc[neocolon.Immunotherapy == 82, 'neo_immunotherapy'] = 1
neocolon.loc[neocolon.Immunotherapy == 85, 'neo_immunotherapy'] = 3
neocolon.loc[neocolon.Immunotherapy == 86, 'neo_immunotherapy'] = 4
neocolon.loc[neocolon.Immunotherapy == 87, 'neo_immunotherapy'] = 4
neocolon.loc[neocolon.Immunotherapy == 88, 'neo_immunotherapy'] = 2
neocolon.loc[neocolon.Immunotherapy == 99, 'neo_immunotherapy'] = 9

print(neocolon[['Immunotherapy','neo_immunotherapy']])
neo_immunotherapy=neocolon['neo_immunotherapy']


#Creating histogram of new neo_immunotherapy variable categories
x_ticks=[0, 1, 2, 3, 4, 9]
x_labs= ['no', 'unl', 'pos', 'lik', 'uni', 'unk']

plt.hist(neo_immunotherapy, bins=8)
plt.xlabel('Neoadjuvant category')
plt.ylabel('Number of observations')
plt.xticks(x_ticks,x_labs)
plt.title('Distribution of cases for neoadjuvant immunotherapy categories')
plt.show()







#Summing chemotherapy and immunotherapy variables
#importing numpy
import numpy as np

def neo_cat_sum(neo_var1, neo_var2):
    neoadj_sum = neocolon.loc[:, [neo_var1, neo_var2]]
    neoadj_sum_array = np.array(neoadj_sum)
    neo_tot = np.sum(neoadj_sum_array, axis=1)
    print(neo_tot)

neo_cat_sum(neocolon['neo_chemotherapy'],neocolon['neo_immunotherapy'])




#Selecting neoadjuvant variable columns to sum across & creating a numpy array
neoadj_sum=neocolon.loc[:, ['neo_chemotherapy','neo_immunotherapy']]
print(neoadj_sum)
neoadj_sum_array=np.array(neoadj_sum)

#Summing across the rows
neo_tot=np.sum(neoadj_sum_array, axis=1)
print(neo_tot)













#Testing

no_neo = [0]
unl_neo= [3, 82]
pos_neo= [88, 1, 2]
lik_neo= [84]
uni_neo= [86, 87]
unk_neo= [99]

neocolon.loc[neocolon.Chemotherapy in no_neo,   'neoTEST_chemotherapy'] = 0
neocolon.loc[neocolon.Chemotherapy in unl_neo,  'neoTEST_chemotherapy'] = 1
neocolon.loc[neocolon.Chemotherapy in pos_neo,  'neoTEST_chemotherapy'] = 2
neocolon.loc[neocolon.Chemotherapy in lik_neo,  'neoTEST_chemotherapy'] = 3
neocolon.loc[neocolon.Chemotherapy in uni_neo,  'neoTEST_chemotherapy'] = 4
neocolon.loc[neocolon.Chemotherapy in unk_neo,  'neoTEST_chemotherapy'] = 9
print(neocolon[['Chemotherapy', 'neo_chemotherapy', 'neoTEST_chemotherapy']])







#Creating function
def