#coding=utf-8
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from splinter import Browser
from selenium import webdriver
import time
import re
import os
import glob
import numpy as np
import pandas as pd
import random


allFiles = glob.glob('*.txt')

def login(browser,user_name,password):
	while not browser.find_by_xpath('//*[@id="gr-register-step1"]/div[9]/strong'):
		browser.reload()
		time.sleep(3)
	try:
		browser.find_by_xpath('//*[@id="gr-register-step1"]/div[9]/strong').first.click()
	except:
		browser.reload()
	time.sleep(3)
	print ("start to fill usrname")
	browser.find_by_id('gr_input_nickname').fill(user_name)
	print ('start to fill password')
	browser.find_by_id('gr_input_pwd1').click()
	browser.find_by_id('gr_input_pwd2').fill(password)
	browser.find_by_id('gr-login-btn').click()
	print ("click done")
	return 0

def get_values(browser,fund_code):
	if not browser.find_by_xpath('//*[@id="tab-1-1-one"]/div[1]/div[1]/a[2]'):
		return 1
	else: 
		browser.find_by_xpath('//*[@id="tab-1-1-one"]/div[1]/div[1]/a[2]').click()
	page_element=browser.find_by_xpath('//*[@id="networth-table_pager"]/span').value
	value_table=[]
	p=(r'共.*页').decode('utf-8')
	pattern=re.compile(p)
	match=re.search(pattern,page_element).group(0)
	total_page=int(re.findall('\d+', match)[0])
	f=open(fund_code+'.txt',"a")
	table=browser.find_by_xpath('//*[@id="networth-table"]').value
	table=table.replace("%","")
	f.write("%s\n"%table)
	for i in range(total_page-1):
		if not browser.find_by_xpath('//*[@id="networth-table_pager"]/a[3]'):
			return 1
		else:
			browser.find_by_xpath('//*[@id="networth-table_pager"]/a[3]').click()
		time.sleep(1)
		table=table.replace("%","")
		table=browser.find_by_xpath('//*[@id="networth-table"]').value
		f.write("%s\n"%table)
	f.close()
	names=[]
	data = pd.read_csv(fund_code+'.txt', sep=" ", header = None)
	columns=['净值日期','单位净值','累计净值(分红再投资)','累计净值(分红不投资)','净值变动'] 
	for name in columns:
		names.append(name.decode('utf-8'))
	data.columns=names
	data.to_csv(fund_code+'.csv',index=False)
	os.remove(fund_code+'.txt')
	return 0
	
	
def splinter(browser,url,fund_code):
	if fund_code+'.txt' in allFiles:
		os.remove(fund_code+'.txt')
		allFiles.remove(fund_code+'.txt')
	print("opened website, initializing...")
	print("opened website, initializing...")
	browser.visit(url)
	print("opened website, initializing...")
	#wait web element loading
	#fill in account and password
	# while browser.is_element_present_by_xpath('//*[@id="gr-register-step1"]/div[9]/strong',wait_time=1):
		# print 0
	# login(browser,'13906805168','cdswjhbkdj1')
	time.sleep(5)
	while get_values(browser,fund_code)==1:
		browser.reload()
	return 0
	
	
def get_names(browser,url):
	browser.visit(url)
	time.sleep(3)
	login(browser,'13906805168','cdswjhbkdj1')
	time.sleep(1)
	browser.find_by_xpath('//*[@id="ranking-tab-content"]/div[1]/div[3]/div[2]/div[4]').click()
	fund_list=[]
	time.sleep(1)
	for i in range(1,51):
		fund_object=browser.find_by_xpath('//*[@id="tab-1-1"]/table/tbody/tr['+str(i)+']')
		browser.find_by_xpath('//*[@id="tab-1-1"]/table/tbody/tr['+str(i)+']/td[2]/a/span')
		fund_list.append(fund_object['name'])
	return fund_list


	
	
	
if __name__ == '__main__':
	browser = Browser('chrome')
	funds=get_names(browser,'http://dc.simuwang.com')
	website ='http://dc.simuwang.com/product/'
	for fund in funds:
		splinter(browser,website+fund+'.html',fund)
		time_visit=int(random.uniform(5,15))
		time.sleep(time_visit)
	browser.quit()
		
	