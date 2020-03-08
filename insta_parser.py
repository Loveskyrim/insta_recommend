import requests
import json

import sys, os


tag = sys.argv[1]
amount = int(sys.argv[2])
end_cursor = ''
query_ident = ''
url = 'https://www.instagram.com/explore/tags/' + tag + '/?__a=1' + end_cursor

keys = [
    'id', 'shortcode', 'edge_media_to_comment',
    'taken_at_timestamp', 'display_url', 'edge_liked_by', 'owner']

user_keys = [
    'id', 'external_url', 'edge_followed_by', 'is_business_account',
    'is_private', 'username']

users = set()

shortcuts = set()

profile_tags = set()

#Print dist as a JSON
def jprint(data_dict):
    print(json.dumps(data_dict, indent=4))


# def extract_json(text, decoder=JSONDecoder()):
#     pos = 0
#     while True:
#         match = text.find('{', pos)
#         if match == -1:
#             break
#         try:
#             result, index = decoder.raw_decode(text[match:])
#             yield result
#             pos = match + index
#         except ValueError:
#             pos = match + 1


def connection(url, session=None):
    # print(url)
    session = session or requests.Session()
    r = session.get(url)
    r_code = r.status_code
    # print(r_code)

    if r_code == requests.codes.ok:
        #the code is 200 or valid
        return r
    else:
        return None

    # browser = webdriver.Safari()
    # browser.get(url)
    # t = 0
    # count = 0
    # while t == 0:
    #     print('RUN!')
    #     while t <= 25:
    #         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(random.uniform(1,1.5))
    #         browser.execute_script("window.scrollTo(0, 0);")

    #         t += 1
    #         count += 1
    #         print('total: ~' + str(count * 4))

    # try:
    #     instapars = browser.find_element_by_xpath("//*[contains(text(), 'window._sharedData = {')]")
        
    #     pre = instapars.get_property("innerHTML")

    #     config = list(extract_json(pre))[0]
    #     entry_data = config.get('entry_data', None)
    #     tag_page = entry_data.get('TagPage', None)[0]
    #     browser.quit()
    #     return tag_page
    # except:
    #     browser.quit()
    # else:
    #     return None


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
    if info:
        likes = get_posts_info(posts)
        return likes


def get_profile_name(data):
    profile = data.get('shortcode_media', None)
    
    if profile:
        profile = profile.get('owner', None).get('username', None)
        return profile
    return None


def posts_connect(url, t):
    """
    posts_connect(url)
    Get username by post shortcut and append it to 'users'
    """
    ig_post_dict = connection(url)

    if ig_post_dict:
        ig_post_dict = ig_post_dict.json()
        # jprint(ig_post_dict)
        post_data = ig_post_dict.get('graphql', None)
        profile_name = get_profile_name(post_data)
        t.write(profile_name+'\n')
        # users.add(profile_name)
        print(profile_name)
    else:
        print('Oops!')


def post_connect(url):
    ig_post_dict = connection(url)

    if ig_post_dict:

        jprint(ig_post_dict)
    else:
        print('Oops!')


def user_page_connect(url, index):
    print('[' + url + ']')
    ig_user_dict = connection(url)

    if ig_user_dict:
        ig_user_dict = ig_user_dict.json()
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
    Get posts from each page of hashtag-search result page.
    """
    ig_data_dict = connection(url)

    if ig_data_dict:
        ig_data_dict = ig_data_dict.json()

        data = ig_data_dict.get('graphql', None).get('hashtag', None)
        media = data.get('edge_hashtag_to_media', None)
        info = media.get('page_info', None)
        end_cursor = info.get('end_cursor', None)
        #Get top posts
        get_posts('edge_hashtag_to_top_posts', data)
        #Get recent posts
        get_posts('edge_hashtag_to_media', data)
        return end_cursor
    else:
        print('Ooops!')
        return None


def get_all_hashtag_posts(url):
    """
    get_all_hashtag_posts(url)
    Take tag-related posts and gets usernames with top posts of these users.
    Calls get_hashtag_posts() to collect posts from each page of hashtag-search result page.
    """
    end_cursor = ''
    for index in range(amount):
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
    with open('tag_usernames/'+tag+'.txt', 'w') as t:
        for shortcut in shortcuts:
            post_url = 'https://www.instagram.com/p/' + shortcut + '/?__a=1'
            posts_connect(post_url, t)
        print("Users: ", len(users))

    # end_cursor = ''
    # for user in users:
    #     print(user)
    #     user_url = 'https://www.instagram.com/' + user + '/?__a=1&max_id=' + end_cursor
        
    #     user_connect(user_url)




# user_connect(user_url)
get_all_hashtag_posts(url)
