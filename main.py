#!/usr/bin/env python2.7

import os, csv, random, string, json, webbrowser
import io, time, operator
import geocoder as gc
from randomdict import RandomDict
from PIL import Image
from sets import Set
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import urllib
import multiprocessing as mp
from slide import App
import config

auth = Oauth1Authenticator(
    consumer_key = config.consumer_key,
    consumer_secret = config.consumer_secret,
    token = config.token,
    token_secret = config.token_secret
)
client = Client(auth)

DEBUG = config.debug
PREFETCH = config.prefetch

''' custom dirs '''
JSON_DIR = 'json'
PIC_DIR = 'photo'

JSON_business   = 'yelp_academic_dataset_business.json'
JSON_review     = 'yelp_academic_dataset_review.json'
JSON_user       = 'yelp_academic_dataset_user.json'
JSON_picture    = 'photo_id_to_business_id.json'

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
            return (True, common)
        return (False, None)

    def get_num_reviews(self):
        return len(self.bids)

def DM(msg):
    if DEBUG:
        print "DEBUG>> %s" % msg


################# local file related ops ######################
def getfile(name, dtype='json'):
    cwd = os.getcwd()
    if dtype == 'picture':
        return cwd + '/' + PIC_DIR + '/' + name
    return cwd + '/' + JSON_DIR + '/' + name

def mkdir(bid):
    cwd = os.getcwd()
    if os.path.isdir(cwd + '/.tmp') is False:
        os.mkdir(cwd + '/.tmp')
    name = cwd + '/.tmp/'+ bid
    if os.path.isdir(name) is False:
        os.mkdir(name)
    return name

################# remote yelp related ops ######################
def form_params(name, lat, lon):
    print lat, lon
    geo = '{},{}'.format(lat,lon)
    params = { 'term':name, 'lang':'en', 'cll': geo}
    if DEBUG:
        print params
    return params

def fetch_pics(obj):
# def fetch_pics(bid, name, city, lat, lon):
    bid = obj['business_id']
    name = obj['name']
    city = obj['city']
    lat = obj['latitude']
    lon = obj['longitude']
    params = form_params(name, lat, lon)
    dir_name = mkdir(bid)

    print params
    resp = client.search(city, **params)
    list_urls = []
    for a in resp.businesses:
        image_url = a.image_url
        if image_url is not None:
            image_url = image_url.replace('ms.jpg', 'o.jpg')
            print a.id, a.name
            list_urls.append(image_url)

    count = 0 
    for url in list_urls:
        urllib.urlretrieve(url, "{}/{}.jpg".format(dir_name, count))
        count += 1
    DM("done fetching {} images in {}".format(len(list_urls), dir_name))
    return bid

################# yelp json related ops ######################
def get_obj_business():
    arr = []
    with open(getfile(JSON_business)) as fin:
        for line in fin:
            obj = json.loads(line)
            if len(obj['state']) == 2 and 'Restaurants' in obj['categories']:
                arr.append(obj)
    return arr
 
def fetch_reviews():
    count = 0
    DM('fetching reviews...')
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
            user_obj.add_bid(bid)
            users[uid] = user_obj
    # TODO: optimize it via memoization (w/ slicing)
    DM('done fetching reviews...')

def fetch_business():
    count = 0
    DM("fetching businesses...")
    with open(getfile(JSON_business)) as fin:
        for line in fin:
            obj = json.loads(line)
            count += 1
            bid = obj['business_id']
            bus[bid] = obj
            r_bus[bid] = obj
    DM("done fetching business... {}".format(len(bus)))
    return

################# slide wrapper (execute only in main process) ######################
def slide_worker(bid):
    App(bid).run()
    return

bus = {}
r_bus = RandomDict()
users = {}

