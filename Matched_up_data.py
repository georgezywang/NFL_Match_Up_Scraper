#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:49:22 2019

@author: wzy
"""

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np

def getMatchUp(url):
    #obtain raw data
    req=Request(url, headers={'User-Agent': 'Chrome/11.0'})
    page = urlopen(req).read()
    page_soup = soup(page, 'html.parser')
    rows_raw=page_soup.find_all('tr')
    
    alldata=[]
    length = 12
    for i in range(length):
        alldata.append([])
        
    count = 0
    for row in rows_raw:
        dataraw = row.find_all('td')
        if str(row).find('thead') ==-1  and count != 0:
            if re.search('[0-9]+-+[0-9]+-+[0-9]{2}',str(dataraw[1]))!=None:
                alldata[0].append(re.search('[A-Z]+[a-z]+<',str(dataraw[0])).group().replace('<',""))
                alldata[1].append(re.search('[0-9]+-+[0-9]+-+[0-9]{2}',str(dataraw[1])).group())
                if re.search('[0-9]+:+[0-9]+[A-Z]{2}',str(dataraw[2]))!= None:
                    alldata[2].append(re.search('[0-9]+:+[0-9]+[A-Z]{2}',str(dataraw[2])).group())
                else:
                    alldata[2].append(" ")
                alldata[3].append(re.search('[[A-Z]+[^<]+<',str(dataraw[3])).group().replace('<',""))
                alldata[5].append(re.search('[[A-Z]+[^<]+<',str(dataraw[5])).group().replace('<',""))
                if str(dataraw[4]).find('@')!=-1:
                    alldata[4]=alldata[5]
                else:
                    alldata[4]=alldata[3]
                for i in range(7,13):
                    if re.search(r"[-+]?\d*\.?\d+|\d+", str(dataraw[7]))!=None:
                        alldata[i-1].append(re.search(r"[-+]?\d*\.?\d+|\d+", str(dataraw[i])).group())
                    else:
                        alldata[i-1].append(" ")
        count+=1
    return alldata

def MatchUpyearrange(startyear,endyear):
    alldat=[]
    for i in range(startyear,endyear+1):
        #It is 2019 now
        print("---------"+"retrieving Match Up data of year " + str(i)+'---------')
        url="https://www.pro-football-reference.com/years/"+str(i)+"/games.htm"
        dat=getMatchUp(url)
        alldat.append(dat)
    return alldat

def sortMatchUpdata(startyear,endyear):
    #reshape the data
    alldat=MatchUpyearrange(startyear,endyear)
    years=endyear-startyear+1
    sorteddata=[]
    for i in range (len(alldat[0])):
        sorteddata.append([])
        
    for i in range(years):
        data_year=alldat[i]
        for j in range(len(alldat[0])):
            for k in range(len(alldat[0][0])):
                sorteddata[j].append(data_year[j][k])
    return sorteddata

def MatchUp2df(sorteddata):
    df=pd.DataFrame(np.array(sorteddata).transpose(), columns=['Day','Date','Time','Winner/tie',\
                    'at','loser/tie','PtsW','PtsL','YdsW','TOW','Ydsl','TOL'])
    return df

def writefile(data,filename):
    print('Writing file: '+filename)
    data.to_csv(filename+'.csv',index=False)

SortedMatchUp = sortMatchUpdata(2005,2019)
writefile(MatchUp2df(SortedMatchUp),'Match_Up_fifteen_years')


            