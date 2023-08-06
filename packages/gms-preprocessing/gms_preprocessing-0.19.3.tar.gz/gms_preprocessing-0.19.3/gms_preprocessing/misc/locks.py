# -*- coding: utf-8 -*-

# gms_preprocessing, spatial and spectral homogenization of satellite remote sensing data
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# Please note the following exception: `gms_preprocessing` depends on tqdm, which
# is distributed under the Mozilla Public Licence (MPL) v2.0 except for the files
# "tqdm/_tqdm.py", "setup.py", "README.rst", "MANIFEST.in" and ".gitignore".
# Details can be found here: https://github.com/tqdm/tqdm/blob/master/LICENCE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Daniel Scheffler'

import time
from redis import Redis
from redis_semaphore import Semaphore
from redis.exceptions import ConnectionError as RedisConnectionError
from retools.lock import Lock, LockTimeout
import functools
from psutil import virtual_memory
from logging import getLogger

from ..options.config import GMS_config as CFG

try:
    redis_conn = Redis(host='localhost', db=0)
    redis_conn.keys()  # may raise ConnectionError, e.g., if redis server is not installed or not running
except RedisConnectionError:
    redis_conn = None


"""NOTE:

To get a list of all currently set redis keys, run:

    from redis import Redis
    conn = Redis('localhost', db=0)
    list(sorted(conn.keys()))

Then, to delete all currently set redis keys, run:

    for i in list(sorted(conn.keys())):
        k = i.decode('utf-8')
        conn.delete(k)
"""


class MultiSlotLock(Semaphore):
    def __init__(self, name='MultiSlotLock', allowed_slots=1, logger=None, **kwargs):
        self.disabled = redis_conn is None or allowed_slots in [None, False]
        self.namespace = name
        self.allowed_slots = allowed_slots
        self.logger = logger or getLogger("RedisLock: '%s'" % name)

        if not self.disabled:
            super(MultiSlotLock, self).__init__(client=redis_conn, count=allowed_slots, namespace=name, **kwargs)

    def acquire(self, timeout=0, target=None):
        if not self.disabled:
            if self.available_count == 0:
                self.logger.info("Waiting for free lock '%s'." % self.namespace)

            token = super(MultiSlotLock, self).acquire(timeout=timeout, target=target)

            self.logger.info("Acquired lock '%s'" % self.namespace +
                             ('.' if self.allowed_slots == 1 else ', slot #%s.' % (int(token) + 1)))

            return token

    def release(self):
        if not self.disabled:
            token = super(MultiSlotLock, self).release()
            if token:
                self.logger.info("Released lock '%s'" % self.namespace +
                                 ('.' if self.allowed_slots == 1 else ', slot #%s.' % (int(token) + 1)))

    def delete(self):
        if not self.disabled:
            self.client.delete(self.check_exists_key)
            self.client.delete(self.available_key)
            self.client.delete(self.grabbed_key)

    def __exit__(self, exc_type, exc_val, exc_tb):
        exitcode = super(MultiSlotLock, self).__exit__(exc_type, exc_val, exc_tb)
        return exitcode


class SharedResourceLock(MultiSlotLock):
    def acquire(self, timeout=0, target=None):
        if not self.disabled:
            token = super(SharedResourceLock, self).acquire(timeout=timeout, target=target)
            self.client.hset(self.grabbed_key_jobID, token, self.current_time)

    def release_all_jobID_tokens(self):
        if not self.disabled:
            for token in self.client.hkeys(self.grabbed_key_jobID):
                self.signal(token)

            self.client.delete(self.grabbed_key_jobID)

    @property
    def grabbed_key_jobID(self):
        return self._get_and_set_key('_grabbed_key_jobID', 'GRABBED_BY_GMSJOB_%s' % CFG.ID)

    def signal(self, token):
        if token is None:
            return None
        with self.client.pipeline() as pipe:
            pipe.multi()
            pipe.hdel(self.grabbed_key, token)
            pipe.hdel(self.grabbed_key_jobID, token)  # only difference to Semaphore.signal()
            pipe.lpush(self.available_key, token)
            pipe.execute()
            return token

    def delete(self):
        if not self.disabled:
            super(SharedResourceLock, self).delete()
            self.client.delete(self.grabbed_key_jobID)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super(SharedResourceLock, self).__exit__(exc_type, exc_val, exc_tb)


