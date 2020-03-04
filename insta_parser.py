import requests
import json
import sys

tag = sys.argv[1]
url = 'https://www.instagram.com/explore/tags/' + tag + '/?__a=1'

keys = [
    'id', 'shortcode', 'edge_media_to_comment',
    'taken_at_timestamp', 'display_url', 'edge_liked_by', 'owner']

user_keys = [
    'id', 'external_url', 'edge_followed_by', 'is_business_account',
    'is_private', 'username']

users = set()

shortcuts = []

profile_tags = set()

def jprint(data_dict):
    print(json.dumps(data_dict, indent=4))


def connection(url, session=None):
    print(url)
    session = session or requests.Session()

    r = session.get(url)
    r_code = r.status_code
    if r_code == requests.codes.ok:
        #the code is 200 or valid
        return r
    else:
        return None


def flatten_list(the_list):
    if the_list:
        flat = ' '.join(list_item for list_item in the_list if list_item)
        return flat
    return None


def get_tags(text):
    if text:
        text = text.split()
        for word in text:
            if word.startswith('#'):
                word = word.strip('#')
                yield word


def get_post_shortcut(media_dict):
    for post in media_dict:
        post = post.get('node', None)
        shortcut = post.get(keys[1], None)
        print(keys[1].upper(), ':', shortcut)
        shortcuts.append(shortcut)


def get_post_info(media_dict):
    """
    get_post_info(media_dict)
    Gets info about instagram post by 'keys' tags
    """
    likes_sum = 0
    post_captions = []
    for post in media_dict:
        post = post.get('node', None)

        post_likes = post.get(keys[5], None). get('count', None)

        likes_sum += post_likes

        print(keys[5].upper(), ':', post_likes)
        try:
            caption = post.get('edge_media_to_caption', None).get('edges', None)[0].get('node').get('text')
        except:
            caption = 'empty'

        print('caption'.upper(), ':', caption)
        if caption:
            post_captions.append(caption)
        
        flat_captions = flatten_list(post_captions)
        if flat_captions:
            tags = set(get_tags(flat_captions))

            set.update(profile_tags, tags)
            # print('we have ', len(profile_tags), ' tags in total')

        print('-------------------------------------------------')
    return likes_sum

def get_posts(form, data, info=None):
    """
    get_posts(form, data, info=None)
    Get post shortcut by calling 'get_post_shortcut(posts)'
    or post info by calling 'get_post_info(posts)'
    """
    posts = data.get(form, None)
    if posts:
        posts = posts.get('edges', None)
    if not info:
        get_post_shortcut(posts)
        return None
    if info:
        likes = get_post_info(posts)
        return likes

def get_profile_name(data):
    profile = data.get('shortcode_media', None)
    
    if profile:
        profile = profile.get('owner', None).get('username', None)
        return profile
    return None

def posts_connect(url):
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
        
        if profile_name not in users:
            users.add(profile_name)
            print(profile_name)
    else:
        print('Oops!')

def user_connect(url):
    """
    user_connect(url)
    Connect to the user from 'users' and gets info from 'user_keys' about this user
    """
    ig_user_dict = connection(url)
    user_likes = 0
    if ig_user_dict:
        ig_user_dict = ig_user_dict.json()
        # jprint(ig_user_dict)
        user_data = ig_user_dict.get('graphql', None).get('user', None)
        for key in user_keys:
            print(key.upper(), ':', user_data.get(key))
        
        video = get_posts('edge_felix_video_timeline', user_data, True)
        media = get_posts('edge_owner_to_timeline_media', user_data, True)

        user_likes = video + media
        print('total likes'.upper(), ':', user_likes)
        print('profile_tags'.upper(), ':', len(profile_tags))
        print('=====================================================')
    else:
        print('OOps!')


def get_everything(url):
    """
    et_everything(url)
    Take tag-related posts and gets usernames with top posts of these users.
    """
    ig_data_dict = connection(url)

    if ig_data_dict:
        ig_data_dict = ig_data_dict.json()
        print(ig_data_dict)
        data = ig_data_dict.get('graphql', None).get('hashtag', None)

        #Get top posts
        get_posts('edge_hashtag_to_top_posts', data)
        #Get recent posts
        get_posts('edge_hashtag_to_media', data)
        for shortcut in shortcuts:
            post_url = 'https://www.instagram.com/p/' + shortcut + '/?__a=1'
            
            posts_connect(post_url)
        print(*users)

        for user in users:
            user_url = 'https://www.instagram.com/' + user + '/?__a=1&max_id= '
            
            user_connect(user_url)

    else:
        print('Ooops!')


# posts_connect(post_url)
# user_connect(user_url)
get_everything(url)