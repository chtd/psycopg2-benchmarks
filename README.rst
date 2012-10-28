Benchmark Python bindings for PostgreSQL using Django
=====================================================

This is a tiny django benchmark, that measures some common operations:

* creating objects in bulk (using ``model.objects.bulk_create``)
* creating objects one at a time
* updating objects one at a time
* querying objects one at a time (accessing ForeignKey field)
* selecting a lot of objects using ``model.objects.all``
* selecting a lot of objects using ``model.objects.all().values_list``

The goal is not to measure the raw speed
of Postgres bindings, but to evaluate them in a way similar to the way
they are used in real-life web applications.

A write-up with benchmark results lives here **TODO**

Install::

    pip install -r requirements.txt

Run::

    ./bench 1000

It will run the benchmark several times, to give PyPy JIT time to warm up.

It will create a test database named ``psycopg2_cffi_test_db``, and
by default will try to access it without password and using you system 
user name - you can change it in ``settings.py``.
