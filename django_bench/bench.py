#!/usr/bin/env python

import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('.')

import time
import random
from datetime import datetime, timedelta
from functools import wraps

from app.models import Post, User


def print_time(fn):
    ''' Print how much time the function took
    '''
    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return fn(*args, **kwargs)
        finally:
            print fn.__name__, time.time() - start, 's'
    return inner


@print_time
def bulk_insert(size):
    ''' Create a lot of object in bulk
    '''
    n_objects = size
    now = datetime.now()
    user_list, post_list = [], []
    for i in xrange(n_objects):
        user, post = new_user_post(i, now)
        user_list.append(user)
        post_list.append(post)
    User.objects.bulk_create(post_list)
    Post.objects.bulk_create(user_list)


def new_user_post(i, now):
    ''' Create new User and Post instances without saving them
    '''
    username = 'user %d' % (i + 1,)
    dt = now - timedelta(seconds=random.randint(0, 1000))
    user = User(username=username)
    post = Post(
            title='A post by ' + username,
            text='a long long text' * 10,
            created_at=dt,
            updated_at=dt,
            author=user)
    return user, post


@print_time
def many_inserts(size):
    ''' Create one object at a time
    '''
    n_objects = size / 10
    now = datetime.now()
    user_list, post_list = [], []
    for i in xrange(n_objects):
        user, post = new_user_post(i, now)
        user.save()
        post.save()


@print_time
def many_updates(size):
    ''' Update one object at a time
    '''
    n_objects = size / 10
    now = datetime.now()
    for post in Post.objects.all()[:n_objects]:
        post.updated_at = now
        post.name += ' (2)'
        post.save()


@print_time
def select_all():
    ''' Create a list with all objects
    '''
    so_many_posts = []
    for _ in xrange(10):
        so_many_posts.extend(Post.objects.all())


@print_time
def select_all_values_list():
    ''' Get all objects with .values_list - less django overhead
    '''
    so_many_posts = []
    for _ in xrange(20):
        so_many_posts.extend((Post.objects.all()\
            .values_list('id', 'name', 'comment', 'created_at', 'updated_at')))


@print_time
def many_selects():
    ''' Trigger queries by accessing ForeignKey field
    '''
    return [post.user for post in Post.objects.all()]


def run_all(size):
    ''' Run all benchmarks. Assumes empty DB
    '''
    assert User.objects.all().count() == 0
    assert Post.objects.all().count() == 0
    bulk_insert(size)
    many_inserts(size)
    many_updates(size)
    many_selects()
    select_all()
    select_all_values_list()


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
