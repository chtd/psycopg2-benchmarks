import time
from functools import wraps


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


def bulk_ids(model, n):
    from django.db import connection
    cursor = connection.cursor()
    sql = "select nextval('%s_id_seq') from generate_series(1,%d)" % \
            (model._meta.db_table, n)
    cursor.execute(sql)
    return [int(r[0]) for r in cursor]
