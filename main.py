#!/usr/bin/env python

import os, csv, random, string, json, webbrowser
from PIL import Image

filenameBusiness = 'yelp_academic_dataset_business.json'

filenamePicJSON = '2016_yelp_dataset_challenge_photos\photo_id_to_business_id.json'

#Change this testBusinessID to the exact string Business_ID of the business that you want to open photos for
testBusinessID = '52oCXlQmP2kXt53xpl9a3w'
#testBusinessID = 'KayYbHCt-RkbGcPdGOThNg'
#Change this testBusinessName to the exact string name of the business that you want to open photos for
#EG. 'Flamingo Las Vegas Hotel & Casino' and 'NGJDjdiDJHmN2xxU7KauuA'
testBusinessName = 'Hazelrock Coffee + Sweets'
#testBusinessName = 'Flamingo Las Vegas Hotel & Casino'


#Star rating of the restaurants must be equal to or greater than this value to get their images opened.
loadThreshold = 3.0

maxNumberOfPicsToLoad = 5

def get_file_p(name):
    currentDirPath = os.getcwd()
    file_path = os.path.join(os.getcwd(),'yelp_dataset_challenge_academic_dataset', name)
    #print(file_path)
    return file_path

def get_foto_p(name):
    currentDirPath = os.getcwd()
    file_path = os.path.join(os.getcwd(), '2016_yelp_dataset_challenge_photos', name)
    #print(file_path)
    return file_path

def getBusinessID(name):
    for i in range(len(businesses)):
        if( businesses[i]['name'] == name):
            #print(businesses[i]['name'], businesses[i]['business_id'])
            foundRestaurant = businesses[i]['business_id']
            return foundRestaurant

def insertIntoIDNames(id, name, aDict):
    if not id in aDict:
        aDict[id] = [name]
    else:
        aDict[id].append(name)

def insertIntoBusinessIDStars(id, stars, aDict):
    if not id in aDict:
        aDict[id] = [stars]
    else:
        aDict[id].append(stars)

def insertIntoBusinessIDPhotoID(id, photoID, aDict):
    if not id in aDict:
        aDict[id] = [photoID]
    else:
        aDict[id].append(photoID)


def insertIntoNamesID(id, name, aDict):
    if not name in aDict:
        aDict[name] = [id]
    else:
        aDict[name].append(id)

def showPhotosOfBusinessID(businessID):
    if ((businessIDStars[businessID][0]) >= loadThreshold):
        if(len(businessIDPhotoID[businessID]) <= maxNumberOfPicsToLoad):
            print(businessIDStars[businessID][0], 'rating greater than or equal to loadThreshold value of ', loadThreshold)
            for i in range(len(businessIDPhotoID[businessID])):
                tempImagePath = get_foto_p((businessIDPhotoID[businessID])[i]+'.jpg')
                webbrowser.open(tempImagePath)
                #print(i,tempImagePath)
        else:
            print(businessIDStars[businessID][0], 'rating greater than or equal to loadThreshold value of ', loadThreshold)
            for i in range(maxNumberOfPicsToLoad):
                tempImagePath = get_foto_p((businessIDPhotoID[businessID])[i] + '.jpg')
                webbrowser.open(tempImagePath)
                # print(i,tempImagePath)
    else:
        print(businessIDStars[businessID][0], 'rating less than loadThreshold value of ', loadThreshold, 'Program will not open the photos for the business!')

''' work in progress function, to do if more time--
def getPhotosForBusiness(businessID, aDict):
    if not name in aDict:
        aDict[name] = [id]
    else:
        aDict[name].append(id)
'''

#dictionaries (key,value)
#IDNames (business_id, name)
IDNames = {}
#namesID (name, business_id)
namesID = {}
#businessIDPhotoID (business_id, photo_id)
businessIDPhotoID = {}
#businessIDStars (business_id, stars)
businessIDStars = {}



fullpath = get_file_p(filenameBusiness)

fullpathPicJSON = get_file_p(filenamePicJSON)
#i = 0

photos = []

with open(filenamePicJSON, encoding="utf8") as json_data:
    dataPics = json.load(json_data)
    #print(d)
    #print(d[1]['business_id'])
    photos = dataPics


businesses = []

for line in open(fullpath, 'r'):
    businesses.append(json.loads(line))


businessesDictionary = dict()

for i in range(len(photos)):
    #print(i, photos[i]['photo_id'])
    #tempID = getBusinessID(businesses[i]['name'])
    tempBusinessID = (photos[i]['business_id'])
    tempPhotoID = (photos[i]['photo_id'])
    insertIntoBusinessIDPhotoID(tempBusinessID, tempPhotoID, businessIDPhotoID)


for i in range(len(businesses)):
    #print(i, businesses[i]['name'])
    #tempID = getBusinessID(businesses[i]['name'])
    tempID = (businesses[i]['business_id'])
    insertIntoIDNames(tempID, businesses[i]['name'], IDNames)
    insertIntoNamesID(tempID, businesses[i]['name'], namesID)
    insertIntoBusinessIDStars(tempID, businesses[i]['stars'], businessIDStars)

'''
#print(IDNames)
#print('helloWorld4')
#print(namesID)


print(len(businesses))
print(IDNames['3ZVKmuK2l7uXPE6lXY4Dbg'])
print(namesID['Grand View Golf Club'])

print(businesses[0].keys())
print(businesses[0]['name'])
print(businesses[0]['categories'])
print(businesses[0]['categories'][1])

print(businesses[1]['business_id'])

tempID = getBusinessID('Grand View Golf Club')
print(tempID)


#print(len(businessIDPhotoID))

#testImagePath = get_file_p('test.jpg')
#This PIL code block doesn't work on windows10
#im = Image.open(testImagePath)
#im.show

#This webbrowser work around uses windows viewer to open the photo
#webbrowser.open(testImagePath)
#print(testImagePath)


#testing webbrowser.open function for opening exact file path
#webbrowser.open('C:\\Users\\wesle_000\\Documents\\582Wcoomber3\\2016_yelp_dataset_challenge_photos\\tkSP0R3EFRbkHGBkKiva_w.jpg')
print(IDNames['NGJDjdiDJHmN2xxU7KauuA'])
'''






#Use the business ID as a key into 'businessIDPhotoID' to get all the photo_id's associated with the business
#print('gettingAllBusinessPhotosTest1', businessIDPhotoID[testBusinessID])
#print('hi3', businessIDPhotoID[namesID['Grand View Golf Club'][0]])




#This block of code is different ways to open/load all the photos of the business 1)by ID 2)by name using namesID dict
#print(IDNames[testBusinessID])
####################################################
#showPhotosOfBusinessID(testBusinessID)
showPhotosOfBusinessID(namesID[testBusinessName][0])

#This shows how to get the Star Rating for a business from its business_ID or its name
#print(businessIDStars[namesID[testBusinessName][0]])
#print(businessIDStars[testBusinessID])


#some test code that searches for dravosburg
#x = next((item for item in businesses if item["city"] == "Dravosburg"))
#print(x)