class IOLock(SharedResourceLock):
    def __init__(self, allowed_slots=1, logger=None, **kwargs):
        self.disabled = CFG.disable_IO_locks

        if not self.disabled:
            super(IOLock, self).__init__(name='IOLock', allowed_slots=allowed_slots, logger=logger, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super(IOLock, self).__exit__(exc_type, exc_val, exc_tb)


class ProcessLock(SharedResourceLock):
    def __init__(self, allowed_slots=1, logger=None, **kwargs):
        self.disabled = CFG.disable_CPU_locks

        if not self.disabled:
            super(ProcessLock, self).__init__(name='ProcessLock', allowed_slots=allowed_slots, logger=logger, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super(ProcessLock, self).__exit__(exc_type, exc_val, exc_tb)


class DatabaseLock(SharedResourceLock):
    def __init__(self, allowed_slots=1, logger=None, **kwargs):
        self.disabled = CFG.disable_DB_locks

        if not self.disabled:
            super(DatabaseLock, self)\
                .__init__(name='DatabaseLock', allowed_slots=allowed_slots, logger=logger, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super(DatabaseLock, self).__exit__(exc_type, exc_val, exc_tb)


class MemoryReserver(object):
    def __init__(self, mem2lock_gb, max_usage=90, logger=None):
        """

        :param mem2lock_gb:    Amount of memory to be reserved during the lock is acquired (gigabytes).
        """
        self.disabled = redis_conn is None or CFG.disable_memory_locks or mem2lock_gb in [None, False]
        self.mem2lock_gb = mem2lock_gb
        self.max_usage = max_usage
        self.logger = logger or getLogger("RedisLock: 'MemoryReserver'")
        self.namespace = 'MemoryReserver'
        self.client = redis_conn
        self.mem_limit = int(virtual_memory().total * max_usage / 100 / 1024 ** 3)

        self._waiting = False

    @property
    def mem_reserved_gb(self):
        return int(self.client.get(self.reserved_key) or 0)

    @property
    def usable_memory_gb(self):
        return int((virtual_memory().total * self.max_usage / 100 - virtual_memory().used) / 1024 ** 3) \
               - int(self.mem_reserved_gb)

    @property
    def acquisition_key(self):
        return "%s:ACQUISITION_LOCK" % self.namespace

    @property
    def reserved_key(self):
        return "%s:MEM_RESERVED" % self.namespace

    @property
    def reserved_key_jobID(self):
        return "%s:MEM_RESERVED_BY_GMSJOB_%s" % (self.namespace, CFG.ID)

    @property
    def waiting_key(self):
        return "%s:NUMBER_WAITING" % self.namespace

    @property
    def waiting_key_jobID(self):
        return "%s:NUMBER_WAITING_GMSJOB_%s" % (self.namespace, CFG.ID)

    @property
    def waiting(self):
        return self._waiting

    @waiting.setter
    def waiting(self, val):
        """Set self.waiting.

        NOTE: This setter does not use a lock. Redis access must be locked by calling function.
        """
        if val is not self._waiting:
            if val:
                self.client.incr(self.waiting_key, 1)
                self.client.incr(self.waiting_key_jobID, 1)
            else:
                self.client.decr(self.waiting_key, 1)
                self.client.decr(self.waiting_key_jobID, 1)

        self._waiting = val

    def acquire(self, timeout=20):
        if not self.disabled:
            try:
                with Lock(self.acquisition_key, expires=20, timeout=timeout, redis=self.client):
                    if self.usable_memory_gb >= self.mem2lock_gb:
                        t_start = time.time()
                        self.waiting = False

                        with self.client.pipeline() as pipe:
                            pipe.multi()
                            pipe.incr(self.reserved_key, self.mem2lock_gb)
                            pipe.incr(self.reserved_key_jobID, self.mem2lock_gb)
                            pipe.execute()

                        self.logger.info('Reserved %s GB of memory.' % self.mem2lock_gb)

                        # warn in case the lock has expired before incrementing reserved_key and reserved_key_jobID
                        if time.time() > t_start + timeout:
                            self.logger.warning('Reservation of memory took more time than expected. '
                                                'Possibly more memory than available has been reserved.')

                    else:
                        if not self.waiting:
                            self.logger.info('Currently usable memory: %s GB. Waiting until at least %s GB are '
                                             'usable.' % (self.usable_memory_gb, self.mem2lock_gb))
                        self.waiting = True

            except LockTimeout:
                self.acquire(timeout=timeout)

            if self.waiting:
                while self.usable_memory_gb < self.mem2lock_gb:
                    time.sleep(1)

                self.acquire(timeout=timeout)

    def release(self):
        if not self.disabled:
            with Lock(self.acquisition_key, expires=20, timeout=20, redis=self.client):
                with redis_conn.pipeline() as pipe:
                    pipe.multi()
                    pipe.decr(self.reserved_key, self.mem2lock_gb)
                    pipe.decr(self.reserved_key_jobID, self.mem2lock_gb)
                    pipe.execute()

                self.logger.info('Released %s GB of reserved memory.' % self.mem2lock_gb)

    def delete(self):
        if not self.disabled:
            with Lock(self.acquisition_key, expires=20, timeout=20, redis=self.client):
                # handle reserved_key and reserved_key_jobID
                mem_reserved_currJob = int(self.client.get(self.reserved_key_jobID) or 0)
                with redis_conn.pipeline() as pipe:
                    pipe.multi()
                    pipe.decr(self.reserved_key_jobID, mem_reserved_currJob)
                    pipe.decr(self.reserved_key, mem_reserved_currJob)
                    pipe.delete(self.reserved_key_jobID)
                    pipe.execute()

                if int(self.client.get(self.reserved_key) or 0) == 0:
                    self.client.delete(self.reserved_key)

                # handle waiting_key and waiting_key_jobID
                n_waiting_currJob = int(self.client.get(self.waiting_key_jobID) or 0)
                with redis_conn.pipeline() as pipe:
                    pipe.multi()
                    pipe.decr(self.waiting_key_jobID, n_waiting_currJob)
                    pipe.decr(self.waiting_key, n_waiting_currJob)
                    pipe.delete(self.waiting_key_jobID)
                    pipe.execute()

                if int(self.client.get(self.waiting_key) or 0) == 0:
                    self.client.delete(self.waiting_key)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

        return True if exc_type is None else False


def acquire_process_lock(**processlock_kwargs):
    """Decorator function for ProcessLock.

    :param processlock_kwargs:  Keyword arguments to be passed to ProcessLock class.
    """

    def decorator(func):
        @functools.wraps(func)  # needed to avoid pickling errors
        def wrapped_func(*args, **kwargs):
            with ProcessLock(**processlock_kwargs):
                result = func(*args, **kwargs)

            return result

        return wrapped_func

    return decorator


def reserve_mem(**memlock_kwargs):
    """Decorator function for MemoryReserver.

    :param memlock_kwargs:  Keyword arguments to be passed to MemoryReserver class.
    """

    def decorator(func):
        @functools.wraps(func)  # needed to avoid pickling errors
        def wrapped_func(*args, **kwargs):
            with MemoryReserver(**memlock_kwargs):
                result = func(*args, **kwargs)

            return result

        return wrapped_func

    return decorator


def release_unclosed_locks():
    if redis_conn:
        for L in [IOLock, ProcessLock]:
            lock = L(allowed_slots=1)
            lock.release_all_jobID_tokens()

            # delete the complete redis namespace if no lock slot is acquired anymore
            if lock.client.hlen(lock.grabbed_key) == 0:
                lock.delete()

        MemoryReserver(1).delete()