################# slide wrapper (execute only in main process) ######################
def get_obj_review():
    count = 0 
    jobs = []

    DM('initializing....')
    # mp.log_to_stderr(logging.DEBUG)
    # jobs.append(mp.Process(name='review', target=fetch_reviews))
    # jobs.append(mp.Process(name='business', target=fetch_business))
    # for p in jobs:
    #     p.start()
    
    # for p in jobs:
    #     p.join()
    
    fetch_reviews()
    fetch_business()

    tmp_map = {}
    tmp_bus = {}
    count = 0
    while count < 15:
        count += 1
        obj = r_bus.random_value()
        bid = obj['business_id']
        stars = obj['stars']
        tmp_map[bid] = stars
        tmp_bus[bid] = obj

    # print_list = []
    # while len(tmp_list) != len(print_list):
    #     candidate = max(tmp_list, key=lambda item:item['stars'])
    #     if candidate not in print_list:
    #         print_list.append(candidiate)
    # print print_list

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
    target_bus = tmp_bus[new_list[choice]]
    target_bid = target_bus['business_id']
    print 'target is... ', target_bid

    check_bid = fetch_pics(target_bus)
    # bid = fetch_pics(bid, name, city, lat, lon)
    # params = form_params(target_bus['name'], target_bus['latitude'],
    #         target_bus['longitude'])
    # resp = client.search(target_bus['city'], **params)
    # for a in resp.businesses:
    #     image_url = a.image_url
    #     if image_url is not None:
    #         image_url = image_url.replace('ms.jpg', 'o.jpg')
    #         print a.id, a.name
    #         print image_url
    if check_bid != target_bid:
        print "ERROR: bid has been changed...!" 
        exit(-1)

    # slide = mp.Process(name='slide', target=slide_worker, args=(target_bid, ))
    # slide.start()
    slide_worker(target_bid)

    ''' given busieness id (bid), find *users* who have written down the
    review'''
    common_users = []
    for k, obj in users.items():
        if obj.has_bid(target_bid):
            common_users.append(obj)
    
    common_bids = {}
    count = 0 
    for obj in common_users:
        count += 1
        for i in range(count, len(common_users)):
            obj2 = common_users[i]
            answer, commons = obj.has_common(obj2)
            if answer:
                for common in commons:
                    if common != target_bid:
                        from_map = None
                        try: # dict = (bid, counts)
                            common_bids[common] += 1
                        except Exception as e:
                            # DNE
                            common_bids[common] = 1
    new_common_bids = sorted(common_bids.items(), key=lambda x: x[1], reverse=True)
    # slide.join()

    DM('common bids len: {}'.format(len(common_bids)))
    count = 0
    for k, v in new_common_bids:
        count += 1 
        obj = bus[k]
        print count, 'count. {}'.format(v), obj['name'], obj['stars']
        if count > 15:
            break
    
    # count < 15? fetch more from random...
    while count < 15:
        count += 1
        obj = r_bus.random_value()
        bid = obj['business_id']
        stars = obj['stars']
        print count, 'count. {}'.format(0), bid, stars
        tmp_map[bid] = stars
        tmp_bus[bid] = obj
    
    return

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


def debug():
    bid = "Y9e3DMJexlctd9pAudL-5A"
    name = "Papa John's Pizza"
    city = "Las Vegas"
    lat = 36.0211192
    lon = -115.1190908
    start = time.time()
    # bid = fetch_pics(bid, name, city, lat, lon)
    end = time.time()
    print ('Time taken: ', end - start)
    App(bid).run()

    bid = "deFBCKjvB6i3-LX12JlIuQ"
    name = "Oyshi Sushi"
    city = "Las Vegas"
    lat = 36.1435827060002
    lon = -115.251559111144
    start = time.time()
    bid = fetch_pics(bid, name, city, lat, lon)
    end = time.time()
    print ('Time taken: ', end - start)
    bid = fetch_pics(bid, name, city, lat, lon)
    App(bid).run()

if __name__ == '__main__':
    # debug()
    main()
    # main_job = mp.Process(name='main', target=main)
    # main_job.start()

