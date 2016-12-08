
import os
import csv
import random
import string
import json

filename = 'yelp_academic_dataset_business2.json'

def get_file_p(name):
	currentDirPath = os.getcwd()
	file_path = os.path.join(os.getcwd(), filename)
	print(file_path)
	return file_path

fullpath = get_file_p(filename)
i = 0

businesses = []

for line in open(filename, 'r'):
        businesses.append(json.loads(line))

data = []

with open(filename) as f:
    for line in f:
        data.append(json.loads(line))

print('helloWorld1')
print(businesses)
print('helloWorld2')


print(len(businesses))
businessesDictionary = dict()

for i in range(len(businesses)):
    print(i, businesses[i]['name'])
    #print(i, businesses[i])

print(businesses[0].keys())
print(businesses[0]['name'])
print(businesses[0]['categories'])
print(businesses[0]['categories'][1])

print(businesses[1]['business_id'])

def getBusinessID(name):
    for i in range(len(businesses)):
        if( businesses[i]['name'] == 'Emil\'s Lounge':
            print(i, businesses[i]['name'])

	return file_path

#some test code that searches for dravosburg
#x = next((item for item in businesses if item["city"] == "Dravosburg"))
#print(x)


