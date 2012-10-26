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
def bulk_insert(n_objects=1000):
    ''' Create a lot of object in bulk
    '''
    users, posts = [], []
    now = datetime.now()
    for i in xrange(n_objects):
        dt = now - timedelta(seconds=random.randint(0, 1000))
        user = User(username='user %d' % (i + 1,))
        post = Post(
                title='A post by user %d' % (i + 1,),
                text='a long long text' * 10,
                created_at=dt,
                updated_at=dt,
                author=user)

    pass # TODO


@print_time
def many_inserts(n_objects=300):
    ''' Create one object at a time
    '''
    pass # TODO


@print_time
def many_updates(n_objects=300):
    ''' Update one object at a time
    '''
    pass # TODO


@print_time
def select_all():
    ''' Create a list with all objects
    '''
    return list(Post.objects.all())


@print_time
def select_all_values_list():
    ''' Get all objects with .values_list - less django overhead
    '''
    return list(Post.objects.all()\
            .values_list('id', 'name', 'comment', 'created_at', 'updated_at'))


@print_time
def many_selects(n_objects=300):
    ''' Trigger queries by accessing ForeignKey field
    '''
    return [post.user for post in Post.objects.all()]
