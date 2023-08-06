#
# Copyright (c) 2018, BWStor, Inc. <www.bwstor.com.cn>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the authors nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANDRES MOREIRA BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""starrydb.py

starrydb module provide functions of a NoSQL database for lightweight data.

"""

import os
import sys
import time
import shutil
import inspect
import threading
import logging
import subprocess
import functools
import pathlib
import multiprocessing.connection
from contextlib import contextmanager

import msgpack
import pylibmc

VERSION = "0.7.1"
LOCK_SH = 0
LOCK_EX = 1
RUN_PATH = "/run/starrydb/"
SERVER_ADDRESS = f"{RUN_PATH}address"
CACHE_SOCKET = f"{RUN_PATH}cache.sock"

class StarryError(Exception):
    '''StarryError'''

    def __init__(self, output):
        self.output = output

def singleton(cls):
    instances = dict()

    @functools.wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

@singleton
class StarryLog(object):
    def __init__(self, file=None, lvl=logging.NOTSET):
        self.logger = None

        if file is not None:
            if pathlib.Path(file).is_file():
                try:
                    logging.basicConfig(
                        handlers=[logging.FileHandler(file)],
                        format=f"%(asctime)s <%(levelname)s> {inspect.stack()[-1][1].split('/')[-1]}[%(process)d]: %(message)s",
                        level=lvl)

                    logging.raiseExceptions = False

                    self.logger = logging.getLogger()
                except:
                    pass
        else:
            try:
                logging.basicConfig(
                    stream=sys.stdout,
                    format=f"%(asctime)s <%(levelname)s> {inspect.stack()[-1][1].split('/')[-1]}[%(process)d]: %(message)s",
                    level=lvl)

                logging.raiseExceptions = False

                self.logger = logging.getLogger()
            except:
                pass

    def debug(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.debug(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

    def info(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.info(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

    def warn(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.warning(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

    def warning(self, msg):
        self.warn(msg)

    def error(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.error(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

    def fatal(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.critical(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

    def exception(self, msg):
        if self.logger is None:
            return None

        try:
            caller = inspect.stack()
            self.logger.exception(f"[{caller[1][1].split('/')[-1]}:{caller[1][2]}] {msg}")
        except:
            pass

class LibMemcachedClient(pylibmc.ThreadMappedPool):
    '''This module supplies a client in Python for memcached based on libmemcached.'''

    def __init__(self, server):
        mc = pylibmc.Client([server], behaviors={"hash": "crc"})

        mc.get_stats()

        super().__init__(mc)

    def flush_all(self):
        with self.reserve() as mc:
            return mc.flush_all()

    def get(self, key):
        with self.reserve() as mc:
            return mc.get(key)

    def set(self, key, value, time=0):
        with self.reserve() as mc:
            if mc.set(key, value, time=time) is False:
                mc.delete(key)
                return False

        return True

    def delete(self, key):
        with self.reserve() as mc:
            return mc.delete(key)

class StarryServer(object):
    def __init__(self, address=SERVER_ADDRESS, depots=[], cache_size=0, log_file=None, log_level="WARNING", rw_ratio=5):
        self.address = address
        self.cursor = 0
        self.depots = {}
        self.logger = StarryLog(log_file, getattr(logging, log_level, logging.WARNING))
        self.rw_ratio = rw_ratio
        self.memcached = None

        pathlib.Path(RUN_PATH).mkdir(exist_ok=True)

        if int(cache_size) > 0:
            try:
                subprocess.check_output("kill -9 `ps axf | grep " + CACHE_SOCKET + " | grep -v grep | awk '{print $1}'`", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except:
                pass

            try:
                os.system(f"memcached -d -u root -a 0777 -D : -C -m {int(cache_size)} -s {CACHE_SOCKET}")

                time.sleep(1)

                self.memcached = LibMemcachedClient(CACHE_SOCKET)
            except Exception as e:
                self.logger.error(f"Caught exception: {e.__doc__}({e})")

                self.memcached = None

        for depot in depots:
            if "path" in depot:
                depot_path = os.path.abspath(depot["path"])

                self.depots[depot_path] = StarryDepot(depot_path, self.logger, self.rw_ratio, self.cursor, self.memcached)

                if depot.get("backup", False) is True:
                    self.depots[depot_path].enableBackup()

                if depot.get("cache", False) is True:
                    self.depots[depot_path].enableCache()

                if depot.get("fsync", False) is True:
                    self.depots[depot_path].enableFsync()

                self.cursor += 1

    def __del__(self):
        self.depots.clear()

        if self.memcached is not None:
            try:
                self.memcached.flush_all()
            except:
                pass

            try:
                subprocess.check_output("kill -9 `ps axf | grep " + CACHE_SOCKET + " | grep -v grep | awk '{print $1}'`", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except:
                pass

    def start(self, backlog=1024, authkey=b'starry'):
        if pathlib.Path(str(self.address)).is_socket():
            try:
                os.remove(self.address)
            except:
                pass

        with multiprocessing.connection.Listener(self.address, backlog=backlog, authkey=authkey) as listener:
            while True:
                try:
                    conn = listener.accept()
                except ConnectionError as e:
                    self.logger.warn(f"Caught exception: {e.__doc__}({e})")
                    continue
                except OSError as e:
                    self.logger.warn(f"Caught exception: {e.__doc__}({e})")
                    break
                except Exception as e:
                    self.logger.warn(f"Caught exception: {e.__doc__}({e})")
                    continue

                try:
                    (depot, mode) = conn.recv()

                    if depot not in self.depots:
                        self.depots[depot] = StarryDepot(depot, self.logger, self.rw_ratio, self.cursor, self.memcached)

                        self.cursor += 1

                    threading.Thread(target=self.depots[depot].executeCommand, args=(conn, mode)).start()
                except Exception as e:
                    self.logger.error(f"Caught exception: {e.__doc__}({e})")

                    try:
                        conn.close()
                    except:
                        pass

class StarryDepot(object):
    def __init__(self, path, logger, rw_ratio, index, memcached):
        self.database = pathlib.Path(path)
        self.logger = logger
        self.rw_ratio = rw_ratio
        self.index = index
        self.memcached = memcached
        self.cache = None
        self.fsync = False
        self.bak = False
        self.depot_lock = threading.Condition()
        self.thread_lock = threading.Condition()
        self.thread_blocking = False
        self.write_wait = 0
        self.read_wait = 0
        self.write_queue = []
        self.read_queue = []

        if not self.database.is_dir():
            raise StarryError(f"path {path} doesn't exist.")

    def executeCommand(self, conn, mode=LOCK_SH):
        def _threadPredicate():
            return not self.thread_blocking

        def _depotPredicate():
            if self.read_wait > 0 or self.write_wait > 0 or len(self.read_queue) > 0 or len(self.write_queue) > 0:
                return False

            return True

        if mode == LOCK_EX:
            with self.thread_lock:
                self.thread_lock.wait_for(_threadPredicate)
                self.thread_blocking = True

        while True:
            try:
                (func, *param) = conn.recv()
            except:
                break

            if mode == LOCK_SH:
                with self.thread_lock:
                    self.thread_lock.wait_for(_threadPredicate)
            else:
                with self.depot_lock:
                    self.depot_lock.wait_for(_depotPredicate)

            try:
                conn.send(getattr(self, func)(*param))
            except Exception as e:
                self.logger.debug(f"Caught exception: {e.__doc__}({e})")

                try:
                    conn.send((False, f"Caught exception: {e.__doc__}({e})"))
                except:
                    pass

                break

        if mode == LOCK_EX:
            with self.thread_lock:
                self.thread_blocking = False
                self.thread_lock.notify_all()

        if self.cache is not None:
            try:
                self.cache.relinquish()
            except:
                pass

        try:
            conn.close()
        except:
            pass

    def enableFsync(self):
        self.fsync = True

        return (True, "")

    def disableFsync(self):
        self.fsync = False

        return (True, "")

    def enableCache(self):
        self.cache = self.memcached

        return (True, "")

    def disableCache(self):
        mark = {"mode": "r", "members": [None]}

        with self._lock(mark):
            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    self._deleteCache(elem.stem)

        self.cache = None

        return (True, "")

    def enableBackup(self):
        if not self.database.joinpath(".backup").is_dir():
            self.database.joinpath(".backup").mkdir(exist_ok=True)

            self.backup()

        self.bak = True

        return (True, "")

    def disableBackup(self):
        self.bak = False

        return (True, "")

    def get(self, key):
        if type(key) is not list:
            key = [key]

        mark = {"mode": "r", "members": [key[0][0]] if type(key[0]) is tuple else [key[0]]}

        with self._lock(mark):
            return self._get(key)

    def update(self, key, value):
        if type(key) is not list:
            key = [key]

        mark = {"mode": "w", "members": [key[0]]}

        with self._lock(mark):
            return self._update(key, value)

    def insert(self, key, value):
        if type(key) is not list:
            key = [key]

        mark = {"mode": "w", "members": [key[0]]}

        with self._lock(mark):
            return self._insert(key, value)

    def delete(self, key):
        if type(key) is not list:
            key = [key]

        mark = {"mode": "w", "members": [key[0]]}

        with self._lock(mark):
            return self._delete(key)

    def copy(self, old_key, new_key):
        mark = {"mode": "w", "members": [old_key, new_key]}

        with self._lock(mark):
            (ret, value) = self._get([old_key])
            if ret is False:
                return (ret, value)

            return self._insert([new_key], value)

    def rename(self, old_key, new_key):
        mark = {"mode": "w", "members": [old_key, new_key]}

        with self._lock(mark):
            (ret, value) = self._get([old_key])
            if ret is False:
                return (ret, value)

            (ret, msg) = self._insert([new_key], value)
            if ret is False:
                return (ret, msg)

            (ret, msg) = self._delete([old_key])
            if ret is False:
                self._delete([new_key])

            return (ret, msg)

    def exist(self, key):
        if type(key) is not list:
            key = [key]

        mark = {"mode": "r", "members": [key[0][0]] if type(key[0]) is tuple else [key[0]]}

        with self._lock(mark):
            (ret, _) = self._get(key)
            return (True, ret)

    def getMulti(self, keys):
        values = {}

        mark = {"mode": "r", "members": list(keys)}

        with self._lock(mark):
            for key in keys:
                (ret, value) = self._get([key])
                if ret is False:
                    return (ret, value)

                values[key] = value

            return (True, values)

    def updateMulti(self, values):
        mark = {"mode": "w", "members": list(values)}

        with self._lock(mark):
            for key, value in values.items():
                (ret, msg) = self._update([key], value)
                if ret is False:
                    return (ret, msg)

            return (True, "")

    def insertMulti(self, values):
        mark = {"mode": "w", "members": list(values)}

        with self._lock(mark):
            for key, value in values.items():
                (ret, msg) = self._insert([key], value)
                if ret is False:
                    return (ret, msg)

            return (True, "")

    def deleteMulti(self, keys):
        mark = {"mode": "w", "members": keys}

        with self._lock(mark):
            for key in keys:
                (ret, msg) = self._delete([key])
                if ret is False:
                    return (ret, msg)

            return (True, "")

    def list(self):
        mark = {"mode": "r", "members": [None]}

        with self._lock(mark):
            return (True, [elem.stem for elem in self.database.glob("*") if elem.suffix == ".mpb"])

    def getAll(self):
        values = {}

        mark = {"mode": "r", "members": [None]}

        with self._lock(mark):
            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    (ret, value) = self._get([elem.stem])
                    if ret is False:
                        return (ret, value)

                    values[elem.stem] = value

            return (True, values)

    def updateAll(self, values):
        mark = {"mode": "w", "members": [None]}

        with self._lock(mark):
            for key, value in values.items():
                (ret, msg) = self._update([key], value)
                if ret is False:
                    return (ret, msg)

            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    if elem.stem not in values:
                        self._delete([elem.stem])

            return (True, "")

    def backup(self):
        mark = {"mode": "w", "members": [None]}

        with self._lock(mark):
            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    (ret, msg) = self._backup(elem.stem)
                    if ret is False:
                        return (ret, msg)

            return (True, "")

    def recover(self):
        mark = {"mode": "w", "members": [None]}

        with self._lock(mark):
            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    (ret, msg) = self._get([elem.stem])
                    if ret is False:
                        self._recover(elem.stem)

            if self.database.joinpath(".backup").is_dir():
                for elem in self.database.joinpath(".backup").glob("*"):
                    if elem.suffix == ".mpb" and not self.database.joinpath(elem.name).exists():
                        (ret, msg) = self._get([elem.stem])
                        if ret is False:
                            self._recover(elem.stem)

            return (True, "")

    def clone(self, path):
        path = pathlib.Path(path)

        if not path.is_dir():
            self.logger.error(f"path {str(path)} doesn't exist.")
            return (False, f"path {str(path)} doesn't exist.")

        for elem in path.glob("*"):
            if elem.suffix == ".mpb":
                elem.unlink()
            elif elem.suffix == ".tmp":
                elem.unlink()

        mark = {"mode": "w", "members": [None]}

        with self._lock(mark):
            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb":
                    (ret, msg) = self._backup(elem.stem, path=path)
                    if ret is False:
                        return (ret, msg)

            return (True, "")

    def upgrade(self, path):
        path = pathlib.Path(path)

        if not path.is_dir():
            self.logger.error(f"No {str(path)}.")
            return (False, f"No {str(path)}.")

        mark = {"mode": "w", "members": [None]}

        with self._lock(mark):
            for elem in path.glob("*"):
                if elem.suffix == ".mpb":
                    (ret, msg) = self._load(elem.stem, path)
                    if ret is False:
                        return (ret, msg)

            for elem in self.database.glob("*"):
                if elem.suffix == ".mpb" and not path.joinpath(elem.name).exists():
                    self._delete([elem.stem])

            return (True, "")

    def clear(self):
        for elem in self.database.glob("*"):
            if elem.suffix == ".mpb":
                self._deleteCache(elem.stem)

                if elem.is_file():
                    try:
                        elem.unlink()
                    except Exception as e:
                        self.logger.error(f"Caught exception: {e.__doc__}({e})")
                        return (False, f"Caught exception: {e.__doc__}({e})")
            elif elem.name == ".backup" and elem.isdir():
                try:
                    shutil.rmtree(elem)
                except Exception as e:
                    self.logger.error(f"Caught exception: {e.__doc__}({e})")
                    return (False, f"Caught exception: {e.__doc__}({e})")

        self.write_queue.clear()
        self.read_queue.clear()

        return (True, "")

    def _getCache(self, key):
        if self.cache is None:
            return None

        try:
            value = self.cache.get(f"{self.index}:{key}")
        except:
            return None

        if value is None:
            return None

        try:
            value = msgpack.unpackb(value, strict_map_key=False)
        except:
            try:
                self.cache.delete(f"{self.index}:{key}")
            except:
                pass

            return None

        return value

    def _setCache(self, key, value):
        if self.cache is not None:
            try:
                self.cache.set(f"{self.index}:{key}", value)
            except:
                return False

        return True

    def _deleteCache(self, key):
        if self.cache is not None:
            try:
                self.cache.delete(f"{self.index}:{key}")
            except:
                return False

        return True

    def _get(self, route):
        branch = route[:]
        key = branch.pop(0)
        filters = []

        if type(key) is tuple:
            (key, filters) = key

            if type(filters) is not list:
                filters = [filters]

        value = self._getCache(key)
        if value is None:
            (ret, data) = _readFile(self.database.joinpath(f"{key}.mpb"))
            if ret is False:
                return (ret, data)

            try:
                value = msgpack.unpackb(data, strict_map_key=False)
                self._setCache(key, data)
            except:
                (ret, value) = self._recover(key)
                if ret is False:
                    return (ret, value)

        if len(branch) > 0:
            (ret, value) = _getPart(value, branch, filters)
            if ret is False:
                return (False, f'Can not find {".".join(branch)} in {key}.')

        return (True, value)

    def _update(self, route, part):
        branch = route[:]
        key = branch.pop(0)
        file = self.database.joinpath(f"{key}.mpb")

        if len(branch) == 0:
            if self._getCache(key) == part:
                return (True, "")

            value = part
        else:
            if not file.exists():
                return (False, f"No {key}.")

            if self.bak is True:
                if not self.database.joinpath(".backup", f"{key}.mpb").exists():
                    (ret, msg) = self._backup(key)
                    if ret is False:
                        return (ret, msg)

            (ret, value) = _readFile(file)
            if ret is False:
                return (ret, value)

            try:
                value = msgpack.unpackb(value, strict_map_key=False)
            except Exception as e:
                self._recover(key)
                return (False, f"Caught exception: {e.__doc__}({e})")

            (ret, msg) = _updatePart(value, branch, part)
            if ret is False:
                return (False, f"Update {key} failed: {msg}")
            elif msg is False:
                return (True, "")

        try:
            value = msgpack.packb(value)
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

        if not file.exists():
            try:
                file.touch()
            except Exception as e:
                try:
                    file.unlink()
                except:
                    pass

                return (False, f"Caught exception: {e.__doc__}({e})")

        (ret, msg) = _writeFile(file, value, self.fsync)
        if ret is False:
            self._recover(key)
            return (ret, msg)

        self._setCache(key, value)

        if self.bak is True:
            return self._backup(key, check_flag=False)

        return (True, "")

    def _insert(self, route, part):
        branch = route[:]
        key = branch.pop(0)
        file = self.database.joinpath(f"{key}.mpb")

        if len(branch) == 0:
            value = part
        else:
            if not file.exists():
                return (False, f"No {key}.")

            if self.bak is True:
                if not self.database.joinpath(".backup", f"{key}.mpb").exists():
                    (ret, msg) = self._backup(key)
                    if ret is False:
                        return (ret, msg)

            (ret, value) = _readFile(file)
            if ret is False:
                return (ret, value)

            try:
                value = msgpack.unpackb(value, strict_map_key=False)
            except Exception as e:
                self._recover(key)
                return (False, f"Caught exception: {e.__doc__}({e})")

            (ret, msg) = _insertPart(value, branch, part)
            if ret is False:
                return (False, f"Insert {key} failed: {msg}")
            elif msg is False:
                return (True, "")

        try:
            value = msgpack.packb(value)
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

        if not file.exists():
            try:
                file.touch()
            except Exception as e:
                try:
                    file.unlink()
                except:
                    pass

                return (False, f"Caught exception: {e.__doc__}({e})")

        (ret, msg) = _writeFile(file, value, self.fsync)
        if ret is False:
            self._recover(key)
            return (ret, msg)

        self._setCache(key, value)

        if self.bak is True:
            return self._backup(key, check_flag=False)

        return (True, "")

    def _delete(self, route):
        branch = route[:]
        key = branch.pop(0)
        file = self.database.joinpath(f"{key}.mpb")
        backup_file = self.database.joinpath(".backup", f"{key}.mpb")

        if not file.exists():
            self._deleteCache(key)

            try:
                file.with_suffix(".mpb.tmp").unlink()
            except:
                pass

            if len(branch) == 0:
                try:
                    backup_file.unlink()
                except:
                    pass

                try:
                    backup_file.with_suffix(".mpb.tmp").unlink()
                except:
                    pass

                return (True, "")
            else:
                self._recover(key)
                return (False, f"No {key}.")

        if self.bak is True:
            if not backup_file.exists():
                (ret, msg) = self._backup(key)
                if ret is False:
                    return (ret, msg)

        if len(branch) == 0:
            self._deleteCache(key)

            try:
                file.with_suffix(".mpb.tmp").unlink()
            except:
                pass

            try:
                file.unlink()
            except Exception as e:
                self._recover(key)
                return (False, f"Caught exception: {e.__doc__}({e})")

            try:
                backup_file.unlink()
            except:
                pass

            try:
                backup_file.with_suffix(".mpb.tmp").unlink()
            except:
                pass

            return (True, "")

        (ret, value) = _readFile(file)
        if ret is False:
            return (ret, value)

        try:
            value = msgpack.unpackb(value, strict_map_key=False)
        except Exception as e:
            self._recover(key)
            return (False, f"Caught exception: {e.__doc__}({e})")

        (ret, msg) = _deletePart(value, branch)
        if ret is False:
            return (False, f"Delete {key} failed: {msg}")

        try:
            value = msgpack.packb(value)
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

        (ret, msg) = _writeFile(file, value, self.fsync)
        if ret is False:
            self._recover(key)
            return (ret, msg)

        self._setCache(key, value)

        if self.bak is True:
            return self._backup(key, check_flag=False)

        return (True, "")

    def _backup(self, key, check_flag=True, path=None):
        file = self.database.joinpath(f"{key}.mpb")

        if not file.exists():
            return (False, f"No {key}.")

        if check_flag is True:
            (ret, data) = _readFile(file)
            if ret is False:
                return (ret, data)

            try:
                msgpack.unpackb(data, strict_map_key=False)
            except Exception as e:
                self._recover(key)
                return (False, f"Caught exception: {e.__doc__}({e})")

        if path is None:
            path = self.database.joinpath(".backup")

        return _copyFile(file, path.joinpath(f"{key}.mpb"), self.fsync)

    def _recover(self, key):
        backup_file = self.database.joinpath(".backup", f"{key}.mpb")

        self._deleteCache(key)

        if not backup_file.exists():
            return (False, f"No {str(backup_file)}.")

        (ret, value) = _readFile(backup_file)
        if ret is False:
            return (ret, value)

        try:
            data = msgpack.unpackb(value, strict_map_key=False)
        except Exception as e:
            try:
                backup_file.unlink()
            except:
                pass

            try:
                backup_file.with_suffix(".mpb.tmp").unlink()
            except:
                pass

            return (False, f"Caught exception: {e.__doc__}({e})")

        (ret, msg) = _copyFile(backup_file, self.database.joinpath(f"{key}.mpb"), self.fsync)
        if ret is False:
            return (ret, msg)

        self._setCache(key, value)

        return (True, data)

    def _load(self, key, path):
        file = self.database.joinpath(f"{key}.mpb")
        backup_file = self.database.joinpath(".backup", f"{key}.mpb")
        source_file = path.joinpath(f"{key}.mpb")

        if not source_file.exists():
            return (False, f"No {str(source_file)}.")

        (ret, value) = _readFile(source_file)
        if ret is False:
            return (ret, value)

        try:
            msgpack.unpackb(value, strict_map_key=False)
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

        if self.bak is True:
            if file.exists():
                if not backup_file.exists():
                    (ret, msg) = self._backup(key)
                    if ret is False:
                        return (ret, msg)

        (ret, msg) = _copyFile(source_file, file, self.fsync)
        if ret is False:
            if not backup_file.exists():
                try:
                    file.unlink()
                except:
                    pass

                try:
                    file.with_suffix(".mpb.tmp").unlink()
                except:
                    pass

                try:
                    backup_file.with_suffix(".mpb.tmp").unlink()
                except:
                    pass
            else:
                self._recover(key)

            return (ret, msg)

        self._setCache(key, value)

        if self.bak is True:
            return self._backup(key, check_flag=False)

        return (True, "")

    @contextmanager
    def _lock(self, mark):
        def _predicate():
            if mark["mode"] == "r":
                if self.write_wait > 0 and (self.read_wait / self.write_wait) <= self.rw_ratio:
                    return False

                if len(self.write_queue) > 0:
                    if None in mark["members"]:
                        return False

                    if any([None in write_members or len(set(write_members) & set(mark["members"])) > 0 for write_members in self.write_queue]):
                        return False
            else:
                if self.write_wait > 0 and (self.read_wait / self.write_wait) > self.rw_ratio:
                    return False

                if len(self.read_queue) > 0:
                    if None in mark["members"]:
                        return False

                    if any([None in read_members or len(set(read_members) & set(mark["members"])) > 0 for read_members in self.read_queue]):
                        return False
                elif len(self.write_queue) > 0:
                    if None in mark["members"]:
                        return False

                    if any([None in write_members or len(set(write_members) & set(mark["members"])) > 0 for write_members in self.write_queue]):
                        return False

            return True

        with self.depot_lock:
            if mark["mode"] == "r":
                self.read_wait += 1
            else:
                self.write_wait += 1

            self.depot_lock.wait_for(_predicate)

            if mark["mode"] == "r":
                self.read_queue.append(mark["members"])
                self.read_wait -= 1
            else:
                self.write_queue.append(mark["members"])
                self.write_wait -= 1

        yield

        with self.depot_lock:
            try:
                if mark["mode"] == "r":
                    self.read_queue.remove(mark["members"])
                else:
                    self.write_queue.remove(mark["members"])
            except:
                pass

            self.depot_lock.notify_all()

class StarryClient(object):
    def __init__(self, path, mode=LOCK_SH, address=SERVER_ADDRESS):
        self.client = multiprocessing.connection.Client(address, authkey=b'starry')
        self.client.send((os.path.abspath(path), mode))

    def __del__(self):
        try:
            self.client.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def close(self):
        try:
            self.client.close()
        except:
            pass

    def _callableForward(self, func, *args):
        try:
            self.client.send((func, *args))
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

        try:
            if self.client.poll(60):
                return self.client.recv()
            else:
                return (False, "timeout")
        except Exception as e:
            return (False, f"Caught exception: {e.__doc__}({e})")

    def get(self, key):
        return self._callableForward("get", key)

    def update(self, key, value):
        return self._callableForward("update", key, value)

    def insert(self, key, value):
        return self._callableForward("insert", key, value)

    def delete(self, key):
        return self._callableForward("delete", key)

    def copy(self, old_key, new_key):
        return self._callableForward("copy", old_key, new_key)

    def rename(self, old_key, new_key):
        return self._callableForward("rename", old_key, new_key)

    def exist(self, key):
        return self._callableForward("exist", key)

    def list(self):
        return self._callableForward("list")

    def getEpoch(self):
        return self._callableForward("getEpoch")

    def backup(self):
        return self._callableForward("backup")

    def recover(self):
        return self._callableForward("recover")

    def clone(self, path):
        return self._callableForward("clone", path)

    def upgrade(self, path):
        return self._callableForward("upgrade", path)

    def clear(self):
        return self._callableForward("clear")

    def getMulti(self, keys):
        return self._callableForward("getMulti", keys)

    def getAll(self):
        return self._callableForward("getAll")

    def updateMulti(self, values):
        return self._callableForward("updateMulti", values)

    def updateAll(self, values):
        return self._callableForward("updateAll", values)

    def insertMulti(self, values):
        return self._callableForward("insertMulti", values)

    def deleteMulti(self, keys):
        return self._callableForward("deleteMulti", keys)

def _getPart(value, branch, filters):
    def _filterValue(value, filters):
        if type(value) is list:
            if any([type(v) is not dict for v in value]):
                return value

            for key in filters:
                if any([key not in v for v in value]):
                    return value

            for v in value:
                for key in list(v):
                    if key not in filters:
                        v.pop(key)

            return value
        elif type(value) is dict:
            for key in filters:
                if key not in value:
                    return value

            for key in list(value):
                if key not in filters:
                    value.pop(key)

            return value

        return value

    for knot in branch:
        branch_filters = []

        if type(knot) is tuple:
            (knot, branch_filters) = knot

            if type(branch_filters) is not list:
                branch_filters = [branch_filters]

        if type(value) is list:
            if type(knot) is int:
                try:
                    value = value[knot]
                except Exception as e:
                    return (False, f"Caught exception: {e.__doc__}({e})")
            elif all([type(v) is dict for v in value]):
                try:
                    value = [v[knot] for v in value if knot in v]
                except Exception as e:
                    return (False, f"Caught exception: {e.__doc__}({e})")
            else:
                return (False, f"Syntax error.")
        elif type(value) is dict and knot in value:
            value = value[knot]
        else:
            return (False, f"Syntax error.")

        if len(branch_filters) > 0:
            value = _filterValue(value, branch_filters)

    if len(filters) > 0:
        return (True, _filterValue(value, filters))

    return (True, value)

def _updatePart(value, branch, part):
    if len(branch) > 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot < len(value):
                return _updatePart(value[knot], branch, part)
        elif type(value) is dict and knot in value:
            return _updatePart(value[knot], branch, part)
    elif len(branch) == 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot < len(value):
                if value[knot] == part:
                    return (True, False)

                value[knot] = part
                return (True, True)
        elif type(value) is dict and knot in value:
            if value[knot] == part:
                return (True, False)

            value[knot] = part
            return (True, True)

    return (False, "Syntax error.")

def _insertPart(value, branch, part):
    if len(branch) > 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot <= len(value):
                return _insertPart(value[knot], branch, part)
        elif type(value) is dict and knot in value:
            return _insertPart(value[knot], branch, part)
    elif len(branch) == 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot <= len(value):
                value.insert(knot, part)
                return (True, "")
        elif type(value) is dict:
            if knot in value and value[knot] == part:
                return (True, False)

            value[knot] = part
            return (True, True)

    return (False, "Syntax error.")

def _deletePart(value, branch):
    if len(branch) > 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot < len(value):
                return _deletePart(value[knot], branch)
        elif type(value) is dict and knot in value:
            return _deletePart(value[knot], branch)
    elif len(branch) == 1:
        knot = branch.pop(0)

        if type(value) is list and type(knot) is int:
            knot = len(value) + knot if knot < 0 else knot

            if 0 <= knot < len(value):
                value.pop(knot)
                return (True, "")
        elif type(value) is dict and knot in value:
            value.pop(knot)
            return (True, "")

    return (False, "Syntax error.")

def _readFile(src):
    try:
        return (True, src.read_bytes())
    except Exception as e:
        return (False, f"Caught exception: {e.__doc__}({e})")

def _writeFile(dst, value, fsync=False):
    try:
        with dst.open(mode="wb", buffering=0) as descriptor:
            descriptor.write(value)
            descriptor.truncate()

            if fsync is True:
                descriptor.flush()
                os.fdatasync(descriptor.fileno())

        if len(value) != dst.stat().st_size:
            return (False, "No space left on device.")
    except Exception as e:
        return (False, f"Caught exception: {e.__doc__}({e})")

    return (True, "")

def _copyFile(src, dst, fsync=False):
    (ret, value) = _readFile(src)
    if ret is False:
        return (ret, value)

    if dst.exists():
        tmp_path = dst.with_suffix(".mpb.tmp")

        (ret, msg) = _writeFile(tmp_path, value, fsync)
        if ret is False:
            try:
                tmp_path.unlink()
            except:
                pass

            return (ret, msg)

        try:
            tmp_path.rename(dst)
        except:
            try:
                tmp_path.unlink()
            except:
                pass

            (ret, msg) = _writeFile(dst, value, fsync)
            if ret is False:
                return (ret, msg)
    else:
        (ret, msg) = _writeFile(dst, value, fsync)
        if ret is False:
            try:
                dst.unlink()
            except:
                pass

            return (ret, msg)

        try:
            dst.chmod(src.stat().st_mode)
            shutil.chown(dst, user=src.stat().st_uid, group=src.stat().st_gid)
        except:
            pass

    return (True, "")
