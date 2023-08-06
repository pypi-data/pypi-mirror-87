import os
from collections import namedtuple

from .backend import fnctlBackend


class BadPositionException(Exception):
    pass


class NegativeLengthException(Exception):
    pass


class OverlapException(Exception):
    pass


class NotLockedException(Exception):
    pass


class MultipleLockException(Exception):
    pass


class SegmentLengthException(Exception):
    pass


class _Region(object):
    def __init__(self, pos, length):
        if pos < 0:
            raise BadPositionException()
        if length < 0:
            raise NegativeLengthException()
        self.fr = pos
        self.to = pos + length - 1
        self.ln = length

    def __repr__(self):
        REGION = namedtuple("Region", ["pos", "end", "size"])
        return str(REGION(self.fr, self.to, self.ln))

    def clash(self, pos, length):
        if length == 0 or self.ln == 0:
            return True
        if pos > self.to:
            return False
        if pos + length < self.fr:
            return False
        if pos + length >= self.fr:
            return True
        if pos <= self.to:
            return True
        return False

    def noclash(self, pos, length):
        return not self.clash(pos, length)

    def overlap(self, other):
        return self.clash(other.fr, other.ln)

    def nooverlap(self, other):
        return not self.overlap(other)


class FileLock(object):
    def __init__(self, fd, backend=None):
        try:
            self._fd = fd.fileno()
        except Exception as ex:
            ex = ex
            self._fd = fd
        self._regions = []
        self._backend = fnctlBackend() if backend == None else backend

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(fd="
            + str(self._fd)
            + ", locks="
            + str(self._regions)
            + ")"
        )

    # low level methods

    def _lock(self, pos, length):
        if length < 0:
            raise NegativeLengthException()
        if not all(map(lambda x: x.noclash(pos, length), self._regions)):
            raise OverlapException()
        self._backend.lockf(self._fd, pos, length)
        self._regions.append(_Region(pos, length))

    def _unlock(self, pos, length):
        if length < 0:
            raise NegativeLengthException()
        fnd = list(filter(lambda x: x.fr == pos, self._regions))
        if len(fnd) == 0:
            raise NotLockedException()
        if len(fnd) > 1:
            raise MultipleLockException()
        ln = fnd[0].ln
        if ln != length:
            raise SegmentLengthException()
        self._backend.unlockf(self._fd, pos, length)
        newregions = list(filter(lambda x: x.fr != pos, self._regions))
        self._regions = newregions

    # generic lock

    def flock(self, pos=0, length=0, lock=True):
        "lock at position a region of bytes"
        if lock:
            self._lock(pos, length)
        else:
            self._unlock(pos, length)
        return self

    # high level methods

    def block(self, lock=True):
        "block lock, complete file"
        self.flock(0, length=0, lock=lock)
        return self

    def pid(self, lock=True):
        "lock the process id"
        self.flock(os.getpid(), 1, lock)
        return self

    def regions(self, regions, lock=True):
        "lock regions at once, or fail"
        done = []
        reex = None

        if lock == False:
            done = regions
        else:
            try:
                for pos, length in regions:
                    self.flock(pos, length)
                    done.append((pos, length))
                done = []
            except Exception as ex:
                reex = ex

        for pos, length in done:
            self.flock(pos, length, lock=False)

        if reex:
            raise reex

        return self

    def rollb(self):
        for r in self._regions:
            self.flock(r.fr, r.ln, lock=False)

    # compatibility

    def open(self):
        return self

    def close(self):
        self.rollb()

    # context

    def __enter__(self):
        return self.open()

    def __exit__(self, t, v, tb):
        self.close()
