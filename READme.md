#Leveraging Current Surveillance Epidemiology and End Results (SEER) Data Elements to Characterize Receipt of Neoadjuvant Treatment

BIOF 309 Spring 2019 Final Project

Melissa Bruno

#Background
- Neoadjuvant therapy, also referred to as induction therapy, is generally defined as systemic therapy given before localized cancer treatment. 
- Routine and accurate collection of this treatment sequence is essential to better understand therapeutic effectiveness and guide strategies in treatment plan for cancer care.
- Problem: a standardized definition for neoadjuvant data collection does not exist in the literature.

#Objective
We aim to leverage existing Surveillance, Epidemiology and End Results (SEER) data elements to investigate the development of an algorithm using data items collected and transmitted through SEER to calculate a score to characterize the likelihood a patient received neoadjuvant treatment.


   ![](/Users/mbruno2/Documents/SEER.png)



#Methods
- Dataset: SEER 2010-2016 colon cancer cases
- The algorithm will use a set of 35 elements selected as the most neoadjuvant-informative variables the score calculation
- These chosen indicator variables will then be translated into the following categories to help calculate neoadjuvant treatment scores: no neoadjuvant treatment, unlikely, possible, definite neoadjuvant treatment, unindicative, and unknown
- The algorithm will then be validated using the SEER*Medicare linked dataset

#First steps with Python
1. Import data as a CSV file
2. View various aspects of the dataset to ensure import was done correctly
3. Data wrangling
4. Exploratory Data Analysis (EDA)
5. Creation of new neoadjuvant variables

#Steps 1-3 (import and wrangling)
import pandas as pd
    pd.read_csv('/Users/mbruno2/Documents/neo_colon.csv')

    neocolon.head()
    neocolon.tail()
    neocolon.describe()

Creating list of variable names:

    for col in neocolon.columns:
         print(col)

Renaming 'age' variable and viewing observations <18yo

    neocolon.rename(columns={'Age recode with <1 year olds':'Age'}, inplace=True)
    print(neocolon[neocolon['Age']<18])

#Step 4: Exploratory Data Analysis (EDA)
import matplotlib.pyplot as plt

Creating variables for the two outcomes of interest

    sys_surg_seq=neocolon['RX Summ--Systemic Surg Seq']
    rad_surg_seq=neocolon['Radiation sequence with surgery']

Histogram for Systemic-Surgery Sequence

    plt.hist(sys_surg_seq, bins=8)
    plt.xlabel('NAACCR code')
    plt.ylabel('Number of observations')
    plt.title('Distribution of cases for Systemic Surgery Sequence')
    plt.show()
   ![](/Users/mbruno2/Documents/sys_surg_seq.png)

Histogram for Radiation-Surgery Sequence

    plt.hist(rad_surg_seq, bins=8)
    plt.xlabel('NAACCR code')
    plt.ylabel('Number of observations')
    plt.title('Distribution of cases for Radiation Surgery Sequence')
    plt.show()
   ![](/Users/mbruno2/Documents/rad_surg_seq.png)

#Step 5: Creating new variables to use in algorithm

First looking at the the unique codes for chemotherapy using the following function:

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
    
      The NAACCR codes for Chemotherapy are:
        0
        1
        2
        3
        99
        82
        85
        86
        87
        88


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
    
    x_ticks=[0, 1, 2, 3, 4, 9]
    x_labs= ['no', 'unl', 'pos', 'lik', 'uni', 'unk']
    
    plt.hist(neo_chemotherapy, bins=8)
    plt.xlabel('Neoadjuvant category')
    plt.ylabel('Number of observations')
    plt.xticks(x_ticks,x_labs)
    plt.title('Distribution of cases for neoadjuvant chemotherapy categories')
    plt.show()
   ![](/Users/mbruno2/Documents/neo_chemo_dist.png)

    
    
    
#Function for creating new variables (draft)

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
    
    

#Function to sum neoadjuvant scores across cases

    #Summing chemotherapy and immunotherapy variables
    #importing numpy
    import numpy as np
    
    def neo_cat_sum(neo_var1, neo_var2):
        '''This function changes the columns of neo_var1 & neo_var2 into
        numpy arrays that can be summed across rows'''
        
        #Creating new dataframe with neo_var1 and neo_var2 as columns
        neoadj_sum = neocolon.loc[:, [neo_var1, neo_var2]]
        
        #Changing new dataframe into numpy array
        neoadj_sum_array = np.array(neoadj_sum)
        
        #Summing across the rows of the dataframe and printing the totals as an array
        neo_tot = np.sum(neoadj_sum_array, axis=1)
        print(neo_tot)
    
    neo_cat_sum('neo_chemotherapy','neo_immunotherapy')
    
Looking into how to add array of row sums as a column back in the neoadj_sum dataframe


    
#Next steps
- Create neoadjuvant category variables for all chosen indicators
- Create descriptive statistics and tables for new categorizations
- Calculate Se, Sp, PPV, and F-score to evaluate performance against outcome sequence variables
- Test on other cancer sites (ex: breast)
- Validate using SEER*Medicare data
