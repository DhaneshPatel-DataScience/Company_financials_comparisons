# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:11:31 2019

@author: dhane
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 10)
pd.set_option('display.width', None)


def datesToMarkers(data, period):
    #Takes column values dates and renmes to desired type 
    from datetime import datetime
    col_list=list(data.columns.values)
    new_col=[]
    if period=='annual':
        for i in col_list:
            reindex=str(i)[0:4]
            new_col.append(reindex)
    if period=='quarterly':
        for i in col_list:
            #print(str(i)[4:10])
            #NOTE: need to convert these matching strings to datetime 
            #and specify intervals that define each quarter 
            #(so companies like FDX gets columns properly renamed)
            #DONE
            
            #print(i)
            #print(type(i))
            i_year=str(i)[0:4]
            q1_date=datetime.strptime(i_year+'-01-01', '%Y-%m-%d').date()
            q2_date=datetime.strptime(i_year+'-04-01', '%Y-%m-%d').date()
            q3_date=datetime.strptime(i_year+'-07-01', '%Y-%m-%d').date()
            q4_date=datetime.strptime(i_year+'-10-01', '%Y-%m-%d').date()
            i_date=datetime.strptime(str(i)[0:10], '%Y-%m-%d').date()
            #print("q1_date: {}".format(q1_date))
            #print("i_date: {}".format(i_date))
            
            if i_date>=q1_date and i_date<q2_date:
                reindex=str(i)[0:4]+'q1'
                #print("Reindex is: " + reindex)
                new_col.append(reindex)
            elif i_date>=q2_date and i_date<q3_date:
                reindex=str(i)[0:4]+'q2'
                #print("Reindex is: " + reindex)
                new_col.append(reindex)
            elif i_date>=q3_date and i_date<q4_date:
                reindex=str(i)[0:4]+'q3'
                #print("Reindex is: " + reindex)
                new_col.append(reindex)
            else:
                reindex=str(i)[0:4]+'q4'
                #print("Reindex is: " + reindex)
                new_col.append(reindex)
            """
            if str(i)[4:10]=='-03-31':
                reindex=str(i)[0:4]+'q1'
                new_col.append(reindex)
            elif str(i)[4:10]=='-12-31':
                reindex=str(i)[0:4]+'q4'
                new_col.append(reindex)
            elif str(i)[4:10]=='-09-30':
                reindex=str(i)[0:4]+'q3'
                new_col.append(reindex)
            elif str(i)[4:10]=='-06-30':
                reindex=str(i)[0:4]+'q2'
                new_col.append(reindex)
            """
    #print(new_col)
    data.columns=new_col
    #Reorganizing data columns
    return data

"""
def reOrganizeColumns(clean_data):
    col_list=list(clean_data.columns.values)
    for i in col_list:
        clean_data.iloc[]
"""  
#def fetchColumn(renamed_data, column='2019q1'):
    

def processData(ticker_list, data_type='metrics', time_type='annual', column_analysis='2019q1'):
   
    for ticker in ticker_list:
        print(ticker)
        filepath=r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data\{}_Financials_{}_{}.xlsx'.format(ticker, data_type, time_type)
        data=pd.read_excel(filepath, index_col=0)
        #print(time_type)
        renamed_data=datesToMarkers(data, time_type)
        #print(clean_data)
        final_df=renamed_data[column_analysis]
        print(final_df)

def pullData(ticker_list, directory, data_type='metrics', time_type='annual'):
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    import urllib.request 
    options=webdriver.ChromeOptions()
    prefs={'download.default_directory': directory}
    options.add_experimental_option('prefs', prefs)
    driver=webdriver.Chrome(options=options)
    for ticker in ticker_list:
        driver.get('https://stockrow.com/{}/financials/{}/{}'.format(ticker, data_type, time_type))
        excel_export_box=WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Export to Excel (.xlsx)')))
        url=excel_export_box.get_attribute('href')
        urllib.request.urlretrieve(url, r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data\{}_Financials_{}_{}.xlsx'.format(ticker, data_type, time_type))       
    driver.close()
               
ticker_list=['BA', 'GILD', 'FDX']
download_dir=r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data'
#pullData(ticker_list, directory=download_dir, time_type='quarterly')

data=processData(ticker_list, time_type='quarterly', column_analysis='2019q1')
#for i in ticker_list:
    #data=processData(i)