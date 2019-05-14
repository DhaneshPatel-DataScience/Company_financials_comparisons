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
    col_list=list(data.columns.values)
    #col_index=list(range(0,len(col_list)))
    new_col=[]
    if period=='a':
        for i in col_list:
            reindex=str(i)[0:4]
            new_col.append(reindex)
    data.columns=new_col
    return data

"""
def reOrganizeColumns(clean_data):
    col_list=list(clean_data.columns.values)
    for i in col_list:
        clean_data.iloc[]
"""  

def processData(ticker, period='a', q_start='2009q2', q_end='2019q1'):
    filepath=r'C:\Users\dhane\OneDrive\Documents\Data_Science_and_Machine_Learning\Python_code_files\Pratical_AI_Applications_Examples\Stock_data_website\Stockrow_excel_exports\financials_{}_{}.xlsx'.format(period, ticker)
    #print(filepath)
    data=pd.read_excel(filepath, index_col=0)
    clean_data=datesToMarkers(data, period)
    print(clean_data)

def pullData(ticker_list, data_type='metrics', time_type='annual'):
    import os
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    driver=webdriver.Chrome()
    for ticker in ticker_list:
        driver.get('https://stockrow.com/{}/financials/{}/{}'.format(ticker, data_type, time_type))
        #excel_export_box=driver.find_element_by_partial_link_text('Export to Excel (.xlsx)')
        #excel_export_box=driver.find_element_by_class_name('button hollow expanded')
        #excel_export_box=driver.find_element_by_css_selector('#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.company-financials > div > div.grid-x.align-center.grid-margin-x.control-buttons > div.cell.medium-7 > a')
        #excel_export_box=driver.find_element_by_xpath('//*[@id="root"]/div/div/section/div/div[2]/div[1]/section[4]/div/div[1]/div[2]/a')
        
        #excel_export_box=driver.find_element_by_xpath('//*[@id="root"]/div/div/section/div/div[2]/div[1]/section[4]/div/div[1]/div[2]/a')
        #excel_export_box=driver.find_element_by_xpath('//*[@id="root"]/div/div/section/div/div[2]/div[1]/section[4]/div/div[1]/div[1]/button')
        #excel_export_box=driver.find_element_by_link_text('Export to Excel (.xlsx)')
        excel_export_box=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.company-financials > div > div.grid-x.align-center.grid-margin-x.control-buttons > div.cell.medium-7 > a')))
        
        #//*[@id="root"]/div/div/section/div/div[2]/div[1]/section[4]/div/div[1]/div[2]/a
        #//*[@id="root"]/div/div/section/div/div[2]/div[1]/section[4]/div/div[1]/div[2]/a
        ##root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.company-financials > div > div.grid-x.align-center.grid-margin-x.control-buttons > div.cell.medium-7 > a
        #document.querySelector('#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.company-financials > div > div.grid-x.align-center.grid-margin-x.control-buttons > div.cell.medium-7 > a')
        #<a class="button hollow expanded" href="/api/companies/B/financials.xlsx?dimension=MRY&amp;section=Metrics&amp;sort=desc" target="_blank">Export to Excel (.xlsx)</a>
        #<a class="button hollow expanded" href="/api/companies/B/financials.xlsx?dimension=MRY&amp;section=Metrics&amp;sort=desc" target="_blank">Export to Excel (.xlsx)</a>
        excel_export_box.click()
        #search_box=driver.find_element_by_id('react-select-2--option-null')
        #search_box.send_keys(ticker)
        break
        
ticker_list=['BA', 'GILD', 'FDX']
pullData(ticker_list)
data=processData('FDX', 'a')