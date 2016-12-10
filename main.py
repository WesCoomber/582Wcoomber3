#!/usr/bin/env python2.7

import os, csv, random, string, json, webbrowser
import io, time, operator
import geocoder as gc
from randomdict import RandomDict
from PIL import Image
from sets import Set

''' custom dirs '''
JSON_DIR = 'json'
PIC_DIR = 'photo'

JSON_business   = 'yelp_academic_dataset_business.json'
JSON_review     = 'yelp_academic_dataset_review.json'
JSON_user       = 'yelp_academic_dataset_user.json'
JSON_picture = 'photo_id_to_business_id.json'

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

def getfile(name, dtype='json'):
    cwd = os.getcwd()
    if dtype == 'picture':
        return cwd + '/' + PIC_DIR + '/' + name
    return cwd + '/' + JSON_DIR + '/' + name

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
                tempImagePath = getfile((businessIDPhotoID[businessID])[i]+'.jpg',dtype='picture')
                webbrowser.open(tempImagePath)
                #print(i,tempImagePath)
        else:
            print(businessIDStars[businessID][0], 
                'rating greater than or equal to loadThreshold value of ', loadThreshold)
            for i in range(maxNumberOfPicsToLoad):
                tempImagePath = getfile((businessIDPhotoID[businessID])[i] +\
                        '.jpg', dtype='picture')
                webbrowser.open(tempImagePath)
                # print(i,tempImagePath)
    else:
        print(businessIDStars[businessID][0], 'rating less than loadThreshold value of ', 
            loadThreshold, 'Program will not open the photos for the business!')

''' work in progress function, to do if more time--
def getPhotosForBusiness(businessID, aDict):
    if not name in aDict:
        aDict[name] = [id]
    else:
        aDict[name].append(id)
'''

def get_obj_business():
    arr = []
    with open(getfile(JSON_business)) as fin:
        for line in fin:
            obj = json.loads(line)
            if len(obj['state']) == 2 and 'Restaurants' in obj['categories']:
                arr.append(obj)
    return arr

def debug():
   return

class User():
    def __init__(self, uid):
        self.uid = uid
        self.bids = []

    def get_uid(self):
        return self.uid

    def add_bid(self, bid):
        self.bids.append(bid)

    def has_bid(self, bid):
        if bid in self.bids:
            return True
        return False

    def get_bids(self):
        return self.bids

    def has_common(self, b):
        common = set(self.bids).intersection(b.get_bids())
        if len(common) > 0:
            return True
        return False

    def get_num_reviews(self):
        return len(self.bids)

def get_obj_review():
    bus = {}
    r_bus = RandomDict()
    reviews = {}
    users = {}
    users_map = {}
    count = 0 

    with open(getfile(JSON_review)) as fin:
        for line in fin:
            obj = json.loads(line)
            bid = obj['business_id']
            uid = obj['user_id']
            try:
                user_obj = users[uid]
            except Exception as e:
                # if new user? create object and add to hash table
                user_obj = User(uid)
            user_obj.add_bus(bid)
            users[uid] = user_obj

    # for k, v in users.items():
    #     count += 1 
    #     print k, v.get_num_reviews()
    #     if count > 100:
    #         return

    with open(getfile(JSON_business)) as fin:
        for line in fin:
            obj = json.loads(line)
            count += 1
            bid = obj['business_id']
            bus[bid] = obj
            r_bus[bid] = obj
    print 'done sorting businesses...', len(bus)

    tmp_map = {}
    tmp_bus = {}
    count = 0
    while count < 15:
        count += 1
        obj = r_bus.random_value()
        bid = obj['business_id']
        stars = obj['stars']
        print '~~~~~',bid,'~~~~~~'
        tmp_map[bid] = stars
        tmp_bus[bid] = obj

    # print_list = []
    # while len(tmp_list) != len(print_list):
    #     candidate = max(tmp_list, key=lambda item:item['stars'])
    #     if candidate not in print_list:
    #         print_list.append(candidiate)
    # print print_list

    for k, v in tmp_bus.items():
        obj = v 
        print k, '>> ', obj['name'], obj['stars']
    print '==============================================================='
    new_tmp = sorted(tmp_map.items(), key=lambda x: x[1], reverse=True)
    new_list = []
    count = 0
    for k,v in new_tmp:
        count += 1
        bid = k
        obj = tmp_bus[bid]
        new_list.append(bid)
        print count, obj['name'], obj['stars'], obj['review_count']

    # choice == bid for now...
    choice = input("select: ")
    choice -= 1
    print choice, new_list[choice], tmp_bus[new_list[choice]]

    common_users = {}

    with open(getfile(JSON_review)) as fin:
        for line in fin:
            obj = json.loads(line)
            bid = obj['business_id']
            uid = obj['user_id']
            if bid == tmp_bus[new_list[choice]]:
                users[uid] += 1
    print 'done finding reviews...'

    vals = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
    count = 0 
    for k, v in vals:
        count += 1 
        print k, v 
        if count > 100:
            return
 
    # with open(getfile(JSON_user)) as fin:
    #     for line in fin:
    #         obj = json.loads(line)
    #         uid = obj['user_id']
    #         count = 0 # obj['review_count']
    #         users[uid] = count
    # print 'done sorting users...', len(users)
   
    return



