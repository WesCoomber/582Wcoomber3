#!/usr/bin/env python2.7

import json, random, time, string, inspect
import os, sys, signal, io, operator
import geocoder as gc
from randomdict import RandomDict
from PIL import Image
from sets import Set
from glob import glob
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import urllib
import multiprocessing as mp
from multiprocessing import Manager, Queue, Process
import threading
from threading import Thread, Lock, Condition
from slide import App
import config
from config import *

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
    geo = '{},{}'.format(lat,lon)
    params = { 'term':name, 'lang':'en', 'cll': geo}
    # DM("params: {}".format(params))
    return params

def fetch_pics(obj):
    bid = obj['business_id']
    name = obj['name']
    city = obj['city']
    lat = obj['latitude']
    lon = obj['longitude']
    params = form_params(name, lat, lon)
    dir_name = mkdir(bid)

    DM("fetching {} images in {}".format(name.encode('utf8'), dir_name.encode('utf8')))
    resp = client.search(city, **params)
    list_urls = []
    for a in resp.businesses:
        image_url = a.image_url
        if image_url is not None:
            image_url = image_url.replace('ms.jpg', 'o.jpg')
            list_urls.append(image_url)

    count = 0 
    for url in list_urls:
        urllib.urlretrieve(url, "{}/{}.jpg".format(dir_name, count))
        count += 1

    if count < 10:
        params = form_params(city, lat, lon)
        resp = client.search(city, **params)
        list_urls = []
        for a in resp.businesses:
            image_url = a.image_url
            if image_url is not None:
                image_url = image_url.replace('ms.jpg', 'o.jpg')
                list_urls.append(image_url)
        for url in list_urls:
            urllib.urlretrieve(url, "{}/{}.jpg".format(dir_name, count))
            count += 1


    DM("done fetching {} images in {}".format(len(list_urls), dir_name.encode('utf8')))
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

def fetch_reviews_opt(user_map, lines):
    DM('Process: {} {} {}'.format(mp.current_process().name, 'Starting', len(lines)))
    count = 0
    for line in lines:
        # if count > 30000:
        #     return
        obj = json.loads(line)
        bid = obj['business_id']
        uid = obj['user_id']
        try:
            # user_obj = users[uid]
            user_obj = user_map[uid]
        except Exception as e:
        # if new user? create object and add to hash table
            user_obj = User(uid)
        user_obj.add_bid(bid)
        user_map[uid] = user_obj
        count += 1
    DM('Process: {} {} {}'.format(mp.current_process().name, 'Exiting', len(lines)))
    return
    
 
def fetch_reviews(user_map):
    count = 0
    DM('fetching reviews... takes about {}'.format("4 mins"))
    num_lines = sum(1 for line in open(getfile(JSON_review)))
    cpus = mp.cpu_count() 
    for_each = int(num_lines / cpus)
    cpus += 1
    DM("{} {} {}".format(for_each, num_lines, cpus))

    line_count = 0
    lines = [[] for i in range(cpus)]
    tmp_lines = []
    count = 0 # index for list
    with open(getfile(JSON_review)) as fin:
        for line in fin:
            line_count += 1
            lines[count].append(line)
            if (line_count % for_each) == 0:
                # print count, line_count, num_lines
                count += 1

    start = time.time()
    jobs = []
    for i in range(cpus):
        # t = Thread(name=i, target=fetch_reviews_opt, args=(user_map, lines[i], ))
        t = mp.Process(name=i, target=fetch_reviews_opt, args=(user_map, lines[i], ))
        jobs.append(t)
        t.start()

    for job in jobs:
        job.join()
    end = time.time()
    # print "Took {} secs".format(end-start)
    DM('done fetching reviews... {}'.format(count))

def fetch_business(bus_map):
    count = 0
    DM("fetching businesses...")
    with open(getfile(JSON_business)) as fin:
        for line in fin:
            obj = json.loads(line)
            count += 1
            bid = obj['business_id']
            # bus[bid] = obj
            bus_map[bid] = obj
            # r_bus[bid] = obj
    DM("done fetching business... {}".format(len(bus_map)))
    return

################# slide wrapper (execute only in main process) ######################
def slide_worker(bid):
    App(bid).run()
    return

################# demo purpose CUI ops ######################
''' takes bus_list, return bus object'''
def show_list(bus_map): 
    count = 0
    new_list = [] # contains bids
    for k,v in bus_map.items():
        # k == bid, v = obj
        count += 1
        bid = k
        obj = v
        new_list.append(bid)
        if DEBUG:
        # if True:
            val = (v['stars']*100.0) + v['review_count']
            print "    %3d. [%5d] %s" % (count, val, obj['name'])
        else:
            print "    %3d. %s" % (count, obj['name'])

    # choice == bid for now...
    choice = 0
    while 1:
        choice = input("==> Select: ")
        if choice <= 0 or choice > len(bus_map): 
            print "Woooops! Retry mannnnn!"
        else:
        #     print choice
            break
    choice -= 1
    bid = new_list[choice]
    bus_obj = bus_map[bid]
    DM("{} {} {}".format(choice, bid, bus_obj))
    return bus_obj
 
################# prefetching stuff ######################
'''TODO:
    - heuristics:
    0. stars
    1. rating 
    2. review_counts
    3. common reviews'''
