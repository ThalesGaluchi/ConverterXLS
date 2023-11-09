import pandas as pd

PATH=''

class CONFIG:
    # PATH = 'OTPDataset1028.xls'
    # data = pd.read_excel(PATH)

    test_id = { 3010 : 'afp',  
        3000 : 'cea', 
        3050 : 'ca19_9',
        3040 : 'ca125', 
        3020 : 'tpsa',
        3030 : 'ca15_3', 
        3060 : 'cyfra21_1', 
        6004 : 'apoa1', 
        4020 : 'he4',
        6014 : 'crp',
        6006 : 'b2m', 
        6020 : 'ttr'
        }
    
    
def get_patient_info(PATH):
        
    input_cols_patient = [ 
            'ACCESSION',
            'PATIENT_F_NAME',
            'PATIENT_L_NAME', 
            'PATIENT_BIRTH', 
            'RECEIVED_DATE',
            'COLLECT_DATE' ,
            'REQ_DATE',
            'PATIENT_GENDER', 
            ]
    
    output_cols_patient = [
        'ACCESSION',
        'name', 'dob', 'gender',  'type',  
        'received date',  'blood date', 'test date',
    ]

    data = pd.read_excel(PATH)
    def format_date(d):
        return f'{d[8:10]}-{d[5:7]}-{d[:4]}'

    test_type = 'OneTest Premium'
    patients = []
    
    # 2.1. Loop on unique 'ACCESSION' ids
    for id in data.ACCESSION.unique():
        
        temp = data.loc[data.ACCESSION==id][input_cols_patient].drop_duplicates()
        
        # 3. Name: from 'PATIENT_F_NAME' and 'PATIENT_L_NAME' to 'name' [A]
        name = temp['PATIENT_F_NAME'] + ' ' + temp['PATIENT_L_NAME']
        name = name.iloc[0]
        
       # 4. Date of birthday: from 'PATIENT_BIRTH' MM/DD/YYY to 'dob' DD-MM-YYYY
        dob = format_date(str(temp['PATIENT_BIRTH'].iloc[0]))      
        
        # 5. Gender: PATIENT_GENDER ['Male', 'Female' ] to 'gender' ['m', 'f' ]
        gender = temp['PATIENT_GENDER'].iloc[0]
        
        # 6. Received Date: 'RECEIVED_DATE' to 'received date',  MM/DD/YYY to 'dob' DD-MM-YYYY
        received_date = format_date(str(temp['RECEIVED_DATE'].iloc[0]))
        
        # 7. Collect Date:  'COLLECT_DATE' to 'blood date', MM/DD/YYY to 'dob' DD-MM-YYYY
        blood_date = format_date(str(temp['COLLECT_DATE'].iloc[0]))
     
        # 8. Required data 'REQ_DATE' to 'test date', MM/DD/YYY to 'dob' DD-MM-YYYY        
        test_date = format_date(str(temp['REQ_DATE'].iloc[0]))                
        
        # 9. Append patient info to a bigger list
        patients.append( [id, name, dob, gender, test_type, received_date, blood_date, test_date ])
    
    # Convert the list to a DataFrame
    result = pd.DataFrame( patients, columns=output_cols_patient)
    result['gender'].replace({'Female': 'f', 'Male': 'm'}, inplace = True)
    # result.set_index('accession', inplace=True)
        
    return result


def get_results(PATH):
    
    
    
    data = pd.read_excel(PATH)

    # Slice the Accession, Test_Id and Result
    df_temp = data[['ACCESSION', 'TEST_ID', 'RESULT_NUMERIC'] ]
    df_temp.set_index( ['ACCESSION','TEST_ID'], inplace = True)
    df_temp = df_temp.unstack(0)
    
    # Slice Required tests only
    df_temp = df_temp.loc[pd.Index(CONFIG.test_id)].T
    
    df_temp.reset_index(inplace=True)
    df_temp.drop('level_0', axis = 1, inplace=True)
    
    # Rename the columns
    df_temp.rename(columns=CONFIG.test_id, inplace = True)

    return df_temp


def convert_columns(PATH_INPUT, PATH_OUTPUT):
    
    if PATH_OUTPUT == '':
        return ""
    
    # 1. Determine the columns to be used in the output file
    cols = [ 'accession', 
                'name', 'dob', 'gender',  'type',  
            'received date',  'blood date', 'test date',
            
            'afp',  'cea', 'ca19_9', 'ca125', 'tpsa',
            'ca15_3', 'cyfra21_1', 'apoa1', 'he4',
            'crp','b2m', 'ttr' ]
    
    # 2. Load input Excel file
    # data = pd.read_excel(PATH)
    
    patient_info = get_patient_info(PATH_INPUT)       

    # Convert the Accession table to a Acession - test table
    df_test_results = get_results(PATH_INPUT)

    result = pd.merge(patient_info, df_test_results, how='left', on='ACCESSION' )
    result.drop('ACCESSION', axis=1, inplace = True)
    result.to_excel(PATH_OUTPUT, index = False)
    
    # return result