''' notes:
originally, we wanted to construct a hierarchy where a user selects 
    state -> city -> restaurants type
but b/c dataset contains only limited types of restaurants, it's meaningless...
OK let's do this... show 20 businesses w/ top review counts, 
upon select, fetch some picture... 
move to next selection (try to find common set of reviewers...) 
'''

def main():
    get_obj_review()
    debug()
    return 

    IDNames = {} # (business_id, name)
    namesID = {} # (name, business_id)
    businessIDPhotoID = {} # (business_id, photo_id)
    businessIDStars = {} # (business_id, stars)

    arr_bus = get_obj_business()

    states = []
    for obj in arr_bus:
        state = str(obj['state'])
        if state not in states:
            states.append(state)
    states = sorted(states, key=str.lower)

    print 'DEBUG', 'len(arr_bus): ', len(arr_bus)
    print "We support only %d states for now, sorry :<" % (len(states))
    tmp_c = 0
    print '   ',
    for s in states:
        tmp_c += 1
        print '%2d. %s ' % (tmp_c, s),
        if tmp_c % 4 == 0:
            print '\n   ',
    choice = input("\nChoose one among the states: ")
    state = states[choice - 1]
    print 'choice: %s ' % (state) 

    ############################################
    cities = []
    for obj in arr_bus:
        if state == obj['state']:
            city = str(obj['city'])
            if city not in cities:
                cities.append(city)
    
    if len(cities) < 1:
        print ("No cities found in state of %s (shame on you..!)" % state)

    cities = sorted(cities, key=str.lower)
    print "We support only %d cities in %s for now, sorry :<" % \
            (len(cities), state)
    tmp_c = 0
    print '   ',
    for s in cities:
        tmp_c += 1
        print '%2d. %s ' % (tmp_c, s),
        if tmp_c % 4 == 0:
            print '\n   ',
    choice = input("\nChoose one among the cities: ")
    city = cities[choice - 1]
    print 'choice: %s ' % (city) 

    ############################################
    cats = []
    for obj in arr_bus:
        if state == obj['state'] and city == obj['city']:
            for category in obj['categories']:
                cat = str(category)
                if cat not in cats and cat != 'Restaurants':
                    cats.append(cat)
    
    if len(cats) < 1:
        print ("No cats found in %s, %s (shame on you..!)" % (city, state))

    cats = sorted(cats, key=str.lower)
    print "We support only %d categories in %s, %s for now, sorry :<" % \
            (len(cats), city, state)
    tmp_c = 0
    # print_format = '{}d.'.format( max(cats, key=len)
    print '   ',
    for s in cats:
        tmp_c += 1
        print '%2d. %s ' % (tmp_c, s),
        if tmp_c % 4 == 0:
            print '\n   ',
    choice = input("\nChoose one among the cities: ")
    cat = cats[choice - 1]
    print 'choice: %s ' % (cat) 
    return

    with open(getfile(JSON_review)) as fin:
        for line in fin:
            obj = json.loads(line)
            bid = obj['business_id']
            uid = obj['user_id']
            print bid, uid
            time.sleep(1)
    return

    with io.open(json_business, encoding='utf8') as data:
        parsed = json.load(data)
        print parsed

    fullpath = getfile(JSON_business)
    json_pic = getfile(JSON_picture)
    photos = []
    businesses = []

    with io.open(json_pic, encoding='utf8') as data:
        pics = json.load(data)
        print(pics)
        #print(data[1]['business_id'])
        photos = pics

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

#testImagePath = getfile('test.jpg')
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
    return


if __name__ == '__main__':
    main()