def get_steroids(bus_map, commons):
    if PREFETCH == False: # if disabled...
        return []

    tmp_map = {}
    for k, v in bus_map.items():
        val = (v['stars'] * 100.0)
        val += v['review_count']
        if inspect.isclass(commons) and len(commons.key()) > 1:
            tmp_val = commons[k]
            print tmp_val
            val += tmp_val
        tmp_map[k] = val

    new_tmp = sorted(tmp_map.items(), key=lambda x: x[1], reverse=True)
    steroids = []
    count = 0
    thrs = 5
    for k,v in new_tmp:
        # v is "stars" , k is bid
        stars = v
        obj = bus_map[k]
        if count < thrs:
            steroids.append(obj)
        count += 1

    DM("Number of steroids: {}".format(count))
    return steroids
    
def exec_steroids(steroids):
    jobs = []
    for obj in steroids:
        t = Thread(name=obj['name'].encode('utf8'), target=fetch_pics, args=(obj, ))
        jobs.append(t)
        t.start()
    return jobs

def get_bus_map(bus, r_bus, commons): 
    tmp_bus = {}
    NUM_BUS = 15
    count = 0

    # if isinstance(commons, list):
    #     for k, v in commons:
    #         print k,v 
    #         print bus[k]
    if isinstance(commons, list) or \
            (inspect.isclass(commons) and len(commons.key())) > 1:
        for k, v in commons:
            count += 1 
            obj = bus[k]
            tmp_bus[k] = obj
            # print obj
            if count > NUM_BUS:
                return tmp_bus
        
    # count < 15? fetch more from random...
    for i in range(count, NUM_BUS):
        obj = r_bus.random_value()
        bid = obj['business_id']
        tmp_bus[bid] = obj
    return tmp_bus

def get_commons(target, users, commons):
    ''' given busieness id (bid), find *users* who have written down the
    review'''
    common_users = []
    for k, obj in users.items():
        if obj.has_bid(target):
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
                    if common != target:
                        from_map = None
                        try: # dict = (bid, counts)
                            common_bids[common] += 1
                        except Exception as e:
                            # DNE
                            common_bids[common] = 1
    ret = sorted(common_bids.items(), key=lambda x: x[1], reverse=True)
    print "DONE~!"
    # print ret

    for k, v in ret:
        commons[k] = v
    return ret

################# slide wrapper (execute only in main process) ######################
''' notes:
originally, we wanted to construct a hierarchy where a user selects 
    state -> city -> restaurants type
but b/c dataset contains only limited types of restaurants, it's meaningless...
OK let's do this... show 20 businesses w/ top review counts, 
upon select, fetch some picture... 
move to next selection (try to find common set of reviewers...) 
'''
def main():
    DM('initializing....')
    count = 0 
    bus = {}
    r_bus = RandomDict()
    users = {}



    jobs = []
    manager = Manager()
    user_map = manager.dict()
    bus_map = manager.dict()
    jobs.append(mp.Process(name='review', target=fetch_reviews, args=(user_map,)))
    jobs.append(mp.Process(name='business', target=fetch_business, args=(bus_map,)))
    for p in jobs:
        p.start()
    for p in jobs:
        p.join()
    
    # fetch_reviews()
    # fetch_business()
    users = user_map
    bus = bus_map

    for k, v in bus.items():
        r_bus[k] = v

    commons = manager.dict()
################ starting ..>! 
    while 1:
        tmp_bus = get_bus_map(bus, r_bus, commons)

        steroids = get_steroids(tmp_bus, commons)
        jobs = exec_steroids(steroids)

        print '==============================================================='
        target_bus = show_list(tmp_bus)
        target_bid = target_bus['business_id']
        DM("target selected is {}".format(target_bid))

        for t in jobs:
            t.join()

        if target_bus not in steroids or PREFETCH is False:
            print ("Steroid-miss: %s " % target_bus['name'])
            eval_start = time.time()
            check_bid = fetch_pics(target_bus)
            print ('Time taken: {}'.format(time.time() - eval_start))
            if check_bid != target_bid:
                print "ERROR: bid has been changed...!" 
                exit(-1)

        ''' TODO: 
        - multiprocessing:
            1. fetching review & business concurrently
            2. manager process for user interaction
        '''

        p = mp.Process(name='commons', target=get_commons, args=(target_bid,
            user_map, commons, ))
        p.start()
        slide_worker(target_bid)
        p.join()

# = = = = = == = = = == = =  == = = = == = == = = == = = == = = = == = = = =#
        # commons = get_commons(target_bid, user_map, commons)
        # print ('common bids len: {}'.format(len(commons)))
        print ('common bids len: {}'.format(len(commons.keys())))
 
    return


##################### init ops stuff ##########################
def init_clean():
    cwd = os.getcwd()
    folders = glob(cwd + "/.tmp/*")
    DM("cleaning .tmp folders...!")
    for folder in folders:
        for jpg in [ f for f in os.listdir(folder) if f.endswith(".jpg") ]:
            name = folder + "/" + jpg
            os.remove(name)
        os.rmdir(folder)
    DM("done cleaning .tmp folders...!")
    return

def init():
    init_clean()
    print "Initializing environments for the program..."
    return

def handler(singnum, frame):
    print ("closing the program...")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    init()
    main()
    # main_job = mp.Process(name='main', target=main)
    # main_job.start()

