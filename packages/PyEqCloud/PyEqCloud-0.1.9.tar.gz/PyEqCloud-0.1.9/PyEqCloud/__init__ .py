import requests
import pandas as pd
from pandas.io.json import json_normalize                      
import getpass
from tqdm import tqdm

import warnings; warnings.filterwarnings('ignore')

def set_user_creds():
    print('Please fill in:')
    print('Equipment Cloud username:')
    username = input()
    print('')
    print('Password:')
    password = getpass.getpass()
    print('')
    #return user, pwd
    
## umwandeln aller columns in numbers
def fkt_columns_to_numbers(df_input): 
    for i_col in tqdm(df_input.columns):
        # converting to numeric
        try:
            #df_input[i_col] = df_input[i_col].astype('float64')
            df_input[i_col] = pd.to_numeric(df_input[i_col],downcast='signed')
        #except ValueError:
        except:
            print('not converted to numeric:', i_col)   

class EqCloudRestApiWrapper:
    # Initializer / Instance Attributes
    def __init__(self, username, password, customerID, url="https://eqcloud.ais-automation.com/customerID/cloudconnect/api/monitoring/v2/history/things/"):
        self.username = username
        self.password = password
        self.url = url.replace('customerID',customerID)
        self.customerID = customerID
        
    def request_processvalues(self, equipment, startTime, endTime, columnList):
        temp_df = pd.DataFrame()
        for i in tqdm(range(len(columnList))):
            pagination_df = pd.DataFrame()
            next_step = True
            step = 1
            while next_step:
#                 code = {
#                         'qp':"{"+'"'+"ts_start"+'":'+'"'+startTime+"+01:00"+'"'+","+'"'+"ts_end"+'"'+':'+'"'+endTime+"+01:00"+'"'+"}",
#                         'step':step
#                         }
                code = {
                         'qp':"{"+'"'+"ts_start"+'":'+'"'+startTime+'"'+","+'"'+"ts_end"+'"'+':'+'"'+endTime+'"'+"}",
                         'step':step
                         }
                print(code)
                response = requests.get(self.url + equipment + "/processvalues/" + columnList[i].strip().replace("'","") + "",
                                         auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                                         params=code,
                                         verify=False)
                json = response.json()
                print(json)
                df = pd.DataFrame.from_dict(json['items'])
                #dd = pd.DataFrame.from_dict(json['controls'])
                df['ChannelID'] = columnList[i].strip().replace("'","")
                if "value_string" in df.columns:
                    df.rename(columns={'value_string': 'value'}, inplace=True)
                if json['controls'][0]['next'] is not None:
                    step += 1
                else:
                    next_step = False
                frames = [pagination_df,df]
                pagination_df = pd.concat(frames,sort=True)
            frames = [temp_df,pagination_df]
            temp_df = pd.concat(frames,sort=True)
        EQ_Cloud_DataFrame = pd.DataFrame()
        temp_df["timestamp"]= temp_df["timestamp"].str.rstrip('Z') 
        temp_df.timestamp = pd.to_datetime(temp_df.timestamp)
        EQ_Cloud_DataFrame = temp_df.pivot_table(values='value', index=['timestamp'], columns=['ChannelID'], aggfunc=lambda x: ' '.join(str(v) for v in x))
        fkt_columns_to_numbers(EQ_Cloud_DataFrame)
        return EQ_Cloud_DataFrame
    
    def request_alarms(self, equipment, startTime, endTime):
        pagination_df = pd.DataFrame()
        step = 1
        next_step = True
        while next_step:
            code = {
                    'qp':"{"+'"'+"ts_start"+'":'+'"'+startTime+"+01:00"+'"'+","+'"'+"ts_end"+'"'+':'+'"'+endTime+"+01:00"+'"'+"}",
                    'step':step
                   }
            response = requests.get(self.url + equipment + "/alarms"+"",
                                     auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                                     params=code,
                                     verify=False)
            json = response.json()
            df = pd.DataFrame.from_dict(json['items'])
            if json['controls'][0]['next'] is not None:
                    step += 1
            else:
                    next_step = False
            frames = [pagination_df,df]
            pagination_df = pd.concat(frames,sort=True)
            pagination_df["ts_start"]= pagination_df["ts_start"].str.rstrip('Z') 
            pagination_df["ts_end"]= pagination_df["ts_end"].str.rstrip('Z') 
            pagination_df.ts_start = pd.to_datetime(pagination_df.ts_start)
            pagination_df.ts_end = pd.to_datetime(pagination_df.ts_end)
        return pagination_df
    
    def request_states(self, equipment, startTime, endTime):
        pagination_df = pd.DataFrame()
        step = 1
        next_step = True
        while next_step:
            code = {
                    'qp':"{"+'"'+"ts_start"+'":'+'"'+startTime+"+01:00"+'"'+","+'"'+"ts_end"+'"'+':'+'"'+endTime+"+01:00"+'"'+"}",
                    'step':step
                   }
            response = requests.get(self.url + equipment + "/states"+"",
                                     auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                                     params=code,
                                     verify=False)
            json = response.json()
            df = pd.DataFrame.from_dict(json['items'])
            if json['controls'][0]['next'] is not None:
                    step += 1
            else:
                    next_step = False
            frames = [pagination_df,df]
            pagination_df = pd.concat(frames,sort=True)
            pagination_df["ts_start"]= pagination_df["ts_start"].str.rstrip('Z') 
            pagination_df["ts_end"]= pagination_df["ts_end"].str.rstrip('Z') 
            pagination_df.ts_start = pd.to_datetime(pagination_df.ts_start)
            pagination_df.ts_end = pd.to_datetime(pagination_df.ts_end)
        return pagination_df
    
    def request_units(self, equipment, startTime, endTime):
        pagination_df = pd.DataFrame()
        step = 1
        next_step = True
        while next_step:
            code = {
                    'qp':"{"+'"'+"ts_start"+'":'+'"'+startTime+"+01:00"+'"'+","+'"'+"ts_end"+'"'+':'+'"'+endTime+"+01:00"+'"'+"}",
                    'step':step
                   }
            response = requests.get(self.url + equipment + "/units"+"",
                                     auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                                     params=code,
                                     verify=False)
            json = response.json()
            df = pd.DataFrame.from_dict(json['items'])
            if json['controls'][0]['next'] is not None:
                    step += 1
            else:
                    next_step = False
            frames = [pagination_df,df]
            pagination_df = pd.concat(frames,sort=True)
            pagination_df["timestamp"]= pagination_df["timestamp"].str.rstrip('Z') 
            pagination_df.timestamp = pd.to_datetime(pagination_df.timestamp)
        return pagination_df

    