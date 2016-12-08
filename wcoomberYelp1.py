
import os
import csv
import random
import string
import json

filenameBusiness = 'yelp_academic_dataset_business2.json'

filenamePicJSON = '2016_yelp_dataset_challenge_photos\photo_id_to_business_id2.json'

def get_file_p(name):
    currentDirPath = os.getcwd()
    file_path = os.path.join(os.getcwd(), name)
    #print(file_path)
    return file_path

def get_foto_p(name):
    currentDirPath = os.getcwd()
    file_path = os.path.join(os.getcwd(), '2016_yelp_dataset_challenge_photos')
    #print(file_path)
    return file_path

def getBusinessID(name):
    for i in range(len(businesses)):
        if( businesses[i]['name'] == name):
            #print(businesses[i]['name'], businesses[i]['business_id'])
            foundRestaurant = businesses[i]['business_id']
            return foundRestaurant

def insertIntoIDNames(id, name, aDict):
    if not name in aDict:
        aDict[id] = [name]
    else:
        aDict[id].append(name)

def insertIntoIDPhotoID(id, photoID, aDict):
    if not name in aDict:
        aDict[id] = [photoID]
    else:
        aDict[id].append(photoID)


def insertIntoNamesID(id, name, aDict):
    if not name in aDict:
        aDict[name] = [id]
    else:
        aDict[name].append(id)

IDNames = {}
namesID = {}
IDPhotoID = {}





fullpath = get_file_p(filenameBusiness)

fullpathPicJSON = get_file_p(filenamePicJSON)
i = 0

print('hi',fullpathPicJSON)


photos = []

with open(filenamePicJSON, encoding="utf8") as json_data:
    d = json.load(json_data)
    print(d)

businesses = []

for line in open(filenameBusiness, 'r'):
    businesses.append(json.loads(line))
"""
data = []

with open(filenameBusiness) as f:
    for line in f:
        tempJSON = json.loads(line)
        data.append(tempJSON)
        tempID = getBusinessID(businesses[i]['name'])
        insertIntoIDNames(tempID, businesses[i]['name'],IDNames)

print('helloWorld1')
print(businesses)
print('helloWorld2')

print(data)
print('helloWorld3')


"""

print(len(businesses))
businessesDictionary = dict()

for i in range(len(businesses)):
    print(i, businesses[i]['name'])
    tempID = getBusinessID(businesses[i]['name'])
    insertIntoIDNames(tempID, businesses[i]['name'], IDNames)
    insertIntoNamesID(tempID, businesses[i]['name'], namesID)


print(IDNames)
print('helloWorld4')
print(namesID)

print(IDNames['3ZVKmuK2l7uXPE6lXY4Dbg'])
print(namesID['Grand View Golf Club'])

print(businesses[0].keys())
print(businesses[0]['name'])
print(businesses[0]['categories'])
print(businesses[0]['categories'][1])

print(businesses[1]['business_id'])

tempID = getBusinessID('Grand View Golf Club')
print(tempID)



#some test code that searches for dravosburg
#x = next((item for item in businesses if item["city"] == "Dravosburg"))
#print(x)


