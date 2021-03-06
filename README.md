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

#Brief coding background
National Association of American Central Cancer Registries (NAACCR) coding
for the SEER Chemotherapy Variable.

    00	None, chemotherapy was not part of the planned first course of therapy.
    01	Chemotherapy, NOS.
    02	Chemotherapy, single agent.
    03	Chemotherapy, multiple agents.
    82	Chemotherapy was not recommended/administered because it was contraindicated due to patient risk factors (i.e., comorbid conditions, advanced age).
    85	Chemotherapy was not administered because the patient died prior to planned or recommended therapy.
    86	Chemotherapy was not administered. It was recommended by the patient's physician, but was not administered as part of first-course therapy. No reason was stated in the patient record.
    87	Chemotherapy was not administered; it was recommended by the patient's physician, but this treatment was refused by the patient, the patient's family member, or the patient's guardian. The refusal was noted in the patient record.
    88	Chemotherapy was recommended, but it is unknown if it was administered.
    99	It is unknown whether a chemotherapeutic agent(s) was recommended or administered because it is not stated in patient record; death certificate-only cases.

Neoadjuvant coding categories for algorithm:

    0   No neoadjuvant therapy would be administered
    1   Unlikely 
    2   Possible 
    3   Likely 
    4   Unindicative of neoadjuvant therapy
    9   Unknown


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

    ![](/Users/mbruno2/Documents/steps.png)

#Steps 1-3 (import and wrangling)
import pandas as pd
    pd.read_csv('/Users/mbruno2/Documents/neo_colon.csv')

    print(neocolon.head())
    print(neocolon.tail())
    print(neocolon.describe())
    neocolon.shape()
    
       Age recode with <1 year olds  ...  Immunotherapy recode (yes, no/unk)
    0                            18  ...                                   0
    1                            17  ...                                   0
    2                            15  ...                                   0
    3                            18  ...                                   0
    4                            18  ...                                   0


       Age recode with <1 year olds  ...  Immunotherapy recode (yes, no/unk)
    count                  25092.000000  ...                        25092.000000
    mean                      14.221226  ...                            0.050136
    std                        2.706808  ...                            0.218229
    min                        3.000000  ...                            0.000000
    25%                       12.000000  ...                            0.000000
    50%                       14.000000  ...                            0.000000
    75%                       16.000000  ...                            0.000000
    max                       18.000000  ...                            1.000000
    
    neocolon.shape
    (25092, 53)


Creating list of variable names:

    for col in neocolon.columns:
         print(col)

    Age recode with <1 year olds
    Sex
    Year of diagnosis
    Month of diagnosis
    SEER registry
    CS Schema v0204+
    Diagnostic Confirmation
    Type of Reporting Source
    Primary Site
    Site recode ICD-O-3/WHO 2008
    Grade
    Grade Path Value
    Grade Path System
    Histologic Type ICD-O-3
    Behavior code ICD-O-3
    Behavior code ICD-O-3 (in-house)
    Histology recode - broad groupings
    SEER Summary Stage 2000
    Derived AJCC Stage Group, 6th ed (2004+)
    Derived AJCC Stage Group, 7th ed (2010+)
    CS tumor size (2004+)
    Regional nodes positive (1988+)
    CS mets at DX-bone (2010+)
    CS mets at DX-brain (2010+)
    CS mets at DX-liver (2010+)
    CS mets at DX-lung (2010+)
    CS mets at DX-bone (in-house)
    CS mets at DX-brain (in-house)
    CS mets at DX-liver (in-house)
    CS mets at DX-lung (in-house)
    RX Year of Surgery
    RX Month of Surgery
    RX Year of Mst Defn Srg
    RX Month of Mst Defn Srg
    RX Year of Radiation
    RX Month of Radiation
    RX Year of Chemo
    RX Month of Chemo
    RX Summ--Treatment Status (2010+)
    RX Summ--Surg Prim Site (1998+)
    RX Summ--Scope Reg LN Sur (2003+)
    RX Summ--Surg Oth Reg/Dis (2003+)
    RX Summ--Systemic Surg Seq
    RX Summ--Transplnt/Endocr
    Reason no cancer-directed surgery
    Radiation sequence with surgery
    Chemotherapy
    Hormone therapy
    Immunotherapy
    Radiation recode
    Chemotherapy recode (yes, no/unk)
    Hormone therapy recode (yes, no/unk)
    Immunotherapy recode (yes, no/unk)



Renaming 'age' variable and viewing observations <18yo

    neocolon.rename(columns={'Age recode with <1 year olds':'Age'}, inplace=True)
    print(neocolon[neocolon['Age']<18])
    
    


#Step 4: Exploratory Data Analysis (EDA)

