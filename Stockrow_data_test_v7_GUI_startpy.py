# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:11:31 2019

@author: dhane
"""

import pandas as pd
import numpy as np
import tkinter

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', None)
#pd.set_option('display.float_format', '{:.3}'.format)

"""
TO DOs
1. Make scientific numbers into M/B or simple dollar amounts or percentages where applicable. 
Maybe do so row wise? DONE
2. Choose a relevant set of rows to keep for final df. DONE
3. Make download location changeable 

EXCEPTIONS HANDLING
1. Invalid ticker entered
2. Bad/invalid directory
3. 

GUI implementation
1. Choose metrics to check out
2. Companies data to pull
3. Create excel spreadsheet as final output
"""

def datesToMarkers(data, period, ticker, row_dict):
    #Takes column values dates and renmes to desired type 
    from datetime import datetime
    col_list=list(data.columns.values)
    new_col=[]
    index_time_level=""
    if period=='annual':
        index_time_level="Year"
        for i in col_list:
            reindex=str(i)[0:4]
            new_col.append(reindex)
    if period=='quarterly':
        index_time_level="Quarter"
        for i in col_list:
            i_year=str(i)[0:4]
            q1_date=datetime.strptime(i_year+'-01-01', '%Y-%m-%d').date()
            q2_date=datetime.strptime(i_year+'-04-05', '%Y-%m-%d').date()
            q3_date=datetime.strptime(i_year+'-07-05', '%Y-%m-%d').date()
            q4_date=datetime.strptime(i_year+'-10-05', '%Y-%m-%d').date()
            i_date=datetime.strptime(str(i)[0:10], '%Y-%m-%d').date()          
            if i_date>=q1_date and i_date<q2_date:
                reindex=str(i)[0:4]+'q1'
                new_col.append(reindex)
            elif i_date>=q2_date and i_date<q3_date:
                reindex=str(i)[0:4]+'q2'
                new_col.append(reindex)
            elif i_date>=q3_date and i_date<q4_date:
                reindex=str(i)[0:4]+'q3'
                new_col.append(reindex)
            else:
                reindex=str(i)[0:4]+'q4'
                new_col.append(reindex)               
    data.columns=new_col
    df_list=[]
    for i in new_col:
        data_final=pd.DataFrame(data[i])
        data_final[index_time_level]=i
        data_final.reset_index(inplace=True)       
        data_final=data_final.rename(columns={i:ticker, 'index': 'Metrics'})
        data_final=data_final.loc[data_final['Metrics'].isin(list(row_dict.keys()))]
        data_final.set_index([index_time_level, 'Metrics'], inplace=True)
        df_list.append(data_final)
    result=pd.concat(df_list)
    return result
   

def processData(ticker_list, data_type='metrics', time_type='annual', row_dict={'Market Cap': 'dollar'}): 
    df_list=[]
    #Get dataframe for each stock with relevant metrics for the given time type
    for ticker in ticker_list:
        filepath=r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data\{}_Financials_{}_{}.xlsx'.format(ticker, data_type, time_type)
        data=pd.read_excel(filepath, index_col=0)
        renamed_data=datesToMarkers(data, time_type, ticker, row_dict)
        df_list.append(renamed_data)
    
    #Merge dataframesfor the multiple companies
    index_time_level=''
    if time_type=='annual':
        index_time_level='Year'
    elif time_type=='quarterly':
        index_time_level='Quarter'
    display_df=pd.DataFrame(df_list[0])
    for i in df_list[1:]:
        display_df=display_df.merge(pd.DataFrame(i), how='inner', on=[index_time_level, 'Metrics'])
    
    #Make column values pretty
    #1. Commas for dollars
    #2. As is for ratios
    #3. % for yields/percentages
    df_T=display_df.T
    df_T=df_T.replace(to_replace=0, value=np.NaN)
    time_index_values=display_df.index.levels[0].values
    for key,value in row_dict.items():
        if value =='dollar':
            for i in time_index_values:
                df_T.loc(axis=1)[i,key]=df_T.loc(axis=1)[i,key].apply(lambda x: '{:,}'.format(int(x)))
        if value =='ratio':
            df_T.loc(axis=1)[:,key]=df_T.loc(axis=1)[:,key].apply(lambda x: round(x,4))
        if value =='percent':
            for i in time_index_values:
                df_T.loc(axis=1)[i,key]=df_T.loc(axis=1)[i,key].apply(lambda x: '{}%'.format(round(x*100, 2)))
    df_T=df_T.replace(to_replace='nan%', value=np.NaN)
    #print(df_T.T)

    
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
        excel_export_box=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Export to Excel (.xlsx)')))
        url=excel_export_box.get_attribute('href')
        #NOTE: Make download locations changeable 
        urllib.request.urlretrieve(url, r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data\{}_Financials_{}_{}.xlsx'.format(ticker, data_type, time_type))       
    driver.close()
    
row_dict=({'Market Cap': 'dollar', 
           'Enterprise Value': 'dollar', 
           'Working Capital': 'dollar',
           'Tangible Asset Value': 'dollar',
           'Net Current Asset Value': 'dollar',
           'Invested Capital': 'dollar',
           'PE ratio': 'ratio', 
           'PB ratio': 'ratio', 
           'PS ratio': 'ratio',
           'R&D to Revenue': 'ratio', 
           'Debt to Equity': 'ratio', 
           'Debt to Assets': 'ratio',
           'Earnings Yield': 'percent', 
           'Dividend Yield': 'percent', 
           'ROIC': 'percent',
           'ROE': 'percent',
           'Return on Tangible Assets': 'percent',
           
           })
            
ticker_list=[]
def get_ticker_list():
    tickers=entry_company.get()
    ticker_list=tickers.split(' ')
    print(tickers)
    print(ticker_list)
row_list=[]
#checkbutton_list=[]
checkbutton_dict={}
def get_row_state():
    for key, value in checkbutton_dict.items():
        print(var.get())
        row_list.append(var.get())
    print(row_list)
#Tkinter GUI implementation
window=tkinter.Tk()
window.title('Company Financial Data Fetching')
#top_frame=tkinter.Frame(window).pack()
#bottom_frame=tkinter.Frame(window).pack(side='bottom')
#input_text=tkinter.StringVar()

label_enter_company=tkinter.Label(window, text= "Please enter company tickers of interest (separated by spaces)").grid(row=0, columnspan=3)
entry_company=tkinter.Entry(window)
entry_company.grid(row=1, columnspan=3)
choose_metrics_button=tkinter.Button(window, text="Update company selection", command=get_ticker_list).grid(columnspan=3, row=2)
label_metric_choice=tkinter.Label(window, text="Please enter choose metrics of interest (check all that apply)").grid(row=3, columnspan=3)
#"""
grid_row=4

#checklabel_list=[]
for key, value in row_dict.items():
    var=tkinter.BooleanVar()
    check_button=tkinter.Checkbutton(window, text=key, variable=var)
    check_button.grid(columnspan=2, row=grid_row)
    #checkbutton_list.append(check_button)
    grid_row+=1
choose_metrics_button=tkinter.Button(window, text="Update row selection", command=get_row_state).grid(columnspan=3, row=grid_row)
grid_row+=1
generate_button=tkinter.Button(window, text="Generate excelsheet").grid(columnspan=3, row=grid_row)
grid_row+=1


#print(checkbutton_list)
#"""

#RUN PROGRAM    
window.mainloop()
#ticker_list=['BA', 'GILD', 'FDX', 'AMZN', 'AAPL', 'GOOGL']
download_dir=r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Company_financial_data'
#pullData(ticker_list, directory=download_dir, time_type='quarterly')
#data=processData(ticker_list, time_type='quarterly', row_dict=row_dict)
