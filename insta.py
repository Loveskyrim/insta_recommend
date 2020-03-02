# import instaloader
import threading
from instaloader import Instaloader, Profile
import pickle

NUM_POSTS = 10
NUM_HASHTAGS = 10
loader = Instaloader()


def profile_form(profile):
    profile_opts = []
            
    profile_opts.append(profile.userid)

    profile_opts.append(profile.username)

    profile_opts.append(profile.followers)

    profile_opts.append(profile.external_url)

    return profile_opts


def get_hashtags(post, tags):
    counter = 0
    for hashtag in post.caption_hashtags:
        if hashtag not in tags:
            tags.add(hashtag)
            counter += 1
            if counter == NUM_HASHTAGS:
                break


def get_post(profile, tags):
    counter = 0
    for post in profile.get_posts():
        get_hashtags(post, tags)
        counter += 1
        if counter == NUM_POSTS:
            break


def account_form(profile, users, tags):
    """
    account_form(profile, users)
    Tries to identify private accounts by getting external url in profile
    """
    form = "business_account"

    if not profile.external_url:
        users[profile.username] = profile_form(profile)
        get_post(profile, tags)
        form = "private_account"

    elif "www.youtube.com" in profile.external_url:
        users[profile.username] = profile_form(profile)
        get_post(profile, tags)
        form = "private_account"

    return form


def get_hashtags_posts(query):
    """
    get_hashtags_posts(query)
    Returns (NUM_POSTS) private accounts with some options
    """
    posts = loader.get_hashtag_posts(query)
    users = {}
    related_tags = set()
    count = 0
    for post in posts:
        profile = post.owner_profile

        if profile.username not in users:
            # Check if there is no external url (means Private account)
            form = account_form(profile, users, related_tags)
            print(form)
            if form == "private_account":
                count += 1

            print('{}: {}'.format(count, profile.username))
            if count == NUM_POSTS:
                break
    return users, related_tags


if __name__ == "__main__":
    hashtag = "california"
    users, tags = get_hashtags_posts(hashtag)
    print(users)
    print(tags)