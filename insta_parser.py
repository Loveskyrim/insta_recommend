import requests
from fake_useragent import UserAgent
import json
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import sys, os
import time
import socks
import socket
# from random import randint
# from bs4 import BeautifulSoup

# from proxy_requests import ProxyRequests

search_type = sys.argv[1] # 'tag' or 'location'
path_csv = sys.argv[2]
# end_cursor = ''
query_ident = ''


keys = [
    'id', 'shortcode', 'edge_media_to_comment',
    'taken_at_timestamp', 'display_url', 'edge_liked_by', 'owner']

user_keys = [
    'id', 'external_url', 'edge_followed_by', 'is_business_account',
    'is_private', 'username']

users = set()

shortcuts = set()

profile_tags = set()

proxies_set = []

global_proxy = None

#Print dist as a JSON
def jprint(data_dict):
    print(json.dumps(data_dict, indent=4))


def get_ip(url):
    i = 0
    while proxies_set:
        print(f"Proxy data - {proxies_set[i]}")
        proxies = {'http': f"socks4://{proxies_set[i]}",
            'https': f"socks4://{proxies_set[i]}"}
        try:
            response = requests.get(url, headers={'User-Agent': UserAgent().chrome}, proxies=proxies, timeout=6)
            r_code = response.status_code
            print(r_code)
            # response = response.json()
            if response and r_code == requests.codes.ok:
                return proxies
            else:
                del proxies_set[i]
        except Exception as e:
            print(e)
            del proxies_set[i]


def connection(url, session=None):
    # print(url)
    # session = session or requests.Session()
    # ssocks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    # socket.socket = socks.socksocket

    r_code = 0  
    proxies = None     
    while True:
        
        print(proxies)
        try:
            r = requests.get(url, headers={'User-Agent': UserAgent().chrome}, proxies=proxies)
            r_code = r.status_code
            r = r.json()
            if r_code == requests.codes.ok:
                break
            else:
                proxies = get_ip(url)
        except Exception as e:
            proxies = get_ip(url)

    return r
        


def proxies_list(fileObj):
    with open(fileObj, 'r') as f:
        for line in f.readlines():
            proxies_set.append(line)


def flatten_list(the_list):
    if the_list:
        flat = ' '.join(list_item for list_item in the_list if list_item)
        return flat
    return None


#Get tags '#' from given text
def get_tags(text):
    if text:
        text = text.split()
        for word in text:
            if word.startswith('#'):
                word = word.strip('#')
                yield word


#Get all post-shortcuts from media_dict
def get_posts_shortcut(media_dict):
    for post in media_dict:
        post = post.get('node', None)
        shortcut = post.get(keys[1], None)
        print(keys[1].upper(), ':', shortcut)
        shortcuts.add(shortcut)


def get_posts_info(media_dict):
    """
    get_posts_info(media_dict)
    Gets info about instagram post by 'keys' tags
    """
    likes_sum = 0
    post_captions = []
    for post in media_dict:
        post = post.get('node', None)

        post_likes = post.get(keys[5], None). get('count', None)
        print(keys[5].upper(), ':', post_likes)
        likes_sum += post_likes

        try:
            caption = post.get('edge_media_to_caption', None).get('edges', None)[0].get('node').get('text')
        except:
            caption = None
        if caption:
            print('caption'.upper(), ':', caption)
            
            tags = set(get_tags(caption))
            print('tags: ', tags)
        
            profile_tags.update(tags)
            tags.clear()

        print('-------------------------------------------------')
    return likes_sum


# def get_first_shortcut(media_dict):

#     post = media_dict[0].get('node', None)
#     shortcut = post.get(keys[1], None)
#     return shortcut


def get_posts(form, data, info=False):
    """
    get_posts(form, data, info=None)
    Get post shortcut by calling 'get_post_shortcut(posts)'
    or post info by calling 'get_posts_info(posts)'
    """
    posts = data.get(form, None)
    if posts:
        posts = posts.get('edges', None)
    # if first:
    #     shortcut = get_first_shortcut(posts)
    #     return shortcut
    if not info:
        get_posts_shortcut(posts)
        return None
    else:
        likes = get_posts_info(posts)
        return likes