Creating variables for the two outcomes of interest

    sys_surg_seq=neocolon['RX Summ--Systemic Surg Seq']
    rad_surg_seq=neocolon['Radiation sequence with surgery']

Histogram for Systemic-Surgery Sequence

    plt.hist(sys_surg_seq, bins=8)
    plt.xlabel('NAACCR code')
    plt.ylabel('Number of observations')
    plt.title('Distribution of cases for Systemic Surgery Sequence')
    plt.xticks(x_ticks_seq)
    plt.show()
   ![](/Users/mbruno2/Documents/sys_surg_seq.png)
   
        0	No systemic therapy and/or surgical procedures; unknown if surgery and/or systemic therapy given
        2	Systemic therapy before surgery
        3	Systemic therapy after surgery
        4	Systemic therapy both before and after surgery
        5	Intraoperative systemic therapy
        6	Intraoperative systemic therapy with other therapy administered before and/or after surgery
        7	Surgery both before and after systemic therapy
        9	Sequence unknown, but both surgery and systemic therapy given

Histogram for Radiation-Surgery Sequence

    plt.hist(rad_surg_seq, bins=8)
    plt.xlabel('NAACCR code')
    plt.ylabel('Number of observations')
    plt.title('Distribution of cases for Radiation Surgery Sequence')
    plt.xticks(x_ticks_seq)
    plt.show()
   ![](/Users/mbruno2/Documents/rad_surg_seq.png)
   
   
        0	No radiation and/or no surgery; unknown if surgery and/or radiation given
        2	Radiation before surgery
        3	Radiation after surgery
        4	Radiation both before and after surgery
        5	Intraoperative radiation
        6	Intraoperative radiation with other radiation given before and/or after surgery
        7	Surgery both before and after radiation
        9	Sequence unknown, but both surgery and radiation were given

#Step 5: Creating new variables to use in algorithm (first attempt)

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
    
    #Adding total as column in neocolon dataframe
    neo_tot= neo_cat_sum('neo_chemotherapy','neo_immunotherapy')
    neocolon['neo_tot']=neo_tot
    
    neocolon['neo_chemotherapy']=neo_chemotherapy.astype(int)
    neocolon['neo_immunotherapy']=neo_immunotherapy.astype(int)
    print(neocolon[['neo_chemotherapy', 'neo_immunotherapy', 'neo_tot']])
    
               neo_chemotherapy  neo_immunotherapy  neo_tot
        0                     0                  0      0.0
        1                     0                  0      0.0
        2                     0                  0      0.0
        3                     0                  0      0.0
        4                     0                  0      0.0
        5                     1                  0      1.0
        6                     0                  0      0.0
        7                     0                  0      0.0
        8                     0                  0      0.0
        9                     0                  0      0.0
        10                    0                  0      0.0
        11                    0                  0      0.0
        12                    1                  2      3.0
        13                    2                  0      2.0


#Function for creating new neoadjuvant variables
This function translates the original NAACCR codes into the new neoadjuvant coding categories

     #Lists for translating NAACCR codes into neoadjuvant codes
        no_neo = [0]
        unl_neo= [3, 82]
        pos_neo= [88, 1, 2]
        lik_neo= [85]
        uni_neo= [86, 87]
        unk_neo= [99]


    def translate_to_neo(og_var):
        '''This function translates the original NAACCR variable coding into the new
        neoadjuvant variable codings and returns a list with the new codings'''
        #Creating empty list for new neoadjuvant variable codes
        new_neo_var=[]
        #Creating new variable codes from above lists of neoadjuvant codes
        for code in og_var:
            if code in no_neo:
                new_neo_var.append(0)
            if code in unl_neo:
                new_neo_var.append(1)
            if code in pos_neo:
                new_neo_var.append(2)
            if code in lik_neo:
                new_neo_var.append(3)
            if code in uni_neo:
                new_neo_var.append(4)
            if code in unk_neo:
                new_neo_var.append(9)
        return new_neo_var

    chemotherapy_neo=translate_to_neo(neocolon["Chemotherapy"])
    neocolon['chemotherapy_neo']=chemotherapy_neo
    print(neocolon[['neo_chemotherapy', 'chemotherapy_neo']])
    
           neo_chemotherapy  chemotherapy_neo
    0                     0                 0
    1                     0                 0
    2                     0                 0
    3                     0                 0
    4                     0                 0
    5                     1                 1
    6                     0                 0
    7                     0                 0
    8                     0                 0
    9                     0                 0
    

    
#Next steps
- Create neoadjuvant category variables for all chosen indicators
- Create descriptive statistics and tables for new categorizations
- Calculate Se, Sp, PPV, and F-score to evaluate performance against outcome sequence variables
- Test on other cancer sites (ex: breast)
- Validate using SEER*Medicare data
