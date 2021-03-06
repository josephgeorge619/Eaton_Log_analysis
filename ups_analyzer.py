#!/bin/env python
# -*- coding: utf-8 -*-
# +----------------------------------------------------------------------+
# | Version : 1.0                                                        |
# | Update  : 12032018                                                   |
# | Script  : UPS Log Analysis                                           |
# | Notes   : This will analyse the UPS logs of last Day, Week & Month   |
# | Author  : Joseph George <Joseph.Fisat@gmail.com>                     |
# +----------------------------------------------------------------------+

import csv
import os
import time
import getopt
import sys
import datetime
from tqdm import tqdm
from datetime import date
from datetime import timedelta
from operator import itemgetter, attrgetter
ups_message=[]
ups_names = []
last_day=[]
last_week = []
last_month = []
toolbar_width = 50
tqdm.monitor_interval = 0
########################################################################################################
#Function for date generation
def Gen_Dates():
        #Generate Date for Last day
        last_day.insert(0, (date.today() - timedelta(days=1)).strftime('%Y/%m/%d'))

        #Generate list of Dates for Last Week
        n = 0
        for i in range(0,7):
                last_week.insert(n, (date.today() - timedelta(days=i)).strftime('%Y/%m/%d'))
                n +=1

        #Generate list of Dates for Last Month
        n = 0
        for i in range(0,30):
                last_month.insert(n, (date.today() - timedelta(days=i)).strftime('%Y/%m/%d'))
                n +=1

#Function for analysis
def Analyse(date_list):
        count=0
        analysis=[]
        for i in ups_names:
            for day in date_list:
                        for j in ups_message:
                                if i in j['Node'] and day in j['\xef\xbb\xbf"Date"']:
                                        count = count + 1
            if count > 0:
        #                        print day+"  Node Name : "+i+"   Count : "+str(count)
                     analysis.insert(0,(i,count))
            count = 0
        sort_analyse=sorted(analysis, key=itemgetter(1), reverse=True)
        n=0
        for i in sort_analyse:
            if n < 25:
                file_writer.write('%-30s ------    Count is:%4s \n' %(i[0],i[1]))
            n += 1

#Display Help
def Usage(script):
    print "Script Usage:   "+'C:\Python27\python.exe '+"%s --filename \"file name.csv\" \n" %(script)
########################################################################################################

#TQDM Progress Bar initialization
probar = tqdm(total=100)

script_loc=os.path.realpath(__file__)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:",["filename="])
except getopt.GetoptError:
        Usage(script_loc)
        exit(0)

for opt, arg in opts:
        if opt == '-h':
            Usage(script_loc)
            sys.exit(1)
        elif opt in ("-f", "--filename"):
            filename = arg
            file_with_path=dir_path+'\\'+filename
try:
        f = open(file_with_path, 'r+')
        reader = csv.DictReader(f)
except:
        print " Please check the input filename!! Unable to open file!! \n Program Exiting!!!   Bye"
        exit(0)
probar.update(5)
file_name_path=(os.path.splitext(f.name)[0])
file_writer = open(file_name_path+"_report.doc", 'w')

#initial Processing
#adding to list so that we can use it mutiple iterations
data = [row for row in reader]
probar.update(5)
#Removing all the messages that does not contain information related to Battery
for i in data:
    if 'under' in i['Message'] or 'Under' in i['Message'] or 'battery' in i['Message'] or 'Battery' in i['Message']:
        ups_message += [i]
probar.update(5)
#Getting Unique UPS Names
n = 0
for i in ups_message:
        if i['Node'] not in ups_names:
                ups_names.insert(n, i['Node'])
                n += 1
probar.update(5)
file_writer.write("############################################################\n")
file_writer.write("#                                                          #\n")
file_writer.write("#                   Final Analysis report                  #\n")
file_writer.write("#                                                          #\n")
file_writer.write("############################################################\n")

#Generate Dates
Gen_Dates()
probar.update(10)

#Analysis for last day
file_writer.write("\n+----------------------------------------------------------+\n")
file_writer.write("|            Yesterday's Report"+str(last_day)+"              |\n")
file_writer.write("+----------------------------------------------------------+\n")
Analyse(last_day)

probar.update(20)
#Analysis for last week
file_writer.write("\n+----------------------------------------------------------+\n")
file_writer.write("|                     Last Week's Report                   |\n")
file_writer.write("+----------------------------------------------------------+\n")
Analyse(last_week)

probar.update(20)
#Analysis for Last Month
file_writer.write("\n+----------------------------------------------------------+\n")
file_writer.write("|                     Last Month's Report                  |\n")
file_writer.write("+----------------------------------------------------------+\n")
Analyse(last_month)
sys.stdout.write("\n")
probar.update(30)
probar.close()
file_writer.close()
sys.stdout.write("Report file Generated\n")