def get_profile_name(data):
    profile = data.get('shortcode_media', None)
    
    if profile:
        profile = profile.get('owner', None).get('username', None)
        return profile
    return None


def posts_connect(shortcut, file):
    """
    posts_connect(url)
    Get username by post shortcut and append it to 'users'
    """
    url = 'https://www.instagram.com/p/' + shortcut + '/?__a=1'
    ig_post_dict = connection(url)

    if ig_post_dict:
        # try:
        #     ig_post_dict = ig_post_dict.json()
        # except Exception as e:
        #     print('Post response is empty')
        # jprint(ig_post_dict)
        post_data = ig_post_dict.get('graphql', None)
        profile_name = get_profile_name(post_data)
        with open(file, 'a') as t:
            t.write(profile_name+'\n')
        # users.add(profile_name)
        print(profile_name)
    else:
        print('Post response is empty')


def post_connect(url):
    ig_post_dict = connection(url)

    if ig_post_dict:

        jprint(ig_post_dict)
    else:
        print('Post response is empty')


def user_page_connect(url, index):
    print('[' + url + ']')
    ig_user_dict = connection(url)

    if ig_user_dict:
        # ig_user_dict = ig_user_dict.json()
        # jprint(ig_user_dict)
        user_data = ig_user_dict.get('graphql', None).get('user', None)
        media = user_data.get('edge_owner_to_timeline_media', None)
        info = media.get('page_info', None)
        end_cursor = info.get('end_cursor', None)

        if index == 0:
            for key in user_keys:
                print(key.upper(), ':', user_data.get(key))
        
        video = get_posts('edge_felix_video_timeline', user_data, True)
        media = get_posts('edge_owner_to_timeline_media', user_data, True)
        return end_cursor, video + media
    else:
        return None, 0


def user_connect(url):
    """
    user_connect(url)
    Connect to the user from 'users' and gets info with 'user_keys'-tags about this user.
    Calls user_page_connect to collect posts from each page
    """
    end_cursor = ''
    user_likes = 0
    for index in range(1):
        temp, likes = user_page_connect(url, index)
        user_likes += likes
        if end_cursor != temp and temp:
            end_cursor = temp
            url = 'https://www.instagram.com/' + tag + '/?__a=1&max_id=' + end_cursor
        else:
            break
        

    print('total likes'.upper(), ':', user_likes)
    print('profile_tags'.upper(), ':', len(profile_tags))
    profile_tags.clear()
    print('=====================================================')



def get_hashtag_posts(url):
    """
    get_hashtag_posts(url)
    Get posts from each page of hashtag-search or location-search result page.
    """
    ig_data_dict = connection(url)

    if ig_data_dict:
        # try:
        #     ig_data_dict = ig_data_dict.json()
        # except Exception as e:
        #     print(e)
        #     return None
        data = ig_data_dict.get('graphql', None)
        if search_type == 'tag':
            data = data.get('hashtag', None)
            media = data.get('edge_hashtag_to_media', None)
            info = media.get('page_info', None)
            end_cursor = info.get('end_cursor', None)
            #Get top posts
            get_posts('edge_hashtag_to_top_posts', data)
            #Get recent posts
            get_posts('edge_hashtag_to_media', data)
        elif search_type == 'location':
            data = data.get('location', None)
            media = data.get('edge_location_to_media', None)
            info = media.get('page_info', None)
            end_cursor = info.get('end_cursor', None)
            #Get top posts
            get_posts('edge_location_to_top_posts', data)
            #Get recent posts
            get_posts('edge_location_to_media', data)
        return end_cursor
    else:
        print('Ooops!')
        return None


