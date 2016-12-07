
import os
import csv
import random
import string
import json

filename = 'yelp_academic_dataset_business.json'

def get_file_p(name):
	currentDirPath = os.getcwd()
	file_path = os.path.join(os.getcwd(), filename)
	print(file_path)
	return file_path

fullpath = get_file_p(filename)
i = 0

with open(fullpath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')


        dr = []
        ps = []
        sb = []
        mbb = []
        psb = []
        wc = []
        wto = []
        fc = []

        drCount = 0
        psCount = 0
        sbCount = 0
        mbbCount = 0
        psbCount = 0
        wcCount = 0
        wtoCount = 0
        fcCount = 0
        
        sbMbbCount = 0

        for row in readCSV:
                dr1 = row[0]
                ps1 = row[1]
                sb1 = row[2]
                mbb1 = row[3]
                psb1 = row[4]
                wc1 = row[5]
                wto1 = row[6]
                fc1 = row[7]

                if dr1 == 'T':
                        drCount = drCount + 1

                if ps1 == 'T':
                        psCount = psCount + 1
                if sb1 == 'T':
                        sbCount = sbCount + 1

                if mbb1 == 'T':
                        mbbCount = mbbCount + 1
                if psb1 == 'T':
                        psbCount = psbCount + 1

                if wc1 == 'T':
                        wcCount = wcCount + 1
                if wto1 == 'T':
                        wtoCount = wtoCount + 1

                if fc1 == 'T':
                        fcCount = fcCount + 1  

                if sb1 == 'T' and mbb1 == 'T':
                	sbMbbCount =  sbMbbCount + 1     

                dr.append(dr1)
                ps.append(ps1)
                sb.append(sb1)
                mbb.append(mbb1)
                psb.append(psb1)
                wc.append(wc1)
                wto.append(wto1)
                fc.append(fc1)

#print(dr)
print(drCount)
#print(ps)
print(psCount)
#print(sb)
print(sbCount)
#print(mbb)
print(mbbCount)
#print(psb)
print(psbCount)
#print(wc)
print(wcCount)
#print(wto)
print(wtoCount)
#print(fc)
print(fcCount)
print('sbMbbCount:'+str(sbMbbCount))

