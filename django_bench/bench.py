#!/usr/bin/env python

import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('.')

import random
from datetime import datetime, timedelta

from app.models import Post, User
from utils import print_time, bulk_ids


def run_all(size):
    ''' Run all benchmarks. Assumes empty DB
    '''
    assert User.objects.all().count() == 0
    assert Post.objects.all().count() == 0
    deco = print_time(profile=True)
    for create_fn in (bulk_insert, many_inserts, many_updates):
        deco(create_fn)(size)
    for select_fn in (many_selects, select_all, select_all_values_list):
        deco(select_fn)()


def bulk_insert(size):
    ''' Create a lot of object in bulk
    '''
    n_objects = size
    now = datetime.now()
    user_list, post_list = [], []
    user_ids, post_ids = [bulk_ids(m, n_objects) for m in (User, Post)]
    for i, user_id, post_id in zip(
            xrange(1, n_objects + 1), user_ids, post_ids):
        user, post = new_user_post(i, now, 'bulk')
        user.id = user_id
        post.author = user
        user_list.append(user)
        post_list.append(post)
    User.objects.bulk_create(user_list)
    Post.objects.bulk_create(post_list)


def many_inserts(size):
    ''' Create one object at a time
    '''
    n_objects = size / 10
    now = datetime.now()
    user_list, post_list = [], []
    for i in xrange(n_objects):
        user, post = new_user_post(i, now, 'single')
        user.save()
        post.author = user
        post.save()


def many_updates(size):
    ''' Update one object at a time
    '''
    n_objects = size / 10
    now = datetime.now()
    for post in Post.objects.all()[:n_objects]:
        post.updated_at = now
        post.title += ' (2)'
        post.save()


def select_all():
    ''' Create a list with all objects
    '''
    so_many_posts = []
    for _ in xrange(10):
        so_many_posts.extend(Post.objects.all())


def select_all_values_list():
    ''' Get all objects with .values_list - less django overhead
    '''
    so_many_posts = []
    for _ in xrange(20):
        so_many_posts.extend((Post.objects.all()\
            .values_list('id', 'title', 'text', 'updated_at')))


def many_selects():
    ''' Trigger queries by accessing ForeignKey field
    '''
    posts = list(Post.objects.all())
    return [post.author for post in posts[: (len(posts) / 4) ]]


def new_user_post(i, now, prefix):
    ''' Create new User and Post instances without saving them
    '''
    username = '%s user %d' % (prefix, i)
    dt = now - timedelta(seconds=random.randint(0, 1000))
    user = User(username=username)
    post = Post(
            title='A post by ' + username,
            text='a long long text' * 10,
            created_at=dt,
            updated_at=dt)
    return user, post


def cli():
    usage = 'usage: ./bench.py 1000, or some other job size'
    if len(sys.argv) != 2:
        print usage
    else:
        try:
            size = int(sys.argv[1])
        except ValueError:
            print usage
        else:
            run_all(size)


if __name__ == '__main__':
    cli()