def get_all_hashtag_posts(url, tag):
    """
    get_all_hashtag_posts(url)
    Take tag-related posts and gets usernames with top posts of these users.
    Calls get_hashtag_posts() to collect posts from each page of hashtag-search result page.
    """
    end_cursor = ''
    for index in range(20):
        temp = get_hashtag_posts(url)
        if end_cursor != temp and temp:
            end_cursor = temp
        else:
            break
        url = 'https://www.instagram.com/explore/tags/' + tag + '/?__a=1&max_id=' + end_cursor
    print("Shortcuts: ", len(shortcuts))

    # path = os.path.dirname('tag_usernames')
    if not os.path.exists('tag_usernames'):
        os.makedirs('tag_usernames')
    file = 'tag_usernames/'+tag+'.txt'
    for shortcut in shortcuts:
        posts_connect(shortcut, file)
        # print("Users: ", len(users))

    # end_cursor = ''
    # for user in users:
    #     print(user)
    #     user_url = 'https://www.instagram.com/' + user + '/?__a=1&max_id=' + end_cursor
        
    #     user_connect(user_url)



def get_all_location_posts(url, tag):
    """
    get_all_location_posts(url)
    Take location-related posts and gets usernames with top posts of these users.
    Calls get_hashtag_posts() to collect posts from each page of location-search result page.
    """
    end_cursor = ''
    for index in range(20):
        url1 = url + end_cursor
        temp = get_hashtag_posts(url1)
        if end_cursor != temp and temp:
            end_cursor = temp
        else:
            break
        # url = url + '?__a=1&max_id=' + end_cursor
    print("Shortcuts: ", len(shortcuts))

    # path = os.path.dirname('tag_usernames')
    if not os.path.exists('location_usernames'):
        os.makedirs('location_usernames')
    file = 'location_usernames/'+tag+'.txt'
    for shortcut in shortcuts:
        posts_connect(shortcut, file)
        # print("Users: ", len(users))


def get_location_id(tag):
    """
    get_location_id(tag)
    Opens browser to get tag- or location-based search page
    """


    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('--headless') # Лучше не использовать
    # chrome_driver_path = get_chrome_driver_path()
    # service_args = [
    # '--proxy=127.0.0.1:9050', # You can change these parameters to your liking.
    # '--proxy-type=socks5', # Use socks4/socks5 based on your usage.
    # ]
    os.environ["webdriver.chrome.driver"] = "/Users/andrejkonovalov/Documents/папка/python/insta_recommend/chromedriver_2"
    driver = webdriver.Chrome(executable_path="/Users/andrejkonovalov/Documents/папка/python/insta_recommend/chromedriver_2", options=options)
    driver.set_window_size(1200, 600)

    url = 'https://www.instagram.com/explore/locations/'
    driver.get(url)

    try:
    	search_field = driver.find_element_by_xpath('.//input[@placeholder="Search"]')
    except:
    	search_field = driver.find_element_by_xpath('.//input[@placeholder="Поиск"]')
    search_field.send_keys(tag)
    time.sleep(3)
    try:
        first_loc_elem = driver.find_element_by_xpath('.//div[contains(@class,"coreSpriteLocation")]')
        first_loc_elem = first_loc_elem.find_element_by_xpath('..').find_element_by_xpath('..')
        ref = first_loc_elem.get_attribute("href")
    except:
    	ref = ''
    driver.quit()
    return ref + '?__a=1&max_id='



def processing():
    
    with open(path_csv, 'r', encoding='utf-8') as fh: #открываем файл на чтение
        data = json.load(fh) #загружаем из файла данные в словарь data


    # tags = []
    for tag in data:
        tag = tag.get('name')
        url = 'https://www.instagram.com/explore/tags/' + tag + '/?__a=1'
        
        if search_type == 'tag':
            get_all_hashtag_posts(url, tag)
        elif search_type == 'location':
            reference = get_location_id(tag)

            if reference != '?__a=1&max_id=':
                get_all_location_posts(reference, tag)
        users.clear()
        shortcuts.clear()
        profile_tags.clear()


proxies_list('socks4.txt')
processing()




